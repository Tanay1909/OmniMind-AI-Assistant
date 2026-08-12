
"""
=========================================================
OmniMind AI Assistant
Response Parser
=========================================================

Normalizes responses from different AI providers
(OpenAI, Gemini, Groq, Ollama, etc.) into a common
internal format.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


# ==========================================================
# STANDARD RESPONSE MODEL
# ==========================================================

@dataclass(slots=True)
class AIResponse:
    """
    Standard response object used throughout the application.
    """

    content: str
    model: str
    provider: str

    finish_reason: str | None = None

    usage: dict[str, Any] = field(default_factory=dict)

    metadata: dict[str, Any] = field(default_factory=dict)


# ==========================================================
# RESPONSE PARSER
# ==========================================================

class ResponseParser:
    """
    Converts provider-specific responses into AIResponse.
    """

    # =====================================================
    # OPENAI
    # =====================================================

    @staticmethod
    def parse_openai(response: Any) -> AIResponse:
        """
        Parse OpenAI Chat Completions response.
        """

        return AIResponse(
            content=response.choices[0].message.content,
            model=response.model,
            provider="OpenAI",
            finish_reason=response.choices[0].finish_reason,
            usage={
                "prompt_tokens": getattr(
                    response.usage,
                    "prompt_tokens",
                    None,
                ),
                "completion_tokens": getattr(
                    response.usage,
                    "completion_tokens",
                    None,
                ),
                "total_tokens": getattr(
                    response.usage,
                    "total_tokens",
                    None,
                ),
            },
        )

    # =====================================================
    # GEMINI
    # =====================================================

    @staticmethod
    def parse_gemini(response: Any) -> AIResponse:
        """
        Parse Gemini response.
        """

        return AIResponse(
            content=getattr(response, "text", ""),
            model="Gemini",
            provider="Google",
        )

    # =====================================================
    # GROQ
    # =====================================================

    @staticmethod
    def parse_groq(response: Any) -> AIResponse:
        """
        Groq is OpenAI-compatible.
        """

        return AIResponse(
            content=response.choices[0].message.content,
            model=response.model,
            provider="Groq",
            finish_reason=response.choices[0].finish_reason,
        )

    # =====================================================
    # OLLAMA
    # =====================================================

    @staticmethod
    def parse_ollama(response: dict) -> AIResponse:
        """
        Parse Ollama REST response.
        """

        return AIResponse(
            content=response.get("response", ""),
            model=response.get("model", "Ollama"),
            provider="Ollama",
            finish_reason="stop",
        )

    # =====================================================
    # GENERIC
    # =====================================================

    @staticmethod
    def parse_text(
        text: str,
        provider: str,
        model: str,
    ) -> AIResponse:
        """
        Parse plain text into AIResponse.
        """

        return AIResponse(
            content=text,
            provider=provider,
            model=model,
        )

    # =====================================================
    # DISPATCH
    # =====================================================

    def parse(
        self,
        provider: str,
        response: Any,
    ) -> AIResponse:
        """
        Parse response according to provider.
        """

        provider = provider.lower()

        if provider == "openai":
            return self.parse_openai(response)

        if provider == "gemini":
            return self.parse_gemini(response)

        if provider == "groq":
            return self.parse_groq(response)

        if provider == "ollama":
            return self.parse_ollama(response)

        raise ValueError(
            f"Unsupported provider: {provider}"
        )


# ==========================================================
# GLOBAL INSTANCE
# ==========================================================

response_parser = ResponseParser()