"""
=========================================================
OmniMind AI Assistant
Analytics Manager
=========================================================

Collects application metrics.

Responsibilities:
- Request statistics
- Tool usage
- Model usage
- Agent usage
- User tracking
- Token consumption
- Execution times
- Success rates
- Error tracking
- Usage trends

Visualization belongs to the Streamlit UI.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

# ==========================================================
# METRIC EVENT
# ==========================================================


@dataclass(slots=True)
class MetricEvent:
    timestamp: str
    category: str
    name: str
    value: float | int | str
    metadata: dict[str, Any] = field(default_factory=dict)


# ==========================================================
# ANALYTICS MANAGER
# ==========================================================


class AnalyticsManager:

    def __init__(self) -> None:

        self.events: list[MetricEvent] = []

        self.tool_counter = Counter()
        self.model_counter = Counter()
        self.route_counter = Counter()
        self.agent_counter = Counter()
        self.error_counter = Counter()

        self.user_counter = Counter()

        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.total_tokens = 0

    # ======================================================
    # GENERIC EVENT
    # ======================================================

    def record(
        self,
        category: str,
        name: str,
        value: float | int | str,
        **metadata: Any,
    ) -> None:

        self.events.append(
            MetricEvent(
                timestamp=datetime.now().isoformat(),
                category=category,
                name=name,
                value=value,
                metadata=metadata,
            )
        )

    # ======================================================
    # REQUESTS
    # ======================================================

    def request(
        self,
        route: str,
    ) -> None:

        self.route_counter[route] += 1

        self.record(
            category="request",
            name=route,
            value=1,
        )

    # ======================================================
    # MODEL
    # ======================================================

    def model(
        self,
        model: str,
    ) -> None:

        self.model_counter[model] += 1

        self.record(
            category="model",
            name=model,
            value=1,
        )

    # ======================================================
    # AGENT
    # ======================================================

    def agent(
        self,
        agent_name: str,
    ) -> None:

        self.agent_counter[agent_name] += 1

        self.record(
            category="agent",
            name=agent_name,
            value=1,
        )

    # ======================================================
    # USER
    # ======================================================

    def user(
        self,
        user_id: str = "default",
    ) -> None:

        self.user_counter[user_id] += 1

        self.record(
            category="user",
            name=user_id,
            value=1,
        )

    # ======================================================
    # TOKENS
    # ======================================================

    def tokens(
        self,
        input_tokens: int = 0,
        output_tokens: int = 0,
    ) -> None:

        input_tokens = max(
            0,
            int(input_tokens),
        )

        output_tokens = max(
            0,
            int(output_tokens),
        )

        total = input_tokens + output_tokens

        self.total_input_tokens += input_tokens
        self.total_output_tokens += output_tokens
        self.total_tokens += total

        self.record(
            category="tokens",
            name="usage",
            value=total,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
        )

    # ======================================================
    # TOOL
    # ======================================================

    def tool(
        self,
        tool: str,
    ) -> None:

        self.tool_counter[tool] += 1

        self.record(
            category="tool",
            name=tool,
            value=1,
        )

    # ======================================================
    # ERROR
    # ======================================================

    def error(
        self,
        error: str,
    ) -> None:

        self.error_counter[error] += 1

        self.record(
            category="error",
            name=error,
            value=1,
        )

    # ======================================================
    # EXECUTION TIME
    # ======================================================

    def execution_time(
        self,
        component: str,
        seconds: float,
    ) -> None:

        self.record(
            category="execution_time",
            name=component,
            value=float(seconds),
        )

    # ======================================================
    # USAGE TREND
    # ======================================================

    def usage_trend(self) -> list[dict[str, Any]]:

        request_events = [event for event in self.events if event.category == "request"]

        return [
            {
                "timestamp": event.timestamp,
                "requests": event.value,
            }
            for event in request_events
        ]

    # ======================================================
    # SUMMARY
    # ======================================================

    def summary(self) -> dict[str, Any]:

        requests = sum(self.route_counter.values())

        activity = [
            {
                "timestamp": event.timestamp,
                "category": event.category,
                "name": event.name,
                "value": event.value,
            }
            for event in self.events[-10:]
        ]

        return {
            # ------------------------------------------
            # Main metrics
            # ------------------------------------------
            "requests": requests,
            "tokens": self.total_tokens,
            "conversations": self.route_counter.get(
                "chat",
                0,
            ),
            "users": len(self.user_counter),
            # ------------------------------------------
            # Usage
            # ------------------------------------------
            "usage": self.usage_trend(),
            # ------------------------------------------
            # Agents
            # ------------------------------------------
            "agents": dict(self.agent_counter),
            # ------------------------------------------
            # Models
            # ------------------------------------------
            "models": dict(self.model_counter),
            # ------------------------------------------
            # Tools
            # ------------------------------------------
            "tools": dict(self.tool_counter),
            # ------------------------------------------
            # Routes
            # ------------------------------------------
            "routes": dict(self.route_counter),
            # ------------------------------------------
            # Errors
            # ------------------------------------------
            "errors": dict(self.error_counter),
            # ------------------------------------------
            # Activity
            # ------------------------------------------
            "activity": activity,
            # ------------------------------------------
            # Health
            # ------------------------------------------
            "health": {
                "status": ("Healthy" if not self.error_counter else "Warning"),
                "errors": sum(self.error_counter.values()),
                "requests": requests,
            },
        }

    # ======================================================
    # EXPORT
    # ======================================================

    def export(self) -> list[dict[str, Any]]:

        return [
            {
                "timestamp": event.timestamp,
                "category": event.category,
                "name": event.name,
                "value": event.value,
                "metadata": event.metadata,
            }
            for event in self.events
        ]

    # ======================================================
    # RESET
    # ======================================================

    def clear(self) -> None:

        self.events.clear()

        self.tool_counter.clear()

        self.model_counter.clear()

        self.route_counter.clear()

        self.agent_counter.clear()

        self.error_counter.clear()

        self.user_counter.clear()

        self.total_input_tokens = 0

        self.total_output_tokens = 0

        self.total_tokens = 0


# ==========================================================
# BACKWARD COMPATIBILITY
# ==========================================================

AnalyticsCollector = AnalyticsManager


# ==========================================================
# GLOBAL INSTANCE
# ==========================================================

analytics = AnalyticsManager()
