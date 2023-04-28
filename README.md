qalog
 
qalogは自身や他人の気づきや質問など幅広い内容をCRUD操作できるアプリケーションです。
 
# Requirement

このアプリケーションを使用する際のリクワイアメント
* vscode
* python 3.11.3
 
# Installation　for my teather

もしあなたが、このアプリケーションを私の為に修正を試み、そのための動作確認を必要とするなら
以下にその方法を記述します。（windowsユーザー向け）

任意のディレクトリで以下の操作を行ってください
```comandprmpt

git clone https://github.com/zero-penguin/qalog.git

```
次にそのディレクトリをvscode等のコードエディタで開きます。
そして一番右下のボタンから４つ目にpythonのバージョン情報が書かれたボタンがあり、
これが以下のようになっているか確認してください。

3.11.3('venv' venv)
 
このように表示されていない場合は、ボタンをクリックして修正してください。
（ほとんどの場合はrecomendされたバージョンをクリックすればOKだと思います。）

そしてvscodeのターミナルから
```
python -m flask --debug
```
と入力し、
http://127.0.0.1:5000/signup
のプロトコルで動作の確認が行えるはずです。

拙いながら説明は以上です。

