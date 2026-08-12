
"""
=========================================================
OmniMind AI Assistant
Core Validator
=========================================================

Validation utilities used throughout the application.
"""

from __future__ import annotations

from pathlib import Path

from config.constants import (
    IMAGE_EXTENSIONS,
    DOCUMENT_EXTENSIONS,
    AUDIO_EXTENSIONS,
    MAX_IMAGE_SIZE_MB,
    MAX_DOCUMENT_SIZE_MB,
    MAX_AUDIO_SIZE_MB,
)

from core.exceptions import (
    MissingAPIKeyError,
    UnsupportedFileTypeError,
    FileTooLargeError,
    ValidationError,
)


class Validator:
    """Central validation utility."""

    # =====================================================
    # API KEY
    # =====================================================

    @staticmethod
    def validate_api_key(api_key: str | None, provider: str) -> bool:
        """
        Validate API key.
        """

        if not api_key or not api_key.strip():
            raise MissingAPIKeyError(
                f"{provider} API key is missing."
            )

        return True

    # =====================================================
    # FILE TYPE
    # =====================================================

    @staticmethod
    def validate_file_extension(
        filename: str,
        allowed_extensions: tuple | list,
    ) -> bool:

        suffix = Path(filename).suffix.lower()

        if suffix not in allowed_extensions:
            raise UnsupportedFileTypeError(
                f"Unsupported file type: {suffix}"
            )

        return True

    # =====================================================
    # FILE SIZE
    # =====================================================

    @staticmethod
    def validate_file_size(
        file_size: int,
        max_size_mb: int,
    ) -> bool:
        """
        file_size should be in bytes.
        """

        max_bytes = max_size_mb * 1024 * 1024

        if file_size > max_bytes:
            raise FileTooLargeError(
                f"Maximum allowed size is {max_size_mb} MB."
            )

        return True

    # =====================================================
    # IMAGE
    # =====================================================

    @classmethod
    def validate_image(
        cls,
        filename: str,
        file_size: int,
    ) -> bool:

        cls.validate_file_extension(
            filename,
            IMAGE_EXTENSIONS,
        )

        cls.validate_file_size(
            file_size,
            MAX_IMAGE_SIZE_MB,
        )

        return True

    # =====================================================
    # DOCUMENT
    # =====================================================

    @classmethod
    def validate_document(
        cls,
        filename: str,
        file_size: int,
    ) -> bool:

        cls.validate_file_extension(
            filename,
            DOCUMENT_EXTENSIONS,
        )

        cls.validate_file_size(
            file_size,
            MAX_DOCUMENT_SIZE_MB,
        )

        return True

    # =====================================================
    # AUDIO
    # =====================================================

    @classmethod
    def validate_audio(
        cls,
        filename: str,
        file_size: int,
    ) -> bool:

        cls.validate_file_extension(
            filename,
            AUDIO_EXTENSIONS,
        )

        cls.validate_file_size(
            file_size,
            MAX_AUDIO_SIZE_MB,
        )

        return True

    # =====================================================
    # CHAT INPUT
    # =====================================================

    @staticmethod
    def validate_prompt(prompt: str) -> bool:

        if not prompt:
            raise ValidationError("Prompt cannot be empty.")

        if len(prompt.strip()) == 0:
            raise ValidationError("Prompt cannot be blank.")

        return True

    # =====================================================
    # MODEL
    # =====================================================

    @staticmethod
    def validate_model(
        model_name: str,
        available_models: dict,
    ) -> bool:

        if model_name not in available_models:
            raise ValidationError(
                f"Unknown model: {model_name}"
            )

        return True

