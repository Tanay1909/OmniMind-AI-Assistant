
"""
=========================================================
OmniMind AI Assistant
Assistant Facade
=========================================================

Main entry point for the entire AI assistant.

Coordinates:
- Router
- Planner
- Workflow Engine
- Memory
- History
- Context Builder
- Prompt Manager
"""

from __future__ import annotations

from typing import Any

from core.context import ContextBuilder
from core.history import HistoryManager
from core.memory import MemoryManager
from core.planner import Planner
from core.prompt_manager import PromptManager
from core.reasoning import ReasoningEngine
from core.router import Router
from core.session import SessionManager
from core.tool_executor import ToolExecutor
from core.workflow import WorkflowEngine


class OmniMindAssistant:
    """
    Main application facade.

    This is the only class the UI should interact with.
    """

    def __init__(
        self,
        workflow: WorkflowEngine,
        tool_executor: ToolExecutor,
    ) -> None:

        self.router = Router()

        self.planner = Planner()

        self.reasoning = ReasoningEngine()

        self.memory = MemoryManager()

        self.history = HistoryManager()

        self.context = ContextBuilder()

        self.prompts = PromptManager()

        self.session = SessionManager()

        self.workflow = workflow

        self.tool_executor = tool_executor

        SessionManager.initialize()

    # =====================================================
    # CHAT
    # =====================================================

    def chat(
        self,
        prompt: str,
    ):
        """
        Main assistant entry point.
        """

        # ----------------------------
        # Save user message
        # ----------------------------

        self.memory.add_message(
            "user",
            prompt,
        )

        # ----------------------------
        # Routing
        # ----------------------------

        route = self.router.route(
            prompt
        )

        # ----------------------------
        # Planning
        # ----------------------------

        plan = self.planner.create_plan(
            prompt
        )

        # ----------------------------
        # Context
        # ----------------------------

        self.context.set_system_prompt(
            self.prompts.system_prompt()
        )

        self.context.set_conversation(
            self.memory.build_context()
        )

        self.context.set_preferences(
            self.memory.get_all_preferences()
        )

        messages = self.context.to_messages()

        # ----------------------------
        # Workflow
        # ----------------------------

        result = self.workflow.execute(
            plan=plan,
            messages=messages,
        )

        # ----------------------------
        # Save assistant response
        # ----------------------------

        if result.response:

            self.memory.add_message(
                "assistant",
                result.response.content,
            )

        return result

    # =====================================================
    # HISTORY
    # =====================================================

    def new_chat(
        self,
        title: str = "New Chat",
    ):

        self.memory.clear_memory()

        return self.history.create_chat(
            title
        )

    def load_chat(
        self,
        conversation_id: str,
    ):

        return self.history.load_chat(
            conversation_id
        )

    def delete_chat(
        self,
        conversation_id: str,
    ):

        self.history.delete_chat(
            conversation_id
        )

    def list_chats(self):

        return self.history.list_chats()

    # =====================================================
    # FILES
    # =====================================================

    def upload(
        self,
        filename: str,
    ):

        SessionManager.add_uploaded_file(
            filename
        )

    # =====================================================
    # SETTINGS
    # =====================================================

    def set_model(
        self,
        model: str,
    ):

        SessionManager.set_model(
            model
        )

    def set_temperature(
        self,
        value: float,
    ):

        SessionManager.set_temperature(
            value
        )

    # =====================================================
    # MEMORY
    # =====================================================

    def clear_chat(self):

        self.memory.clear_memory()

    # =====================================================
    # STATUS
    # =====================================================

    def info(self) -> dict[str, Any]:

        return {

            "messages":
                self.memory.message_count(),

            "preferences":
                len(
                    self.memory.get_all_preferences()
                ),

            "history":
                len(
                    self.history.list_chats()
                ),
        }
