"""
=========================================================
OmniMind AI Assistant
Security Utilities
=========================================================

Reusable cryptographic and security helper functions.
"""

from __future__ import annotations

import hashlib
import hmac
import secrets
from pathlib import Path

# =========================================================
# SHA-256 HASH
# =========================================================


def hash_text(text: str) -> str:
    """
    Generate SHA-256 hash.
    """

    return hashlib.sha256(text.encode("utf-8")).hexdigest()


# =========================================================
# HASH VERIFICATION
# =========================================================


def verify_hash(
    text: str,
    hashed: str,
) -> bool:
    """
    Verify SHA-256 hash.
    """

    return hmac.compare_digest(
        hash_text(text),
        hashed,
    )


# =========================================================
# RANDOM TOKEN
# =========================================================


def generate_token(
    length: int = 32,
) -> str:
    """
    Generate secure random token.
    """

    return secrets.token_hex(length)


# =========================================================
# RANDOM URL TOKEN
# =========================================================


def generate_urlsafe_token(
    length: int = 32,
) -> str:
    """
    Generate URL-safe token.
    """

    return secrets.token_urlsafe(length)


# =========================================================
# RANDOM PASSWORD
# =========================================================


def generate_password(
    length: int = 16,
) -> str:
    """
    Generate secure password.
    """

    alphabet = (
        "abcdefghijklmnopqrstuvwxyz"
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        "0123456789"
        "!@#$%^&*()-_=+"
    )

    return "".join(secrets.choice(alphabet) for _ in range(length))


# =========================================================
# RANDOM SECRET
# =========================================================


def generate_secret(
    bytes_length: int = 32,
) -> str:
    """
    Generate cryptographic secret.
    """

    return secrets.token_hex(bytes_length)


# =========================================================
# HMAC SIGNATURE
# =========================================================


def hmac_signature(
    message: str,
    secret: str,
) -> str:
    """
    Generate HMAC SHA-256 signature.
    """

    return hmac.new(
        secret.encode(),
        message.encode(),
        hashlib.sha256,
    ).hexdigest()


# =========================================================
# VERIFY SIGNATURE
# =========================================================


def verify_signature(
    message: str,
    secret: str,
    signature: str,
) -> bool:
    """
    Verify HMAC signature.
    """

    expected = hmac_signature(
        message,
        secret,
    )

    return hmac.compare_digest(
        expected,
        signature,
    )


# =========================================================
# FILE HASH
# =========================================================


def file_checksum(
    path: str | Path,
    algorithm: str = "sha256",
) -> str:
    """
    Calculate file checksum.
    """

    hasher = hashlib.new(algorithm)

    with open(path, "rb") as file:

        while chunk := file.read(8192):

            hasher.update(chunk)

    return hasher.hexdigest()


# =========================================================
# RANDOM HEX
# =========================================================


def random_hex(
    length: int = 16,
) -> str:
    """
    Generate random hexadecimal string.
    """

    return secrets.token_hex(length)


# =========================================================
# RANDOM BYTES
# =========================================================


def random_bytes(
    length: int = 32,
) -> bytes:
    """
    Generate secure random bytes.
    """

    return secrets.token_bytes(length)


# =========================================================
# MASK TEXT
# =========================================================


def mask_text(
    text: str,
    visible: int = 4,
) -> str:
    """
    Mask sensitive text.

    Example:
    ABCDEFGH1234
        ->
    ********1234
    """

    if len(text) <= visible:

        return "*" * len(text)

    return "*" * (len(text) - visible) + text[-visible:]


# =========================================================
# CONSTANT TIME COMPARE
# =========================================================


def secure_compare(
    first: str,
    second: str,
) -> bool:
    """
    Compare two strings securely.
    """

    return hmac.compare_digest(
        first,
        second,
    )
