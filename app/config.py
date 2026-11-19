"""Application configuration loaded from environment variables."""
import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-key-change-me")

    # Database: SQLite by default, but DATABASE_URL lets prod switch to
    # PostgreSQL (e.g. postgresql://user:pass@host:5432/dbname) with no code change.
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "sqlite:///" + os.path.join(basedir, "app.db")
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Uploads
    UPLOAD_FOLDER = os.path.join(basedir, "app", "static", "uploads")
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10 MB hard cap at the WSGI level
    ALLOWED_IMAGE_EXTENSIONS = {"png", "jpg", "jpeg", "webp", "gif"}
    ALLOWED_DOCUMENT_EXTENSIONS = {"pdf"}
    MAX_IMAGE_SIZE_BYTES = 5 * 1024 * 1024
    MAX_DOCUMENT_SIZE_BYTES = 10 * 1024 * 1024

    # Admin bootstrap (used by `flask create-admin`)
    ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")
    ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", "admin@example.com")
    ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "changeme123")

    # Local admin mode (set by the desktop launcher): auto-login from 127.0.0.1 and
    # enable the "Publier" button. Never set this on a public server.
    LOCAL_ADMIN = os.environ.get("LOCAL_ADMIN") == "1"

    # Sessions / remember-me
    REMEMBER_COOKIE_DURATION = timedelta(days=14)

    # Languages
    LANGUAGES = ["fr", "en"]
    DEFAULT_LANGUAGE = os.environ.get("DEFAULT_LANGUAGE", "fr")

    # Privacy-friendly analytics (Plausible / Umami). Leave empty to disable.
    ANALYTICS_SCRIPT_SRC = os.environ.get("ANALYTICS_SCRIPT_SRC", "")
    ANALYTICS_SCRIPT_DOMAIN = os.environ.get("ANALYTICS_SCRIPT_DOMAIN", "")

    # Rate limiting storage (in-memory by default, use redis:// in production)
    RATELIMIT_STORAGE_URI = os.environ.get("RATELIMIT_STORAGE_URI", "memory://")

    SITE_URL = os.environ.get("SITE_URL", "http://localhost:5000")


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False


config_by_name = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}
