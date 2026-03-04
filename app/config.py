from os import getenv
from dotenv import load_dotenv

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{getenv('PY_USER')}:{getenv('PY_PASSWORD')}"
        f"@{getenv('PY_HOST')}/{getenv('PY_DATABASE')}?charset=utf8"
    )
    MOVE_DIR = getenv("PRIVATE_PATH", "/path/to/move")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

