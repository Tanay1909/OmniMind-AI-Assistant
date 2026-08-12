"""
=========================================================
OmniMind AI Assistant
Workflow Manager Page
=========================================================

Enterprise AI Workflow Manager

Features
--------
- Create Workflow
- Plan Workflow
- Execute Workflow
- Monitor Progress
- Workflow History
- Export Results
"""

from __future__ import annotations

import json
from dataclasses import asdict, is_dataclass
from typing import Any

import streamlit as st

from components.footer import footer
from components.navbar import navbar
from components.notifications import notifications
from components.sidebar import sidebar
from components.workflow import workflow_component


class WorkflowPage:
    """
    Workflow Management Dashboard.

    Uses the centralized WorkflowComponent so that
    Planner, ReasoningEngine, ToolExecutor and LLM
    are initialized consistently.
    """

    def __init__(self) -> None:

        # -------------------------------------------------
        # Use the already configured workflow component.
        # -------------------------------------------------

        self.workflow_component = workflow_component

        self.engine = workflow_component.engine

        self.planner = workflow_component.planner

    # =====================================================
    # CONFIG
    # =====================================================

    def configure(self) -> None:

        st.set_page_config(
            page_title="Workflow",
            page_icon="⚙️",
            layout="wide",
            initial_sidebar_state="expanded",
        )

    # =====================================================
    # SIDEBAR
    # =====================================================

    def render_sidebar(self) -> dict[str, Any]:

        return sidebar.render()

    # =====================================================
    # HEADER
    # =====================================================

    def render_header(
        self,
        model: str,
    ) -> None:

        navbar.render(
            page_title="⚙️ Workflow Manager",
            model_name=model,
        )

    # =====================================================
    # WORKFLOW CONFIGURATION
    # =====================================================

    def workflow_configuration(self) -> dict[str, str]:

        st.subheader("Workflow Configuration")

        workflow_name = st.text_input(
            "Workflow Name",
            placeholder="Example: Research Pipeline",
        )

        workflow_type = st.selectbox(
            "Workflow Type",
            [
                "Research",
                "Coding",
                "Document Analysis",
                "Vision",
                "Speech",
                "Custom",
            ],
        )

        prompt = st.text_area(
            "Workflow Prompt",
            placeholder=(
                "Example: Research the latest developments "
                "in artificial intelligence and summarize them."
            ),
            height=160,
        )

        description = st.text_area(
            "Description",
            height=100,
            placeholder=("Describe what this workflow should accomplish."),
        )

        return {
            "name": workflow_name.strip(),
            "type": workflow_type,
            "prompt": prompt.strip(),
            "description": description.strip(),
        }

    # =====================================================
    # ACTIONS
    # =====================================================

    def actions(self) -> dict[str, bool]:

        col1, col2, col3 = st.columns(3)

        with col1:

            plan = st.button(
                "📝 Plan",
                use_container_width=True,
            )

        with col2:

            execute = st.button(
                "▶ Execute",
                use_container_width=True,
                type="primary",
            )

        with col3:

            clear = st.button(
                "🗑 Clear",
                use_container_width=True,
            )

        return {
            "plan": plan,
            "execute": execute,
            "clear": clear,
        }

    # =====================================================
    # CREATE PLAN
    # =====================================================

    def create_plan(
        self,
        workflow: dict[str, str],
    ):

        prompt = workflow.get(
            "prompt",
            "",
        ).strip()

        if not prompt:

            notifications.warning(
                "Planner",
                "Please enter a workflow prompt.",
            )

            return None

        try:

            plan = self.planner.create_plan(prompt)

            st.session_state["workflow_plan"] = plan

            notifications.success(
                "Planner",
                "Workflow planned successfully.",
            )

            return plan

        except Exception as exc:

            notifications.error(
                "Planner",
                str(exc),
            )

            return None

    # =====================================================
    # EXECUTE WORKFLOW
    # =====================================================

    def execute_workflow(
        self,
        workflow: dict[str, str],
    ):

        prompt = workflow.get(
            "prompt",
            "",
        ).strip()

        if not prompt:

            notifications.warning(
                "Workflow",
                "Please enter a workflow prompt.",
            )

            return None

        try:

            # ---------------------------------------------
            # Create execution plan
            # ---------------------------------------------

            plan = self.planner.create_plan(prompt)

            st.session_state["workflow_plan"] = plan

            # ---------------------------------------------
            # Messages expected by WorkflowEngine
            # ---------------------------------------------

            messages = [
                {
                    "role": "user",
                    "content": prompt,
                }
            ]

            # ---------------------------------------------
            # Execute
            # ---------------------------------------------

            with st.spinner("Executing workflow..."):

                result = self.engine.execute(
                    plan=plan,
                    messages=messages,
                )

            # ---------------------------------------------
            # Save result
            # ---------------------------------------------

            st.session_state["workflow_result"] = result

            if result.success:

                notifications.success(
                    "Workflow",
                    "Execution completed successfully.",
                )

            else:

                notifications.error(
                    "Workflow",
                    result.error or "Workflow execution failed.",
                )

            return result

        except Exception as exc:

            notifications.error(
                "Workflow",
                str(exc),
            )

            return None

    # =====================================================
    # HANDLE ACTIONS
    # =====================================================

    def handle_actions(
        self,
        workflow: dict[str, str],
        actions: dict[str, bool],
    ) -> None:

        # -------------------------------------------------
        # CLEAR
        # -------------------------------------------------

        if actions["clear"]:

            st.session_state.pop(
                "workflow_plan",
                None,
            )

            st.session_state.pop(
                "workflow_result",
                None,
            )

            notifications.info(
                "Workflow",
                "Workspace cleared.",
            )

            st.rerun()

        # -------------------------------------------------
        # PLAN
        # -------------------------------------------------

        if actions["plan"]:

            self.create_plan(workflow)

        # -------------------------------------------------
        # EXECUTE
        # -------------------------------------------------

        if actions["execute"]:

            self.execute_workflow(workflow)

    # =====================================================
    # CONVERT OBJECT TO JSON
    # =====================================================

    @staticmethod
    def serialize(
        value: Any,
    ) -> Any:
        """
        Convert OmniMind dataclasses and nested objects
        into JSON-compatible structures.
        """

        if is_dataclass(value):

            return asdict(value)

        if isinstance(
            value,
            dict,
        ):

            return {
                str(key): WorkflowPage.serialize(item) for key, item in value.items()
            }

        if isinstance(
            value,
            (list, tuple),
        ):

            return [WorkflowPage.serialize(item) for item in value]

        if hasattr(
            value,
            "value",
        ):

            return value.value

        return value

    # =====================================================
    # DISPLAY PLAN
    # =====================================================

    def display_plan(
        self,
    ) -> None:

        plan = st.session_state.get("workflow_plan")

        if plan is None:

            return

        st.divider()

        st.subheader("📝 Workflow Plan")

        st.write(f"**Request:** {plan.user_request}")

        if not plan.steps:

            st.info("No execution steps were created.")

            return

        for step in plan.steps:

            with st.expander(
                f"{step.id}. {step.name}",
                expanded=True,
            ):

                st.write(step.description)

                st.caption(f"Type: `{step.step_type.value}`")

                if step.tool:

                    st.caption(f"Tool: `{step.tool}`")

                if step.parameters:

                    st.json(step.parameters)

    # =====================================================
    # DISPLAY RESULT
    # =====================================================

    def display_result(
        self,
    ) -> None:

        result = st.session_state.get("workflow_result")

        if result is None:

            return

        st.divider()

        st.subheader("⚡ Execution Result")

        # -------------------------------------------------
        # Status
        # -------------------------------------------------

        if result.success:

            st.success("Workflow completed successfully.")

        else:

            st.error(result.error or "Workflow execution failed.")

        # -------------------------------------------------
        # AI response
        # -------------------------------------------------

        if result.response:

            st.markdown("### 🤖 AI Response")

            st.write(result.response.content)

        # -------------------------------------------------
        # Executed steps
        # -------------------------------------------------

        if result.executed_steps:

            st.markdown("### 🔄 Executed Steps")

            for step in result.executed_steps:

                st.markdown(f"✓ {step}")

        # -------------------------------------------------
        # Tool results
        # -------------------------------------------------

        if result.tool_results:

            st.markdown("### 🔧 Tool Results")

            for (
                tool_name,
                tool_result,
            ) in result.tool_results.items():

                with st.expander(tool_name):

                    if tool_result.success:

                        st.write(tool_result.data)

                        st.caption(
                            f"Execution time: " f"{tool_result.execution_time:.3f}s"
                        )

                    else:

                        st.error(tool_result.error or "Tool failed.")

        # -------------------------------------------------
        # Metadata
        # -------------------------------------------------

        if result.metadata:

            with st.expander("Workflow Metadata"):

                st.json(self.serialize(result.metadata))

    # =====================================================
    # HISTORY
    # =====================================================

    def history(self) -> None:

        st.divider()

        st.subheader("📚 Workflow History")

        history = st.session_state.get(
            "workflow_history",
            [],
        )

        if not history:

            st.info("No workflow history available.")

            return

        for index, item in enumerate(
            reversed(history),
            start=1,
        ):

            status = "✅ Success" if item.get("success") else "❌ Failed"

            prompt = item.get(
                "prompt",
                "Workflow",
            )

            with st.expander(f"{status} — {prompt[:70]}"):

                st.write(f"**Prompt:** {prompt}")

                st.write(f"**Duration:** " f"{item.get('duration', 0):.2f}s")

                steps = item.get(
                    "steps",
                    [],
                )

                if steps:

                    st.write("**Steps:**")

                    for step in steps:

                        st.markdown(f"- {step}")

                if item.get("error"):

                    st.error(item["error"])

    # =====================================================
    # EXPORT
    # =====================================================

    def export(self) -> None:

        result = st.session_state.get("workflow_result")

        if result is None:

            return

        st.divider()

        st.subheader("📤 Export")

        exported = json.dumps(
            self.serialize(result),
            indent=4,
            default=str,
        )

        st.download_button(
            "📥 Download Workflow Result",
            exported,
            file_name="workflow_result.json",
            mime="application/json",
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

        workflow = self.workflow_configuration()

        actions = self.actions()

        st.divider()

        self.handle_actions(
            workflow,
            actions,
        )

        self.display_plan()

        self.display_result()

        self.history()

        self.export()

        st.divider()

        self.render_footer()


# ==========================================================
# GLOBAL INSTANCE
# ==========================================================

workflow_page = WorkflowPage()


# ==========================================================
# MAIN
# ==========================================================


def main() -> None:

    workflow_page.render()


if __name__ == "__main__":

    main()
