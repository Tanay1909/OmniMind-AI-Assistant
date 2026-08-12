
"""
=========================================================
OmniMind AI Assistant
Cache Manager
=========================================================

Provides in-memory caching for AI responses,
embeddings, search results, and document processing.
"""

from __future__ import annotations

from typing import Any

from cachetools import TTLCache


class CacheManager:
    """
    Central cache manager.
    """

    def __init__(
        self,
        max_size: int = 500,
        ttl: int = 3600,
    ) -> None:
        """
        Args:
            max_size: Maximum cached items.
            ttl: Time-to-live in seconds.
        """

        self.cache = TTLCache(
            maxsize=max_size,
            ttl=ttl,
        )

    # =====================================================
    # BASIC OPERATIONS
    # =====================================================

    def get(
        self,
        key: str,
        default: Any = None,
    ) -> Any:
        """
        Get cached value.
        """

        return self.cache.get(key, default)

    def set(
        self,
        key: str,
        value: Any,
    ) -> None:
        """
        Save value to cache.
        """

        self.cache[key] = value

    def exists(
        self,
        key: str,
    ) -> bool:
        """
        Check whether key exists.
        """

        return key in self.cache

    def delete(
        self,
        key: str,
    ) -> None:
        """
        Delete cache entry.
        """

        self.cache.pop(key, None)

    def clear(self) -> None:
        """
        Remove all cached data.
        """

        self.cache.clear()

    # =====================================================
    # AI RESPONSE CACHE
    # =====================================================

    def cache_response(
        self,
        prompt: str,
        response: str,
    ) -> None:

        self.set(
            f"response:{prompt}",
            response,
        )

    def get_cached_response(
        self,
        prompt: str,
    ) -> str | None:

        return self.get(f"response:{prompt}")

    # =====================================================
    # DOCUMENT CACHE
    # =====================================================

    def cache_document(
        self,
        file_hash: str,
        document,
    ) -> None:

        self.set(
            f"document:{file_hash}",
            document,
        )

    def get_document(
        self,
        file_hash: str,
    ):

        return self.get(f"document:{file_hash}")

    # =====================================================
    # EMBEDDINGS
    # =====================================================

    def cache_embedding(
        self,
        text_hash: str,
        embedding,
    ) -> None:

        self.set(
            f"embedding:{text_hash}",
            embedding,
        )

    def get_embedding(
        self,
        text_hash: str,
    ):

        return self.get(f"embedding:{text_hash}")

    # =====================================================
    # SEARCH CACHE
    # =====================================================

    def cache_search(
        self,
        query: str,
        results,
    ) -> None:

        self.set(
            f"search:{query}",
            results,
        )

    def get_search(
        self,
        query: str,
    ):

        return self.get(f"search:{query}")

    # =====================================================
    # IMAGE CACHE
    # =====================================================

    def cache_image_analysis(
        self,
        image_hash: str,
        result,
    ) -> None:

        self.set(
            f"image:{image_hash}",
            result,
        )

    def get_image_analysis(
        self,
        image_hash: str,
    ):

        return self.get(f"image:{image_hash}")

    # =====================================================
    # AUDIO CACHE
    # =====================================================

    def cache_audio(
        self,
        audio_hash: str,
        transcript: str,
    ) -> None:

        self.set(
            f"audio:{audio_hash}",
            transcript,
        )

    def get_audio(
        self,
        audio_hash: str,
    ):

        return self.get(f"audio:{audio_hash}")

    # =====================================================
    # CACHE INFO
    # =====================================================

    def size(self) -> int:
        """
        Current cache size.
        """

        return len(self.cache)

    def keys(self):
        """
        Return all cache keys.
        """

        return list(self.cache.keys())


# ==========================================================
# GLOBAL CACHE INSTANCE
# ==========================================================

cache = CacheManager()
