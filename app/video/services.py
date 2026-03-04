# app/video/services.py

from datetime import date
import re
import os
from .utils import (
    list_video_files,
    is_video_file,
    is_file,
    extract_date_from_filename,
    get_file_size_mb,
    get_file_mtime,
    build_video_url,
)
from os.path import join

# 設定のインポート
from app.config import Config

# 動画ファイルのリストを取得するサービス関数
def get_video_list():
    # 動画ファイルのディレクトリを設定から取得
    dir_path = Config.MOVE_DIR
    base_url = "https://snake-fish.com/elfinito/move/"

    move_list = []
    name_list = []
    newest_day = date(2000, 1, 1)

    # ディレクトリが存在しない場合はスキップ
    if not os.path.isdir(dir_path):
        print(f"Warning: Directory not found: {dir_path}")
        return move_list, newest_day, name_list

    for filename in list_video_files(dir_path):
        full_path = join(dir_path, filename)

        if not is_file(full_path):
            continue
        if not is_video_file(filename):
            continue

        # 動画メンバー取得
        match = re.search(r"\d{8}_(.*)_(.*).mp4", filename)
        if match:
            name_list.append(match.group(1))
            name_list.append(match.group(2))

        file_date = extract_date_from_filename(filename)
        if file_date is None:
            continue

        size = get_file_size_mb(full_path)
        updated_at = get_file_mtime(full_path)
        url = build_video_url(base_url, filename)

        if newest_day < file_date:
            newest_day = file_date

        move_list.append({
            "name": filename,
            "size": size,
            "date": file_date,
            "updated_at": updated_at,
            "url": url
        })

    sorted_list = sorted(move_list, key=lambda x: x["updated_at"], reverse=True)

    # 重複を削除して名前リストをソート
    name_list = sorted(set(name_list))

    return sorted_list, newest_day, name_list

