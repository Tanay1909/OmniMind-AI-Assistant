"""
=========================================================
OmniMind AI Assistant
Analytics Models
=========================================================

Shared analytics models used across the application.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field

# ==========================================================
# EVENT TYPE
# ==========================================================


class EventType(str, Enum):
    """
    Types of analytics events.
    """

    REQUEST = "request"
    RESPONSE = "response"
    TOOL = "tool"
    ERROR = "error"
    MODEL = "model"
    SEARCH = "search"
    OCR = "ocr"
    EXPORT = "export"
    LOGIN = "login"
    CUSTOM = "custom"


# ==========================================================
# TOKEN USAGE
# ==========================================================


class TokenUsage(BaseModel):
    """
    LLM token statistics.
    """

    model_config = ConfigDict(validate_assignment=True)

    prompt_tokens: int = 0

    completion_tokens: int = 0

    total_tokens: int = 0

    estimated_cost: float = 0.0

    model_name: str | None = None


# ==========================================================
# PERFORMANCE METRICS
# ==========================================================


class PerformanceMetrics(BaseModel):
    """
    Execution performance.
    """

    model_config = ConfigDict(validate_assignment=True)

    latency_ms: float = 0.0

    processing_time: float = 0.0

    cpu_usage: float | None = None

    memory_usage: float | None = None

    success: bool = True


# ==========================================================
# ANALYTICS EVENT
# ==========================================================


class AnalyticsEvent(BaseModel):
    """
    One analytics event.
    """

    model_config = ConfigDict(validate_assignment=True)

    id: str = Field(default_factory=lambda: str(uuid4()))

    event_type: EventType

    timestamp: datetime = Field(default_factory=datetime.utcnow)

    source: str

    action: str

    metadata: dict[str, Any] = Field(default_factory=dict)


# ==========================================================
# REQUEST METRICS
# ==========================================================


class RequestMetrics(BaseModel):
    """
    Metrics for a single request.
    """

    model_config = ConfigDict(validate_assignment=True)

    request_id: str = Field(default_factory=lambda: str(uuid4()))

    route: str

    model: str

    user_input_length: int

    response_length: int = 0

    token_usage: TokenUsage = Field(default_factory=TokenUsage)

    performance: PerformanceMetrics = Field(default_factory=PerformanceMetrics)

    timestamp: datetime = Field(default_factory=datetime.utcnow)


# ==========================================================
# AGENT METRICS
# ==========================================================


class AgentMetrics(BaseModel):
    """
    Agent execution statistics.
    """

    model_config = ConfigDict(validate_assignment=True)

    agent_name: str

    requests: int = 0

    successful_requests: int = 0

    failed_requests: int = 0

    average_latency: float = 0.0

    total_tokens: int = 0

    metadata: dict[str, Any] = Field(default_factory=dict)

    @property
    def success_rate(self) -> float:

        if self.requests == 0:
            return 0.0

        return round(
            (self.successful_requests / self.requests) * 100,
            2,
        )


# ==========================================================
# ANALYTICS SUMMARY
# ==========================================================


class AnalyticsSummary(BaseModel):
    """
    Dashboard summary.
    """

    model_config = ConfigDict(validate_assignment=True)

    generated_at: datetime = Field(default_factory=datetime.utcnow)

    total_requests: int = 0

    successful_requests: int = 0

    failed_requests: int = 0

    total_tokens: int = 0

    average_latency: float = 0.0

    active_models: list[str] = Field(default_factory=list)

    active_agents: list[str] = Field(default_factory=list)

    metadata: dict[str, Any] = Field(default_factory=dict)

    @property
    def success_rate(self) -> float:

        if self.total_requests == 0:
            return 0.0

        return round(
            (self.successful_requests / self.total_requests) * 100,
            2,
        )
