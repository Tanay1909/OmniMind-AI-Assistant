"""
=========================================================
OmniMind AI Assistant
Translation Service
=========================================================

Provides:

- Language Detection
- Text Translation

Default Provider:

- Google Translate

Future Providers:

- DeepL
- OpenAI
- Gemini
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

from deep_translator import GoogleTranslator
from langdetect import detect

# ==========================================================
# TRANSLATION RESULT
# ==========================================================


@dataclass(slots=True)
class TranslationResult:
    """
    Standard translation response.
    """

    original_text: str

    translated_text: str

    source_language: str

    target_language: str

    provider: str

    metadata: dict[str, Any] = field(default_factory=dict)


# ==========================================================
# BASE TRANSLATION PROVIDER
# ==========================================================


class BaseTranslationProvider(ABC):
    """
    Base class for translation providers.
    """

    @abstractmethod
    def detect_language(
        self,
        text: str,
    ) -> str:

        raise NotImplementedError

    @abstractmethod
    def translate(
        self,
        text: str,
        source_language: str,
        target_language: str,
    ) -> TranslationResult:

        raise NotImplementedError


# ==========================================================
# GOOGLE TRANSLATE PROVIDER
# ==========================================================


class GoogleTranslateProvider(BaseTranslationProvider):
    """
    Google Translate implementation.
    """

    PROVIDER_NAME = "Google Translate"

    # ======================================================
    # LANGUAGE DETECTION
    # ======================================================

    def detect_language(
        self,
        text: str,
    ) -> str:

        if not text or not text.strip():

            return "unknown"

        try:

            return detect(text)

        except Exception:

            return "unknown"

    # ======================================================
    # TRANSLATION
    # ======================================================

    def translate(
        self,
        text: str,
        source_language: str = "auto",
        target_language: str = "en",
    ) -> TranslationResult:

        if not text or not text.strip():

            raise ValueError("Text cannot be empty.")

        translated = GoogleTranslator(
            source=source_language,
            target=target_language,
        ).translate(text)

        detected_language = source_language

        if source_language == "auto":

            detected_language = self.detect_language(text)

        return TranslationResult(
            original_text=text,
            translated_text=translated,
            source_language=detected_language,
            target_language=target_language,
            provider=self.PROVIDER_NAME,
        )


# ==========================================================
# TRANSLATION SERVICE
# ==========================================================


class TranslationService:
    """
    Unified Translation Service.

    Default provider:
        Google Translate
    """

    def __init__(
        self,
        provider: BaseTranslationProvider | None = None,
    ) -> None:

        self.provider = provider if provider is not None else GoogleTranslateProvider()

    # ======================================================
    # LANGUAGE DETECTION
    # ======================================================

    def detect_language(
        self,
        text: str,
    ) -> str:

        return self.provider.detect_language(text)

    # ======================================================
    # TRANSLATION
    # ======================================================

    def translate(
        self,
        text: str,
        target_language: str = "en",
        source_language: str = "auto",
    ) -> str:
        """
        Translate text and return only
        the translated string.

        Compatible with SpeechAgent.
        """

        result = self.provider.translate(
            text=text,
            source_language=source_language,
            target_language=target_language,
        )

        return result.translated_text

    # ======================================================
    # FULL TRANSLATION RESULT
    # ======================================================

    def translate_result(
        self,
        text: str,
        target_language: str = "en",
        source_language: str = "auto",
    ) -> TranslationResult:
        """
        Return complete translation information.
        """

        return self.provider.translate(
            text=text,
            source_language=source_language,
            target_language=target_language,
        )

    # ======================================================
    # PROVIDER INFO
    # ======================================================

    def provider_name(
        self,
    ) -> str:

        return self.provider.__class__.__name__

    # ======================================================
    # HEALTH CHECK
    # ======================================================

    def health_check(
        self,
    ) -> bool:

        return self.provider is not None
