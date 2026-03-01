from flask import Flask
from .config import Config
from .extensions import db, access_logger

# Blueprint読込
from .video import video_bp
from .logs import logs_bp
from .api import api_bp

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)

    # DB初期化
    db.init_app(app)

    # Blueprint 登録
    app.register_blueprint(video_bp, url_prefix="/video")
    app.register_blueprint(logs_bp, url_prefix="/logs")
    app.register_blueprint(api_bp, url_prefix="/api")

    return app

