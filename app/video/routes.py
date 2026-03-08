# app/video/routes.py

from flask import Blueprint, render_template, request, send_from_directory
from os.path import join
from .services import get_video_list

# 利用する共通ログ処理
from ..utils import log_request_info

video_bp = Blueprint(
    "video",
    __name__,
    template_folder="templates",
    static_folder="static"
)

# 動画ブループリントへのアクセス時のみ呼び出す
video_bp.before_request(log_request_info)

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

# アイコンの設定
@video_bp.route('/favicon.ico')
def favicon():
  # ./static/favicon.icoを送信
  return send_from_directory(join(video_bp.root_path, 'static'), 'favicon.ico')

@video_bp.route("/")
def index():
    video_list, newest_day, name_list = get_video_list()

    # 動画リストフィルタリングパラメータ取得
    page = request.args.get("page", "20")
    # 件数によるフィルタリング
    if page.isdigit():
        page = int(page)
        if page > 0:
            video_list = video_list[:page]
    # 全件出力
    elif page == "all":
        pass
    # 名前によるフィルタリング
    else:
        video_list = [entry for entry in video_list if page in entry["name"]]

    return render_template(
        "index.html",
        list=video_list,
        start_day=newest_day,
        name_list=name_list,
        page=page
    )

