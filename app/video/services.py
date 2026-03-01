# app/video/services.py

from datetime import date
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

def get_video_list():
    dir_path = "/home/users/2/lolipop.jp-62450bf91a38e3ec/move"
    base_url = "https://snake-fish.com/elfinito/move/"

    move_list = []
    newest_day = date(2000, 1, 1)

    for filename in list_video_files(dir_path):
        full_path = join(dir_path, filename)

        if not is_file(full_path):
            continue
        if not is_video_file(filename):
            continue

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

    return sorted_list, newest_day

