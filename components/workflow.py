"""
=========================================================
OmniMind AI Assistant
Workflow Component
=========================================================

Visual workflow execution interface.

Connects:

Planner
    ↓
ExecutionPlan
    ↓
WorkflowEngine
    ↓
ReasoningEngine
    ↓
ToolExecutor
    ↓
LLM

This component is compatible with the current
core.workflow architecture.
"""

from __future__ import annotations

import time

import streamlit as st

from core.planner import Planner
from core.reasoning import ReasoningEngine
from core.tool_executor import ToolExecutor
from core.workflow import WorkflowEngine, WorkflowResult

from services.gemini_service import GeminiService
from services.llm_service import LLMRequest

# ==========================================================
# LLM ADAPTER
# ==========================================================


class WorkflowLLMAdapter:
    """
    Adapter between WorkflowEngine and BaseLLMService.

    WorkflowEngine expects:

        generate(messages)

    OmniMind LLM services expect:

        generate(LLMRequest)
    """

    def __init__(self) -> None:

        self.provider = GeminiService()

    # ------------------------------------------------------

    def generate(
        self,
        messages: list[dict[str, str]],
        **kwargs,
    ):

        request = LLMRequest(
            model=kwargs.get(
                "model",
                GeminiService.DEFAULT_MODEL,
            ),
            messages=messages,
            temperature=kwargs.get(
                "temperature",
                0.7,
            ),
            max_tokens=kwargs.get(
                "max_tokens",
                2048,
            ),
        )

        return self.provider.generate(request)


# ==========================================================
# WORKFLOW COMPONENT
# ==========================================================


