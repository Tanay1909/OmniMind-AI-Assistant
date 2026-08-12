"""
=========================================================
OmniMind AI Assistant
Chat Agent
=========================================================

Primary conversational agent.

Responsibilities
----------------
- Build conversation context
- Generate LLM responses
- Store conversation history
- Update memory
- Track analytics
"""

from __future__ import annotations

import traceback

from agents.base_agent import (
    AgentRequest,
    AgentResponse,
    BaseAgent,
)

from core.context import ContextBuilder
from core.history import HistoryManager
from core.memory import MemoryManager
from core.prompt_manager import PromptManager
from core.session import SessionManager

from services.analytics_service import AnalyticsService
from services.llm_service import (
    BaseLLMService,
    LLMRequest,
)


class ChatAgent(BaseAgent):
    """
    Main conversational AI agent.
    """

    GEMINI_MODEL = "gemini-3.5-flash-lite"

    def __init__(
        self,
        llm: BaseLLMService,
        prompt_manager: PromptManager,
        memory: MemoryManager,
        history: HistoryManager,
        context_builder: ContextBuilder,
        analytics: AnalyticsService | None = None,
    ) -> None:

        super().__init__(
            name="Chat Agent",
            description="General purpose conversational AI",
        )

        self.llm = llm
        self.prompt_manager = prompt_manager
        self.memory = memory
        self.history = history
        self.context_builder = context_builder
        self.analytics = analytics

    # =====================================================
    # MAIN
    # =====================================================

    def run(
        self,
        request: AgentRequest,
    ) -> AgentResponse:

        self.validate(request)

        try:

            # --------------------------------------------
            # Save User Message
            # --------------------------------------------

            self.memory.add_message(
                "user",
                request.query,
            )

            conversation_id = SessionManager.get("current_chat")

            if conversation_id:
                self.history.append_message(
                    conversation_id,
                    "user",
                    request.query,
                )

            # --------------------------------------------
            # Build Context
            # --------------------------------------------

            context = self.context_builder.to_messages()

            system_prompt = self.prompt_manager.system_prompt()

            messages = [
                {
                    "role": "system",
                    "content": system_prompt,
                }
            ]

            messages.extend(context)

            messages.append(
                {
                    "role": "user",
                    "content": request.query,
                }
            )

            # --------------------------------------------
            # Generate Gemini Response
            # --------------------------------------------

            llm_request = LLMRequest(
                messages=messages,
                model=self.GEMINI_MODEL,
            )

            llm_response = self.llm.generate(llm_request)

            answer = llm_response.content

            # --------------------------------------------
            # Save Assistant Response
            # --------------------------------------------

            self.memory.add_message(
                "assistant",
                answer,
            )

            if conversation_id:
                self.history.append_message(
                    conversation_id,
                    "assistant",
                    answer,
                )

            # --------------------------------------------
            # Analytics
            # --------------------------------------------

            if self.analytics:
                self.analytics.record_request(
                    route="chat",
                    model=llm_response.model,
                    duration=0,
                )

            return AgentResponse(
                success=True,
                output=answer,
                agent=self.name,
                metadata={
                    "provider": llm_response.provider,
                    "model": llm_response.model,
                    "tokens": llm_response.total_tokens,
                },
            )

        except Exception as exc:

            traceback.print_exc()

            if self.analytics:
                self.analytics.record_error(type(exc).__name__)

            return AgentResponse(
                success=False,
                output=None,
                error=str(exc),
                agent=self.name,
            )
