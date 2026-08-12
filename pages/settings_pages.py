"""
=========================================================
OmniMind AI Assistant
Settings Page
=========================================================

Application configuration dashboard.
"""

from __future__ import annotations

import json

import streamlit as st

from components.footer import footer
from components.navbar import navbar
from components.notifications import notifications
from components.settings import settings_component
from components.sidebar import sidebar
from core.analytics import analytics
from services.analytics_service import AnalyticsService


class SettingsPage:
    """Application Settings Dashboard."""

    def __init__(self):
        self.analytics = analytics
        self.service = AnalyticsService(analytics)

    # =====================================================
    # PAGE CONFIG
    # =====================================================

    def configure(self):
        st.set_page_config(
            page_title="Settings",
            page_icon="⚙️",
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
            page_title="⚙️ Application Settings",
            model_name=model,
        )

    # =====================================================
    # SETTINGS
    # =====================================================

    def render_settings(self):
        settings_component.render()

    # =====================================================
    # ACTION BUTTONS
    # =====================================================

    def render_actions(self):
        col1, col2, col3 = st.columns(3)

        with col1:
            save = st.button(
                "💾 Save",
                use_container_width=True,
            )

        with col2:
            reset = st.button(
                "🔄 Reset",
                use_container_width=True,
            )

        with col3:
            export = st.button(
                "📤 Export",
                use_container_width=True,
            )

        return save, reset, export

    # =====================================================
    # HANDLE BUTTONS
    # =====================================================

    def handle_actions(self, save, reset, export):

        if save:
            notifications.success(
                "Settings",
                "Configuration saved.",
            )

        if reset:
            st.session_state.clear()

            notifications.info(
                "Settings",
                "Configuration reset.",
            )

            st.rerun()

        if export:

            exported = json.dumps(
                st.session_state,
                indent=4,
                default=str,
            )

            st.download_button(
                label="Download Settings",
                data=exported,
                file_name="settings.json",
                mime="application/json",
            )

    # =====================================================
    # SYSTEM INFORMATION
    # =====================================================

    def system_information(self):

        st.subheader("System")

        try:
            stats = self.analytics.dashboard()

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Models",
                len(stats.get("models", {})),
            )

            col2.metric(
                "Requests",
                stats.get("requests", 0),
            )

            col3.metric(
                "Users",
                stats.get("users", 0),
            )

        except Exception:
            st.info("Analytics information is currently unavailable.")

    # =====================================================
    # FOOTER
    # =====================================================

    def render_footer(self):
        footer.render()

    # =====================================================
    # MAIN PAGE
    # =====================================================

    def render(self):

        self.configure()

        config = self.render_sidebar()

        model = config.get("model", "GPT-4.1")

        self.render_header(model)

        self.render_settings()

        st.divider()

        save, reset, export = self.render_actions()

        self.handle_actions(
            save,
            reset,
            export,
        )

        st.divider()

        self.system_information()

        st.divider()

        self.render_footer()


settings_page = SettingsPage()


def main():
    settings_page.render()


if __name__ == "__main__":
    main()
