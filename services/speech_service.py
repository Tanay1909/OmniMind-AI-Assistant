"""
=========================================================
OmniMind AI Assistant
Speech Service
=========================================================

Provides:

- Speech-to-Text (STT)
- Text-to-Speech (TTS)

Default Providers:

- Groq Whisper
- Google gTTS
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from config.config import settings

# ==========================================================
# RESULT
# ==========================================================


@dataclass(slots=True)
class SpeechResult:
    """
    Standard speech recognition result.
    """

    text: str

    language: str = "unknown"

    duration: float | None = None

    provider: str = "Unknown"

    metadata: dict[str, Any] = field(default_factory=dict)


# ==========================================================
# BASE STT PROVIDER
# ==========================================================


class BaseSpeechToTextProvider(ABC):
    """
    Base Speech-to-Text provider.
    """

    @abstractmethod
    def transcribe(
        self,
        audio_path: str | Path,
    ) -> SpeechResult:

        raise NotImplementedError


# ==========================================================
# BASE TTS PROVIDER
# ==========================================================


class BaseTextToSpeechProvider(ABC):
    """
    Base Text-to-Speech provider.
    """

    @abstractmethod
    def synthesize(
        self,
        text: str,
        output_path: str | Path,
    ) -> Path:

        raise NotImplementedError


# ==========================================================
# GROQ WHISPER PROVIDER
# ==========================================================


class GroqWhisperProvider(BaseSpeechToTextProvider):
    """
    Groq Whisper Speech-to-Text provider.
    """

    MODEL = "whisper-large-v3-turbo"

    def __init__(
        self,
        api_key: str | None = None,
    ) -> None:

        from groq import Groq

        self.api_key = api_key or getattr(
            settings,
            "GROQ_API_KEY",
            None,
        )

        if not self.api_key:

            raise ValueError("GROQ_API_KEY is not configured.")

        self.client = Groq(api_key=self.api_key)

    # ======================================================
    # TRANSCRIBE
    # ======================================================

    def transcribe(
        self,
        audio_path: str | Path,
    ) -> SpeechResult:

        audio_path = Path(audio_path)

        if not audio_path.exists():

            raise FileNotFoundError(f"Audio file not found: {audio_path}")

        with audio_path.open("rb") as audio_file:

            response = self.client.audio.transcriptions.create(
                model=self.MODEL,
                file=audio_file,
                response_format="verbose_json",
                temperature=0.0,
            )

        text = getattr(
            response,
            "text",
            "",
        )

        language = getattr(
            response,
            "language",
            "unknown",
        )

        duration = getattr(
            response,
            "duration",
            None,
        )

        return SpeechResult(
            text=text,
            language=language,
            duration=duration,
            provider="Groq Whisper",
            metadata={
                "model": self.MODEL,
            },
        )


# ==========================================================
# GOOGLE TTS PROVIDER
# ==========================================================


class GTTSProvider(BaseTextToSpeechProvider):
    """
    Google Text-to-Speech provider.
    """

    def synthesize(
        self,
        text: str,
        output_path: str | Path,
    ) -> Path:

        from gtts import gTTS

        if not text or not text.strip():

            raise ValueError("Text cannot be empty.")

        output_path = Path(output_path)

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        tts = gTTS(
            text=text,
            lang="en",
        )

        tts.save(str(output_path))

        return output_path


# ==========================================================
# SPEECH SERVICE
# ==========================================================


class SpeechService:
    """
    Unified Speech Service.

    Default STT:
        Groq Whisper

    Default TTS:
        Google gTTS
    """

    def __init__(
        self,
        stt_provider: BaseSpeechToTextProvider | None = None,
        tts_provider: BaseTextToSpeechProvider | None = None,
    ) -> None:

        self.stt = stt_provider if stt_provider is not None else GroqWhisperProvider()

        self.tts = tts_provider if tts_provider is not None else GTTSProvider()

    # ======================================================
    # SPEECH → TEXT
    # ======================================================

    def transcribe(
        self,
        audio_path: str | Path,
    ) -> str:

        result = self.stt.transcribe(audio_path)

        return result.text

    # ======================================================
    # SPEECH → TEXT RESULT
    # ======================================================

    def speech_to_text(
        self,
        audio_path: str | Path,
    ) -> SpeechResult:

        return self.stt.transcribe(audio_path)

    # ======================================================
    # TEXT → SPEECH
    # ======================================================

    def text_to_speech(
        self,
        text: str,
        output_path: str | Path = ("outputs/speech.mp3"),
    ) -> str:

        audio = self.tts.synthesize(
            text=text,
            output_path=output_path,
        )

        return str(audio)

    # ======================================================
    # PROVIDER INFO
    # ======================================================

    def provider_name(
        self,
    ) -> str:

        return self.stt.__class__.__name__

    # ======================================================
    # HEALTH CHECK
    # ======================================================

    def health_check(
        self,
    ) -> bool:

        return self.stt is not None and self.tts is not None
