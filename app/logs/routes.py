from flask import Blueprint, abort, request
from datetime import date
from sqlalchemy.exc import SQLAlchemyError
from ..extensions import db, access_logger
from .models import TAccessLog

logs_bp = Blueprint("logs", __name__, template_folder="templates", static_folder="static")

@logs_bp.before_app_request
def log_request_info():

    ua = request.user_agent.string

    # SNS除外
    if "Instagram" in ua or " [FB" in ua or "facebookexternalhit" in ua:
        access_logger.info(f"Blocked SNS crawler: {ua}")
        abort(403)

    # 静的ファイル除外
    if request.path.startswith("/static") or request.path == "/favicon.ico":
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

