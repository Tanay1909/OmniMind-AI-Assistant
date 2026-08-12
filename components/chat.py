"""
=========================================================
OmniMind AI Assistant
Reusable Streamlit Chat Interface
=========================================================
"""

from __future__ import annotations

from typing import Iterable

import streamlit as st

from agents.base_agent import AgentRequest
from agents.chat_agent import ChatAgent

from models.chat import (
    ChatMessage,
    MessageRole,
)

from core.prompt_manager import PromptManager
from core.memory import MemoryManager
from core.history import HistoryManager
from core.context import ContextBuilder
from core.analytics import analytics

from services.analytics_service import AnalyticsService
from services.gemini_service import GeminiService


class ChatComponent:
    """
    Reusable Streamlit Chat UI.
    """

    def __init__(self) -> None:

        # =================================================
        # CORE COMPONENTS
        # =================================================

        self.prompt_manager = PromptManager()

        self.memory = MemoryManager()

        self.history = HistoryManager()

        self.context_builder = ContextBuilder()

        # =================================================
        # ANALYTICS
        # =================================================
        # IMPORTANT:
        # Use the GLOBAL AnalyticsManager instance.
        #
        # AnalyticsPage also reads this same instance,
        # so Chat metrics will appear in the dashboard.

        self.analytics = AnalyticsService(analytics)

        # =================================================
        # LLM
        # =================================================

        self.llm = GeminiService()

        # =================================================
        # CHAT AGENT
        # =================================================

        self.agent = ChatAgent(
            llm=self.llm,
            prompt_manager=self.prompt_manager,
            memory=self.memory,
            history=self.history,
            context_builder=self.context_builder,
            analytics=self.analytics,
        )

    # =====================================================
    # INITIALIZE
    # =====================================================

    def initialize(self) -> None:

        if "messages" not in st.session_state:

            st.session_state.messages = []

        if "message_count" not in st.session_state:

            st.session_state.message_count = 0

    # =====================================================
    # RENDER HISTORY
    # =====================================================

    def render_history(
        self,
        messages: Iterable[ChatMessage] | None = None,
    ) -> None:

        messages = messages or st.session_state.messages

        for message in messages:

            self.render_message(message)

    # =====================================================
    # RENDER MESSAGE
    # =====================================================

    def render_message(
        self,
        message: ChatMessage,
    ) -> None:

        role = "assistant" if message.role == MessageRole.ASSISTANT else "user"

        with st.chat_message(role):

            st.markdown(message.content)

    # =====================================================
    # CHAT INPUT
    # =====================================================

    def chat_input(self) -> str | None:

        return st.chat_input("Ask OmniMind anything...")

    # =====================================================
    # SEND MESSAGE
    # =====================================================

    def send(
        self,
        prompt: str,
    ) -> None:

        # =================================================
        # USER MESSAGE
        # =================================================

        user_message = ChatMessage(
            role=MessageRole.USER,
            content=prompt,
        )

        st.session_state.messages.append(user_message)

        st.session_state.message_count += 1

        self.render_message(user_message)

        # =================================================
        # ASSISTANT RESPONSE
        # =================================================

        with st.chat_message("assistant"):

            placeholder = st.empty()

            with st.spinner("Gemini is thinking..."):

                response = self.agent.run(
                    AgentRequest(
                        query=prompt,
                    )
                )

            # ---------------------------------------------
            # SUCCESS
            # ---------------------------------------------

            if response.success:

                placeholder.markdown(response.output)

                assistant_message = ChatMessage(
                    role=MessageRole.ASSISTANT,
                    content=response.output,
                )

                st.session_state.messages.append(assistant_message)

                st.session_state.message_count += 1

            # ---------------------------------------------
            # ERROR
            # ---------------------------------------------

            else:

                placeholder.error(response.error or "Something went wrong.")

    # =====================================================
    # CLEAR CHAT
    # =====================================================

    def clear(self) -> None:

        st.session_state.messages = []

        st.session_state.message_count = 0

    # =====================================================
    # EXPORT CHAT
    # =====================================================

    def export_markdown(self) -> str:

        lines = []

        for message in st.session_state.messages:

            role = "User" if message.role == MessageRole.USER else "Assistant"

            lines.append(f"## {role}\n\n" f"{message.content}\n")

        return "\n".join(lines)

    # =====================================================
    # MAIN
    # =====================================================

    def render(self) -> None:

        self.initialize()

        self.render_history()

        prompt = self.chat_input()

        if prompt:

            self.send(prompt)


# ==========================================================
# GLOBAL COMPONENT
# ==========================================================

chat_component = ChatComponent()
