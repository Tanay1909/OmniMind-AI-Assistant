"""
=========================================================
OmniMind AI Assistant
Image Utilities
=========================================================

Reusable image processing utilities.
"""

from __future__ import annotations

import base64
import io
from pathlib import Path
from typing import Tuple

from PIL import Image

# =========================================================
# LOAD IMAGE
# =========================================================


def load_image(path: str | Path) -> Image.Image:
    """
    Load an image from disk.
    """
    return Image.open(path)


# =========================================================
# SAVE IMAGE
# =========================================================


def save_image(
    image: Image.Image,
    path: str | Path,
    format: str | None = None,
) -> Path:
    """
    Save an image.
    """
    path = Path(path)

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    image.save(path, format=format)

    return path


# =========================================================
# IMAGE SIZE
# =========================================================


def image_dimensions(
    image: Image.Image,
) -> Tuple[int, int]:
    """
    Return image width and height.
    """
    return image.size


# =========================================================
# RESIZE
# =========================================================


def resize_image(
    image: Image.Image,
    width: int,
    height: int,
) -> Image.Image:
    """
    Resize image.
    """
    return image.resize(
        (width, height),
        Image.LANCZOS,
    )


# =========================================================
# THUMBNAIL
# =========================================================


def create_thumbnail(
    image: Image.Image,
    size: tuple[int, int] = (256, 256),
) -> Image.Image:
    """
    Create thumbnail.
    """
    thumbnail = image.copy()

    thumbnail.thumbnail(
        size,
        Image.LANCZOS,
    )

    return thumbnail


# =========================================================
# ROTATE
# =========================================================


def rotate_image(
    image: Image.Image,
    angle: float,
) -> Image.Image:
    """
    Rotate image.
    """
    return image.rotate(
        angle,
        expand=True,
    )


# =========================================================
# CROP
# =========================================================


def crop_image(
    image: Image.Image,
    left: int,
    top: int,
    right: int,
    bottom: int,
) -> Image.Image:
    """
    Crop image.
    """
    return image.crop((left, top, right, bottom))


# =========================================================
# GRAYSCALE
# =========================================================


def to_grayscale(
    image: Image.Image,
) -> Image.Image:
    """
    Convert image to grayscale.
    """
    return image.convert("L")


# =========================================================
# RGB
# =========================================================


def to_rgb(
    image: Image.Image,
) -> Image.Image:
    """
    Convert image to RGB.
    """
    return image.convert("RGB")


# =========================================================
# BASE64 ENCODE
# =========================================================


def image_to_base64(
    image: Image.Image,
    format: str = "PNG",
) -> str:
    """
    Convert image to Base64 string.
    """
    buffer = io.BytesIO()

    image.save(
        buffer,
        format=format,
    )

    return base64.b64encode(buffer.getvalue()).decode("utf-8")


# =========================================================
# BASE64 DECODE
# =========================================================


def base64_to_image(
    encoded: str,
) -> Image.Image:
    """
    Decode Base64 string.
    """
    image_bytes = base64.b64decode(encoded)

    return Image.open(io.BytesIO(image_bytes))


# =========================================================
# IMAGE FORMAT
# =========================================================


def image_format(
    image: Image.Image,
) -> str | None:
    """
    Return image format.
    """
    return image.format


# =========================================================
# IMAGE MODE
# =========================================================


def image_mode(
    image: Image.Image,
) -> str:
    """
    Return image color mode.
    """
    return image.mode


# =========================================================
# IMAGE METADATA
# =========================================================


def image_metadata(
    image: Image.Image,
) -> dict:
    """
    Return image metadata.
    """
    return {
        "width": image.width,
        "height": image.height,
        "mode": image.mode,
        "format": image.format,
    }


# =========================================================
# VERIFY IMAGE
# =========================================================


def verify_image(
    path: str | Path,
) -> bool:
    """
    Verify image integrity.
    """
    try:
        with Image.open(path) as img:
            img.verify()
        return True

    except Exception:
        return False


# =========================================================
# SUPPORTED FORMATS
# =========================================================


def supported_formats() -> list[str]:
    """
    Return supported image formats.
    """
    return sorted(Image.registered_extensions().keys())
