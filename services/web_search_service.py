"""
=========================================================
OmniMind AI Assistant
Web Search Service
=========================================================

Provides a unified interface for web search.

Supported Providers
-------------------
- Tavily
"""

from __future__ import annotations

import os
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

import requests

# ==========================================================
# SEARCH RESULT
# ==========================================================


@dataclass(slots=True)
class SearchResult:
    """
    Represents a single search result.
    """

    title: str
    url: str
    snippet: str
    provider: str
    metadata: dict[str, Any] = field(default_factory=dict)


# ==========================================================
# BASE PROVIDER
# ==========================================================


class BaseSearchProvider(ABC):

    @abstractmethod
    def search(
        self,
        query: str,
        max_results: int = 5,
    ) -> list[SearchResult]:
        pass


# ==========================================================
# TAVILY PROVIDER
# ==========================================================


class TavilySearchProvider(BaseSearchProvider):

    API_URL = "https://api.tavily.com/search"

    def __init__(
        self,
        api_key: str,
    ) -> None:

        self.api_key = api_key

    def search(
        self,
        query: str,
        max_results: int = 5,
    ) -> list[SearchResult]:

        payload = {
            "api_key": self.api_key,
            "query": query,
            "max_results": max_results,
        }

        response = requests.post(
            self.API_URL,
            json=payload,
            timeout=30,
        )

        response.raise_for_status()

        data = response.json()

        results: list[SearchResult] = []

        for item in data.get("results", []):

            results.append(
                SearchResult(
                    title=item.get("title", ""),
                    url=item.get("url", ""),
                    snippet=item.get("content", ""),
                    provider="Tavily",
                )
            )

        return results


# ==========================================================
# WEB SEARCH SERVICE
# ==========================================================


class WebSearchService:
    """
    High-level interface for web searching.
    """

    def __init__(
        self,
        provider: BaseSearchProvider | None = None,
    ) -> None:

        if provider is not None:
            self.provider = provider
            return

        api_key = os.getenv("TAVILY_API_KEY") or os.getenv("TAVILY_API")

        if not api_key:
            raise RuntimeError("TAVILY_API_KEY not found in environment variables.")

        self.provider = TavilySearchProvider(api_key)

    # =====================================================
    # SEARCH
    # =====================================================

    def search(
        self,
        query: str,
        max_results: int = 5,
    ) -> list[SearchResult]:

        return self.provider.search(
            query=query,
            max_results=max_results,
        )
