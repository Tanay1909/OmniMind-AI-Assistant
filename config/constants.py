"""
=========================================================
OmniMind AI Assistant
Application Constants
=========================================================
"""

from pathlib import Path

# ==========================================================
# PROJECT PATHS
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

CONFIG_DIR = BASE_DIR / "config"
ASSETS_DIR = BASE_DIR / "assets"
UPLOADS_DIR = BASE_DIR / "uploads"
DATABASE_DIR = BASE_DIR / "database"
EXPORTS_DIR = BASE_DIR / "exports"
LOGS_DIR = BASE_DIR / "logs"
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"

# ==========================================================
# UPLOAD DIRECTORIES
# ==========================================================

IMAGE_UPLOAD_DIR = UPLOADS_DIR / "images"
DOCUMENT_UPLOAD_DIR = UPLOADS_DIR / "documents"
AUDIO_UPLOAD_DIR = UPLOADS_DIR / "audio"
TEMP_UPLOAD_DIR = UPLOADS_DIR / "temporary"

# ==========================================================
# DATABASE
# ==========================================================

SQLITE_DATABASE = DATABASE_DIR / "assistant.db"

VECTOR_DATABASE = DATABASE_DIR / "vector_store"

CHAT_HISTORY = DATABASE_DIR / "conversations"

# ==========================================================
# EXPORTS
# ==========================================================

PDF_EXPORT = EXPORTS_DIR / "pdf"

CSV_EXPORT = EXPORTS_DIR / "csv"

CHAT_EXPORT = EXPORTS_DIR / "chats"

# ==========================================================
# SUPPORTED FILE TYPES
# ==========================================================

IMAGE_EXTENSIONS = (
    ".png",
    ".jpg",
    ".jpeg",
    ".webp",
    ".bmp"
)

DOCUMENT_EXTENSIONS = (
    ".pdf",
    ".docx",
    ".txt",
    ".md"
)

AUDIO_EXTENSIONS = (
    ".wav",
    ".mp3",
    ".m4a",
    ".ogg"
)

# ==========================================================
# MIME TYPES
# ==========================================================

IMAGE_MIME_TYPES = [
    "image/png",
    "image/jpeg",
    "image/webp",
    "image/bmp"
]

DOCUMENT_MIME_TYPES = [
    "application/pdf",
    "text/plain",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
]

# ==========================================================
# LANGUAGES
# ==========================================================

SUPPORTED_LANGUAGES = [
    "English",
    "Hindi",
    "Spanish",
    "French",
    "German",
    "Japanese",
    "Chinese"
]

# ==========================================================
# AI MODELS
# ==========================================================

OPENAI_MODELS = [
    "gpt-5.5",
    "gpt-5.5-mini"
]

GEMINI_MODELS = [
    "gemini-3.5-flash",
]

EMBEDDING_MODELS = [
    "text-embedding-3-small",
    "text-embedding-3-large"
]

# ==========================================================
# STREAMLIT THEMES
# ==========================================================

THEMES = [
    "Light",
    "Dark",
    "System"
]

# ==========================================================
# SIDEBAR MENU
# ==========================================================

MENU_ITEMS = [
    "🏠 Home",
    "💬 AI Chat",
    "📄 Document Chat",
    "🖼 Image Analysis",
    "🎤 Voice Assistant",
    "🌐 Web Search",
    "🤖 AI Agents",
    "📊 Analytics",
    "📜 History",
    "⚙ Settings"
]

# ==========================================================
# CHAT ROLES
# ==========================================================

USER = "user"

ASSISTANT = "assistant"

SYSTEM = "system"

# ==========================================================
# FILE SIZE LIMITS
# ==========================================================

MAX_IMAGE_SIZE_MB = 10

MAX_DOCUMENT_SIZE_MB = 25

MAX_AUDIO_SIZE_MB = 20

# ==========================================================
# IMAGE SETTINGS
# ==========================================================

MAX_IMAGE_WIDTH = 2048

MAX_IMAGE_HEIGHT = 2048

# ==========================================================
# RAG SETTINGS
# ==========================================================

DEFAULT_CHUNK_SIZE = 1000

DEFAULT_CHUNK_OVERLAP = 200

DEFAULT_TOP_K = 5

# ==========================================================
# SESSION KEYS
# ==========================================================

SESSION_CHAT = "chat_history"

SESSION_MESSAGES = "messages"

SESSION_MODEL = "selected_model"

SESSION_MEMORY = "memory"

# ==========================================================
# LOGGING
# ==========================================================

LOG_FORMAT = (
    "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# ==========================================================
# STATUS
# ==========================================================

SUCCESS = "success"

ERROR = "error"

WARNING = "warning"

INFO = "info"

# ==========================================================
# APPLICATION INFORMATION
# ==========================================================

AUTAUTHOR = "Tanay Sadhu"

PROJECT_NAME = "OmniMind AI Assistant"

APP_NAME = PROJECT_NAME

VERSION = "1.0.0"

# ==========================================================
# RANDOM
# ==========================================================

DEFAULT_ENCODING = "utf-8"

DEFAULT_TIMEOUT = 60

CACHE_TTL = 3600

# ==========================================================
# Backward Compatibility
# ==========================================================

APP_NAME = PROJECT_NAME
AUTHOR = "Tanay Sadhu"

PROJECT_NAME = "OmniMind AI Assistant"

APP_NAME = PROJECT_NAME

VERSION = "1.0.0"

LICENSE = "MIT"
