# app/video/utils.py

from datetime import datetime
from os import listdir
from os.path import join, getsize, getmtime, isfile

def list_video_files(dir_path: str):
    """ディレクトリ内のファイル一覧を返す"""
    return listdir(dir_path)

def is_video_file(filename: str) -> bool:
    """mp4 ファイルかどうか判定"""
    return filename.lower().endswith(".mp4")

def is_file(path: str) -> bool:
    """通常ファイルかどうか"""
    return isfile(path)

def extract_date_from_filename(filename: str):
    """ファイル名先頭8桁 (YYYYMMDD) を date 型に変換"""
    try:
        return datetime.strptime(filename[:8], "%Y%m%d").date()
    except ValueError:
        return None

def get_file_size_mb(path: str) -> str:
    """ファイルサイズを MB 文字列で返す"""
    size = getsize(path)
    return f"{round(size / (1024 * 1024), 2)}MB"

def get_file_mtime(path: str):
    """更新日時を datetime に変換して返す"""
    return datetime.fromtimestamp(getmtime(path))

def build_video_url(base_url: str, filename: str) -> str:
    """動画の URL を生成"""
    return base_url + filename

