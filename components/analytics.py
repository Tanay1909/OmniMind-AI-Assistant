"""
=========================================================
OmniMind AI Assistant
Analytics Component
=========================================================

Reusable analytics dashboard.
"""

from __future__ import annotations

import streamlit as st

from services.analytics_service import AnalyticsService
from core.analytics import analytics


class AnalyticsComponent:
    """
    Analytics dashboard.
    """

    def __init__(self) -> None:

        self.service = AnalyticsService(analytics)

    # =====================================================
    # HEADER
    # =====================================================

    def render_header(self) -> None:

        st.header("📊 Analytics Dashboard")
        st.caption("Monitor usage, performance and AI statistics.")

    # =====================================================
    # SUMMARY
    # =====================================================

    def render_summary(self, summary: dict) -> None:

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Requests", summary.get("requests", 0))
        col2.metric("Tokens", summary.get("tokens", 0))
        col3.metric("Conversations", summary.get("conversations", 0))
        col4.metric("Models", len(summary.get("models", {})))

    # =====================================================
    # MODEL USAGE
    # =====================================================

    def render_model_usage(self, summary: dict) -> None:

        st.subheader("Model Usage")

        models = summary.get("models", {})

        if models:
            st.bar_chart(models)
        else:
            st.info("No model usage data available.")

    # =====================================================
    # RECENT ACTIVITY
    # =====================================================

    def activity_feed(self, activity: list) -> None:

        if not activity:
            st.info("No recent activity.")
            return

        for event in reversed(activity):

            with st.expander(
                f"{event.get('category', 'Event')} • {event.get('name', '')}"
            ):

                st.write(f"**Value:** {event.get('value', '')}")

                if event.get("timestamp"):
                    st.caption(event["timestamp"])

    # =====================================================
    # SYSTEM HEALTH
    # =====================================================

    def system_health(self, health: dict) -> None:

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Status",
            health.get("status", "Healthy"),
        )

        col2.metric(
            "Requests",
            health.get("requests", 0),
        )

        col3.metric(
            "Errors",
            health.get("errors", 0),
        )

    # =====================================================
    # MAIN DASHBOARD
    # =====================================================

    def render(self) -> None:

        self.render_header()

        summary = self.service.dashboard()

        self.render_summary(summary)

        st.divider()

        self.render_model_usage(summary)

        st.divider()

        st.subheader("Recent Activity")
        self.activity_feed(summary.get("activity", []))

        st.divider()

        st.subheader("System Health")
        self.system_health(summary.get("health", {}))


analytics_component = AnalyticsComponent()
