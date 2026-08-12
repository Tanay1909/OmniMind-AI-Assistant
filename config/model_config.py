"""
=========================================================
OmniMind AI Assistant
AI Model Configuration
=========================================================
"""

from dataclasses import dataclass

# ==========================================================
# MODEL CONFIGURATION
# ==========================================================

@dataclass(frozen=True)
class ModelConfig:
    provider: str
    model_name: str
    temperature: float
    max_tokens: int
    top_p: float


# ==========================================================
# OPENAI MODELS
# ==========================================================

GPT_55 = ModelConfig(
    provider="OpenAI",
    model_name="gpt-5.5",
    temperature=0.7,
    max_tokens=4096,
    top_p=1.0,
)

GPT_55_MINI = ModelConfig(
    provider="OpenAI",
    model_name="gpt-5.5-mini",
    temperature=0.7,
    max_tokens=4096,
    top_p=1.0,
)

# ==========================================================
# GEMINI MODELS
# ==========================================================

GEMINI_PRO = ModelConfig(
    provider="Google",
    model_name="gemini-3.5-flash",
    temperature=0.7,
    max_tokens=8192,
    top_p=1.0,
)

GEMINI_FLASH = ModelConfig(
    provider="Google",
    model_name="gemini-3.5-flash",
    temperature=0.7,
    max_tokens=8192,
    top_p=1.0,
)

# ==========================================================
# EMBEDDING MODELS
# ==========================================================

EMBEDDING_MODELS = {
    "openai": "text-embedding-3-small",
    "openai_large": "text-embedding-3-large",
}

# ==========================================================
# VISION MODELS
# ==========================================================

VISION_MODELS = {
    "openai": "gpt-5.5",
    "gemini": "gemini-3.5-flash",
}

# ==========================================================
# SPEECH MODELS
# ==========================================================

SPEECH_TO_TEXT = {
    "openai": "whisper-1",
}

TEXT_TO_SPEECH = {
    "openai": "gpt-4o-mini-tts",
    "gtts": "gtts",
}

# ==========================================================
# AVAILABLE MODELS
# ==========================================================

AVAILABLE_CHAT_MODELS = {
    "GPT-5.5": GPT_55,
    "GPT-5.5 Mini": GPT_55_MINI,
    "Gemini 2.5 Pro": GEMINI_PRO,
    "Gemini 2.5 Flash": GEMINI_FLASH,
}

DEFAULT_CHAT_MODEL = "GPT-5.5"

# ==========================================================
# RAG CONFIGURATION
# ==========================================================

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
TOP_K = 5

# ==========================================================
# CHAT DEFAULTS
# ==========================================================

DEFAULT_TEMPERATURE = 0.7
DEFAULT_TOP_P = 1.0
DEFAULT_MAX_TOKENS = 4096

# ==========================================================
# IMAGE SETTINGS
# ==========================================================

MAX_IMAGE_WIDTH = 2048
MAX_IMAGE_HEIGHT = 2048

# ==========================================================
# DOCUMENT SETTINGS
# ==========================================================

MAX_DOCUMENT_PAGES = 200

# ==========================================================
# AUDIO SETTINGS
# ==========================================================

MAX_AUDIO_LENGTH_SECONDS = 300

# ==========================================================
# API RETRIES
# ==========================================================

MAX_RETRIES = 3
RETRY_DELAY = 2
