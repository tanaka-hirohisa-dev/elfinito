# app/video/routes.py

from flask import Blueprint, render_template, request
from .services import get_video_list

video_bp = Blueprint(
    "video",
    __name__,
    template_folder="templates",
    static_folder="static"
)

@video_bp.errorhandler(404)
def page_not_found(e):
    # デバッグ用にリクエスト情報を表示
    html = f"""
        <h1>404 Not Found</h1>
        <p>Requested URL: {request.url}</p>
        <p>Method: {request.method}</p>
        <p>Args: {request.args}</p>
    """
    return html, 404

@video_bp.route("/")
def index():
    video_list, newest_day = get_video_list()
    return render_template("index.html", list=video_list, start_day=newest_day)

