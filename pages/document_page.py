"""
=========================================================
OmniMind AI Assistant
Document Intelligence Page
=========================================================

Upload, analyze, summarize and chat with documents.
"""

from __future__ import annotations

import streamlit as st

from components.sidebar import sidebar
from components.navbar import navbar
from components.document import document_component
from components.notifications import notifications
from components.footer import footer


class DocumentPage:
    """
    Document Intelligence Page.
    """

    def __init__(self):
        pass

    # =====================================================
    # PAGE CONFIGURATION
    # =====================================================

    def configure(self):

        st.set_page_config(
            page_title="Documents",
            page_icon="📄",
            layout="wide",
            initial_sidebar_state="expanded",
        )

    # =====================================================
    # SIDEBAR
    # =====================================================

    def render_sidebar(self):

        return sidebar.render()

    # =====================================================
    # NAVBAR
    # =====================================================

    def render_header(
        self,
        model: str,
    ):

        navbar.render(
            page_title="📄 Document Intelligence",
            model_name=model,
        )

    # =====================================================
    # QUICK ACTIONS
    # =====================================================

    def render_actions(self):

        col1, col2, col3 = st.columns(3)

        with col1:

            if st.button(
                "📝 New Analysis",
                use_container_width=True,
            ):

                notifications.info("Document", "Ready for a new document.")

        with col2:

            if st.button(
                "🗑 Clear Workspace",
                use_container_width=True,
            ):

                st.session_state.pop(
                    "uploaded_document",
                    None,
                )

                notifications.success("Workspace", "Workspace cleared.")

                st.rerun()

        with col3:

            if st.button(
                "📤 Export Results",
                use_container_width=True,
            ):

                notifications.info("Export", "Export functionality coming soon.")

    # =====================================================
    # DOCUMENT WORKSPACE
    # =====================================================

    def render_workspace(self):

        document_component.render()

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

        self.render_header(config["model"])

        self.render_actions()

        st.divider()

        self.render_workspace()

        st.divider()

        self.render_footer()


document_page = DocumentPage()


def main():

    document_page.render()


if __name__ == "__main__":

    main()
