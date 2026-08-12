"""
=========================================================
OmniMind AI Assistant
Workflow Models
=========================================================

Shared workflow models used across the application.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field

# ==========================================================
# WORKFLOW STATUS
# ==========================================================


class WorkflowStatus(str, Enum):
    """
    Workflow execution status.
    """

    PENDING = "pending"

    RUNNING = "running"

    COMPLETED = "completed"

    FAILED = "failed"

    CANCELLED = "cancelled"


# ==========================================================
# STEP STATUS
# ==========================================================


class StepStatus(str, Enum):
    """
    Individual workflow step status.
    """

    PENDING = "pending"

    RUNNING = "running"

    COMPLETED = "completed"

    FAILED = "failed"

    SKIPPED = "skipped"


# ==========================================================
# EXECUTION STRATEGY
# ==========================================================


class ExecutionStrategy(str, Enum):
    """
    Workflow execution mode.
    """

    SEQUENTIAL = "sequential"

    PARALLEL = "parallel"

    DAG = "dag"


# ==========================================================
# WORKFLOW STEP
# ==========================================================


class WorkflowStep(BaseModel):
    """
    One workflow step.
    """

    model_config = ConfigDict(validate_assignment=True)

    id: str = Field(default_factory=lambda: str(uuid4()))

    name: str

    agent: str

    action: str

    status: StepStatus = StepStatus.PENDING

    input_data: dict[str, Any] = Field(default_factory=dict)

    output_data: Any | None = None

    dependencies: list[str] = Field(default_factory=list)

    started_at: datetime | None = None

    completed_at: datetime | None = None

    execution_time: float = 0.0

    error: str | None = None

    metadata: dict[str, Any] = Field(default_factory=dict)


# ==========================================================
# WORKFLOW
# ==========================================================


class Workflow(BaseModel):
    """
    Workflow definition.
    """

    model_config = ConfigDict(validate_assignment=True)

    id: str = Field(default_factory=lambda: str(uuid4()))

    name: str

    description: str = ""

    strategy: ExecutionStrategy = ExecutionStrategy.SEQUENTIAL

    status: WorkflowStatus = WorkflowStatus.PENDING

    created_at: datetime = Field(default_factory=datetime.utcnow)

    started_at: datetime | None = None

    completed_at: datetime | None = None

    steps: list[WorkflowStep] = Field(default_factory=list)

    metadata: dict[str, Any] = Field(default_factory=dict)

    # =====================================================
    # METHODS
    # =====================================================

    def add_step(
        self,
        step: WorkflowStep,
    ) -> None:

        self.steps.append(step)

    @property
    def total_steps(self) -> int:

        return len(self.steps)

    @property
    def completed_steps(self) -> int:

        return len([step for step in self.steps if step.status == StepStatus.COMPLETED])

    @property
    def failed_steps(self) -> int:

        return len([step for step in self.steps if step.status == StepStatus.FAILED])

    @property
    def progress(self) -> float:

        if self.total_steps == 0:
            return 0.0

        return round(
            (self.completed_steps / self.total_steps) * 100,
            2,
        )


# ==========================================================
# WORKFLOW RESULT
# ==========================================================


class WorkflowResult(BaseModel):
    """
    Final workflow execution result.
    """

    model_config = ConfigDict(validate_assignment=True)

    workflow_id: str

    status: WorkflowStatus

    success: bool

    output: Any | None = None

    execution_time: float = 0.0

    completed_steps: int = 0

    total_steps: int = 0

    errors: list[str] = Field(default_factory=list)

    metadata: dict[str, Any] = Field(default_factory=dict)

    @property
    def success_rate(self) -> float:

        if self.total_steps == 0:
            return 0.0

        return round(
            (self.completed_steps / self.total_steps) * 100,
            2,
        )


# ==========================================================
# WORKFLOW EXECUTION LOG
# ==========================================================


class WorkflowExecutionLog(BaseModel):
    """
    Workflow execution history.
    """

    model_config = ConfigDict(validate_assignment=True)

    workflow_id: str

    timestamp: datetime = Field(default_factory=datetime.utcnow)

    step_name: str

    status: StepStatus

    message: str

    metadata: dict[str, Any] = Field(default_factory=dict)
