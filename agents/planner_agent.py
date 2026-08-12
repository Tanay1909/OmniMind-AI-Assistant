"""
=========================================================
OmniMind AI Assistant
Planner Agent
=========================================================

Responsibilities
----------------
- Analyze user intent
- Select required agents
- Create execution plans
- Estimate execution strategy

The Planner DOES NOT execute tasks.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from agents.base_agent import (
    AgentRequest,
    AgentResponse,
    BaseAgent,
)

# ==========================================================
# AGENT TYPES
# ==========================================================


class AgentType(Enum):

    CHAT = "chat"

    DOCUMENT = "document"

    VISION = "vision"

    WEB = "web"

    CODING = "coding"

    RESEARCH = "research"

    MEMORY = "memory"


# ==========================================================
# PLAN STEP
# ==========================================================


@dataclass(slots=True)
class PlanStep:

    order: int

    agent: AgentType

    action: str

    parameters: dict[str, Any] = field(default_factory=dict)


# ==========================================================
# EXECUTION PLAN
# ==========================================================


@dataclass(slots=True)
class ExecutionPlan:

    steps: list[PlanStep]

    parallel: bool = False

    metadata: dict[str, Any] = field(default_factory=dict)


# ==========================================================
# PLANNER AGENT
# ==========================================================


class PlannerAgent(BaseAgent):
    """
    Creates execution plans for the Orchestrator.
    """

    def __init__(self) -> None:

        super().__init__(name="Planner Agent", description="Creates execution plans.")

    # =====================================================
    # INTENT ANALYSIS
    # =====================================================

    def detect_agent(
        self,
        request: AgentRequest,
    ) -> AgentType:

        query = request.query.lower()

        if any(
            word in query
            for word in [
                "code",
                "python",
                "java",
                "bug",
                "debug",
                "algorithm",
                "program",
            ]
        ):
            return AgentType.CODING

        if any(
            word in query
            for word in [
                "image",
                "photo",
                "picture",
                "ocr",
                "vision",
            ]
        ):
            return AgentType.VISION

        if any(
            word in query
            for word in [
                "pdf",
                "document",
                "resume",
                "report",
            ]
        ):
            return AgentType.DOCUMENT

        if any(
            word in query
            for word in [
                "latest",
                "today",
                "news",
                "current",
                "search",
            ]
        ):
            return AgentType.WEB

        if any(
            word in query
            for word in [
                "compare",
                "research",
                "analyze",
                "study",
            ]
        ):
            return AgentType.RESEARCH

        return AgentType.CHAT

    # =====================================================
    # PLAN
    # =====================================================

    def create_plan(
        self,
        request: AgentRequest,
    ) -> ExecutionPlan:

        agent = self.detect_agent(request)

        step = PlanStep(
            order=1,
            agent=agent,
            action="run",
            parameters=request.context,
        )

        return ExecutionPlan(
            steps=[step],
            parallel=False,
            metadata={
                "intent": agent.value,
            },
        )

    # =====================================================
    # MAIN
    # =====================================================

    def run(
        self,
        request: AgentRequest,
    ) -> AgentResponse:

        self.validate(request)

        try:

            plan = self.create_plan(request)

            return AgentResponse(
                success=True,
                output=plan,
                agent=self.name,
                metadata=plan.metadata,
            )

        except Exception as exc:

            return AgentResponse(
                success=False,
                output=None,
                error=str(exc),
                agent=self.name,
            )
