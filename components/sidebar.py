"""
=========================================================
OmniMind AI Assistant
Sidebar Component
=========================================================

Reusable Streamlit sidebar used across the application.
"""

from __future__ import annotations

import streamlit as st

from config.ui_config import UIConfig


class Sidebar:
    """
    Reusable application sidebar.
    """

    def __init__(self) -> None:

        self.ui = UIConfig()

    # =====================================================
    # HEADER
    # =====================================================

    def render_header(self) -> None:
        """
        Sidebar header.
        """

        st.sidebar.markdown("# 🤖 OmniMind AI")

        st.sidebar.caption("Multimodal Intelligent Assistant")

        st.sidebar.divider()

    # =====================================================
    # NAVIGATION
    # =====================================================

    def render_navigation(self) -> str:
        """
        Main navigation.
        """

        return st.sidebar.radio(
            "Navigation",
            [
                "💬 Chat",
                "📄 Documents",
                "🖼 Vision",
                "🎤 Speech",
                "🌐 Research",
                "💻 Coding",
                "🧠 Memory",
                "📊 Analytics",
                "⚙ Settings",
            ],
        )

    # =====================================================
    # MODEL INFO
    # =====================================================

    def render_model_info(self) -> str:
        """
        Display active model.
        """

        st.sidebar.subheader("Active Model")

        page = st.session_state.get(
            "current_page",
            "💬 Chat",
        )

        if page == "💻 Coding":

            provider = "Groq"
            model = "Qwen3 Coder 480B"

        else:

            provider = "Google Gemini"
            model = "Gemini Flash"

        st.sidebar.info(f"Provider : {provider}\n\n" f"Model : {model}")

        return model

    # =====================================================
    # TEMPERATURE
    # =====================================================

    def render_temperature(self) -> float:
        """
        Temperature slider.
        """

        return st.sidebar.slider(
            "Temperature",
            min_value=0.0,
            max_value=2.0,
            value=0.7,
            step=0.1,
        )

    # =====================================================
    # FEATURES
    # =====================================================

    def render_features(self) -> dict:
        """
        Feature toggles.
        """

        st.sidebar.subheader("Features")

        return {
            "Memory": st.sidebar.checkbox(
                "Enable Memory",
                value=True,
            ),
            "Streaming": st.sidebar.checkbox(
                "Streaming",
                value=True,
            ),
            "Web Search": st.sidebar.checkbox(
                "Web Search",
                value=True,
            ),
            "Vision": st.sidebar.checkbox(
                "Vision",
                value=True,
            ),
            "Speech": st.sidebar.checkbox(
                "Speech",
                value=True,
            ),
        }

    # =====================================================
    # SESSION
    # =====================================================

    def render_session_info(self) -> None:
        """
        Session information.
        """

        st.sidebar.divider()

        st.sidebar.markdown("### Session")

        st.sidebar.metric(
            "Messages",
            st.session_state.get(
                "message_count",
                0,
            ),
        )

        st.sidebar.metric(
            "Documents",
            st.session_state.get(
                "document_count",
                0,
            ),
        )

    # =====================================================
    # ACTIONS
    # =====================================================

    def render_actions(self) -> bool:
        """
        Sidebar buttons.
        """

        st.sidebar.divider()

        return st.sidebar.button(
            "🗑 Clear Conversation",
            use_container_width=True,
        )

    # =====================================================
    # FOOTER
    # =====================================================

    def render_footer(self) -> None:
        """
        Footer.
        """

        st.sidebar.divider()

        st.sidebar.caption("OmniMind AI v1.0")

    # =====================================================
    # COMPLETE SIDEBAR
    # =====================================================

    def render(self) -> dict:
        """
        Render complete sidebar.
        """

        self.render_header()

        page = self.render_navigation()

        st.session_state["current_page"] = page

        model = self.render_model_info()

        temperature = self.render_temperature()

        features = self.render_features()

        self.render_session_info()

        clear = self.render_actions()

        self.render_footer()

        return {
            "page": page,
            "model": model,
            "temperature": temperature,
            "features": features,
            "clear": clear,
        }


sidebar = Sidebar()
