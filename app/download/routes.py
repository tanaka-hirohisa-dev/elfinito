# app/download/routes.py

from flask import Blueprint, render_template, request
# 設定のインポート
from app.config import Config
from os.path import join, isfile
from flask import send_from_directory, abort
from app.extensions import access_logger

# 利用する共通ログ処理
from ..utils import log_request_info

download_bp = Blueprint("download",__name__)

# 動画ブループリントへのアクセス時のみ呼び出す
download_bp.before_request(log_request_info)

@download_bp.route("/<path:filename>")
def download_file(filename):

  MOVE_DIR = Config.MOVE_DIR  # 設定からMOVE_DIRを取得

  # パラメータチェック
  normalized_path = join(MOVE_DIR, filename)
  if not normalized_path.startswith(MOVE_DIR):
    abort(400, description="Invalid file path")

  try:
    # ファイル存在チェック
    access_logger.info("call download_file")
    access_logger.info(MOVE_DIR)

    file_path = join(MOVE_DIR, filename)
    if not isfile(file_path):
      abort(404)

    # send_from_directory はディレクトリとファイル名を分けて指定
    return send_from_directory(
      directory=MOVE_DIR
     ,path=filename
     ,as_attachment=True   # 強制ダウンロード
    )
  except Exception as e:
    # エラー時は500
    abort(500, description=str(e))
