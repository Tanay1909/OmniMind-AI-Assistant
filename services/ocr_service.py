"""
=========================================================
OmniMind AI Assistant
OCR Service
=========================================================

Provides a unified interface for Optical Character
Recognition (OCR).

Supported Providers
-------------------
- EasyOCR
- Tesseract (future)
- PaddleOCR (future)
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import easyocr

# ==========================================================
# OCR RESULT
# ==========================================================


@dataclass(slots=True)
class OCRResult:
    """
    Standard OCR response.
    """

    text: str
    provider: str
    confidence: float
    metadata: dict[str, Any] = field(default_factory=dict)


# ==========================================================
# BASE OCR PROVIDER
# ==========================================================


class BaseOCRProvider(ABC):
    """
    Base OCR provider.
    """

    @abstractmethod
    def extract_text(
        self,
        image_path: str | Path,
    ) -> OCRResult:
        raise NotImplementedError


# ==========================================================
# EASYOCR PROVIDER
# ==========================================================


class EasyOCRProvider(BaseOCRProvider):
    """
    EasyOCR implementation.

    The EasyOCR model is loaded lazily when OCR is
    actually requested. This prevents the model download
    from blocking Streamlit application startup.
    """

    def __init__(
        self,
        languages: list[str] | None = None,
    ) -> None:

        self.languages = languages or ["en"]

        # Reader is intentionally NOT created here.
        self.reader = None

    # ======================================================
    # LAZY INITIALIZATION
    # ======================================================

    def _get_reader(self):

        if self.reader is None:

            self.reader = easyocr.Reader(
                self.languages,
                gpu=False,
            )

        return self.reader

    # ======================================================
    # OCR
    # ======================================================

    def extract_text(
        self,
        image_path: str | Path,
    ) -> OCRResult:

        image_path = Path(image_path)

        if not image_path.exists():
            raise FileNotFoundError(f"Image not found: {image_path}")

        if not image_path.is_file():
            raise ValueError(f"Image path is not a file: {image_path}")

        reader = self._get_reader()

        results = reader.readtext(str(image_path))

        text_lines: list[str] = []
        confidences: list[float] = []

        for _, text, confidence in results:

            text_lines.append(text)

            confidences.append(float(confidence))

        average_confidence = sum(confidences) / len(confidences) if confidences else 0.0

        return OCRResult(
            text="\n".join(text_lines),
            provider="EasyOCR",
            confidence=average_confidence,
            metadata={
                "lines": len(text_lines),
                "image": str(image_path),
                "gpu": False,
            },
        )


# ==========================================================
# OCR SERVICE
# ==========================================================


class OCRService:
    """
    Unified OCR Service.
    """

    def __init__(
        self,
        provider: BaseOCRProvider | None = None,
    ) -> None:

        self.provider = provider or EasyOCRProvider()

    # ======================================================
    # OCR
    # ======================================================

    def extract_text(
        self,
        image_path: str | Path,
    ) -> OCRResult:

        return self.provider.extract_text(image_path)

    # ======================================================
    # PROVIDER INFO
    # ======================================================

    def provider_name(
        self,
    ) -> str:

        return self.provider.__class__.__name__

    # ======================================================
    # HEALTH
    # ======================================================

    def health_check(
        self,
    ) -> bool:

        # Do NOT initialize EasyOCR here.
        return True
