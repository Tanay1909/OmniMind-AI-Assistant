"""
=========================================================
OmniMind AI Assistant
Navbar Component
=========================================================

Reusable top navigation/header for the application.
"""

from __future__ import annotations

from datetime import datetime

import streamlit as st


class Navbar:
    """
    Application navbar.
    """

    def __init__(self) -> None:
        pass

    # =====================================================
    # HEADER
    # =====================================================

    def render(
        self,
        page_title: str,
        model_name: str,
    ) -> None:
        """
        Render application navbar.
        """

        left, center, right = st.columns([3, 2, 2])

        # ===============================================
        # LEFT
        # ===============================================

        with left:

            st.title(page_title)

            st.caption("OmniMind AI Assistant")

        # ===============================================
        # CENTER
        # ===============================================

        with center:

            st.metric(
                "Current Model",
                model_name,
            )

            st.caption(datetime.now().strftime("%d %b %Y"))

        # ===============================================
        # RIGHT
        # ===============================================

        with right:

            st.metric(
                "Status",
                "🟢 Online",
            )

            st.caption("Ready")

        st.divider()

    # =====================================================
    # QUICK ACTIONS
    # =====================================================

    def quick_actions(self) -> dict:
        """
        Render quick action buttons.
        """

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            new_chat = st.button(
                "💬 New Chat",
                use_container_width=True,
            )

        with col2:

            upload = st.button(
                "📄 Upload",
                use_container_width=True,
            )

        with col3:

            export = st.button(
                "📤 Export",
                use_container_width=True,
            )

        with col4:

            settings = st.button(
                "⚙ Settings",
                use_container_width=True,
            )

        return {
            "new_chat": new_chat,
            "upload": upload,
            "export": export,
            "settings": settings,
        }

    # =====================================================
    # SESSION INFO
    # =====================================================

    def session_summary(self) -> None:
        """
        Display current session summary.
        """

        messages = st.session_state.get(
            "message_count",
            0,
        )

        documents = st.session_state.get(
            "document_count",
            0,
        )

        tokens = st.session_state.get(
            "token_usage",
            0,
        )

        latency = st.session_state.get(
            "latency",
            "0 ms",
        )

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Messages",
            messages,
        )

        col2.metric(
            "Documents",
            documents,
        )

        col3.metric(
            "Tokens",
            tokens,
        )

        col4.metric(
            "Latency",
            latency,
        )


navbar = Navbar()
