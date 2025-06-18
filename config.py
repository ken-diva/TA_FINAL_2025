import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "your-secret-key-here"

    # MySQL Configuration
    MYSQL_HOST = os.environ.get("MYSQL_HOST") or "localhost"
    MYSQL_USER = os.environ.get("MYSQL_USER") or "root"
    MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD") or ""
    MYSQL_DB = os.environ.get("MYSQL_DB") or "sport_room_booking"
    MYSQL_PORT = int(os.environ.get("MYSQL_PORT", 3306))

    # Flask-MySQLdb configuration
    MYSQL_CURSORCLASS = "DictCursor"
    MYSQL_AUTOCOMMIT = True

    # Upload folder for images and 3D models
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
