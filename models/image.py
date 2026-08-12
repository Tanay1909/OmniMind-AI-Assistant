"""
=========================================================
OmniMind AI Assistant
Image Models
=========================================================

Shared image models used across the application.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field

# ==========================================================
# IMAGE FORMAT
# ==========================================================


class ImageFormat(str, Enum):
    """Supported image formats."""

    PNG = "png"
    JPG = "jpg"
    JPEG = "jpeg"
    WEBP = "webp"
    BMP = "bmp"
    TIFF = "tiff"
    GIF = "gif"
    UNKNOWN = "unknown"


# ==========================================================
# IMAGE METADATA
# ==========================================================


class ImageMetadata(BaseModel):
    """
    General image metadata.
    """

    model_config = ConfigDict(validate_assignment=True)

    id: str = Field(default_factory=lambda: str(uuid4()))

    filename: str

    format: ImageFormat = ImageFormat.UNKNOWN

    width: int

    height: int

    channels: int = 3

    file_size: int = 0

    color_mode: str = "RGB"

    dpi: int | None = None

    created_at: datetime = Field(default_factory=datetime.utcnow)

    metadata: dict[str, Any] = Field(default_factory=dict)

    @property
    def resolution(self) -> str:
        return f"{self.width} × {self.height}"

    @property
    def aspect_ratio(self) -> float:
        return round(self.width / self.height, 3)


# ==========================================================
# BOUNDING BOX
# ==========================================================


class BoundingBox(BaseModel):
    """
    Rectangle coordinates.
    """

    model_config = ConfigDict(validate_assignment=True)

    x: float

    y: float

    width: float

    height: float

    confidence: float = 1.0


# ==========================================================
# OCR REGION
# ==========================================================


class OCRRegion(BaseModel):
    """
    OCR detected text.
    """

    model_config = ConfigDict(validate_assignment=True)

    text: str

    confidence: float

    bounding_box: BoundingBox

    language: str | None = None


# ==========================================================
# DETECTED OBJECT
# ==========================================================


class DetectedObject(BaseModel):
    """
    Object detection result.
    """

    model_config = ConfigDict(validate_assignment=True)

    label: str

    confidence: float

    bounding_box: BoundingBox

    metadata: dict[str, Any] = Field(default_factory=dict)


# ==========================================================
# IMAGE ANALYSIS RESULT
# ==========================================================


class ImageAnalysisResult(BaseModel):
    """
    Complete image analysis.
    """

    model_config = ConfigDict(validate_assignment=True)

    image: ImageMetadata

    description: str | None = None

    ocr_regions: list[OCRRegion] = Field(default_factory=list)

    detected_objects: list[DetectedObject] = Field(default_factory=list)

    tags: list[str] = Field(default_factory=list)

    metadata: dict[str, Any] = Field(default_factory=dict)

    @property
    def object_count(self) -> int:
        return len(self.detected_objects)

    @property
    def text_count(self) -> int:
        return len(self.ocr_regions)

    @property
    def has_text(self) -> bool:
        return bool(self.ocr_regions)

    @property
    def has_objects(self) -> bool:
        return bool(self.detected_objects)
