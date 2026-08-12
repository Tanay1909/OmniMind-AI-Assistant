
"""
=========================================================
OmniMind AI Assistant
Task Planner
=========================================================

Creates execution plans from user requests.

The planner does not execute tools. It only decides
what should happen. Execution is handled by the
Workflow Engine.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


# ==========================================================
# STEP TYPES
# ==========================================================

class StepType(str, Enum):
    LLM = "llm"
    TOOL = "tool"
    SEARCH = "search"
    OCR = "ocr"
    RAG = "rag"
    MEMORY = "memory"
    OUTPUT = "output"


# ==========================================================
# PLAN STEP
# ==========================================================

@dataclass(slots=True)
class PlanStep:
    """
    Single executable step.
    """

    id: int

    name: str

    step_type: StepType

    description: str

    tool: str | None = None

    parameters: dict = field(default_factory=dict)


# ==========================================================
# EXECUTION PLAN
# ==========================================================

@dataclass(slots=True)
class ExecutionPlan:
    """
    Ordered list of execution steps.
    """

    user_request: str

    steps: list[PlanStep] = field(default_factory=list)

    metadata: dict = field(default_factory=dict)


# ==========================================================
# PLANNER
# ==========================================================

class Planner:
    """
    Creates execution plans.
    """

    def create_plan(
        self,
        prompt: str,
    ) -> ExecutionPlan:

        prompt_lower = prompt.lower()

        plan = ExecutionPlan(
            user_request=prompt
        )

        step_id = 1

        # ----------------------------------------------
        # OCR
        # ----------------------------------------------

        if any(
            keyword in prompt_lower
            for keyword in (
                "image",
                "scan",
                "extract text",
                "ocr",
            )
        ):

            plan.steps.append(
                PlanStep(
                    id=step_id,
                    name="OCR",
                    step_type=StepType.OCR,
                    description="Extract text from image.",
                    tool="ocr",
                )
            )

            step_id += 1

        # ----------------------------------------------
        # PDF
        # ----------------------------------------------

        if any(
            keyword in prompt_lower
            for keyword in (
                "pdf",
                "document",
            )
        ):

            plan.steps.append(
                PlanStep(
                    id=step_id,
                    name="Read Document",
                    step_type=StepType.TOOL,
                    description="Extract document text.",
                    tool="pdf_reader",
                )
            )

            step_id += 1

        # ----------------------------------------------
        # Web Search
        # ----------------------------------------------

        if any(
            keyword in prompt_lower
            for keyword in (
                "latest",
                "today",
                "news",
                "search",
                "current",
            )
        ):

            plan.steps.append(
                PlanStep(
                    id=step_id,
                    name="Search Web",
                    step_type=StepType.SEARCH,
                    description="Retrieve latest information.",
                    tool="web_search",
                )
            )

            step_id += 1

        # ----------------------------------------------
        # Knowledge Retrieval
        # ----------------------------------------------

        if any(
            keyword in prompt_lower
            for keyword in (
                "knowledge",
                "manual",
                "company",
                "policy",
            )
        ):

            plan.steps.append(
                PlanStep(
                    id=step_id,
                    name="Retrieve Knowledge",
                    step_type=StepType.RAG,
                    description="Retrieve relevant knowledge.",
                    tool="rag",
                )
            )

            step_id += 1

        # ----------------------------------------------
        # LLM
        # ----------------------------------------------

        plan.steps.append(
            PlanStep(
                id=step_id,
                name="Generate Response",
                step_type=StepType.LLM,
                description="Generate AI response.",
                tool="llm",
            )
        )

        step_id += 1

        # ----------------------------------------------
        # OUTPUT
        # ----------------------------------------------

        plan.steps.append(
            PlanStep(
                id=step_id,
                name="Return Response",
                step_type=StepType.OUTPUT,
                description="Send final answer to user.",
            )
        )

        return plan


# ==========================================================
# GLOBAL INSTANCE
# ==========================================================

planner = Planner()