class WorkflowComponent:
    """
    Workflow execution UI.
    """

    def __init__(self) -> None:

        # --------------------------------------------------
        # Core services
        # --------------------------------------------------

        self.planner = Planner()

        self.reasoning = ReasoningEngine()

        self.tool_executor = ToolExecutor()

        self.llm = WorkflowLLMAdapter()

        # --------------------------------------------------
        # Workflow engine
        # --------------------------------------------------

        self.engine = WorkflowEngine(
            tool_executor=self.tool_executor,
            reasoning=self.reasoning,
            llm=self.llm,
        )

        # --------------------------------------------------
        # History
        # --------------------------------------------------

        if "workflow_history" not in st.session_state:

            st.session_state["workflow_history"] = []

    # ======================================================
    # HEADER
    # ======================================================

    def render_header(self) -> None:

        st.header("⚡ Workflow Engine")

        st.caption("Plan, execute, monitor and manage AI workflows.")

    # ======================================================
    # WORKFLOW INFORMATION
    # ======================================================

    def workflow_information(self) -> None:

        with st.expander(
            "ℹ️ How Workflow Engine Works",
            expanded=False,
        ):

            st.markdown("""
                **Workflow execution pipeline**

                1. User enters a task.
                2. Planner creates an execution plan.
                3. Reasoning engine selects a strategy.
                4. Workflow engine executes each step.
                5. Tools are called when required.
                6. Gemini generates the final response.
                7. Results are displayed below.
                """)

    # ======================================================
    # PROMPT
    # ======================================================

    def workflow_parameters(self) -> dict:

        st.subheader("Workflow Input")

        prompt = st.text_area(
            "Prompt",
            placeholder=("Example: Explain how machine learning works."),
            height=160,
        )

        return {
            "prompt": prompt,
        }

    # ======================================================
    # PLAN PREVIEW
    # ======================================================

    def show_plan(
        self,
        prompt: str,
    ):

        if not prompt.strip():

            return None

        plan = self.planner.create_plan(prompt.strip())

        with st.expander(
            "🔎 Execution Plan",
            expanded=True,
        ):

            for step in plan.steps:

                st.markdown(f"**{step.id}. {step.name}**")

                st.caption(f"Type: `{step.step_type.value}`")

                st.write(step.description)

                if step.tool:

                    st.caption(f"Tool: `{step.tool}`")

        return plan

    # ======================================================
    # EXECUTION
    # ======================================================

    def execute(
        self,
        prompt: str,
    ) -> WorkflowResult | None:

        if not prompt.strip():

            st.warning("Please enter a workflow prompt.")

            return None

        # --------------------------------------------------
        # Create plan
        # --------------------------------------------------

        plan = self.planner.create_plan(prompt.strip())

        # --------------------------------------------------
        # Prepare messages
        # --------------------------------------------------

        messages = [
            {
                "role": "user",
                "content": prompt.strip(),
            }
        ]

        # --------------------------------------------------
        # Execute
        # --------------------------------------------------

        start = time.perf_counter()

        with st.spinner("Executing workflow..."):

            result = self.engine.execute(
                plan=plan,
                messages=messages,
            )

        duration = time.perf_counter() - start

        # --------------------------------------------------
        # History
        # --------------------------------------------------

        history_item = {
            "prompt": prompt,
            "success": result.success,
            "duration": duration,
            "steps": list(result.executed_steps),
            "error": result.error,
        }

        st.session_state["workflow_history"].append(history_item)

        return result

    # ======================================================
    # RESULT
    # ======================================================

    def show_result(
        self,
        result: WorkflowResult,
    ) -> None:

        st.subheader("Result")

        # --------------------------------------------------
        # Failure
        # --------------------------------------------------

        if not result.success:

            st.error(result.error or "Workflow execution failed.")

            return

        # --------------------------------------------------
        # LLM response
        # --------------------------------------------------

        if result.response:

            response_text = result.response.content

            st.markdown(response_text)

        else:

            st.info("Workflow completed without a final response.")

        # --------------------------------------------------
        # Executed steps
        # --------------------------------------------------

        st.divider()

        st.subheader("Executed Steps")

        for step in result.executed_steps:

            st.markdown(f"✓ {step}")

        # --------------------------------------------------
        # Tool results
        # --------------------------------------------------

        if result.tool_results:

            st.divider()

            st.subheader("Tool Results")

            for name, tool_result in result.tool_results.items():

                with st.expander(name):

                    if tool_result.success:

                        st.write(tool_result.data)

                        st.caption(
                            f"Execution time: " f"{tool_result.execution_time:.3f}s"
                        )

                    else:

                        st.error(tool_result.error or "Tool execution failed.")

        # --------------------------------------------------
        # Metadata
        # --------------------------------------------------

        if result.metadata:

            with st.expander("Workflow Metadata"):

                st.json(result.metadata)

    # ======================================================
    # HISTORY
    # ======================================================

    def execution_history(self) -> None:

        st.subheader("Execution History")

        history = st.session_state.get(
            "workflow_history",
            [],
        )

        if not history:

            st.info("No workflow executions yet.")

            return

        for index, execution in enumerate(
            reversed(history),
            start=1,
        ):

            status = "✅ Success" if execution["success"] else "❌ Failed"

            with st.expander(f"{status} — " f"{execution['prompt'][:60]}"):

                st.write(f"**Prompt:** " f"{execution['prompt']}")

                st.write(f"**Duration:** " f"{execution['duration']:.2f}s")

                st.write("**Steps:**")

                for step in execution["steps"]:

                    st.markdown(f"- {step}")

                if execution["error"]:

                    st.error(execution["error"])

    # ======================================================
    # CLEAR
    # ======================================================

    def clear_history(self) -> None:

        if st.button(
            "🗑 Clear Workflow History",
            use_container_width=True,
        ):

            st.session_state["workflow_history"] = []

            st.rerun()

    # ======================================================
    # MAIN
    # ======================================================

    def render(self) -> None:

        self.render_header()

        self.workflow_information()

        parameters = self.workflow_parameters()

        prompt = parameters["prompt"]

        st.divider()

        # --------------------------------------------------
        # Plan preview
        # --------------------------------------------------

        if prompt.strip():

            self.show_plan(prompt)

        st.divider()

        # --------------------------------------------------
        # Actions
        # --------------------------------------------------

        col1, col2 = st.columns(2)

        with col1:

            execute_clicked = st.button(
                "▶ Execute Workflow",
                use_container_width=True,
                type="primary",
            )

        with col2:

            clear_clicked = st.button(
                "🗑 Clear History",
                use_container_width=True,
            )

        # --------------------------------------------------
        # Clear
        # --------------------------------------------------

        if clear_clicked:

            st.session_state["workflow_history"] = []

            st.rerun()

        # --------------------------------------------------
        # Execute
        # --------------------------------------------------

        if execute_clicked:

            result = self.execute(prompt)

            if result:

                if result.success:

                    st.success("Workflow completed successfully.")

                self.show_result(result)

        # --------------------------------------------------
        # History
        # --------------------------------------------------

        st.divider()

        self.execution_history()


# ==========================================================
# GLOBAL INSTANCE
# ==========================================================


workflow_component = WorkflowComponent()
