import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:

    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "LifeLink@2026"
    )

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "sqlite:///" + os.path.join(BASE_DIR, "lifelink.db")
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER = os.path.join(
        "static",
        "uploads"
    )

    MAX_CONTENT_LENGTH = 5 * 1024 * 1024

    ALLOWED_EXTENSIONS = {
        "png",
        "jpg",
        "jpeg"
    }

    MAIL_SERVER = "smtp.gmail.com"

    MAIL_PORT = 587

    MAIL_USE_TLS = True

    MAIL_USE_SSL = False

    MAIL_USERNAME = os.getenv(
        "MAIL_USERNAME",
        "lifelink.bloodconnect@gmail.com"
    )

    MAIL_PASSWORD = os.getenv(
        "MAIL_PASSWORD",
        ""
    )

    MAIL_DEFAULT_SENDER = MAIL_USERNAME