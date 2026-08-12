"""
=========================================================
OmniMind AI Assistant
Response Models
=========================================================

Shared response models used across the application.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Generic, TypeVar
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field

T = TypeVar("T")


# ==========================================================
# RESPONSE STATUS
# ==========================================================


class ResponseStatus(str, Enum):
    """
    Standard response status.
    """

    SUCCESS = "success"

    ERROR = "error"

    WARNING = "warning"

    INFO = "info"


# ==========================================================
# BASE RESPONSE
# ==========================================================


class APIResponse(BaseModel, Generic[T]):
    """
    Standard application response.
    """

    model_config = ConfigDict(validate_assignment=True)

    id: str = Field(default_factory=lambda: str(uuid4()))

    status: ResponseStatus = ResponseStatus.SUCCESS

    success: bool = True

    message: str = "Request completed successfully."

    data: T | None = None

    metadata: dict[str, Any] = Field(default_factory=dict)

    timestamp: datetime = Field(default_factory=datetime.utcnow)


# ==========================================================
# ERROR DETAILS
# ==========================================================


class ErrorDetails(BaseModel):
    """
    Detailed error information.
    """

    model_config = ConfigDict(validate_assignment=True)

    code: str

    message: str

    details: dict[str, Any] = Field(default_factory=dict)

    stack_trace: str | None = None


# ==========================================================
# ERROR RESPONSE
# ==========================================================


class ErrorResponse(APIResponse[None]):
    """
    Error response.
    """

    status: ResponseStatus = ResponseStatus.ERROR

    success: bool = False

    error: ErrorDetails


# ==========================================================
# PAGINATION
# ==========================================================


class Pagination(BaseModel):
    """
    Pagination information.
    """

    model_config = ConfigDict(validate_assignment=True)

    page: int = 1

    page_size: int = 10

    total_items: int = 0

    total_pages: int = 0

    has_next: bool = False

    has_previous: bool = False


# ==========================================================
# PAGINATED RESPONSE
# ==========================================================


class PaginatedResponse(APIResponse[list[T]], Generic[T]):
    """
    Response containing paginated data.
    """

    pagination: Pagination


# ==========================================================
# WORKFLOW RESPONSE
# ==========================================================


class WorkflowResponse(APIResponse[T], Generic[T]):
    """
    Response returned by workflow execution.
    """

    workflow_id: str

    completed_steps: int = 0

    total_steps: int = 0

    execution_time: float = 0.0

    warnings: list[str] = Field(default_factory=list)

    @property
    def progress(self) -> float:
        """
        Workflow completion percentage.
        """

        if self.total_steps == 0:
            return 0.0

        return round(
            (self.completed_steps / self.total_steps) * 100,
            2,
        )


# ==========================================================
# STREAM RESPONSE
# ==========================================================


class StreamChunk(BaseModel):
    """
    One streaming response chunk.
    """

    model_config = ConfigDict(validate_assignment=True)

    chunk_id: str = Field(default_factory=lambda: str(uuid4()))

    content: str

    finished: bool = False

    metadata: dict[str, Any] = Field(default_factory=dict)


# ==========================================================
# BULK RESPONSE
# ==========================================================


class BulkResponse(APIResponse[list[T]], Generic[T]):
    """
    Response for batch operations.
    """

    processed: int = 0

    succeeded: int = 0

    failed: int = 0

    errors: list[ErrorDetails] = Field(default_factory=list)

    @property
    def success_rate(self) -> float:

        if self.processed == 0:
            return 0.0

        return round(
            (self.succeeded / self.processed) * 100,
            2,
        )
