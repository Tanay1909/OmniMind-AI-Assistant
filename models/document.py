"""
=========================================================
OmniMind AI Assistant
Document Models
=========================================================

Shared document models used across the application.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field

# ==========================================================
# DOCUMENT TYPE
# ==========================================================


class DocumentType(str, Enum):
    """Supported document types."""

    PDF = "pdf"
    DOCX = "docx"
    TXT = "txt"
    MD = "markdown"
    HTML = "html"
    CSV = "csv"
    XLSX = "xlsx"
    IMAGE = "image"
    UNKNOWN = "unknown"


# ==========================================================
# DOCUMENT METADATA
# ==========================================================


class DocumentMetadata(BaseModel):
    """Metadata associated with a document."""

    model_config = ConfigDict(validate_assignment=True)

    filename: str

    file_type: DocumentType = DocumentType.UNKNOWN

    file_size: int = 0

    page_count: int = 0

    language: str | None = None

    author: str | None = None

    created_at: datetime | None = None

    modified_at: datetime | None = None

    source: str | None = None

    checksum: str | None = None

    extra: dict[str, Any] = Field(default_factory=dict)


# ==========================================================
# DOCUMENT CHUNK
# ==========================================================


class DocumentChunk(BaseModel):
    """
    Represents one chunk of a document
    used for embedding/RAG.
    """

    model_config = ConfigDict(validate_assignment=True)

    id: str = Field(default_factory=lambda: str(uuid4()))

    document_id: str

    chunk_index: int

    text: str

    page_number: int | None = None

    token_count: int = 0

    embedding: list[float] | None = None

    metadata: dict[str, Any] = Field(default_factory=dict)


# ==========================================================
# DOCUMENT
# ==========================================================


class Document(BaseModel):
    """
    Represents a complete document.
    """

    model_config = ConfigDict(validate_assignment=True)

    id: str = Field(default_factory=lambda: str(uuid4()))

    title: str

    content: str

    metadata: DocumentMetadata

    chunks: list[DocumentChunk] = Field(default_factory=list)

    tags: list[str] = Field(default_factory=list)

    created_at: datetime = Field(default_factory=datetime.utcnow)

    updated_at: datetime = Field(default_factory=datetime.utcnow)

    indexed: bool = False

    # =====================================================
    # METHODS
    # =====================================================

    def add_chunk(
        self,
        chunk: DocumentChunk,
    ) -> None:
        """Add a chunk to the document."""

        self.chunks.append(chunk)
        self.updated_at = datetime.utcnow()

    def clear_chunks(self) -> None:
        """Remove all chunks."""

        self.chunks.clear()
        self.indexed = False
        self.updated_at = datetime.utcnow()

    @property
    def chunk_count(self) -> int:
        """Return total number of chunks."""

        return len(self.chunks)

    @property
    def word_count(self) -> int:
        """Approximate word count."""

        return len(self.content.split())

    @property
    def character_count(self) -> int:
        """Total characters."""

        return len(self.content)

    def mark_indexed(self) -> None:
        """Mark document as indexed."""

        self.indexed = True
        self.updated_at = datetime.utcnow()


# ==========================================================
# DOCUMENT SEARCH RESULT
# ==========================================================


class DocumentSearchResult(BaseModel):
    """
    Result returned by the RAG retriever.
    """

    model_config = ConfigDict(validate_assignment=True)

    chunk: DocumentChunk

    similarity_score: float

    document_title: str

    metadata: dict[str, Any] = Field(default_factory=dict)
