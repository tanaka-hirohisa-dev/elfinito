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
    app.register_blueprint(video_bp, url_prefix="/")
    app.register_blueprint(logs_bp, url_prefix="/logs")
    app.register_blueprint(api_bp, url_prefix="/api")

    # グローバルエラーハンドラ
    @app.errorhandler(500)
    def internal_server_error(error):
        access_logger.error(f"500 Internal Server Error: {error}")
        return {
            "error": "Internal Server Error",
            "message": str(error)
        }, 500

    @app.errorhandler(Exception)
    def handle_exception(error):
        access_logger.error(f"Unhandled exception: {error}", exc_info=True)
        return {
            "error": "Server Error",
            "message": "An unexpected error occurred"
        }, 500

    return app

