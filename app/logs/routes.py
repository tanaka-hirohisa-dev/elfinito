from flask import Blueprint

# 複数のブループリントから呼び出す共有機能として移動した
from ..utils import log_request_info

logs_bp = Blueprint("logs", __name__, template_folder="templates", static_folder="static")

# アプリ全体で使う場合は before_app_request に登録
logs_bp.before_app_request(log_request_info)

