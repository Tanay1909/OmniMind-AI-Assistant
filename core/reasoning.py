
"""
=========================================================
OmniMind AI Assistant
Reasoning Engine
=========================================================

Coordinates high-level reasoning strategies for the
assistant.

Responsibilities:
- Select an appropriate reasoning strategy
- Prepare execution guidance
- Support iterative workflows
- Remain independent of any specific LLM provider
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


# ==========================================================
# REASONING TYPES
# ==========================================================

class ReasoningType(str, Enum):
    DIRECT = "direct"
    TOOL_USE = "tool_use"
    MULTI_STEP = "multi_step"
    REFLECTION = "reflection"


# ==========================================================
# REASONING RESULT
# ==========================================================

@dataclass(slots=True)
class ReasoningResult:
    """
    Output produced by the reasoning engine.
    """

    strategy: ReasoningType

    objective: str

    recommended_tools: list[str] = field(default_factory=list)

    notes: list[str] = field(default_factory=list)

    metadata: dict[str, Any] = field(default_factory=dict)


# ==========================================================
# BASE STRATEGY
# ==========================================================

class ReasoningStrategy(ABC):
    """
    Base class for all reasoning strategies.
    """

    @abstractmethod
    def execute(
        self,
        request: str,
    ) -> ReasoningResult:
        raise NotImplementedError


# ==========================================================
# DIRECT ANSWER
# ==========================================================

class DirectReasoning(ReasoningStrategy):

    def execute(
        self,
        request: str,
    ) -> ReasoningResult:

        return ReasoningResult(
            strategy=ReasoningType.DIRECT,
            objective=request,
        )


# ==========================================================
# TOOL REASONING
# ==========================================================

class ToolReasoning(ReasoningStrategy):

    def execute(
        self,
        request: str,
    ) -> ReasoningResult:

        tools = []

        lower = request.lower()

        if "pdf" in lower:
            tools.append("pdf_reader")

        if "image" in lower:
            tools.append("vision")

        if "translate" in lower:
            tools.append("translator")

        if "search" in lower or "latest" in lower:
            tools.append("web_search")

        return ReasoningResult(
            strategy=ReasoningType.TOOL_USE,
            objective=request,
            recommended_tools=tools,
        )


# ==========================================================
# MULTI STEP
# ==========================================================

class MultiStepReasoning(ReasoningStrategy):

    def execute(
        self,
        request: str,
    ) -> ReasoningResult:

        return ReasoningResult(
            strategy=ReasoningType.MULTI_STEP,
            objective=request,
            notes=[
                "Break task into smaller steps.",
                "Execute each step sequentially.",
                "Combine intermediate results.",
            ],
        )


# ==========================================================
# REFLECTION
# ==========================================================

class ReflectionReasoning(ReasoningStrategy):

    def execute(
        self,
        request: str,
    ) -> ReasoningResult:

        return ReasoningResult(
            strategy=ReasoningType.REFLECTION,
            objective=request,
            notes=[
                "Review generated answer.",
                "Check completeness.",
                "Improve if necessary.",
            ],
        )


# ==========================================================
# ENGINE
# ==========================================================

class ReasoningEngine:
    """
    Selects the appropriate reasoning strategy.
    """

    def __init__(self):

        self.direct = DirectReasoning()

        self.tool = ToolReasoning()

        self.multi = MultiStepReasoning()

        self.reflection = ReflectionReasoning()

    def choose_strategy(
        self,
        request: str,
    ) -> ReasoningStrategy:

        lower = request.lower()

        if any(
            word in lower
            for word in (
                "latest",
                "today",
                "search",
                "pdf",
                "image",
                "translate",
            )
        ):
            return self.tool

        if any(
            word in lower
            for word in (
                "compare",
                "plan",
                "analyze",
                "research",
            )
        ):
            return self.multi

        if any(
            word in lower
            for word in (
                "review",
                "improve",
                "check",
            )
        ):
            return self.reflection

        return self.direct

    def reason(
        self,
        request: str,
    ) -> ReasoningResult:

        strategy = self.choose_strategy(
            request
        )

        return strategy.execute(
            request
        )


# ==========================================================
# GLOBAL INSTANCE
# ==========================================================

reasoning_engine = ReasoningEngine()
