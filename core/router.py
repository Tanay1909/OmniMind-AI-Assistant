
"""
=========================================================
OmniMind AI Assistant
Request Router
=========================================================

Routes user requests to the appropriate workflow.

Responsibilities:
- Analyze user requests
- Select workflow
- Select AI model
- Determine required capabilities
- Produce routing decisions
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


# ==========================================================
# ROUTES
# ==========================================================

class RouteType(str, Enum):

    CHAT = "chat"

    DOCUMENT = "document"

    IMAGE = "image"

    AUDIO = "audio"

    SEARCH = "search"

    RAG = "rag"

    AGENT = "agent"


# ==========================================================
# ROUTE DECISION
# ==========================================================

@dataclass(slots=True)
class RouteDecision:

    route: RouteType

    model: str

    requires_tools: bool = False

    requires_search: bool = False

    requires_rag: bool = False

    requires_vision: bool = False

    metadata: dict = field(default_factory=dict)


# ==========================================================
# ROUTER
# ==========================================================

class Router:

    """
    Intelligent request router.
    """

    def route(
        self,
        request: str,
    ) -> RouteDecision:

        lower = request.lower()

        # ------------------------------------------
        # IMAGE
        # ------------------------------------------

        if any(
            word in lower
            for word in (
                "image",
                "photo",
                "picture",
                "ocr",
                "scan",
            )
        ):

            return RouteDecision(
                route=RouteType.IMAGE,
                model="Gemini Vision",
                requires_tools=True,
                requires_vision=True,
            )

        # ------------------------------------------
        # AUDIO
        # ------------------------------------------

        if any(
            word in lower
            for word in (
                "audio",
                "voice",
                "speech",
            )
        ):

            return RouteDecision(
                route=RouteType.AUDIO,
                model="Whisper",
                requires_tools=True,
            )

        # ------------------------------------------
        # PDF
        # ------------------------------------------

        if any(
            word in lower
            for word in (
                "pdf",
                "document",
                "report",
            )
        ):

            return RouteDecision(
                route=RouteType.DOCUMENT,
                model="GPT-5.5",
                requires_tools=True,
                requires_rag=True,
            )

        # ------------------------------------------
        # SEARCH
        # ------------------------------------------

        if any(
            word in lower
            for word in (
                "today",
                "latest",
                "news",
                "current",
                "search",
            )
        ):

            return RouteDecision(
                route=RouteType.SEARCH,
                model="GPT-5.5",
                requires_search=True,
                requires_tools=True,
            )

        # ------------------------------------------
        # AGENT
        # ------------------------------------------

        if any(
            word in lower
            for word in (
                "plan",
                "analyze",
                "research",
                "workflow",
                "step by step",
            )
        ):

            return RouteDecision(
                route=RouteType.AGENT,
                model="GPT-5.5",
                requires_tools=True,
            )

        # ------------------------------------------
        # DEFAULT
        # ------------------------------------------

        return RouteDecision(
            route=RouteType.CHAT,
            model="GPT-5.5",
        )


# ==========================================================
# GLOBAL INSTANCE
# ==========================================================

router = Router()
