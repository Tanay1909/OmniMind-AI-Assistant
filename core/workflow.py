
"""
=========================================================
OmniMind AI Assistant
Workflow Engine
=========================================================

Executes an ExecutionPlan produced by the Planner.

Responsibilities:
- Execute plan steps sequentially
- Invoke tools
- Call the LLM
- Collect intermediate results
- Handle execution failures
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from core.planner import (
    ExecutionPlan,
    PlanStep,
    StepType,
)
from core.reasoning import (
    ReasoningEngine,
)
from core.tool_executor import (
    ToolExecutor,
    ToolResult,
)
from core.response_parser import AIResponse


# ==========================================================
# LLM INTERFACE
# ==========================================================

class LLMProvider:
    """
    Every LLM service should implement this method.
    """

    def generate(
        self,
        messages: list[dict[str, str]],
        **kwargs,
    ) -> AIResponse:
        raise NotImplementedError


# ==========================================================
# WORKFLOW RESULT
# ==========================================================

@dataclass(slots=True)
class WorkflowResult:
    """
    Result returned by the workflow engine.
    """

    success: bool

    response: AIResponse | None = None

    executed_steps: list[str] = field(default_factory=list)

    tool_results: dict[str, ToolResult] = field(default_factory=dict)

    metadata: dict[str, Any] = field(default_factory=dict)

    error: str | None = None


# ==========================================================
# WORKFLOW ENGINE
# ==========================================================

class WorkflowEngine:
    """
    Executes an execution plan.
    """

    def __init__(
        self,
        tool_executor: ToolExecutor,
        reasoning: ReasoningEngine,
        llm: LLMProvider,
    ):

        self.tool_executor = tool_executor
        self.reasoning = reasoning
        self.llm = llm

    # =====================================================
    # EXECUTE
    # =====================================================

    def execute(
        self,
        plan: ExecutionPlan,
        messages: list[dict[str, str]],
    ) -> WorkflowResult:

        result = WorkflowResult(success=True)

        # High-level reasoning
        reasoning_result = self.reasoning.reason(
            plan.user_request
        )

        result.metadata["reasoning"] = reasoning_result

        for step in plan.steps:

            result.executed_steps.append(step.name)

            try:

                self._execute_step(
                    step,
                    messages,
                    result,
                )

            except Exception as exc:

                result.success = False

                result.error = str(exc)

                break

        return result

    # =====================================================
    # SINGLE STEP
    # =====================================================

    def _execute_step(
        self,
        step: PlanStep,
        messages: list[dict[str, str]],
        result: WorkflowResult,
    ) -> None:

        # ------------------------------
        # Tool
        # ------------------------------

        if step.step_type in (
            StepType.TOOL,
            StepType.OCR,
            StepType.SEARCH,
            StepType.RAG,
        ):

            tool_result = self.tool_executor.execute(
                step.tool,
                **step.parameters,
            )

            result.tool_results[
                step.name
            ] = tool_result

            return

        # ------------------------------
        # LLM
        # ------------------------------

        if step.step_type == StepType.LLM:

            result.response = self.llm.generate(
                messages
            )

            return

        # ------------------------------
        # Output
        # ------------------------------

        if step.step_type == StepType.OUTPUT:

            return


# ==========================================================
# FACTORY
# ==========================================================

def create_workflow(
    tool_executor: ToolExecutor,
    reasoning: ReasoningEngine,
    llm: LLMProvider,
) -> WorkflowEngine:
    """
    Factory helper.
    """

    return WorkflowEngine(
        tool_executor=tool_executor,
        reasoning=reasoning,
        llm=llm,
    )
