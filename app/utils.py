# app/utils.py
"""共有ユーティリティ関数を収めるモジュール

現在はリクエスト情報をログに残す処理のみ実装している。
各ブループリントからインポートして使用する。
"""

from flask import abort, request
from datetime import date
from sqlalchemy.exc import SQLAlchemyError

from .extensions import db, access_logger
from .models import TAccessLog


def log_request_info():
    """リクエスト情報を DB に記録する。

    - SNS クローラーを拒否
    - 静的ファイルをスキップ
    - エラーが発生した場合はログを記録してロールバック

    この関数はブループリント側で
    ``before_app_request`` や ``before_request`` に登録して使う。
    """

    ua = request.user_agent.string

    # SNS除外
    if "Instagram" in ua or " [FB" in ua or "facebookexternalhit" in ua:
        access_logger.info(f"Blocked SNS crawler: {ua}")
        abort(403)

    # 静的ファイル除外
    if request.path in ("/static/", "/favicon.ico"):
        return

    try:
        new_access = TAccessLog(
            as_of_date=date.today(),
            path=request.path,
            ip=request.remote_addr,
            user_agent=ua
        )
        db.session.add(new_access)
        db.session.commit()

    except SQLAlchemyError as e:
        access_logger.error(f"SQLAlchemy error: {e}")
        db.session.rollback()
    except Exception as e:
        access_logger.error(f"Unexpected error while logging request: {e}")
        db.session.rollback()
