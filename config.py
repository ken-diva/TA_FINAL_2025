import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    # Flask configuration
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-secret-key-change-in-production"

    # MySQL configuration
    MYSQL_HOST = os.environ.get("MYSQL_HOST") or "localhost"
    MYSQL_USER = os.environ.get("MYSQL_USER") or "root"
    MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD") or ""
    MYSQL_DATABASE = os.environ.get("MYSQL_DB") or "sport_room_booking"
    MYSQL_PORT = int(os.environ.get("MYSQL_PORT") or 3306)

    # Session configuration
    SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
