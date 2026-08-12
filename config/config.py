"""
=========================================================
OmniMind AI Assistant
Configuration File
=========================================================
"""

import os
from dotenv import load_dotenv

# ==========================================================
# LOAD ENVIRONMENT VARIABLES
# ==========================================================

load_dotenv()

# ==========================================================
# APPLICATION
# ==========================================================

APP_NAME = "OmniMind AI"
APP_VERSION = "1.0.0"

APP_DESCRIPTION = """
An Intelligent Multimodal AI Assistant built using
Large Language Models, Computer Vision,
Speech AI, and Retrieval-Augmented Generation.
"""

PAGE_TITLE = "OmniMind AI Assistant"
PAGE_ICON = "🤖"

LAYOUT = "wide"
SIDEBAR_STATE = "expanded"

# ==========================================================
# API KEYS
# ==========================================================

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Gemini uses Google API Key
GEMINI_API_KEY = GOOGLE_API_KEY

# Optional APIs
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

# ==========================================================
# AVAILABLE MODELS
# ==========================================================

AVAILABLE_MODELS = {
    "Gemini": [
        "gemini-2.5-flash",
        "gemini-2.5-flash-lite",
    ],
    "OpenAI": [
        "gpt-3.5-turbo",
    ],
}

# ==========================================================
# CHAT SETTINGS
# ==========================================================

TEMPERATURE = 0.7
MAX_TOKENS = 4096
TOP_P = 1.0
MAX_CHAT_HISTORY = 20

# ==========================================================
# FILE SETTINGS
# ==========================================================

MAX_FILE_SIZE_MB = 25

SUPPORTED_IMAGE_FORMATS = [
    "png",
    "jpg",
    "jpeg",
    "webp",
]

SUPPORTED_DOCUMENT_FORMATS = [
    "pdf",
    "docx",
    "txt",
]

SUPPORTED_AUDIO_FORMATS = [
    "wav",
    "mp3",
    "m4a",
]

# ==========================================================
# DATABASE
# ==========================================================

DATABASE_PATH = "database/assistant.db"
VECTOR_DB_PATH = "database/vector_store"
CONVERSATION_PATH = "database/conversations"

# ==========================================================
# UPLOADS
# ==========================================================

UPLOAD_FOLDER = "uploads"
IMAGE_FOLDER = "uploads/images"
DOCUMENT_FOLDER = "uploads/documents"
AUDIO_FOLDER = "uploads/audio"
TEMP_FOLDER = "uploads/temporary"

# ==========================================================
# EXPORTS
# ==========================================================

EXPORT_FOLDER = "exports"
PDF_EXPORT = "exports/pdf"
CSV_EXPORT = "exports/csv"
CHAT_EXPORT = "exports/chats"

# ==========================================================
# LOGGING
# ==========================================================

LOG_LEVEL = "INFO"
LOG_FILE = "logs/application.log"

# ==========================================================
# CACHE
# ==========================================================

ENABLE_CACHE = True
CACHE_SIZE = 100

# ==========================================================
# RAG
# ==========================================================

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
TOP_K = 5

# ==========================================================
# MEMORY
# ==========================================================

ENABLE_MEMORY = True
MEMORY_LIMIT = 100

# ==========================================================
# WEB SEARCH
# ==========================================================

ENABLE_WEB_SEARCH = True
SEARCH_RESULTS = 5

# ==========================================================
# ANALYTICS
# ==========================================================

ENABLE_ANALYTICS = True
TRACK_USAGE = True

# ==========================================================
# SETTINGS OBJECT
# ==========================================================


class Settings:

    def __init__(self):

        # Application
        self.APP_NAME = APP_NAME
        self.APP_VERSION = APP_VERSION
        self.APP_DESCRIPTION = APP_DESCRIPTION
        self.PAGE_TITLE = PAGE_TITLE
        self.PAGE_ICON = PAGE_ICON
        self.LAYOUT = LAYOUT
        self.SIDEBAR_STATE = SIDEBAR_STATE

        # API Keys
        self.OPENAI_API_KEY = OPENAI_API_KEY
        self.GOOGLE_API_KEY = GOOGLE_API_KEY
        self.GEMINI_API_KEY = GEMINI_API_KEY
        self.GROQ_API_KEY = GROQ_API_KEY
        self.SERPER_API_KEY = SERPER_API_KEY

        # Available Models
        self.AVAILABLE_MODELS = AVAILABLE_MODELS

        # Chat
        self.TEMPERATURE = TEMPERATURE
        self.MAX_TOKENS = MAX_TOKENS
        self.TOP_P = TOP_P
        self.MAX_CHAT_HISTORY = MAX_CHAT_HISTORY

        # File Settings
        self.MAX_FILE_SIZE_MB = MAX_FILE_SIZE_MB
        self.SUPPORTED_IMAGE_FORMATS = SUPPORTED_IMAGE_FORMATS
        self.SUPPORTED_DOCUMENT_FORMATS = SUPPORTED_DOCUMENT_FORMATS
        self.SUPPORTED_AUDIO_FORMATS = SUPPORTED_AUDIO_FORMATS

        # Database
        self.DATABASE_PATH = DATABASE_PATH
        self.VECTOR_DB_PATH = VECTOR_DB_PATH
        self.CONVERSATION_PATH = CONVERSATION_PATH

        # Uploads
        self.UPLOAD_FOLDER = UPLOAD_FOLDER
        self.IMAGE_FOLDER = IMAGE_FOLDER
        self.DOCUMENT_FOLDER = DOCUMENT_FOLDER
        self.AUDIO_FOLDER = AUDIO_FOLDER
        self.TEMP_FOLDER = TEMP_FOLDER

        # Exports
        self.EXPORT_FOLDER = EXPORT_FOLDER
        self.PDF_EXPORT = PDF_EXPORT
        self.CSV_EXPORT = CSV_EXPORT
        self.CHAT_EXPORT = CHAT_EXPORT

        # Logging
        self.LOG_LEVEL = LOG_LEVEL
        self.LOG_FILE = LOG_FILE

        # Cache
        self.ENABLE_CACHE = ENABLE_CACHE
        self.CACHE_SIZE = CACHE_SIZE

        # RAG
        self.CHUNK_SIZE = CHUNK_SIZE
        self.CHUNK_OVERLAP = CHUNK_OVERLAP
        self.TOP_K = TOP_K

        # Memory
        self.ENABLE_MEMORY = ENABLE_MEMORY
        self.MEMORY_LIMIT = MEMORY_LIMIT

        # Web Search
        self.ENABLE_WEB_SEARCH = ENABLE_WEB_SEARCH
        self.SEARCH_RESULTS = SEARCH_RESULTS

        # Analytics
        self.ENABLE_ANALYTICS = ENABLE_ANALYTICS
        self.TRACK_USAGE = TRACK_USAGE


settings = Settings()
