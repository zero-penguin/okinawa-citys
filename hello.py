from flask import Flask
from flask import render_template

#大枠を生成 ルーティング
app = Flask(__name__)

nums1 =[
    1,2,3,4,5
]

nums2 = [
    2,4,6,8,10
]




#http:~5000/japanで表示 可変URLの設定
@app.route("/")
#関数の設定
def japan():
    #templeateを用いるためのrender
    return render_template('test.html', nums1=nums1, nums2=nums2, results=results)



# 上記のように複数のルートを生成しておけば、
# 一般的なブログアプリのように複数のページを生成することが出来る