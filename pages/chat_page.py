"""
=========================================================
OmniMind AI Assistant
Chat Page
=========================================================

Main conversational AI interface.
"""

from __future__ import annotations

import streamlit as st

from components.sidebar import sidebar
from components.navbar import navbar
from components.chat import chat_component
from components.footer import footer
from components.notifications import notifications


class ChatPage:
    """
    Main Chat Page.
    """

    def __init__(self):

        pass

    # =====================================================
    # PAGE CONFIG
    # =====================================================

    def configure(self):

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
    # NAVBAR
    # =====================================================

    def render_header(
        self,
        model: str,
    ):

        navbar.render(
            page_title="💬 AI Chat",
            model_name=model,
        )

    # =====================================================
    # MAIN CHAT
    # =====================================================

    def render_chat(self):

        chat_component.render()

    # =====================================================
    # QUICK ACTIONS
    # =====================================================

    def actions(
        self,
        config,
    ):

        if config["clear"]:

            chat_component.clear()

            notifications.success(
                "Conversation",
                "Conversation cleared successfully.",
            )

            st.rerun()

    # =====================================================
    # FOOTER
    # =====================================================

    def render_footer(self):

        footer.render()

    # =====================================================
    # COMPLETE PAGE
    # =====================================================

    def render(self):

        self.configure()

        config = self.render_sidebar()

        self.render_header(config["model"])

        self.actions(config)

        self.render_chat()

        self.render_footer()


chat_page = ChatPage()


def main():

    chat_page.render()


if __name__ == "__main__":

    main()
