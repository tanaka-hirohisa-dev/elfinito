from flask_sqlalchemy import SQLAlchemy
import logging
from logging.handlers import RotatingFileHandler

db = SQLAlchemy()

# アクセスログ
access_logger = logging.getLogger("werkzeug")
handler = RotatingFileHandler(
    "access.log", maxBytes=1_000_000, backupCount=5, encoding="utf-8"
)
access_logger.addHandler(handler)

