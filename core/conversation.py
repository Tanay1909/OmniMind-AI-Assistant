
"""
=========================================================
OmniMind AI Assistant
Conversation Manager
=========================================================

Orchestrates the complete conversation lifecycle.

Responsibilities:
- Accept user messages
- Update memory
- Build LLM context
- Call the selected AI model
- Store responses
- Save conversation history
"""

from __future__ import annotations

from typing import Protocol

from core.context import ContextBuilder
from core.history import HistoryManager
from core.memory import MemoryManager
from core.session import SessionManager


# ==========================================================
# LLM PROVIDER INTERFACE
# ==========================================================

class LLMProvider(Protocol):
    """
    Every AI provider should implement this interface.
    """

    def generate(
        self,
        messages: list[dict[str, str]],
        **kwargs,
    ) -> str:
        ...


# ==========================================================
# CONVERSATION MANAGER
# ==========================================================

class ConversationManager:
    """
    Handles the conversation workflow.
    """

    def __init__(
        self,
        llm: LLMProvider,
        memory: MemoryManager,
        history: HistoryManager,
        context_builder: ContextBuilder,
    ):

        self.llm = llm
        self.memory = memory
        self.history = history
        self.context_builder = context_builder

        SessionManager.initialize()

    # =====================================================
    # START CHAT
    # =====================================================

    def start_chat(
        self,
        title: str = "New Chat",
    ):

        chat = self.history.create_chat(title)

        SessionManager.set(
            "current_chat",
            chat.id,
        )

        self.memory.clear_memory()

        return chat

    # =====================================================
    # SEND MESSAGE
    # =====================================================

    def send_message(
        self,
        prompt: str,
    ) -> str:

        # Save user message
        self.memory.add_message(
            "user",
            prompt,
        )

        # Build context
        self.context_builder.set_conversation(
            self.memory.build_context()
        )

        messages = self.context_builder.to_messages()

        # Generate AI response
        response = self.llm.generate(messages)

        # Save assistant response
        self.memory.add_message(
            "assistant",
            response,
        )

        # Persist chat
        conversation_id = SessionManager.get(
            "current_chat"
        )

        if conversation_id:

            self.history.append_message(
                conversation_id,
                "user",
                prompt,
            )

            self.history.append_message(
                conversation_id,
                "assistant",
                response,
            )

        return response

    # =====================================================
    # HISTORY
    # =====================================================

    def list_chats(self):

        return self.history.list_chats()

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

    # =====================================================
    # RESET
    # =====================================================

    def clear(self):

        self.memory.clear_memory()

        self.context_builder = ContextBuilder()

        SessionManager.set(
            "current_chat",
            None,
        )

