"""
=========================================================
OmniMind AI Assistant
Base Agent
=========================================================

Abstract base class for all intelligent agents.

Every agent in OmniMind should inherit from BaseAgent.

Examples
--------
- ChatAgent
- DocumentAgent
- VisionAgent
- ResearchAgent
- CodingAgent
- PlannerAgent
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

# ==========================================================
# AGENT REQUEST
# ==========================================================


@dataclass(slots=True)
class AgentRequest:
    """
    Standard request passed to an agent.
    """

    query: str

    context: dict[str, Any] = field(default_factory=dict)

    metadata: dict[str, Any] = field(default_factory=dict)


# ==========================================================
# AGENT RESPONSE
# ==========================================================


@dataclass(slots=True)
class AgentResponse:
    """
    Standard response returned by an agent.
    """

    success: bool

    output: Any

    agent: str

    metadata: dict[str, Any] = field(default_factory=dict)

    error: str | None = None


# ==========================================================
# BASE AGENT
# ==========================================================


class BaseAgent(ABC):
    """
    Abstract base class for all OmniMind agents.
    """

    def __init__(
        self,
        name: str,
        description: str,
    ) -> None:

        self.name = name

        self.description = description

    # ------------------------------------------------------

    @abstractmethod
    def run(
        self,
        request: AgentRequest,
    ) -> AgentResponse:
        """
        Execute the agent.
        """
        raise NotImplementedError

    # ------------------------------------------------------

    def can_handle(
        self,
        request: AgentRequest,
    ) -> bool:
        """
        Determines whether this agent can handle the request.

        Override in subclasses if needed.
        """
        return True

    # ------------------------------------------------------

    def validate(
        self,
        request: AgentRequest,
    ) -> None:
        """
        Basic request validation.
        """

        if not request.query.strip():

            raise ValueError("Query cannot be empty.")

    # ------------------------------------------------------

    def info(self) -> dict[str, str]:
        """
        Agent metadata.
        """

        return {
            "name": self.name,
            "description": self.description,
        }

    # ------------------------------------------------------

    def __repr__(self) -> str:

        return f"{self.__class__.__name__}" f"(name='{self.name}')"
