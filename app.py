#!/usr/bin/env python3

from os.path import join, getsize, getmtime, isfile
from os import listdir,getenv
from datetime import datetime,date
from flask import Flask, render_template, send_from_directory,  g, request, session, redirect
import logging
from logging.handlers import RotatingFileHandler
import pymysql
from dotenv import load_dotenv

# 環境変数読込
load_dotenv()

# フレームワーク初期化
app = Flask(__name__)

# アクセスログ用オブジェクト
access_logger = logging.getLogger('werkzeug')
access_logger.setLevel(logging.INFO)

# ログフォーマット（IP, メソッド, パス, ステータスコード, User-Agent）
formatter = logging.Formatter(
  '[%(asctime)s] %(levelname)s in %(module)s: '
  '%(message)s'
)

# ローテーション付きファイルハンドラー（最大1MB × 5世代）
file_handler = RotatingFileHandler('access.log', maxBytes=1_000_000, backupCount=5, encoding='utf-8')
file_handler.setFormatter(formatter)
access_logger.addHandler(file_handler)

# DB接続
def get_connection():

  try:
    con = pymysql.connect(
      host=getenv('PY_HOST')
     ,user=getenv('PY_USER')
     ,password=getenv('PY_PASSWORD')
     ,database=getenv('PY_DATABASE')
     ,charset="utf8mb4"
#     ,cursorclass=pymysql.cursors.DictCursor
    )
    return con
  except pymysql.MySQLError as e:
    access_logger.info(f"DB接続エラー: {e}")
    return None


# アクセス前リクエストをフック
@app.before_request
def log_request_info():
  access_logger.info(
    f"{request.remote_addr} {request.method} {request.path} "
    f"User-Agent: {request.user_agent.string}"
  )
  # DB接続
  con = get_connection()
  if not con:
    return "データベース接続失敗"

  try:
    # カーソルを取得
    cursor = con.cursor()

    # INSERT分発行
    cursor.execute(
      "INSERT INTO t_access_log VALUES('%s','%s', '%s','%s',NULL)" % \
      (date.today()
      ,f"{request.path}"
      ,f"{request.remote_addr}"
      ,f"{request.user_agent.string}"
      )
    )

  except pymysql.MySQLError as e:
    access_logger.info(f"SQL実行エラー: {e}")

  finally:
    con.commit()
    con.close()

# アイコンの設定
@app.route('/favicon.ico')
def favicon():
  # ./static/favicon.icoを送信
  return send_from_directory(join(app.root_path, 'static'), 'favicon.ico')


# トップページ
@app.route("/")
def index():

  # 定数定義 
  dir_path = "./move"
  url = "https://snake-fish.com/elfinito/move/"

  # 変数定義
  move_list = []
  newest_day = "2000/01/01" 

  # 各ファイルループ処理
  for f in listdir(dir_path):

    # 動画フルURL作成
    full_path = join(dir_path, f)

    # ファイル以外は処理対処外
    if not isfile(full_path):
      break

    # mp4以外は処理対象外
    if not ".mp4" in f:
      break
 
    # ファイルステータス取得
    size = getsize(full_path)
    mtime = getmtime(full_path)
    buf_date = f[0:4] + "/" + f[4:6] + "/" + f[6:8]

    # 基準日MAXを保持
    if newest_day < buf_date :
      newest_day = buf_date

    # 動画リストに情報追加
    move_list.append({
      "name": f
     ,"size": str(round( int(f"{size}") / (1024 * 1024), 2)) + "MB"
     ,"date": buf_date
     ,"updated_at": f"{datetime.fromtimestamp(mtime)}"
     ,"url": url + f
    })

  # ソートする
  sorted_list = sorted(move_list, key=lambda x: x["updated_at"], reverse=True)


  # ./templates/index.htmlを送信
  return render_template('index.html', list=sorted_list, start_day=newest_day)


# 呼び出し
if __name__ == "__main__":
  app.run(threaded=True)
