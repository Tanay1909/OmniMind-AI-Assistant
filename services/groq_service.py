"""
=========================================================
OmniMind AI Assistant
Groq LLM Service
=========================================================

Groq implementation of the BaseLLMService.

Uses the official Groq Python SDK.
"""

from __future__ import annotations

from groq import Groq

from config import GROQ_API_KEY

from services.llm_service import (
    BaseLLMService,
    LLMRequest,
    LLMResponse,
)


class GroqService(BaseLLMService):
    """
    Groq LLM Service.
    """

    def __init__(self) -> None:

        super().__init__("Groq")

        if not GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY is not configured.")

        self.client = Groq(
            api_key=GROQ_API_KEY,
        )

    # =====================================================
    # GENERATE
    # =====================================================

    def generate(
        self,
        request: LLMRequest,
    ) -> LLMResponse:

        if not request.model:
            raise ValueError("LLMRequest.model is required.")

        try:

            # Debug
            print("=" * 60)
            print("Groq model received:", request.model)
            print("=" * 60)

            response = self.client.chat.completions.create(
                model=request.model,
                messages=request.messages,
                temperature=request.temperature,
                max_tokens=request.max_tokens,
                top_p=request.top_p,
                stream=request.stream,
            )

            if request.stream:
                raise NotImplementedError("Streaming responses are not implemented.")

            message = response.choices[0].message.content or ""

            usage = response.usage

            return LLMResponse(
                content=message,
                provider=self.provider_name,
                model=request.model,
                finish_reason=response.choices[0].finish_reason or "stop",
                input_tokens=usage.prompt_tokens,
                output_tokens=usage.completion_tokens,
                total_tokens=usage.total_tokens,
            )

        except Exception as exc:
            raise RuntimeError(f"Groq API Error: {str(exc)}") from exc

    # =====================================================
    # HEALTH CHECK
    # =====================================================

    def health_check(self) -> bool:

        try:

            self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "user",
                        "content": "Hello",
                    }
                ],
                max_tokens=5,
            )

            return True

        except Exception:

            return False

    # =====================================================
    # AVAILABLE MODELS
    # =====================================================

    def available_models(self) -> list[str]:

        return [
            "llama-3.3-70b-versatile",
            "deepseek-r1-distill-llama-70b",
        ]

    # =====================================================
    # FEATURES
    # =====================================================

    def supports_streaming(self) -> bool:

        return True

    def supports_function_calling(self) -> bool:

        return False

    def supports_vision(self) -> bool:

        return False
