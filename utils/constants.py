"""
=========================================================
OmniMind AI Assistant
Application Constants
=========================================================

Central location for all application-wide constants.
"""

from __future__ import annotations

from pathlib import Path

# =========================================================
# APPLICATION
# =========================================================

APP_NAME = "OmniMind AI Assistant"

APP_VERSION = "1.0.0"

APP_AUTHOR = "OpenAI"

APP_DESCRIPTION = "Enterprise Multimodal AI Assistant"

# =========================================================
# PROJECT PATHS
# =========================================================

PROJECT_ROOT = Path.cwd()

DATA_DIR = PROJECT_ROOT / "data"

UPLOAD_DIR = PROJECT_ROOT / "uploads"

TEMP_DIR = PROJECT_ROOT / "temp"

LOG_DIR = PROJECT_ROOT / "logs"

CACHE_DIR = PROJECT_ROOT / "cache"

MODEL_DIR = PROJECT_ROOT / "models"

REPORT_DIR = PROJECT_ROOT / "reports"

EXPORT_DIR = PROJECT_ROOT / "exports"

# =========================================================
# DIRECTORIES
# =========================================================

DIRECTORIES = [
    DATA_DIR,
    UPLOAD_DIR,
    TEMP_DIR,
    LOG_DIR,
    CACHE_DIR,
    MODEL_DIR,
    REPORT_DIR,
    EXPORT_DIR,
]

# =========================================================
# FILE TYPES
# =========================================================

IMAGE_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".bmp",
    ".gif",
    ".webp",
}

AUDIO_EXTENSIONS = {
    ".wav",
    ".mp3",
    ".ogg",
    ".flac",
    ".m4a",
}

VIDEO_EXTENSIONS = {
    ".mp4",
    ".avi",
    ".mov",
    ".mkv",
    ".webm",
}

DOCUMENT_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".txt",
    ".csv",
    ".xlsx",
    ".pptx",
}

SUPPORTED_EXTENSIONS = (
    IMAGE_EXTENSIONS | AUDIO_EXTENSIONS | VIDEO_EXTENSIONS | DOCUMENT_EXTENSIONS
)

# =========================================================
# AI MODELS
# =========================================================

DEFAULT_CHAT_MODEL = "gpt-4.1"

DEFAULT_EMBEDDING_MODEL = "text-embedding-3-large"

DEFAULT_TRANSCRIPTION_MODEL = "whisper-1"

DEFAULT_TEMPERATURE = 0.7

MAX_TOKENS = 4096

# =========================================================
# STREAMLIT
# =========================================================

PAGE_TITLE = APP_NAME

PAGE_ICON = "🤖"

LAYOUT = "wide"

SIDEBAR_STATE = "expanded"

# =========================================================
# CACHE
# =========================================================

DEFAULT_CACHE_TTL = 3600

CACHE_SIZE = 1000

# =========================================================
# FILE LIMITS
# =========================================================

MAX_UPLOAD_SIZE_MB = 100

MAX_FILENAME_LENGTH = 255

# =========================================================
# DATABASE
# =========================================================

DEFAULT_PAGE_SIZE = 25

MAX_PAGE_SIZE = 100

# =========================================================
# LOGGING
# =========================================================

LOG_FILE_NAME = "omnimind.log"

LOG_LEVEL = "INFO"

# =========================================================
# STATUS
# =========================================================

STATUS_SUCCESS = "success"

STATUS_ERROR = "error"

STATUS_WARNING = "warning"

STATUS_INFO = "info"

# =========================================================
# HTTP
# =========================================================

HTTP_OK = 200

HTTP_CREATED = 201

HTTP_BAD_REQUEST = 400

HTTP_UNAUTHORIZED = 401

HTTP_FORBIDDEN = 403

HTTP_NOT_FOUND = 404

HTTP_INTERNAL_SERVER_ERROR = 500

# =========================================================
# MIME TYPES
# =========================================================

MIME_PDF = "application/pdf"

MIME_JSON = "application/json"

MIME_TEXT = "text/plain"

MIME_PNG = "image/png"

MIME_JPEG = "image/jpeg"

MIME_MP3 = "audio/mpeg"

MIME_WAV = "audio/wav"

# =========================================================
# COLORS
# =========================================================

PRIMARY_COLOR = "#2563EB"

SUCCESS_COLOR = "#22C55E"

WARNING_COLOR = "#FACC15"

ERROR_COLOR = "#EF4444"

INFO_COLOR = "#0EA5E9"

# =========================================================
# USER ROLES
# =========================================================

ROLE_ADMIN = "admin"

ROLE_USER = "user"

ROLE_GUEST = "guest"

# =========================================================
# CREATE DIRECTORIES
# =========================================================


def create_directories():
    """
    Create application directories.
    """

    for directory in DIRECTORIES:

        directory.mkdir(
            parents=True,
            exist_ok=True,
        )


create_directories()
