"""
=========================================================
OmniMind AI Assistant
Notification Component
=========================================================

Centralized notification system used throughout
the application.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

import streamlit as st


class NotificationComponent:
    """
    Central notification manager.
    """

    def __init__(self) -> None:

        if "notifications" not in st.session_state:
            st.session_state["notifications"] = []

    # =====================================================
    # INTERNAL
    # =====================================================

    def _store(
        self,
        level: str,
        title: str,
        message: str,
    ) -> None:

        if "notifications" not in st.session_state:
            st.session_state["notifications"] = []

        st.session_state["notifications"].append(
            {
                "level": level,
                "title": title,
                "message": message,
                "timestamp": datetime.now(),
            }
        )

    # =====================================================
    # SUCCESS
    # =====================================================

    def success(
        self,
        title: str,
        message: str,
    ) -> None:

        st.success(message)
        st.toast(f"✅ {title}")

        self._store(
            "success",
            title,
            message,
        )

    # =====================================================
    # ERROR
    # =====================================================

    def error(
        self,
        title: str,
        message: str,
    ) -> None:

        st.error(message)
        st.toast(f"❌ {title}")

        self._store(
            "error",
            title,
            message,
        )

    # =====================================================
    # WARNING
    # =====================================================

    def warning(
        self,
        title: str,
        message: str,
    ) -> None:

        st.warning(message)
        st.toast(f"⚠️ {title}")

        self._store(
            "warning",
            title,
            message,
        )

    # =====================================================
    # INFO
    # =====================================================

    def info(
        self,
        title: str,
        message: str,
    ) -> None:

        st.info(message)
        st.toast(f"ℹ️ {title}")

        self._store(
            "info",
            title,
            message,
        )

    # =====================================================
    # PROGRESS
    # =====================================================

    def progress(
        self,
        title: str,
        value: float,
    ) -> Any:

        st.caption(title)
        return st.progress(value)

    # =====================================================
    # SPINNER
    # =====================================================

    def spinner(
        self,
        text: str,
    ):

        return st.spinner(text)

    # =====================================================
    # ACTIVITY FEED
    # =====================================================

    def activity_feed(self) -> None:

        st.subheader("🔔 Activity")

        notifications = st.session_state.get("notifications", [])

        if not notifications:
            st.info("No notifications.")
            return

        for notification in reversed(notifications):

            with st.expander(
                f"{notification['timestamp']:%H:%M:%S} • {notification['title']}"
            ):

                st.write(notification["message"])
                st.caption(f"Type: {notification['level']}")

    # =====================================================
    # CLEAR
    # =====================================================

    def clear(self) -> None:

        st.session_state["notifications"] = []

    # =====================================================
    # COUNT
    # =====================================================

    def count(self) -> int:

        return len(st.session_state.get("notifications", []))

    # =====================================================
    # BADGE
    # =====================================================

    def badge(self) -> None:

        st.metric(
            "Notifications",
            self.count(),
        )

    # =====================================================
    # EXPORT
    # =====================================================

    def export(self) -> list[dict]:

        return list(st.session_state.get("notifications", []))


notifications = NotificationComponent()
