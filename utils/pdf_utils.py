"""
=========================================================
OmniMind AI Assistant
PDF Utilities
=========================================================

Reusable PDF processing utilities.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from PyPDF2 import PdfReader, PdfWriter

# =========================================================
# LOAD PDF
# =========================================================


def load_pdf(path: str | Path) -> PdfReader:
    """
    Load PDF document.
    """
    return PdfReader(str(path))


# =========================================================
# PAGE COUNT
# =========================================================


def page_count(path: str | Path) -> int:
    """
    Return number of pages.
    """
    reader = PdfReader(str(path))
    return len(reader.pages)


# =========================================================
# EXTRACT TEXT
# =========================================================


def extract_text(
    path: str | Path,
) -> str:
    """
    Extract text from all pages.
    """

    reader = PdfReader(str(path))

    text = []

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text.append(page_text)

    return "\n".join(text)


# =========================================================
# EXTRACT PAGE
# =========================================================


def extract_page_text(
    path: str | Path,
    page_number: int,
) -> str:
    """
    Extract text from one page.
    """

    reader = PdfReader(str(path))

    return reader.pages[page_number].extract_text()


# =========================================================
# METADATA
# =========================================================


def extract_metadata(
    path: str | Path,
) -> dict[str, Any]:
    """
    Return PDF metadata.
    """

    reader = PdfReader(str(path))

    metadata = reader.metadata or {}

    return dict(metadata)


# =========================================================
# SPLIT PDF
# =========================================================


def split_pdf(
    path: str | Path,
    output_directory: str | Path,
) -> list[Path]:
    """
    Split PDF into single-page PDFs.
    """

    reader = PdfReader(str(path))

    output_directory = Path(output_directory)

    output_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    outputs = []

    for index, page in enumerate(reader.pages):

        writer = PdfWriter()

        writer.add_page(page)

        output_file = output_directory / f"page_{index+1}.pdf"

        with open(output_file, "wb") as pdf:

            writer.write(pdf)

        outputs.append(output_file)

    return outputs


# =========================================================
# MERGE PDF
# =========================================================


def merge_pdfs(
    pdf_files: list[str | Path],
    output_file: str | Path,
) -> Path:
    """
    Merge multiple PDFs.
    """

    writer = PdfWriter()

    for pdf in pdf_files:

        reader = PdfReader(str(pdf))

        for page in reader.pages:

            writer.add_page(page)

    output_file = Path(output_file)

    output_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with open(output_file, "wb") as merged:

        writer.write(merged)

    return output_file


# =========================================================
# CREATE PDF
# =========================================================


def create_pdf(
    output_file: str | Path,
) -> PdfWriter:
    """
    Create empty PDF writer.
    """

    return PdfWriter()


# =========================================================
# SAVE PDF
# =========================================================


def save_pdf(
    writer: PdfWriter,
    output_file: str | Path,
) -> Path:
    """
    Save PDF writer.
    """

    output_file = Path(output_file)

    output_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with open(output_file, "wb") as pdf:

        writer.write(pdf)

    return output_file


# =========================================================
# ROTATE PAGE
# =========================================================


def rotate_page(
    input_pdf: str | Path,
    output_pdf: str | Path,
    page_number: int,
    angle: int = 90,
) -> Path:
    """
    Rotate one page.
    """

    reader = PdfReader(str(input_pdf))

    writer = PdfWriter()

    for index, page in enumerate(reader.pages):

        if index == page_number:

            page.rotate(angle)

        writer.add_page(page)

    return save_pdf(
        writer,
        output_pdf,
    )


# =========================================================
# PDF INFO
# =========================================================


def pdf_info(
    path: str | Path,
) -> dict[str, Any]:
    """
    Return general PDF information.
    """

    return {
        "pages": page_count(path),
        "metadata": extract_metadata(path),
        "file": Path(path).name,
        "size_bytes": Path(path).stat().st_size,
    }
