"""
=========================================================
OmniMind AI Assistant
Vision Agent
=========================================================

Responsibilities
----------------
- Image Understanding
- OCR
- Visual Question Answering
- Caption Generation
- Image Summarization
"""

from __future__ import annotations

from pathlib import Path

from agents.base_agent import (
    BaseAgent,
    AgentRequest,
    AgentResponse,
)

from core.exceptions import AgentException

from services.analytics_service import AnalyticsService
from services.image_service import ImageService
from services.ocr_service import (
    OCRService,
    EasyOCRProvider,
)
from services.gemini_service import GeminiService
from services.llm_service import LLMRequest


class VisionAgent(BaseAgent):
    """
    Multimodal Vision Agent.

    Uses:
    - EasyOCR for text extraction
    - Gemini Vision for image understanding
    """

    def __init__(
        self,
        image_service: ImageService | None = None,
        ocr_service: OCRService | None = None,
        llm: GeminiService | None = None,
        analytics: AnalyticsService | None = None,
    ) -> None:

        super().__init__(
            name="VisionAgent",
            description=(
                "Handles OCR, image understanding, "
                "caption generation and visual reasoning."
            ),
        )

        # =================================================
        # IMAGE SERVICE
        # =================================================

        self.image_service = (
            image_service if image_service is not None else ImageService()
        )

        # =================================================
        # OCR SERVICE
        # =================================================

        self.ocr_service = (
            ocr_service
            if ocr_service is not None
            else OCRService(EasyOCRProvider(["en"]))
        )

        # =================================================
        # GEMINI VISION
        # =================================================

        self.llm = llm if llm is not None else GeminiService()

        # =================================================
        # ANALYTICS
        # =================================================

        self.analytics = analytics

    # =====================================================
    # OCR
    # =====================================================

    def extract_text(
        self,
        image_path: str | Path,
    ) -> str:
        """
        Extract text from an image using EasyOCR.
        """

        try:

            image_path = Path(image_path)

            if not image_path.exists():

                raise FileNotFoundError(f"Image not found: {image_path}")

            result = self.ocr_service.extract_text(image_path)

            return result.text or ""

        except Exception as e:

            raise AgentException(f"OCR failed: {e}") from e

    # =====================================================
    # GEMINI VISION
    # =====================================================

    def _vision_generate(
        self,
        prompt: str,
        image_path: str | Path,
    ) -> str:
        """
        Send the actual image to Gemini Vision.
        """

        image_path = Path(image_path)

        if not image_path.exists():

            raise FileNotFoundError(f"Image not found: {image_path}")

        if not image_path.is_file():

            raise ValueError(f"Image path is not a file: {image_path}")

        # -------------------------------------------------
        # Create LLM request
        # -------------------------------------------------

        request = LLMRequest(
            model=GeminiService.DEFAULT_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            temperature=0.3,
            max_tokens=2048,
            metadata={
                "image_path": str(image_path),
            },
        )

        # -------------------------------------------------
        # Gemini receives image through metadata
        # -------------------------------------------------

        response = self.llm.generate(request)

        return response.content

    # =====================================================
    # IMAGE DESCRIPTION
    # =====================================================

    def describe_image(
        self,
        image_path: str | Path,
    ) -> str:
        """
        Generate a detailed description of the image.
        """

        try:

            prompt = """
Analyze the uploaded image carefully.

Describe:

1. Main subjects
2. Objects
3. People, if visible
4. Colors
5. Background
6. Environment
7. Important visual details
8. Any visible text

Do not invent details that are not visible.
"""

            return self._vision_generate(
                prompt=prompt,
                image_path=image_path,
            )

        except Exception as e:

            raise AgentException(f"Image description failed: {e}") from e

    # =====================================================
    # VISUAL QUESTION ANSWERING
    # =====================================================

    def answer_question(
        self,
        image_path: str | Path,
        question: str,
    ) -> str:
        """
        Answer a question using the actual image.
        """

        try:

            if not question.strip():

                raise ValueError("Question cannot be empty.")

            prompt = f"""
Analyze the uploaded image and answer the
following question accurately.

Question:
{question}

Use only information that can be determined
from the image.

If the answer cannot be determined from the
image, clearly say so.
"""

            return self._vision_generate(
                prompt=prompt,
                image_path=image_path,
            )

        except Exception as e:

            raise AgentException(f"Visual question answering failed: {e}") from e

    # =====================================================
    # IMAGE SUMMARY
    # =====================================================

    def summarize_image(
        self,
        image_path: str | Path,
    ) -> str:
        """
        Generate a concise summary of the image.
        """

        prompt = """
Summarize the uploaded image in one clear
and informative paragraph.

Mention the most important visible subjects,
objects, scene and details.

Do not invent information.
"""

        try:

            return self._vision_generate(
                prompt=prompt,
                image_path=image_path,
            )

        except Exception as e:

            raise AgentException(f"Image summarization failed: {e}") from e

    # =====================================================
    # CAPTION
    # =====================================================

    def caption_image(
        self,
        image_path: str | Path,
    ) -> str:
        """
        Generate a short caption.
        """

        prompt = """
Generate a short, accurate caption for the
uploaded image.

Keep it concise and describe the main subject
or scene.
"""

        try:

            return self._vision_generate(
                prompt=prompt,
                image_path=image_path,
            )

        except Exception as e:

            raise AgentException(f"Image caption generation failed: {e}") from e

    # =====================================================
    # COMPATIBILITY METHOD
    # =====================================================

    def generate_caption(
        self,
        image_path: str | Path,
    ) -> str:
        """
        Compatibility method used by VisionPage.
        """

        return self.caption_image(image_path)

    # =====================================================
    # COMPLETE IMAGE ANALYSIS
    # =====================================================

    def analyze_image(
        self,
        image_path: str | Path,
    ) -> dict[str, str]:
        """
        Perform complete image analysis.

        Returns:
        - OCR
        - Description
        - Summary
        """

        try:

            image_path = Path(image_path)

            if not image_path.exists():

                raise FileNotFoundError(f"Image not found: {image_path}")

            # -------------------------------------------------
            # OCR
            # -------------------------------------------------

            ocr_text = self.extract_text(image_path)

            # -------------------------------------------------
            # Gemini Description
            # -------------------------------------------------

            description = self.describe_image(image_path)

            # -------------------------------------------------
            # Gemini Summary
            # -------------------------------------------------

            summary = self.summarize_image(image_path)

            # -------------------------------------------------
            # Analytics
            # -------------------------------------------------

            if self.analytics:

                try:

                    self.analytics.record_request(
                        route="vision",
                        model=GeminiService.DEFAULT_MODEL,
                        duration=0.0,
                    )

                except Exception:
                    pass

            return {
                "ocr": ocr_text,
                "description": description,
                "summary": summary,
            }

        except Exception as e:

            raise AgentException(f"Image analysis failed: {e}") from e

    # =====================================================
    # BASE AGENT RUN
    # =====================================================

    def run(
        self,
        request: AgentRequest,
    ) -> AgentResponse:
        """
        Execute the Vision Agent.
        """

        try:

            self.validate(request)

            context = request.context or {}

            image_path = context.get("image_path")

            if not image_path:

                raise AgentException("Missing 'image_path' in request context.")

            answer = self.answer_question(
                image_path=image_path,
                question=request.query,
            )

            return AgentResponse(
                success=True,
                output=answer,
                agent=self.name,
                metadata={
                    "image_path": str(image_path),
                },
            )

        except Exception as e:

            if self.analytics:

                try:

                    self.analytics.record_error(type(e).__name__)

                except Exception:
                    pass

            return AgentResponse(
                success=False,
                output=None,
                error=str(e),
                agent=self.name,
            )

    # =====================================================
    # HEALTH CHECK
    # =====================================================

    def health(
        self,
    ) -> dict[str, str]:
        """
        Return Vision Agent health information.
        """

        return {
            "agent": self.name,
            "status": "healthy",
            "image_service": (self.image_service.__class__.__name__),
            "ocr_service": (self.ocr_service.__class__.__name__),
            "llm_service": (self.llm.__class__.__name__),
        }
