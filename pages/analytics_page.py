"""
=========================================================
OmniMind AI Assistant
Analytics Dashboard
=========================================================

Enterprise Analytics Dashboard

Features
--------
• Usage Statistics
• Token Consumption
• Model Performance
• Agent Activity
• Workflow Metrics
• System Health
• Charts
"""

from __future__ import annotations

import streamlit as st

from services.analytics_service import AnalyticsService

from components.sidebar import sidebar
from components.navbar import navbar
from components.footer import footer
from components.analytics import analytics_component
from components.charts import charts
from components.notifications import notifications
from core.analytics import analytics

class AnalyticsPage:

    def __init__(self):

        self.service = AnalyticsService(analytics)

    # =====================================================
    # CONFIG
    # =====================================================

    def configure(self):

        st.set_page_config(
            page_title="Analytics",
            page_icon="📊",
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

    def render_header(self, model):

        navbar.render(
            page_title="📊 Analytics Dashboard",
            model_name=model,
        )

    # =====================================================
    # ACTIONS
    # =====================================================

    def actions(self):

        col1, col2 = st.columns(2)

        with col1:

            refresh = st.button(
                "🔄 Refresh",
                use_container_width=True,
            )

        with col2:

            export = st.button(
                "📤 Export Report",
                use_container_width=True,
            )

        return {
            "refresh": refresh,
            "export": export,
        }

    # =====================================================
    # LOAD DATA
    # =====================================================

    def load_data(self):

        return self.service.dashboard()

    # =====================================================
    # METRICS
    # =====================================================

    def metrics(self, data):

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Requests", data["requests"])

        col2.metric("Tokens", data["tokens"])

        col3.metric("Conversations", data["conversations"])

        col4.metric("Users", data["users"])

    # =====================================================
    # CHARTS
    # =====================================================

    def render_charts(self, data):

        st.subheader("Usage Trends")

        charts.line_chart(data["usage"])

        st.subheader("Agent Usage")

        charts.bar_chart(data["agents"])

        st.subheader("Model Distribution")

        charts.pie_chart(data["models"])

    # =====================================================
    # HEALTH
    # =====================================================

    def health(self, data):

        st.subheader("System Health")

        analytics_component.system_health(data["health"])

    # =====================================================
    # RECENT ACTIVITY
    # =====================================================

    def activity(self, data):

        st.subheader("Recent Activity")

        analytics_component.activity_feed(data["activity"])

    # =====================================================
    # EXPORT
    # =====================================================

    def export(self, actions, data):

        if not actions["export"]:

            return

        report = self.service.export_dashboard()

        st.download_button(
            "Download Analytics",
            report,
            file_name="analytics_report.json",
            mime="application/json",
        )

        notifications.success("Analytics", "Report generated.")

    # =====================================================
    # FOOTER
    # =====================================================

    def render_footer(self):

        footer.render()

    # =====================================================
    # MAIN
    # =====================================================

    def render(self):

        self.configure()

        config = self.render_sidebar()

        self.render_header(config["model"])

        actions = self.actions()

        data = self.load_data()

        st.divider()

        self.metrics(data)

        st.divider()

        self.render_charts(data)

        st.divider()

        self.health(data)

        st.divider()

        self.activity(data)

        st.divider()

        self.export(
            actions,
            data,
        )

        self.render_footer()


analytics_page = AnalyticsPage()


def main():

    analytics_page.render()


if __name__ == "__main__":

    main()
