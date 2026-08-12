"""
=========================================================
OmniMind AI Assistant
Gemini Service
=========================================================

Google Gemini implementation of BaseLLMService.

Supports:
- Normal text generation
- Image understanding
- Vision questions
- Document/text generation

Important:
-----------
The normal text-generation path is preserved so existing
Chat, Document, Research, Dashboard and other modules
continue to work.

Vision support is activated only when:

    request.metadata["image_path"]

is provided.
"""

from __future__ import annotations

from pathlib import Path

from google import genai

from config.config import settings

from services.llm_service import (
    BaseLLMService,
    LLMRequest,
    LLMResponse,
)


class GeminiService(BaseLLMService):
    """
    Google Gemini implementation.
    """

    # Current stable multimodal Gemini model.
    DEFAULT_MODEL = "gemini-3.1-flash-lite"

    def __init__(
        self,
        api_key: str | None = None,
    ) -> None:

        super().__init__("Gemini")

        self.api_key = (
            api_key
            or settings.GOOGLE_API_KEY
        )

        if not self.api_key:
            raise ValueError(
                "GOOGLE_API_KEY is not configured."
            )

        self.client = genai.Client(
            api_key=self.api_key
        )

    # =====================================================
    # GENERATE
    # =====================================================

    def generate(
        self,
        request: LLMRequest,
    ) -> LLMResponse:
        """
        Generate a Gemini response.

        Normal text requests continue through the normal
        text-generation path.

        If request.metadata contains an image_path,
        Gemini receives both the image and the prompt.
        """

        if not request.model:
            raise ValueError(
                "Gemini model is required."
            )

        print("=" * 60)
        print(
            "PROVIDER :",
            self.provider_name,
        )
        print(
            "MODEL    :",
            request.model,
        )
        print("=" * 60)

        # -------------------------------------------------
        # Convert messages to prompt
        # -------------------------------------------------

        prompt = self._convert_messages(
            request.messages
        )

        # -------------------------------------------------
        # Check for image
        # -------------------------------------------------

        image_path = None

        if request.metadata:

            image_path = request.metadata.get(
                "image_path"
            )

        # =================================================
        # NORMAL TEXT REQUEST
        # =================================================

        if not image_path:

            response = self.client.models.generate_content(
                model=request.model,
                contents=prompt,
            )

        # =================================================
        # VISION REQUEST
        # =================================================

        else:

            image_path = Path(image_path)

            if not image_path.exists():
                raise FileNotFoundError(
                    f"Image not found: {image_path}"
                )

            if not image_path.is_file():
                raise ValueError(
                    f"Image path is not a file: {image_path}"
                )

            # Upload image to Gemini.
            uploaded_file = self.client.files.upload(
                file=str(image_path)
            )

            response = self.client.models.generate_content(
                model=request.model,
                contents=[
                    prompt,
                    uploaded_file,
                ],
            )

        # -------------------------------------------------
        # Extract response
        # -------------------------------------------------

        text = ""

        if response.text:
            text = response.text

        # -------------------------------------------------
        # Usage information
        # -------------------------------------------------

        usage = getattr(
            response,
            "usage_metadata",
            None,
        )

        input_tokens = (
            getattr(
                usage,
                "prompt_token_count",
                0,
            )
            if usage
            else 0
        )

        output_tokens = (
            getattr(
                usage,
                "candidates_token_count",
                0,
            )
            if usage
            else 0
        )

        total_tokens = (
            getattr(
                usage,
                "total_token_count",
                input_tokens + output_tokens,
            )
            if usage
            else input_tokens + output_tokens
        )

        # -------------------------------------------------
        # Return standardized response
        # -------------------------------------------------

        return LLMResponse(
            content=text,
            provider=self.provider_name,
            model=request.model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=total_tokens,
            metadata={
                "finish_reason": "stop",
                "vision": bool(image_path),
                "image_path": (
                    str(image_path)
                    if image_path
                    else None
                ),
            },
        )

    # =====================================================
    # HEALTH CHECK
    # =====================================================

    def health_check(self) -> bool:
        """
        Check whether Gemini is available.
        """

        try:

            self.client.models.generate_content(
                model=self.DEFAULT_MODEL,
                contents="Hello",
            )

            return True

        except Exception as exc:

            print(
                "Gemini health check failed:",
                exc,
            )

            return False

    # =====================================================
    # MODELS
    # =====================================================

    def available_models(self) -> list[str]:
        """
        Return supported Gemini models used by OmniMind.
        """

        return [
            self.DEFAULT_MODEL,
        ]

    # =====================================================
    # FEATURES
    # =====================================================

    def supports_streaming(self) -> bool:
        """
        Gemini supports streaming generation.
        """

        return True

    def supports_function_calling(self) -> bool:
        """
        Gemini supports function calling.
        """

        return True

    def supports_vision(self) -> bool:
        """
        Gemini model supports image input.
        """

        return True

    # =====================================================
    # PRIVATE
    # =====================================================

    @staticmethod
    def _convert_messages(
        messages: list[dict[str, str]],
    ) -> str:
        """
        Convert standardized LLM messages into a
        Gemini-compatible text prompt.

        This preserves the existing text-chat behavior.
        """

        prompt_parts = []

        for message in messages:

            role = message.get(
                "role",
                "user",
            ).upper()

            content = message.get(
                "content",
                "",
            )

            prompt_parts.append(
                f"{role}: {content}"
            )

        return "\n\n".join(
            prompt_parts
        )

