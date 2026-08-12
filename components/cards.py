"""
=========================================================
OmniMind AI Assistant
Reusable Card Components
=========================================================
"""

from __future__ import annotations

from typing import Callable

import streamlit as st


class Card:
    """
    Collection of reusable Streamlit cards.
    """

    # =====================================================
    # METRIC CARD
    # =====================================================

    @staticmethod
    def metric(
        title: str,
        value,
        delta: str | None = None,
    ) -> None:

        st.metric(
            label=title,
            value=value,
            delta=delta,
        )

    # =====================================================
    # INFO CARD
    # =====================================================

    @staticmethod
    def info(
        title: str,
        content: str,
    ) -> None:

        with st.container(border=True):

            st.subheader(title)

            st.write(content)

    # =====================================================
    # FEATURE CARD
    # =====================================================

    @staticmethod
    def feature(
        icon: str,
        title: str,
        description: str,
    ) -> None:

        with st.container(border=True):

            st.markdown(f"## {icon} {title}")

            st.write(description)

    # =====================================================
    # BACKWARD COMPATIBILITY
    # =====================================================

    @staticmethod
    def feature_card(
        title: str,
        description: str,
    ) -> None:
        """
        Compatibility wrapper for older pages.
        """

        icon = ""

        icon_map = {
            "💬": "💬",
            "📄": "📄",
            "🖼": "🖼",
            "🎤": "🎤",
            "🔬": "🔬",
            "💻": "💻",
            "🧠": "🧠",
            "⚙": "⚙",
            "📊": "📊",
        }

        for emoji, value in icon_map.items():

            if title.startswith(emoji):

                icon = value
                title = title.replace(emoji, "").strip()
                break

        Card.feature(
            icon=icon,
            title=title,
            description=description,
        )

    # =====================================================
    # STATUS CARD
    # =====================================================

    @staticmethod
    def status(
        title: str,
        status: str,
    ) -> None:

        color = {
            "online": "🟢",
            "offline": "🔴",
            "warning": "🟡",
        }.get(status.lower(), "⚪")

        with st.container(border=True):

            st.markdown(f"### {title}")

            st.write(f"{color} {status.title()}")

    # =====================================================
    # AGENT CARD
    # =====================================================

    @staticmethod
    def agent(
        name: str,
        description: str,
        active: bool = True,
    ) -> None:

        badge = "🟢 Active" if active else "🔴 Disabled"

        with st.container(border=True):

            st.markdown(f"### 🤖 {name}")

            st.caption(badge)

            st.write(description)

    # =====================================================
    # ACTION CARD
    # =====================================================

    @staticmethod
    def action(
        title: str,
        description: str,
        button_text: str,
        key: str,
    ) -> bool:

        with st.container(border=True):

            st.subheader(title)

            st.write(description)

            clicked = st.button(
                button_text,
                key=key,
                use_container_width=True,
            )

        return clicked

    # =====================================================
    # USER CARD
    # =====================================================

    @staticmethod
    def user(
        name: str,
        role: str,
        email: str | None = None,
    ) -> None:

        with st.container(border=True):

            st.markdown(f"## 👤 {name}")

            st.caption(role)

            if email:

                st.write(email)

    # =====================================================
    # DOCUMENT CARD
    # =====================================================

    @staticmethod
    def document(
        filename: str,
        filetype: str,
        size: str,
    ) -> None:

        with st.container(border=True):

            st.markdown(f"### 📄 {filename}")

            st.write(f"Type: {filetype}")

            st.write(f"Size: {size}")

    # =====================================================
    # WORKFLOW CARD
    # =====================================================

    @staticmethod
    def workflow(
        name: str,
        status: str,
        progress: int,
    ) -> None:

        with st.container(border=True):

            st.subheader(name)

            st.write(f"Status: {status}")

            st.progress(progress)

    # =====================================================
    # CUSTOM CARD
    # =====================================================

    @staticmethod
    def custom(
        title: str,
        renderer: Callable[[], None],
    ) -> None:

        with st.container(border=True):

            st.subheader(title)

            renderer()


cards = Card()
