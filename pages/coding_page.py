"""
=========================================================
OmniMind AI Assistant
Coding Page
=========================================================

AI Software Engineering Workspace
"""

from __future__ import annotations

import streamlit as st

from agents.base_agent import AgentRequest
from agents.coding_agent import CodingAgent

from components.footer import footer
from components.navbar import navbar
from components.notifications import notifications
from components.sidebar import sidebar

from core.prompt_manager import PromptManager

from services.groq_service import GroqService


class CodingPage:
    """
    AI Coding Workspace.
    """

    def __init__(self) -> None:

        self.llm = GroqService()

        self.prompt_manager = PromptManager()

        self.agent = CodingAgent(
            llm=self.llm,
            prompt_manager=self.prompt_manager,
        )

    # =====================================================
    # PAGE CONFIG
    # =====================================================

    def configure(self) -> None:

        st.set_page_config(
            page_title="Coding",
            page_icon="💻",
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
    ) -> None:

        navbar.render(
            page_title="💻 AI Coding Assistant",
            model_name=model,
        )

    # =====================================================
    # INPUT PANEL
    # =====================================================

    def input_panel(self) -> dict:

        language = st.selectbox(
            "Programming Language",
            [
                "Python",
                "Java",
                "C++",
                "JavaScript",
                "Go",
                "Rust",
                "SQL",
            ],
        )

        task = st.selectbox(
            "Task",
            [
                "Generate Code",
                "Explain Code",
                "Debug Code",
                "Optimize Code",
                "Generate Documentation",
                "Generate Unit Tests",
            ],
        )

        prompt = st.text_area(
            "Prompt / Source Code",
            height=300,
            placeholder="Describe your coding task or paste your code...",
        )

        return {
            "language": language,
            "task": task,
            "prompt": prompt,
        }

    # =====================================================
    # ACTIONS
    # =====================================================

    def actions(self) -> dict:

        col1, col2 = st.columns(2)

        with col1:

            run = st.button(
                "🚀 Run",
                use_container_width=True,
            )

        with col2:

            clear = st.button(
                "🗑 Clear",
                use_container_width=True,
            )

        return {
            "run": run,
            "clear": clear,
        }

    # =====================================================
    # EXECUTE
    # =====================================================

    def execute(
        self,
        data: dict,
        actions: dict,
    ) -> None:

        if actions["clear"]:

            st.session_state.pop(
                "coding_result",
                None,
            )

            st.rerun()

        if not actions["run"]:
            return

        if not data["prompt"].strip():

            notifications.warning(
                "Coding",
                "Please enter a prompt.",
            )

            return

        task_map = {
            "Generate Code": "generate",
            "Explain Code": "explain",
            "Debug Code": "debug",
            "Optimize Code": "refactor",
            "Generate Documentation": "document",
            "Generate Unit Tests": "test",
        }

        request = AgentRequest(
            query=data["prompt"],
            context={
                "task": task_map[data["task"]],
                "language": data["language"],
            },
        )

        with st.spinner("Groq is generating your code..."):

            response = self.agent.run(request)

        if response.success:

            st.session_state["coding_result"] = response.output

            notifications.success(
                "Coding",
                "Task completed successfully.",
            )

        else:

            notifications.error(
                "Coding",
                response.error,
            )

    # =====================================================
    # OUTPUT
    # =====================================================

    def output(self) -> None:

        result = st.session_state.get("coding_result")

        if not result:
            return

        st.subheader("AI Response")

        st.code(
            result,
            language="python",
        )

        st.download_button(
            label="📥 Download Result",
            data=result,
            file_name="coding_result.txt",
            mime="text/plain",
            use_container_width=True,
        )

    # =====================================================
    # FOOTER
    # =====================================================

    def render_footer(self) -> None:

        footer.render()

    # =====================================================
    # MAIN
    # =====================================================

    def render(self) -> None:

        self.configure()

        config = self.render_sidebar()

        self.render_header(config["model"])

        data = self.input_panel()

        actions = self.actions()

        st.divider()

        self.execute(
            data,
            actions,
        )

        self.output()

        st.divider()

        self.render_footer()


coding_page = CodingPage()


def main() -> None:

    coding_page.render()


if __name__ == "__main__":
    main()
