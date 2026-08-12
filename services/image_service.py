"""
=========================================================
OmniMind AI Assistant
Image Service
=========================================================

Handles:
- Image loading
- Validation
- Metadata extraction
- Resize
- Thumbnail generation
- Format conversion
- Image preprocessing
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from PIL import Image, ImageOps

# ==========================================================
# IMAGE INFO
# ==========================================================


@dataclass(slots=True)
class ImageInfo:
    """
    Metadata about an image.
    """

    filename: str

    width: int

    height: int

    mode: str

    format: str

    size_bytes: int

    metadata: dict[str, Any] = field(default_factory=dict)


# ==========================================================
# IMAGE SERVICE
# ==========================================================


class ImageService:
    """
    Utility service for image processing.
    """

    SUPPORTED_FORMATS = {
        ".png",
        ".jpg",
        ".jpeg",
        ".bmp",
        ".webp",
        ".tiff",
    }

    # ------------------------------------------------------

    def load(
        self,
        image_path: str | Path,
    ) -> Image.Image:

        image_path = Path(image_path)

        if image_path.suffix.lower() not in self.SUPPORTED_FORMATS:
            raise ValueError(f"Unsupported image format: {image_path.suffix}")

        return Image.open(image_path)

    # ------------------------------------------------------

    def save(
        self,
        image: Image.Image,
        output_path: str | Path,
    ) -> None:

        image.save(output_path)

    # ------------------------------------------------------

    def resize(
        self,
        image: Image.Image,
        width: int,
        height: int,
    ) -> Image.Image:

        return image.resize((width, height))

    # ------------------------------------------------------

    def thumbnail(
        self,
        image: Image.Image,
        size: tuple[int, int] = (300, 300),
    ) -> Image.Image:

        img = image.copy()

        img.thumbnail(size)

        return img

    # ------------------------------------------------------

    def grayscale(
        self,
        image: Image.Image,
    ) -> Image.Image:

        return ImageOps.grayscale(image)

    # ------------------------------------------------------

    def normalize(
        self,
        image: Image.Image,
    ) -> Image.Image:

        return ImageOps.autocontrast(image)

    # ------------------------------------------------------

    def rotate(
        self,
        image: Image.Image,
        angle: float,
    ) -> Image.Image:

        return image.rotate(
            angle,
            expand=True,
        )

    # ------------------------------------------------------

    def convert(
        self,
        image: Image.Image,
        mode: str,
    ) -> Image.Image:

        return image.convert(mode)

    # ------------------------------------------------------

    def info(
        self,
        image_path: str | Path,
    ) -> ImageInfo:

        image_path = Path(image_path)

        image = self.load(image_path)

        return ImageInfo(
            filename=image_path.name,
            width=image.width,
            height=image.height,
            mode=image.mode,
            format=image.format or "",
            size_bytes=image_path.stat().st_size,
            metadata=image.info,
        )

    # ------------------------------------------------------

    def dimensions(
        self,
        image_path: str | Path,
    ) -> tuple[int, int]:

        image = self.load(image_path)

        return image.width, image.height

    # ------------------------------------------------------

    def preprocess_for_ocr(
        self,
        image: Image.Image,
    ) -> Image.Image:
        """
        Basic preprocessing for OCR.
        """

        image = ImageOps.grayscale(image)

        image = ImageOps.autocontrast(image)

        return image
