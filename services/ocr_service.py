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
    """

    def __init__(
        self,
        languages: list[str] | None = None,
    ) -> None:

        self.languages = languages or ["en"]

        self.reader = easyocr.Reader(self.languages)

    def extract_text(
        self,
        image_path: str | Path,
    ) -> OCRResult:

        image_path = Path(image_path)

        results = self.reader.readtext(str(image_path))

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
    # Helper
    # ======================================================

    def provider_name(
        self,
    ) -> str:

        return self.provider.__class__.__name__

    # ======================================================
    # Health
    # ======================================================

    def health_check(
        self,
    ) -> bool:

        return True
