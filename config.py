import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Project root directory
BASE_DIR = Path(__file__).resolve().parent


class Config:

    SECRET_KEY = os.getenv("SECRET_KEY")

    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

    OLLAMA_MODEL = "qwen2.5:3b"

    UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")

    REPORT_FOLDER = os.path.join(BASE_DIR, "reports")

    MAX_CONTENT_LENGTH = 16 * 1024 * 1024