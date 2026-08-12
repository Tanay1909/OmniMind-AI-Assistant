"""
=========================================================
OmniMind AI Assistant
Analytics Service
=========================================================

Business layer for analytics.

Provides:
- Request statistics
- Token statistics
- Conversation statistics
- User statistics
- Agent usage
- Model usage
- Usage trends
- System health
- Activity feed
- Dashboard export
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from core.analytics import AnalyticsManager


class AnalyticsService:
    """
    High-level analytics service.
    """

    def __init__(
        self,
        collector: AnalyticsManager,
    ) -> None:

        self.collector = collector

    # =====================================================
    # REQUESTS
    # =====================================================

    def record_request(
        self,
        route: str,
        model: str,
        duration: float,
    ) -> None:

        self.collector.request(route)

        self.collector.model(model)

        self.collector.execution_time(
            route,
            duration,
        )

    # =====================================================
    # TOOLS
    # =====================================================

    def record_tool(
        self,
        tool_name: str,
    ) -> None:

        self.collector.tool(tool_name)

    # =====================================================
    # ERRORS
    # =====================================================

    def record_error(
        self,
        error_name: str,
    ) -> None:

        self.collector.error(error_name)

    # =====================================================
    # EVENTS
    # =====================================================

    def record_event(
        self,
        name: str,
        metadata: dict[str, Any] | None = None,
    ) -> None:

        self.collector.record(
            category="event",
            name=name,
            value=1,
            **(metadata or {}),
        )

    # =====================================================
    # SUMMARY
    # =====================================================

    def summary(
        self,
    ) -> dict[str, Any]:

        return self.collector.summary()

    # =====================================================
    # DASHBOARD
    # =====================================================

    def dashboard(
        self,
    ) -> dict[str, Any]:

        summary = self.collector.summary()

        # -------------------------------------------------
        # Existing analytics data
        # -------------------------------------------------

        requests = summary.get(
            "requests",
            0,
        )

        tokens = summary.get(
            "tokens",
            0,
        )

        conversations = summary.get(
            "conversations",
            0,
        )

        models = summary.get(
            "models",
            {},
        )

        agents = summary.get(
            "agents",
            {},
        )

        usage = summary.get(
            "usage",
            [],
        )

        activity = summary.get(
            "activity",
            [],
        )

        health = summary.get(
            "health",
            {
                "status": "Healthy",
            },
        )

        # -------------------------------------------------
        # Users
        #
        # The current AnalyticsManager does not appear
        # to provide a users metric, so default to 0
        # instead of raising KeyError.
        # -------------------------------------------------

        users = summary.get(
            "users",
            0,
        )

        # -------------------------------------------------
        # Dashboard response
        # -------------------------------------------------

        return {
            "requests": requests,
            "tokens": tokens,
            "conversations": conversations,
            "users": users,
            "usage": usage,
            "agents": agents,
            "models": models,
            "activity": activity,
            "health": health,
        }

    # =====================================================
    # EXPORT
    # =====================================================

    def export_json(
        self,
        output_path: str | Path,
    ):

        return self.collector.export()

    # =====================================================
    # DASHBOARD EXPORT
    # =====================================================

    def export_dashboard(
        self,
    ) -> str:

        import json

        data = self.dashboard()

        return json.dumps(
            data,
            indent=4,
            default=str,
        )
