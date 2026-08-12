"""
=========================================================
OmniMind AI Assistant
PDF Service
=========================================================

Handles:
- PDF text extraction
- Metadata extraction
- Page-wise parsing
- OCR fallback for scanned PDFs
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import fitz  # PyMuPDF

from services.ocr_service import OCRService

# ==========================================================
# PAGE
# ==========================================================


@dataclass(slots=True)
class PDFPage:

    page_number: int

    text: str


# ==========================================================
# DOCUMENT
# ==========================================================


@dataclass(slots=True)
class PDFDocument:

    filename: str

    total_pages: int

    pages: list[PDFPage]

    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def full_text(self) -> str:

        return "\n\n".join(page.text for page in self.pages)


# ==========================================================
# PDF SERVICE
# ==========================================================


class PDFService:

    def __init__(
        self,
        ocr_service: OCRService | None = None,
    ):

        self.ocr_service = ocr_service

    # ------------------------------------------------------

    def load(
        self,
        pdf_path: str | Path,
    ) -> PDFDocument:

        pdf_path = Path(pdf_path)

        document = fitz.open(pdf_path)

        pages = []

        for index, page in enumerate(document):

            text = page.get_text().strip()

            # ------------------------------------
            # OCR fallback
            # ------------------------------------

            if not text and self.ocr_service is not None:

                pix = page.get_pixmap()

                image_path = pdf_path.parent / (f"_page_{index}.png")

                pix.save(image_path)

                result = self.ocr_service.extract_text(image_path)

                text = result.text

                image_path.unlink(missing_ok=True)

            pages.append(
                PDFPage(
                    page_number=index + 1,
                    text=text,
                )
            )

        metadata = document.metadata

        pdf = PDFDocument(
            filename=pdf_path.name,
            total_pages=len(pages),
            pages=pages,
            metadata=metadata,
        )

        document.close()

        return pdf

    # ------------------------------------------------------

    def extract_text(
        self,
        pdf_path: str | Path,
    ) -> str:

        return self.load(pdf_path).full_text

    # ------------------------------------------------------

    def extract_pages(
        self,
        pdf_path: str | Path,
    ) -> list[str]:

        pdf = self.load(pdf_path)

        return [page.text for page in pdf.pages]

    # ------------------------------------------------------

    def get_metadata(
        self,
        pdf_path: str | Path,
    ) -> dict:

        pdf = self.load(pdf_path)

        return pdf.metadata
