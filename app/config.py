import os
from dotenv import load_dotenv
from datetime import timedelta

# Load environment variables from .env
load_dotenv()

class Config:
    # Flask secret key for session signing
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY", "dev-secret-key")

    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "postgresql://postgres:secret@localhost:5432/kishoreeeee"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable track modifications to save resources

    # Session configuration
    SESSION_TYPE = "filesystem"
    SESSION_PERMANENT = False
    PERMANENT_SESSION_LIFETIME = timedelta(hours=1)  # Optional: session expiry

    # CORS settings if needed
    CORS_SUPPORTS_CREDENTIALS = True
