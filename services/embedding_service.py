"""
=========================================================
OmniMind AI Assistant
Embedding Service
=========================================================

Provides a unified interface for generating text embeddings.

Supported Provider
------------------
- Sentence Transformers
"""

from __future__ import annotations

from abc import ABC, abstractmethod

import numpy as np
from sentence_transformers import SentenceTransformer

# ==========================================================
# BASE EMBEDDING PROVIDER
# ==========================================================


class BaseEmbeddingProvider(ABC):
    """
    Abstract base class for embedding providers.
    """

    @abstractmethod
    def embed(self, text: str) -> list[float]:
        raise NotImplementedError

    @abstractmethod
    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        raise NotImplementedError


# ==========================================================
# SENTENCE TRANSFORMER PROVIDER
# ==========================================================


class SentenceTransformerProvider(BaseEmbeddingProvider):
    """
    Local embedding provider using Sentence Transformers.
    """

    def __init__(
        self,
        model: str = "all-MiniLM-L6-v2",
    ) -> None:

        self.model = SentenceTransformer(model)

    def embed(
        self,
        text: str,
    ) -> list[float]:

        return self.model.encode(
            text,
            convert_to_numpy=True,
            normalize_embeddings=True,
        ).tolist()

    def embed_batch(
        self,
        texts: list[str],
    ) -> list[list[float]]:

        return self.model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True,
        ).tolist()


# ==========================================================
# EMBEDDING SERVICE
# ==========================================================


class EmbeddingService:
    """
    High-level embedding interface.
    """

    def __init__(
        self,
        provider: BaseEmbeddingProvider | None = None,
    ) -> None:

        self.provider = provider or SentenceTransformerProvider()

    def embed(
        self,
        text: str,
    ) -> list[float]:

        return self.provider.embed(text)

    def embed_batch(
        self,
        texts: list[str],
    ) -> list[list[float]]:

        return self.provider.embed_batch(texts)

    @staticmethod
    def normalize(
        vector: list[float],
    ) -> list[float]:

        arr = np.array(vector)

        norm = np.linalg.norm(arr)

        if norm == 0:
            return vector

        return (arr / norm).tolist()

    @staticmethod
    def cosine_similarity(
        vector1: list[float],
        vector2: list[float],
    ) -> float:

        a = np.array(vector1)

        b = np.array(vector2)

        return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))
