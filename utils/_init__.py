"""
=========================================================
OmniMind AI Assistant
Utility Package
=========================================================

Central utility package shared across the entire project.

This package contains reusable helper functions that are
independent of business logic.

Modules
-------
helpers
validators
file_utils
text_utils
image_utils
audio_utils
pdf_utils
date_utils
security
formatters
logger
cache_utils
retry
constants
"""

from .helpers import *
from .validators import *
from .file_utils import *
from .text_utils import *
from .image_utils import *
from .audio_utils import *
from .pdf_utils import *
from .date_utils import *
from .security import *
from .formatters import *
from .logger import *
from .cache_utils import *
from .retry import *
from .constants import *

__version__ = "1.0.0"

__author__ = "OmniMind AI Team"

__all__ = [
    # Helpers
    "safe_execute",
    "flatten",
    "chunk_list",
    "generate_uuid",
    # Validators
    "is_email",
    "is_url",
    "is_empty",
    "is_number",
    # File Utilities
    "ensure_directory",
    "file_exists",
    "file_size",
    "allowed_extension",
    # Text Utilities
    "clean_text",
    "normalize_text",
    "truncate_text",
    "word_count",
    # Image Utilities
    "image_dimensions",
    "resize_image",
    # Audio Utilities
    "audio_duration",
    "convert_audio",
    # PDF Utilities
    "page_count",
    "extract_metadata",
    # Date Utilities
    "current_timestamp",
    "current_datetime",
    "format_datetime",
    # Security
    "hash_text",
    "verify_hash",
    "generate_token",
    # Formatters
    "format_bytes",
    "format_duration",
    "format_number",
    # Logger
    "get_logger",
    # Cache
    "clear_cache",
    "cache_key",
    # Retry
    "retry",
    # Constants
    "DEFAULT_ENCODING",
]
