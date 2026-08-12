"""
=========================================================
OmniMind AI Assistant
Reusable Modal Components
=========================================================
"""

from __future__ import annotations

from typing import Callable, Any

import streamlit as st


class ModalComponent:
    """
    Collection of reusable modal dialogs.
    """

    # =====================================================
    # CONFIRMATION
    # =====================================================

    @staticmethod
    def confirmation(
        title: str,
        message: str,
        on_confirm: Callable[[], Any],
    ):

        @st.dialog(title)
        def dialog():

            st.write(message)

            col1, col2 = st.columns(2)

            with col1:

                if st.button(
                    "✅ Confirm",
                    use_container_width=True,
                ):

                    on_confirm()

                    st.success("Completed successfully.")

                    st.rerun()

            with col2:

                if st.button(
                    "❌ Cancel",
                    use_container_width=True,
                ):

                    st.rerun()

        dialog()

    # =====================================================
    # ALERT
    # =====================================================

    @staticmethod
    def alert(
        title: str,
        message: str,
        level: str = "info",
    ):

        @st.dialog(title)
        def dialog():

            if level == "success":

                st.success(message)

            elif level == "warning":

                st.warning(message)

            elif level == "error":

                st.error(message)

            else:

                st.info(message)

            if st.button("Close"):

                st.rerun()

        dialog()

    # =====================================================
    # TEXT PREVIEW
    # =====================================================

    @staticmethod
    def text_preview(
        title: str,
        content: str,
    ):

        @st.dialog(title)
        def dialog():

            st.text_area(
                "Preview",
                value=content,
                height=400,
            )

            st.button("Close")

        dialog()

    # =====================================================
    # MARKDOWN PREVIEW
    # =====================================================

    @staticmethod
    def markdown_preview(
        title: str,
        markdown: str,
    ):

        @st.dialog(title)
        def dialog():

            st.markdown(markdown)

            st.button("Close")

        dialog()

    # =====================================================
    # IMAGE PREVIEW
    # =====================================================

    @staticmethod
    def image_preview(
        title: str,
        image,
    ):

        @st.dialog(title)
        def dialog():

            st.image(
                image,
                use_container_width=True,
            )

            st.button("Close")

        dialog()

    # =====================================================
    # JSON VIEWER
    # =====================================================

    @staticmethod
    def json_view(
        title: str,
        data,
    ):

        @st.dialog(title)
        def dialog():

            st.json(data)

            st.button("Close")

        dialog()

    # =====================================================
    # FORM MODAL
    # =====================================================

    @staticmethod
    def form(
        title: str,
        renderer: Callable[[], Any],
    ):

        @st.dialog(title)
        def dialog():

            renderer()

        dialog()

    # =====================================================
    # CUSTOM MODAL
    # =====================================================

    @staticmethod
    def custom(
        title: str,
        renderer: Callable[[], Any],
    ):

        @st.dialog(title)
        def dialog():

            renderer()

        dialog()


modals = ModalComponent()
