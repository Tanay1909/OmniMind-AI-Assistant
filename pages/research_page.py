"""
=========================================================
OmniMind AI Assistant
Research Page
=========================================================

AI-powered research workspace with:

• Web Search
• AI Summarization
• Source Comparison
• Report Generation
• Question Answering
"""

from __future__ import annotations

import streamlit as st

from agents.research_agent import ResearchAgent

from components.footer import footer
from components.navbar import navbar
from components.notifications import notifications
from components.sidebar import sidebar


class ResearchPage:
    """
    AI Research Workspace.
    """

    def __init__(self):

        self.agent = ResearchAgent()

    # =====================================================
    # PAGE CONFIG
    # =====================================================

    def configure(self):

        st.set_page_config(
            page_title="Research",
            page_icon="🔬",
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
            page_title="🔬 AI Research",
            model_name=model,
        )

    # =====================================================
    # SEARCH
    # =====================================================

    def search_box(self):

        return st.text_input(
            "Research Topic",
            placeholder=("Example: Explain Retrieval-Augmented Generation"),
        )

    # =====================================================
    # OPTIONS
    # =====================================================

    def options(self):

        col1, col2, col3 = st.columns(3)

        with col1:

            max_results = st.slider(
                "Sources",
                3,
                15,
                5,
            )

        with col2:

            summarize = st.checkbox(
                "Summarize",
                value=True,
            )

        with col3:

            export = st.checkbox(
                "Enable Export",
                value=False,
            )

        return {
            "max_results": max_results,
            "summarize": summarize,
            "export": export,
        }

    # =====================================================
    # ACTION BUTTONS
    # =====================================================

    def actions(self):

        col1, col2 = st.columns(2)

        with col1:

            research = st.button(
                "🚀 Start Research",
                use_container_width=True,
            )

        with col2:

            clear = st.button(
                "🗑 Clear",
                use_container_width=True,
            )

        return {
            "research": research,
            "clear": clear,
        }

    # =====================================================
    # RESULTS
    # =====================================================

    def results(
        self,
        query,
        options,
        actions,
    ):

        if actions["clear"]:

            st.session_state.pop(
                "research_results",
                None,
            )

            st.rerun()

        if not actions["research"]:

            return

        if not query.strip():

            notifications.warning(
                "Research",
                "Please enter a topic.",
            )

            return

        with st.spinner("Researching..."):

            result = self.agent.research(
                query=query,
                max_results=options["max_results"],
                summarize=options["summarize"],
            )

        st.session_state["research_results"] = result

        notifications.success(
            "Research",
            "Research completed.",
        )

        self.display(result)

    # =====================================================
    # DISPLAY
    # =====================================================

    def display(
        self,
        result,
    ):

        if not result:

            return

        st.subheader("Summary")

        st.write(
            result.get(
                "summary",
                "",
            )
        )

        st.divider()

        st.subheader("Key Findings")

        findings = result.get(
            "findings",
            [],
        )

        for item in findings:

            st.markdown(f"- {item}")

        st.divider()

        st.subheader("Sources")

        for source in result.get(
            "sources",
            [],
        ):

            with st.expander(
                source.get(
                    "title",
                    "Source",
                )
            ):

                st.write(
                    source.get(
                        "url",
                        "",
                    )
                )

                st.write(
                    source.get(
                        "snippet",
                        "",
                    )
                )

    # =====================================================
    # FOOTER
    # =====================================================

    def render_footer(self):

        footer.render()

    # =====================================================
    # MAIN
    # =====================================================

    def render(self):

        self.configure()

        config = self.render_sidebar()

        self.render_header(config["model"])

        query = self.search_box()

        options = self.options()

        actions = self.actions()

        st.divider()

        self.results(
            query,
            options,
            actions,
        )

        if "research_results" in st.session_state:

            st.divider()

            self.display(st.session_state["research_results"])

        st.divider()

        self.render_footer()


research_page = ResearchPage()


def main():

    research_page.render()


if __name__ == "__main__":

    main()
