"""
=========================================================
OmniMind AI Assistant
Speech Agent
=========================================================

Handles:
- Speech-to-Text
- Text-to-Speech
- Translation
- Audio Summarization
- Language Detection
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from agents.base_agent import (
    BaseAgent,
    AgentRequest,
    AgentResponse,
)

from services.speech_service import SpeechService
from services.translation_service import TranslationService
from services.llm_factory import LLMService

from core.exceptions import AgentException


class SpeechAgent(BaseAgent):
    """
    AI Speech Agent.
    """

    def __init__(self) -> None:

        super().__init__(
            name="SpeechAgent",
            description=(
                "Handles speech recognition, translation, "
                "summarization and text-to-speech."
            ),
        )

        self.speech_service = SpeechService()
        self.translation_service = TranslationService()
        self.llm_service = LLMService()

    # ======================================================
    # Base Agent
    # ======================================================

    def run(
        self,
        request: AgentRequest,
    ) -> AgentResponse:

        try:

            self.validate(request)

            response = self.llm_service.generate(request.query)

            return AgentResponse(
                success=True,
                output=response,
                agent=self.name,
            )

        except Exception as e:

            return AgentResponse(
                success=False,
                output=None,
                agent=self.name,
                error=str(e),
            )
    # ======================================================
    # Speech → Text
    # ======================================================

    def transcribe(
        self,
        audio_path: str | Path,
    ) -> str:

        try:

            return self.speech_service.transcribe(audio_path)

        except Exception as e:

            raise AgentException(f"Speech transcription failed: {e}") from e

    # ======================================================
    # Text → Speech
    # ======================================================

    def text_to_speech(
        self,
        text: str,
        output_path: str | Path = "outputs/speech.mp3",
    ) -> str:

        try:

            return self.speech_service.text_to_speech(
                text=text,
                output_path=output_path,
            )

        except Exception as e:

            raise AgentException(f"TTS generation failed: {e}") from e

    # ======================================================
    # Translation
    # ======================================================

    def translate(
        self,
        audio_path: str | Path,
        target_language: str = "en",
    ) -> str:

        transcript = self.transcribe(audio_path)

        return self.translation_service.translate(
            transcript,
            target_language=target_language,
        )

    # ======================================================
    # Summarization
    # ======================================================

    def summarize(
        self,
        audio_path: str | Path,
    ) -> str:

        transcript = self.transcribe(audio_path)

        prompt = "Summarize the following transcript:\n\n" f"{transcript}"

        return self.llm_service.generate(prompt)

    # ======================================================
    # Language Detection
    # ======================================================

    def detect_language(
        self,
        audio_path: str | Path,
    ) -> str:

        transcript = self.transcribe(audio_path)

        return self.translation_service.detect_language(transcript)

    # ======================================================
    # Audio Analysis
    # ======================================================

    def analyze_audio(
        self,
        audio_path: str | Path,
    ) -> dict[str, Any]:

        transcript = self.transcribe(audio_path)

        language = self.translation_service.detect_language(transcript)

        summary = self.llm_service.generate(
            f"Summarize this transcript:\n\n{transcript}"
        )

        return {
            "transcript": transcript,
            "language": language,
            "summary": summary,
        }
    # ======================================================
    # Ask AI
    # ======================================================

    def ask(
        self,
        audio_path: str | Path,
    ) -> str:
        """
        Transcribe the audio and ask the LLM to respond.
        """

        transcript = self.transcribe(audio_path)

        return self.llm_service.generate(transcript)

    # ======================================================
    # Conversation
    # ======================================================

    def converse(
        self,
        audio_path: str | Path,
    ) -> dict[str, str]:
        """
        Generate an AI reply and convert it to speech.
        """

        transcript = self.transcribe(audio_path)

        reply = self.llm_service.generate(transcript)

        audio_file = self.text_to_speech(reply)

        return {
            "transcript": transcript,
            "reply": reply,
            "audio": audio_file,
        }

    # ======================================================
    # Health Check
    # ======================================================

    def health(
        self,
    ) -> dict[str, str]:
        """
        Check the status of all dependent services.
        """

        return {
            "agent": self.name,
            "status": "healthy",
            "speech_service": self.speech_service.provider_name(),
            "translation_service": self.translation_service.provider_name(),
            "llm_service": self.llm_service.__class__.__name__,
        }
