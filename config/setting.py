
"""
=========================================================
OmniMind AI Assistant
Application Settings
=========================================================
"""

from __future__ import annotations

import os
from pathlib import Path
from dotenv import load_dotenv

# ==========================================================
# PROJECT ROOT
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

# ==========================================================
# LOAD ENVIRONMENT VARIABLES
# ==========================================================

load_dotenv(BASE_DIR / ".env")

# ==========================================================
# APPLICATION
# ==========================================================

APP_NAME = os.getenv("APP_NAME", "OmniMind AI")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
APP_ENV = os.getenv("APP_ENV", "development")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# ==========================================================
# API KEYS
# ==========================================================

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
SERPER_API_KEY = os.getenv("SERPER_API_KEY", "")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "")

# ==========================================================
# DATABASE
# ==========================================================

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///database/assistant.db"
)

VECTOR_DB_PATH = os.getenv(
    "VECTOR_DB_PATH",
    "database/vector_store"
)

# ==========================================================
# DIRECTORIES
# ==========================================================

UPLOAD_DIR = Path(os.getenv("UPLOAD_DIR", "uploads"))
EXPORT_DIR = Path(os.getenv("EXPORT_DIR", "exports"))

# ==========================================================
# AI SETTINGS
# ==========================================================

DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "gpt-5.5")
DEFAULT_TEMPERATURE = float(os.getenv("DEFAULT_TEMPERATURE", "0.7"))
DEFAULT_MAX_TOKENS = int(os.getenv("DEFAULT_MAX_TOKENS", "4096"))

# ==========================================================
# STREAMLIT
# ==========================================================

STREAMLIT_PORT = int(os.getenv("STREAMLIT_SERVER_PORT", "8501"))
HEADLESS = os.getenv(
    "STREAMLIT_SERVER_HEADLESS",
    "true"
).lower() == "true"

# ==========================================================
# VALIDATION
# ==========================================================

def validate_settings() -> None:
    """
    Validate required configuration.
    """

    required = {
        "OPENAI_API_KEY": OPENAI_API_KEY,
        "GOOGLE_API_KEY": GOOGLE_API_KEY,
    }

    missing = [
        key
        for key, value in required.items()
        if not value
    ]

    if missing:
        raise RuntimeError(
            "Missing required environment variables: "
            + ", ".join(missing)
        )

# ==========================================================
# OPTIONAL STARTUP VALIDATION
# ==========================================================

# Uncomment this in production if at least one provider
# must always be configured.
#
# validate_settings()

