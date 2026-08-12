"""
=========================================================
OmniMind AI Assistant
Memory Management Page
=========================================================

Features
--------
• View Conversation Memory
• Search Memory
• Filter by Category
• Favorite Memories
• Archive Memories
• Delete Memories
• Export JSON
• Memory Statistics
"""

from __future__ import annotations

import json

import streamlit as st

from agents.memory_agent import MemoryAgent

from core.memory import MemoryCategory

from components.footer import footer
from components.navbar import navbar
from components.notifications import notifications
from components.sidebar import sidebar


class MemoryPage:
    """
    Advanced Memory Management Page.
    """

    def __init__(self):

        self.agent = MemoryAgent()

    # =====================================================
    # CONFIG
    # =====================================================

    def configure(self):

        st.set_page_config(
            page_title="Memory",
            page_icon="🧠",
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

    def render_header(
        self,
        model: str,
    ):

        navbar.render(
            page_title="🧠 Memory Manager",
            model_name=model,
        )

    # =====================================================
    # FILTERS
    # =====================================================

    def render_filters(self):

        col1, col2 = st.columns(2)

        with col1:

            query = st.text_input(
                "Search Memory",
                placeholder="Search memories...",
            )

        with col2:

            category = st.selectbox(
                "Category",
                [
                    "All",
                    *[category.value for category in MemoryCategory],
                ],
            )

        return query, category

    # =====================================================
    # ACTIONS
    # =====================================================

    def render_actions(self):

        col1, col2, col3 = st.columns(3)

        with col1:

            refresh = st.button(
                "🔄 Refresh",
                use_container_width=True,
            )

        with col2:

            export = st.button(
                "📤 Export",
                use_container_width=True,
            )

        with col3:

            clear = st.button(
                "🗑 Clear Memory",
                use_container_width=True,
            )

        if clear:

            self.agent.clear()

            notifications.success(
                "Memory",
                "Memory cleared successfully.",
            )

            st.rerun()

        return refresh, export

    # =====================================================
    # LOAD MEMORIES
    # =====================================================

    def load_memories(
        self,
        query: str,
        category: str,
    ):

        if query:

            memories = self.agent.search(query)

        else:

            memories = self.agent.recall()

        if category != "All":

            memories = [
                memory for memory in memories if memory.category.value == category
            ]

        return memories
    # =====================================================
    # MEMORY TABLE
    # =====================================================

    def render_memory_table(
        self,
        memories,
        export: bool,
    ):

        st.subheader("📚 Stored Memories")

        if not memories:

            st.info("No memories found.")

            return

        exported_data = []

        for memory in memories:

            exported_data.append(memory.to_dict())

            with st.expander(
                f"{memory.category.value} • {memory.role} • {memory.created_at[:19]}"
            ):

                st.write(memory.content)

                st.caption(f"ID : {memory.id}")

                if memory.tags:

                    st.write("**Tags:** " + ", ".join(memory.tags))

                if memory.metadata:

                    st.json(memory.metadata)

                col1, col2, col3, col4 = st.columns(4)

                # ==========================================
                # FAVORITE
                # ==========================================

                with col1:

                    if memory.favorite:

                        if st.button(
                            "⭐ Unfavorite",
                            key=f"fav_{memory.id}",
                        ):

                            self.agent.unfavorite(memory.id)

                            notifications.success(
                                "Memory",
                                "Removed from favorites.",
                            )

                            st.rerun()

                    else:

                        if st.button(
                            "☆ Favorite",
                            key=f"fav_{memory.id}",
                        ):

                            self.agent.favorite(memory.id)

                            notifications.success(
                                "Memory",
                                "Added to favorites.",
                            )

                            st.rerun()

                # ==========================================
                # ARCHIVE
                # ==========================================

                with col2:

                    if memory.archived:

                        if st.button(
                            "Restore",
                            key=f"restore_{memory.id}",
                        ):

                            self.agent.restore(memory.id)

                            notifications.success(
                                "Memory",
                                "Memory restored.",
                            )

                            st.rerun()

                    else:

                        if st.button(
                            "Archive",
                            key=f"archive_{memory.id}",
                        ):

                            self.agent.archive(memory.id)

                            notifications.success(
                                "Memory",
                                "Memory archived.",
                            )

                            st.rerun()

                # ==========================================
                # DELETE
                # ==========================================

                with col3:

                    if st.button(
                        "Delete",
                        key=f"delete_{memory.id}",
                    ):

                        self.agent.delete(memory.id)

                        notifications.success(
                            "Memory",
                            "Memory deleted.",
                        )

                        st.rerun()

                # ==========================================
                # VIEW JSON
                # ==========================================

                with col4:

                    if st.button(
                        "View JSON",
                        key=f"json_{memory.id}",
                    ):

                        st.json(memory.to_dict())

        # ==============================================
        # EXPORT
        # ==============================================

        if export:

            st.download_button(
                label="📥 Download Memory JSON",
                data=json.dumps(
                    exported_data,
                    indent=4,
                ),
                file_name="memory_export.json",
                mime="application/json",
            )
    # =====================================================
    # STATISTICS
    # =====================================================

    def render_statistics(self):

        stats = self.agent.statistics()

        st.subheader("📊 Memory Statistics")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Total Memories",
            stats.total_memories,
        )

        col2.metric(
            "Active",
            stats.active_memories,
        )

        col3.metric(
            "Archived",
            stats.archived_memories,
        )

        col4, col5, col6 = st.columns(3)

        col4.metric(
            "Favorites",
            stats.favorite_memories,
        )

        col5.metric(
            "Categories",
            stats.total_categories,
        )

        col6.metric(
            "Preferences",
            stats.total_preferences,
        )

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

        self.render_header(
            config["model"],
        )

        query, category = self.render_filters()

        refresh, export = self.render_actions()

        if refresh:

            st.rerun()

        memories = self.load_memories(
            query=query,
            category=category,
        )

        st.divider()

        self.render_memory_table(
            memories,
            export,
        )

        st.divider()

        self.render_statistics()

        st.divider()

        self.render_footer()


# ==========================================================
# GLOBAL PAGE
# ==========================================================

memory_page = MemoryPage()


def main():

    memory_page.render()


if __name__ == "__main__":

    main()
