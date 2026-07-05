import os

class Config:

    # =====================================
    # Secret Key
    # =====================================

    SECRET_KEY = "LifeLink@2026"

    # =====================================
    # Database Configuration
    # =====================================

    SQLALCHEMY_DATABASE_URI = (
        "mysql+pymysql://root:ntranna%24567A@localhost/lifelink"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # =====================================
    # Upload Configuration
    # =====================================

    UPLOAD_FOLDER = os.path.join("static", "uploads")

    MAX_CONTENT_LENGTH = 5 * 1024 * 1024

    ALLOWED_EXTENSIONS = {
        "png",
        "jpg",
        "jpeg"
    }

    # =====================================
    # Gmail SMTP Configuration
    # =====================================

    MAIL_SERVER = "smtp.gmail.com"

    MAIL_PORT = 587

    MAIL_USE_TLS = True

    MAIL_USE_SSL = False

    MAIL_USERNAME = "lifelink.bloodconnect@gmail.com"

    MAIL_PASSWORD = "tius mzld vona ivoc"

    MAIL_DEFAULT_SENDER = "lifelink.bloodconnect@gmail.com"