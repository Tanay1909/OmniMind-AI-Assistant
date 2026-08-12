"""
=========================================================
OmniMind AI Assistant
Dashboard
=========================================================

Application Home Dashboard

Features
--------
• System Overview
• AI Capability Cards
• Usage Metrics
• Recent Activity
• Quick Navigation
• Health Monitoring
"""

from __future__ import annotations

import streamlit as st

from components.sidebar import sidebar
from components.navbar import navbar
from components.footer import footer
from components.cards import cards
from components.analytics import analytics_component

from core.analytics import analytics
from services.analytics_service import AnalyticsService


class DashboardPage:
    """
    OmniMind Dashboard Page.
    """

    def __init__(self) -> None:

        # Analytics Service
        self.analytics = AnalyticsService(analytics)

    # =====================================================
    # PAGE CONFIG
    # =====================================================

    def configure(self) -> None:

        st.set_page_config(
            page_title="OmniMind AI",
            page_icon="🤖",
            layout="wide",
            initial_sidebar_state="expanded",
        )

    # =====================================================
    # SIDEBAR
    # =====================================================

    def render_sidebar(self):

        return sidebar.render()

    # =====================================================
    # HEADER
    # =====================================================

    def render_header(
        self,
        model: str,
    ) -> None:

        navbar.render(
            page_title="🏠 OmniMind Dashboard",
            model_name=model,
        )

    # =====================================================
    # HERO SECTION
    # =====================================================

    def hero(self) -> None:

        st.title("🤖 OmniMind AI Assistant")

        st.markdown("""
Welcome to **OmniMind AI** — your unified AI workspace.

Use multiple intelligent agents to:

- 💬 Chat with AI
- 📄 Analyze Documents
- 🖼 Understand Images
- 🎤 Process Speech
- 🔬 Perform Research
- 💻 Generate Code
- 🧠 Manage Memory
- ⚙ Execute Workflows
""")

    # =====================================================
    # KPI METRICS
    # =====================================================

    def metrics(self) -> None:

        stats = self.analytics.dashboard()

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "Requests",
            stats.get("requests", 0),
        )

        c2.metric(
            "Tokens",
            stats.get("tokens", 0),
        )

        c3.metric(
            "Conversations",
            stats.get("conversations", 0),
        )

        c4.metric(
            "Active Models",
            len(stats.get("models", {})),
        )

    # =====================================================
    # FEATURE CARDS
    # =====================================================

    def features(self) -> None:

        st.subheader("AI Capabilities")

        col1, col2, col3 = st.columns(3)

        with col1:

            cards.feature_card(
                title="💬 Chat",
                description="General AI conversations",
            )

            cards.feature_card(
                title="📄 Documents",
                description="Summaries, OCR and RAG",
            )

            cards.feature_card(
                title="🖼 Vision",
                description="Image understanding",
            )

        with col2:

            cards.feature_card(
                title="🎤 Speech",
                description="Speech-to-Text & TTS",
            )

            cards.feature_card(
                title="🔬 Research",
                description="AI web research",
            )

            cards.feature_card(
                title="💻 Coding",
                description="AI software engineering",
            )

        with col3:

            cards.feature_card(
                title="🧠 Memory",
                description="Long-term AI memory",
            )

            cards.feature_card(
                title="⚙ Workflow",
                description="Multi-agent pipelines",
            )

            cards.feature_card(
                title="📊 Analytics",
                description="Usage insights",
            )

    # =====================================================
    # RECENT ACTIVITY
    # =====================================================

    def activity(self) -> None:

        st.subheader("Recent Activity")

        stats = self.analytics.dashboard()

        analytics_component.activity_feed(
            stats.get("activity", []),
        )

    # =====================================================
    # SYSTEM HEALTH
    # =====================================================

    def health(self) -> None:

        st.subheader("System Health")

        stats = self.analytics.dashboard()

        analytics_component.system_health(
            stats.get("health", {}),
        )

    # =====================================================
    # QUICK ACTIONS
    # =====================================================

    def quick_actions(self) -> None:

        st.subheader("Quick Actions")

        col1, col2, col3 = st.columns(3)

        with col1:

            st.page_link(
                "pages/chat_page.py",
                label="💬 Open Chat",
            )

        with col2:

            st.page_link(
                "pages/document_page.py",
                label="📄 Analyze Documents",
            )

        with col3:

            st.page_link(
                "pages/research_page.py",
                label="🔬 Start Research",
            )

    # =====================================================
    # FOOTER
    # =====================================================

    def render_footer(self) -> None:

        footer.render()

    # =====================================================
    # MAIN
    # =====================================================

    def render(self) -> None:

        self.configure()

        config = self.render_sidebar()

        self.render_header(
            config["model"],
        )

        self.hero()

        st.divider()

        self.metrics()

        st.divider()

        self.features()

        st.divider()

        self.activity()

        st.divider()

        self.health()

        st.divider()

        self.quick_actions()

        st.divider()

        self.render_footer()


dashboard_page = DashboardPage()


def main() -> None:

    dashboard_page.render()


if __name__ == "__main__":
    main()
