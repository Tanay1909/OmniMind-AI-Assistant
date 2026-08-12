"""
=========================================================
OmniMind AI Assistant
History Component
=========================================================

Reusable conversation history component.
"""

from __future__ import annotations

from datetime import datetime

import streamlit as st

from core.history import HistoryManager


class HistoryComponent:
    """
    Conversation history UI.
    """

    def __init__(self):

        self.history = HistoryManager()

    # =====================================================
    # HEADER
    # =====================================================

    def render_header(self):

        st.subheader("🕘 Conversation History")

        st.caption("Browse and manage previous conversations.")

    # =====================================================
    # SEARCH
    # =====================================================

    def search_box(self):

        return st.text_input(
            "Search Conversations",
            placeholder="Search by title or content...",
        )

    # =====================================================
    # FILTER
    # =====================================================

    def filter_options(self):

        return st.selectbox(
            "Filter",
            [
                "All",
                "Today",
                "This Week",
                "This Month",
            ],
        )

    # =====================================================
    # LOAD
    # =====================================================

    def load_history(self):

        return self.history.get_all()

    # =====================================================
    # LIST
    # =====================================================

    def render_conversations(
        self,
        conversations,
        query: str,
    ):

        if query:

            conversations = [
                conversation
                for conversation in conversations
                if query.lower() in conversation.title.lower()
            ]

        if not conversations:

            st.info("No conversations found.")

            return

        for conversation in conversations:

            with st.expander(
                conversation.title,
                expanded=False,
            ):

                st.caption(f"Created: " f"{conversation.created_at:%d %b %Y %H:%M}")

                preview = (
                    conversation.messages[-1].content[:150]
                    if conversation.messages
                    else "Empty conversation"
                )

                st.write(preview)

                col1, col2, col3 = st.columns(3)

                with col1:

                    if st.button(
                        "Open",
                        key=f"open_{conversation.id}",
                    ):

                        st.session_state.active_conversation = conversation.id

                with col2:

                    if st.button(
                        "Export",
                        key=f"export_{conversation.id}",
                    ):

                        markdown = self.history.export_markdown(conversation.id)

                        st.download_button(
                            "Download",
                            markdown,
                            file_name=(f"{conversation.title}.md"),
                            mime="text/markdown",
                            key=f"download_{conversation.id}",
                        )

                with col3:

                    if st.button(
                        "Delete",
                        key=f"delete_{conversation.id}",
                    ):

                        self.history.delete(conversation.id)

                        st.success("Conversation deleted.")

                        st.rerun()

    # =====================================================
    # STATISTICS
    # =====================================================

    def render_statistics(
        self,
        conversations,
    ):

        total = len(conversations)

        messages = sum(len(c.messages) for c in conversations)

        latest = max(
            (c.created_at for c in conversations),
            default=None,
        )

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Conversations",
            total,
        )

        col2.metric(
            "Messages",
            messages,
        )

        col3.metric(
            "Latest",
            latest.strftime("%d %b") if latest else "-",
        )

    # =====================================================
    # MAIN
    # =====================================================

    def render(self):

        self.render_header()

        query = self.search_box()

        self.filter_options()

        conversations = self.load_history()

        self.render_statistics(conversations)

        st.divider()

        self.render_conversations(
            conversations,
            query,
        )


history_component = HistoryComponent()
