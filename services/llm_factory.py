"""
=========================================================
OmniMind AI Assistant
LLM Factory
=========================================================

Provides a unified LLMService interface that routes
requests to the configured provider.

Supported Providers
-------------------
- Gemini
- Groq

Supports
--------
- Text Generation
- Vision (Images)
- Future Multimodal Extensions
"""

from __future__ import annotations

from config.config import settings

from services.llm_service import (
    LLMRequest,
    LLMResponse,
)


class LLMService:
    """
    Compatibility wrapper for OmniMind agents.
    """

    def __init__(self) -> None:

        provider_name = getattr(
            settings,
            "LLM_PROVIDER",
            "gemini",
        ).lower()

        if provider_name == "gemini":

            from services.gemini_service import GeminiService

            self.provider = GeminiService()

        elif provider_name == "groq":

            from services.groq_service import GroqService

            self.provider = GroqService()

        else:

            raise ValueError(f"Unsupported LLM provider: {provider_name}")
    # =====================================================
    # GENERATE
    # =====================================================

    def generate(
        self,
        prompt: str,
        model: str | None = None,
        image_path: str | None = None,
        temperature: float = 0.7,
        max_tokens: int = 2048,
    ) -> str:
        """
        Generate a response from the configured LLM.

        Parameters
        ----------
        prompt : str
            User prompt.
        model : str | None
            Optional model override.
        image_path : str | None
            Optional image for multimodal models.
        temperature : float
            Sampling temperature.
        max_tokens : int
            Maximum output tokens.
        """

        # ---------------------------------------------
        # Default model selection
        # ---------------------------------------------

        if model is None:

            if self.provider.name.lower() == "gemini":
                model = "gemini-3.1-flash-lite"

            elif self.provider.name.lower() == "groq":
                model = "llama-3.3-70b-versatile"

            else:

                models = self.provider.available_models()

                if not models:
                    raise RuntimeError("No models available for provider.")

                model = models[0]

        # ---------------------------------------------
        # Metadata
        # ---------------------------------------------

        metadata = {}

        if image_path is not None:
            metadata["image_path"] = image_path

        # ---------------------------------------------
        # Build request
        # ---------------------------------------------

        request = LLMRequest(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            temperature=temperature,
            max_tokens=max_tokens,
            metadata=metadata,
        )

        # ---------------------------------------------
        # Generate response
        # ---------------------------------------------

        response: LLMResponse = self.provider.generate(request)

        return response.content
    # =====================================================
    # HEALTH CHECK
    # =====================================================

    def health_check(self) -> bool:
        """
        Check whether the configured provider is healthy.
        """

        return self.provider.health_check()

    # =====================================================
    # AVAILABLE MODELS
    # =====================================================

    def available_models(self) -> list[str]:
        """
        Return all available models for the provider.
        """

        return self.provider.available_models()

    # =====================================================
    # FEATURE SUPPORT
    # =====================================================

    def supports_streaming(self) -> bool:
        """
        Whether the provider supports streaming responses.
        """

        return self.provider.supports_streaming()

    def supports_vision(self) -> bool:
        """
        Whether the provider supports vision inputs.
        """

        return self.provider.supports_vision()

    def supports_function_calling(self) -> bool:
        """
        Whether the provider supports function/tool calling.
        """

        return self.provider.supports_function_calling()

    # =====================================================
    # PROVIDER INFO
    # =====================================================

    @property
    def name(self) -> str:
        """
        Current provider name.
        """

        return self.provider.name

    @property
    def provider_name(self) -> str:
        """
        Alias for current provider name.
        """

        return self.provider.name
