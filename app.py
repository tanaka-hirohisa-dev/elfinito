#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from os.path import join, getsize, getmtime, isfile
from os import listdir,getenv
from datetime import datetime,date
from flask import Flask, render_template, send_from_directory,  g, request, session, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
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
DB_HOST     = getenv('PY_HOST')
DB_USER     = getenv('PY_USER')
DB_PASSWORD = getenv('PY_PASSWORD')
DB_NAME     = getenv('PY_DATABASE')
app.config['SQLALCHEMY_DATABASE_URI'] = (
  f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}?charset=utf8"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# モデルクラス
class TAccessLog(db.Model):
  __tablename__ = 't_access_log'
  id = db.Column(db.Integer, primary_key=True)
  as_of_date = db.Column(db.Date, nullable=False)
  path = db.Column(db.String(100), nullable=False)
  ip = db.Column(db.String(20), nullable=False)
  user_agent = db.Column(db.String(500), nullable=False)
  created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now(), onupdate=db.func.now(), nullable=False)

  def to_dict(self):
    return {"id": self.id, "as_of_date": self.as_of_date, "path": self.path, "ip": self.ip, 'user_agent': self.user_agent, 'created_at': self.created_at}

# アクセス前リクエストをフック
@app.before_request
def log_request_info():

  # 静的ファイルは除外
  if request.path.startswith("/static") or request.path == "/favicon.ico":
    return

  access_logger.info(
    f"{request.remote_addr} {request.method} {request.path} "
    f"User-Agent: {request.user_agent.string}"
  )

  try:

    # アクセス情報書込
    new_access = TAccessLog(
      as_of_date=date.today()
      ,path=request.path
      ,ip=request.remote_addr
      ,user_agent=request.user_agent
    )
    db.session.add(new_access)
    db.session.commit()

  except SQLAlchemyError as e:
    access_logger.error(f"SQLAlchemy error: {e}")
    db.session.rollback()

  finally:
    pass

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
  newest_day = date(2000, 1, 1)

  # 各ファイルループ処理
  for f in listdir(dir_path):

    # 動画フルURL作成
    full_path = join(dir_path, f)

    # ファイル以外は処理対処外
    if not isfile(full_path):
      continue

    # mp4以外は処理対象外
    if not f.lower().endswith(".mp4"):
      continue
 
    # ファイルステータス取得
    size = getsize(full_path)
    mtime = getmtime(full_path)
    buf_date = datetime.strptime(f[:8], "%Y%m%d").date()

    # 基準日MAXを保持
    if newest_day < buf_date :
      newest_day = buf_date

    # 動画リストに情報追加
    move_list.append({
      "name": f
     ,"size": str(round( int(f"{size}") / (1024 * 1024), 2)) + "MB"
     ,"date": buf_date
     ,"updated_at": datetime.fromtimestamp(mtime)
     ,"url": url + f
    })

  # ソートする
  sorted_list = sorted(move_list, key=lambda x: x["updated_at"], reverse=True)


  # ./templates/index.htmlを送信
  return render_template('index.html', list=sorted_list, start_day=newest_day)


# 呼び出し
if __name__ == "__main__":
  app.run(threaded=True)
