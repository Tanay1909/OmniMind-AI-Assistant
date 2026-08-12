"""
=========================================================
OmniMind AI Assistant
Validation Utilities
=========================================================

Reusable validation functions for the entire application.
"""

from __future__ import annotations

import re
import uuid
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

# =========================================================
# EMPTY VALUE
# =========================================================


def is_empty(value: Any) -> bool:
    """
    Check whether a value is empty.
    """

    if value is None:
        return True

    if isinstance(value, str):
        return value.strip() == ""

    if isinstance(value, (list, tuple, set, dict)):
        return len(value) == 0

    return False


# =========================================================
# EMAIL
# =========================================================

EMAIL_PATTERN = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")


def is_email(email: str) -> bool:
    """
    Validate email address.
    """

    if is_empty(email):
        return False

    return bool(EMAIL_PATTERN.fullmatch(email.strip()))


# =========================================================
# URL
# =========================================================


def is_url(url: str) -> bool:
    """
    Validate URL.
    """

    try:
        parsed = urlparse(url)

        return all(
            [
                parsed.scheme in ("http", "https"),
                parsed.netloc,
            ]
        )

    except Exception:
        return False


# =========================================================
# PHONE NUMBER
# =========================================================

PHONE_PATTERN = re.compile(r"^\+?[0-9]{10,15}$")


def is_phone(phone: str) -> bool:
    """
    Validate phone number.
    """

    if is_empty(phone):
        return False

    phone = phone.replace(" ", "")

    return bool(PHONE_PATTERN.fullmatch(phone))


# =========================================================
# PASSWORD
# =========================================================


def is_strong_password(password: str) -> bool:
    """
    Minimum:
    • 8 characters
    • uppercase
    • lowercase
    • digit
    • special character
    """

    if len(password) < 8:
        return False

    if not re.search(r"[A-Z]", password):
        return False

    if not re.search(r"[a-z]", password):
        return False

    if not re.search(r"\d", password):
        return False

    if not re.search(r"[!@#$%^&*()_\-+=<>?/]", password):
        return False

    return True


# =========================================================
# INTEGER
# =========================================================


def is_integer(value: Any) -> bool:
    """
    Check integer.
    """

    try:
        int(value)
        return True

    except (ValueError, TypeError):
        return False


# =========================================================
# FLOAT
# =========================================================


def is_float(value: Any) -> bool:
    """
    Check float.
    """

    try:
        float(value)
        return True

    except (ValueError, TypeError):
        return False


# =========================================================
# NUMBER
# =========================================================


def is_number(value: Any) -> bool:
    """
    Check numeric value.
    """

    return is_integer(value) or is_float(value)


# =========================================================
# RANGE
# =========================================================


def in_range(
    value: float,
    minimum: float,
    maximum: float,
) -> bool:
    """
    Validate numeric range.
    """

    return minimum <= value <= maximum


# =========================================================
# UUID
# =========================================================


def is_uuid(value: str) -> bool:
    """
    Validate UUID.
    """

    try:
        uuid.UUID(value)
        return True

    except Exception:
        return False


# =========================================================
# FILE EXTENSION
# =========================================================


def allowed_extension(
    filename: str,
    extensions: list[str],
) -> bool:
    """
    Check allowed extension.
    """

    suffix = Path(filename).suffix.lower()

    extensions = [
        ext.lower() if ext.startswith(".") else f".{ext.lower()}" for ext in extensions
    ]

    return suffix in extensions


# =========================================================
# FILE SIZE
# =========================================================


def max_file_size(
    size_bytes: int,
    max_mb: int,
) -> bool:
    """
    Validate maximum file size.
    """

    return size_bytes <= max_mb * 1024 * 1024


# =========================================================
# IMAGE FILE
# =========================================================

IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".gif",
    ".webp",
}


def is_image(filename: str) -> bool:
    """
    Validate image file.
    """

    return Path(filename).suffix.lower() in IMAGE_EXTENSIONS


# =========================================================
# AUDIO FILE
# =========================================================

AUDIO_EXTENSIONS = {
    ".wav",
    ".mp3",
    ".ogg",
    ".flac",
    ".m4a",
}


def is_audio(filename: str) -> bool:
    """
    Validate audio file.
    """

    return Path(filename).suffix.lower() in AUDIO_EXTENSIONS


# =========================================================
# PDF
# =========================================================


def is_pdf(filename: str) -> bool:
    """
    Validate PDF file.
    """

    return Path(filename).suffix.lower() == ".pdf"


# =========================================================
# JSON
# =========================================================


def is_json(text: str) -> bool:
    """
    Check JSON string.
    """

    import json

    try:
        json.loads(text)
        return True

    except Exception:
        return False
