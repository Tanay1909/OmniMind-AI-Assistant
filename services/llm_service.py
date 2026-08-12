"""
=========================================================
OmniMind AI Assistant
Base LLM Service
=========================================================

Defines the common interface for all Large Language Model
providers used by OmniMind.

All providers (OpenAI, Gemini, Groq, Ollama, etc.)
must inherit from BaseLLMService.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

# ==========================================================
# REQUEST
# ==========================================================


@dataclass(slots=True)
class LLMRequest:
    """
    Standard request passed to an LLM provider.
    """

    messages: list[dict[str, str]]

    # Required
    model: str

    temperature: float = 0.7
    max_tokens: int = 2048
    top_p: float = 1.0
    stream: bool = False

    metadata: dict[str, Any] = field(default_factory=dict)


# ==========================================================
# RESPONSE
# ==========================================================


@dataclass(slots=True)
class LLMResponse:
    """
    Standard response returned by an LLM provider.
    """

    content: str

    provider: str

    model: str

    finish_reason: str = "stop"

    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0

    metadata: dict[str, Any] = field(default_factory=dict)


# ==========================================================
# BASE LLM SERVICE
# ==========================================================


class BaseLLMService(ABC):
    """
    Abstract base class for all LLM providers.
    """

    def __init__(
        self,
        provider_name: str,
    ) -> None:

        self.provider_name = provider_name

    # =====================================================
    # ABSTRACT METHODS
    # =====================================================

    @abstractmethod
    def generate(
        self,
        request: LLMRequest,
    ) -> LLMResponse:
        """
        Generate a response from the provider.
        """
        pass

    @abstractmethod
    def health_check(self) -> bool:
        """
        Check provider availability.
        """
        pass

    @abstractmethod
    def available_models(self) -> list[str]:
        """
        Return all supported models.
        """
        pass

    # =====================================================
    # OPTIONAL FEATURES
    # =====================================================

    def supports_streaming(self) -> bool:
        return False

    def supports_vision(self) -> bool:
        return False

    def supports_function_calling(self) -> bool:
        return False

    # =====================================================
    # PROPERTIES
    # =====================================================

    @property
    def name(self) -> str:
        return self.provider_name

    # =====================================================
    # REPRESENTATION
    # =====================================================

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}" f"(provider='{self.provider_name}')"
