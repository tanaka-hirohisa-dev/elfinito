環境構築

■PIPのインストール

インストールスクリプト取得
lolipopの古いバージョンと合わせて、pipも古いバージョンを指定
$ curl https://bootstrap.pypa.io/pip/3.7/get-pip.py  -o get-pip.py

ユーザ権限でインストールする
$ python3 get-pip.py --user

pipをアップデートする
$ python3 -m pip install --upgrade pip

余計なごみを削除
$ rm get-pip.py

■必要なパッケージをインストール
pip3 install flask
pip install flask_sqlalchemy
pip install python-dotenv
