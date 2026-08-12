"""
=========================================================
OmniMind AI Assistant
Search Models
=========================================================

Shared search models used across the application.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field, HttpUrl

# ==========================================================
# SEARCH PROVIDER
# ==========================================================


class SearchProvider(str, Enum):
    """
    Supported search providers.
    """

    TAVILY = "tavily"
    SERPER = "serper"
    BRAVE = "brave"
    DUCKDUCKGO = "duckduckgo"
    GOOGLE = "google"
    BING = "bing"
    UNKNOWN = "unknown"


# ==========================================================
# SEARCH QUERY
# ==========================================================


class SearchQuery(BaseModel):
    """
    Search request information.
    """

    model_config = ConfigDict(validate_assignment=True)

    id: str = Field(default_factory=lambda: str(uuid4()))

    query: str

    provider: SearchProvider = SearchProvider.UNKNOWN

    max_results: int = 5

    language: str = "en"

    safe_search: bool = True

    created_at: datetime = Field(default_factory=datetime.utcnow)

    metadata: dict[str, Any] = Field(default_factory=dict)


# ==========================================================
# CITATION
# ==========================================================


class Citation(BaseModel):
    """
    Citation information.
    """

    model_config = ConfigDict(validate_assignment=True)

    title: str

    url: HttpUrl

    source: str | None = None

    published_date: datetime | None = None

    metadata: dict[str, Any] = Field(default_factory=dict)


# ==========================================================
# SEARCH RESULT
# ==========================================================


class SearchResult(BaseModel):
    """
    One search result.
    """

    model_config = ConfigDict(validate_assignment=True)

    id: str = Field(default_factory=lambda: str(uuid4()))

    title: str

    url: HttpUrl

    snippet: str

    content: str | None = None

    provider: SearchProvider = SearchProvider.UNKNOWN

    rank: int = 1

    score: float | None = None

    published_date: datetime | None = None

    citation: Citation | None = None

    metadata: dict[str, Any] = Field(default_factory=dict)


# ==========================================================
# SEARCH RESPONSE
# ==========================================================


class SearchResponse(BaseModel):
    """
    Complete search response.
    """

    model_config = ConfigDict(validate_assignment=True)

    query: SearchQuery

    results: list[SearchResult] = Field(default_factory=list)

    processing_time: float | None = None

    total_results: int = 0

    metadata: dict[str, Any] = Field(default_factory=dict)

    @property
    def result_count(self) -> int:
        return len(self.results)

    @property
    def has_results(self) -> bool:
        return bool(self.results)

    @property
    def top_result(self) -> SearchResult | None:
        if not self.results:
            return None
        return self.results[0]

    def add_result(self, result: SearchResult) -> None:
        self.results.append(result)
        self.total_results = len(self.results)


# ==========================================================
# RESEARCH REPORT
# ==========================================================


class ResearchReport(BaseModel):
    """
    Structured research output.
    """

    model_config = ConfigDict(validate_assignment=True)

    id: str = Field(default_factory=lambda: str(uuid4()))

    title: str

    query: str

    summary: str

    findings: list[str] = Field(default_factory=list)

    citations: list[Citation] = Field(default_factory=list)

    confidence: float | None = None

    created_at: datetime = Field(default_factory=datetime.utcnow)

    metadata: dict[str, Any] = Field(default_factory=dict)

    @property
    def citation_count(self) -> int:
        return len(self.citations)
