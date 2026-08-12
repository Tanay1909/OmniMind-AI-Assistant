"""
=========================================================
OmniMind AI Assistant
Cache Utilities
=========================================================

Reusable caching utilities with TTL support.
"""

from __future__ import annotations

import functools
import threading
import time
from collections.abc import Callable
from typing import Any

# =========================================================
# MEMORY CACHE
# =========================================================


class MemoryCache:
    """
    Thread-safe in-memory cache with TTL support.
    """

    def __init__(self):
        self._cache: dict[str, tuple[Any, float | None]] = {}
        self._lock = threading.Lock()

    # -----------------------------------------------------

    def set(
        self,
        key: str,
        value: Any,
        ttl: int | None = None,
    ) -> None:
        """
        Store value with optional TTL.
        """

        expiry = None

        if ttl is not None:
            expiry = time.time() + ttl

        with self._lock:
            self._cache[key] = (value, expiry)

    # -----------------------------------------------------

    def get(
        self,
        key: str,
        default: Any = None,
    ) -> Any:
        """
        Retrieve cached value.
        """

        with self._lock:

            if key not in self._cache:
                return default

            value, expiry = self._cache[key]

            if expiry is not None and expiry < time.time():
                del self._cache[key]
                return default

            return value

    # -----------------------------------------------------

    def delete(
        self,
        key: str,
    ) -> bool:
        """
        Delete cache entry.
        """

        with self._lock:

            if key in self._cache:
                del self._cache[key]
                return True

        return False

    # -----------------------------------------------------

    def clear(self):
        """
        Clear cache.
        """

        with self._lock:
            self._cache.clear()

    # -----------------------------------------------------

    def exists(
        self,
        key: str,
    ) -> bool:
        """
        Check key existence.
        """

        return self.get(key) is not None

    # -----------------------------------------------------

    def cleanup(self):
        """
        Remove expired entries.
        """

        now = time.time()

        with self._lock:

            expired = [
                key
                for key, (_, expiry) in self._cache.items()
                if expiry is not None and expiry < now
            ]

            for key in expired:
                del self._cache[key]

    # -----------------------------------------------------

    def size(self) -> int:
        """
        Number of cache entries.
        """

        self.cleanup()

        return len(self._cache)

    # -----------------------------------------------------

    def stats(self) -> dict[str, Any]:
        """
        Cache statistics.
        """

        self.cleanup()

        return {
            "entries": len(self._cache),
            "timestamp": time.time(),
        }


# =========================================================
# GLOBAL CACHE
# =========================================================

cache = MemoryCache()


# =========================================================
# FUNCTION CACHE DECORATOR
# =========================================================


def cached(
    ttl: int | None = None,
):
    """
    Decorator for caching function results.
    """

    def decorator(func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            key = str(
                (
                    func.__module__,
                    func.__name__,
                    args,
                    tuple(sorted(kwargs.items())),
                )
            )

            value = cache.get(key)

            if value is not None:
                return value

            value = func(*args, **kwargs)

            cache.set(
                key,
                value,
                ttl,
            )

            return value

        return wrapper

    return decorator


# =========================================================
# CACHE INVALIDATION
# =========================================================


def invalidate(
    key: str,
) -> bool:
    """
    Remove cache entry.
    """

    return cache.delete(key)


# =========================================================
# CLEAR ALL CACHE
# =========================================================


def clear_cache():
    """
    Remove every cache entry.
    """

    cache.clear()


# =========================================================
# CACHE INFO
# =========================================================


def cache_info():
    """
    Return cache statistics.
    """

    return cache.stats()
