"""
=========================================================
OmniMind AI Assistant
Vector Store
=========================================================

Abstract vector database interface with an
in-memory implementation. Future backends
(FAISS, ChromaDB, Pinecone, Weaviate, Milvus)
can implement the same interface.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4

import math

# ==========================================================
# VECTOR DOCUMENT
# ==========================================================


@dataclass
class VectorDocument:
    """
    Vector document.
    """

    id: str = field(default_factory=lambda: str(uuid4()))

    text: str = ""

    embedding: list[float] = field(default_factory=list)

    metadata: dict[str, Any] = field(default_factory=dict)


# ==========================================================
# SEARCH RESULT
# ==========================================================


@dataclass
class VectorSearchResult:
    """
    Search result.
    """

    document: VectorDocument

    score: float


# ==========================================================
# BASE STORE
# ==========================================================


class BaseVectorStore(ABC):
    """
    Abstract vector database.
    """

    @abstractmethod
    def add(
        self,
        document: VectorDocument,
    ) -> None:
        pass

    @abstractmethod
    def add_many(
        self,
        documents: list[VectorDocument],
    ) -> None:
        pass

    @abstractmethod
    def search(
        self,
        embedding: list[float],
        top_k: int = 5,
    ) -> list[VectorSearchResult]:
        pass

    @abstractmethod
    def delete(
        self,
        document_id: str,
    ) -> None:
        pass

    @abstractmethod
    def clear(self) -> None:
        pass

    @abstractmethod
    def count(self) -> int:
        pass


# ==========================================================
# MEMORY STORE
# ==========================================================


class InMemoryVectorStore(BaseVectorStore):
    """
    Simple in-memory vector store.
    Suitable for development/testing.
    """

    def __init__(self):

        self.documents: dict[str, VectorDocument] = {}

    # ======================================================

    def add(
        self,
        document: VectorDocument,
    ) -> None:

        self.documents[document.id] = document

    def add_many(
        self,
        documents: list[VectorDocument],
    ) -> None:

        for document in documents:
            self.add(document)

    def delete(
        self,
        document_id: str,
    ) -> None:

        self.documents.pop(document_id, None)

    def clear(self) -> None:

        self.documents.clear()

    def count(self) -> int:

        return len(self.documents)

    # ======================================================

    def search(
        self,
        embedding: list[float],
        top_k: int = 5,
    ) -> list[VectorSearchResult]:

        results = []

        for document in self.documents.values():

            score = cosine_similarity(
                embedding,
                document.embedding,
            )

            results.append(
                VectorSearchResult(
                    document=document,
                    score=score,
                )
            )

        results.sort(
            key=lambda x: x.score,
            reverse=True,
        )

        return results[:top_k]


# ==========================================================
# SIMILARITY
# ==========================================================


def cosine_similarity(
    vector1: list[float],
    vector2: list[float],
) -> float:
    """
    Cosine similarity.
    """

    if not vector1 or not vector2:
        return 0.0

    if len(vector1) != len(vector2):
        return 0.0

    dot = sum(a * b for a, b in zip(vector1, vector2))

    norm1 = math.sqrt(sum(a * a for a in vector1))

    norm2 = math.sqrt(sum(b * b for b in vector2))

    if norm1 == 0 or norm2 == 0:
        return 0.0

    return dot / (norm1 * norm2)


# ==========================================================
# FACTORY
# ==========================================================


class VectorStoreFactory:
    """
    Creates vector store instances.
    """

    @staticmethod
    def create(
        backend: str = "memory",
    ) -> BaseVectorStore:

        backend = backend.lower()

        if backend == "memory":
            return InMemoryVectorStore()

        raise ValueError(f"Unsupported vector backend: {backend}")


# ==========================================================
# DEFAULT STORE
# ==========================================================

vector_store = VectorStoreFactory.create()
