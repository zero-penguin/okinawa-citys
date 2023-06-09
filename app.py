from flask import Flask
from flask import render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required

# パスワードの非表示化と確認機能のインポート
from werkzeug.security import generate_password_hash, check_password_hash

from datetime import datetime
import pytz
import os

# インスタンス化
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
# ランダムなシークレットキーの作成
app.config['SECRET_KEY'] = os.urandom(24)
# アプリにデータベースを紐づけ
db = SQLAlchemy(app)

# ログインマネージャのインスタンス化
login_manager = LoginManager()
# アプリにログイン機能を紐づけ
login_manager.init_app(app)

#databaseの作成
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    body = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(pytz.timezone('Asia/Tokyo')))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(12),unique=True)

@app.route('/', methods=['GET','POST'])
@login_required
def index():
    if request.method == 'GET':
        # Postに保存されている全てのデータの取得
        posts = Post.query.all()
        return render_template('index.html', posts=posts)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User(username=username, password=generate_password_hash(password, method='sha256')) 
        #入れたデータを保存
        db.session.add(user)
        #保存されたデータに変更
        db.session.commit()
        #login.htmlに移動
        return redirect('/login')
    else:
        return render_template('signup.html')

# 下記にデコレーターによるセキュリティ強化があるが、その実施に必要なコード    
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Userのデータベースから合致する名前を探す。
        user = User.query.filter_by(username=username).first() 
        # 探し出されたユーザー名のパスワードと入力されたパスワードが同じならば
        if check_password_hash(user.password, password):
             # importしたlogin_userを用いてログインする
            login_user(user)
            # トップページに移動する
            return redirect('/')
    else:
        return render_template('login.html')
    
@app.route('/logout')
# デコレーターの設定により、ログインしているユーザーのみアクセス出来るようにセキュリティ
@login_required
def logout():
    logout_user()
    return redirect('/login')

@app.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    #新しい投稿がされたなら、createのform内のname=title,bodyを取得する
    if request.method == 'POST':
        title = request.form.get('title')
        body = request.form.get('body')
        #取得したデータをデータベースに入れる
        post = Post(title=title, body=body) 
        #入れたデータを保存
        db.session.add(post)
        #保存されたデータに変更
        db.session.commit()
        #変更されたらトップページに戻る
        return redirect('/')
    else:
        return render_template('create.html')
    
# index.htmlのa href="/{{post.id}}/update"からidを受取り、可変型のルーティングで取得する
@app.route('/<int:id>/update', methods=['GET','POST'])
@login_required
def update(id):
    # postのインスタンス化 idをURLに入れておく
    post = Post.query.get(id)
    if request.method == 'GET':
        return render_template('update.html', post=post)
    else:
        # インスタンス化されたpostに上書きする
        post.title = request.form.get('title')
        post.body = request.form.get('body')

        # 更新
        db.session.commit()
        return redirect('/')

@app.route('/<int:id>/delete', methods=['GET'])
@login_required
def delete(id):
    # postのインスタンス化
    post = Post.query.get(id)
    
    db.session.delete(post)
    db.session.commit()
    return redirect('/')