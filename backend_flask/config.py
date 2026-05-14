import os
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
DEFAULT_DB_PATH = ROOT_DIR / "backend" / "data" / "hireflow.db"
DEFAULT_UPLOAD_FOLDER = ROOT_DIR / "backend" / "uploads"


def _sqlite_uri_from_path(path_value):
    db_path = Path(path_value).expanduser()
    if not db_path.is_absolute():
        db_path = ROOT_DIR / db_path
    return f"sqlite:///{db_path}"


class Config:
    SECRET_KEY = os.getenv("ACCESS_TOKEN_SECRET", "hireflow-dev-secret")
    JWT_SECRET = SECRET_KEY
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        _sqlite_uri_from_path(os.getenv("HIREFLOW_DB_PATH", DEFAULT_DB_PATH)),
    )
    UPLOAD_FOLDER = Path(os.getenv("HIREFLOW_UPLOAD_FOLDER", DEFAULT_UPLOAD_FOLDER))
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024
    REMOTIVE_API_URL = os.getenv(
        "REMOTIVE_API_URL",
        "https://remotive.com/api/remote-jobs",
    )
    ROOT_DIR = ROOT_DIR
