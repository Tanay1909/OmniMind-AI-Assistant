"""
=========================================================
OmniMind AI Assistant
Coding Agent
=========================================================

Responsibilities
----------------
- Code Generation
- Code Debugging
- Code Explanation
- Code Refactoring
- Unit Test Generation
- Documentation Generation
"""

from __future__ import annotations

import traceback
from enum import Enum

from agents.base_agent import (
    BaseAgent,
    AgentRequest,
    AgentResponse,
)

from core.prompt_manager import PromptManager

from services.analytics_service import AnalyticsService
from services.llm_service import (
    BaseLLMService,
    LLMRequest,
)

# ==========================================================
# TASK TYPES
# ==========================================================


class CodingTask(Enum):
    GENERATE = "generate"
    DEBUG = "debug"
    EXPLAIN = "explain"
    REFACTOR = "refactor"
    TEST = "test"
    DOCUMENT = "document"
    REVIEW = "review"


# ==========================================================
# CODING AGENT
# ==========================================================


class CodingAgent(BaseAgent):

    GROQ_MODEL = "llama-3.3-70b-versatile"

    # Alternative:
    # GROQ_MODEL = "llama-3.3-70b-versatile"

    def __init__(
        self,
        llm: BaseLLMService,
        prompt_manager: PromptManager,
        analytics: AnalyticsService | None = None,
    ) -> None:

        super().__init__(
            name="Coding Agent",
            description="AI Software Engineering Assistant",
        )

        self.llm = llm
        self.prompt_manager = prompt_manager
        self.analytics = analytics

    # =====================================================
    # BUILD PROMPT
    # =====================================================

    def build_prompt(
        self,
        task: CodingTask,
        content: str,
    ) -> str:

        prompts = {
            CodingTask.GENERATE: "Generate clean, production-ready code.\n\n",
            CodingTask.DEBUG: "Debug the following code. Explain the issue and provide the corrected version.\n\n",
            CodingTask.EXPLAIN: "Explain the following code in detail.\n\n",
            CodingTask.REFACTOR: "Refactor the following code following best practices.\n\n",
            CodingTask.TEST: "Generate unit tests for the following code.\n\n",
            CodingTask.DOCUMENT: "Generate documentation for the following code.\n\n",
            CodingTask.REVIEW: "Review the following code and suggest improvements.\n\n",
        }

        return prompts[task] + content

    # =====================================================
    # EXECUTE
    # =====================================================

    def execute(
        self,
        task: CodingTask,
        content: str,
    ) -> str:

        prompt = self.build_prompt(task, content)

        llm_request = LLMRequest(
            model=self.GROQ_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            temperature=0.7,
            max_tokens=2048,
        )

        response = self.llm.generate(llm_request)

        return response.content

    # =====================================================
    # RUN
    # =====================================================

    def run(
        self,
        request: AgentRequest,
    ) -> AgentResponse:

        try:

            self.validate(request)

            context = request.context or {}

            task = CodingTask(context.get("task", "generate"))

            result = self.execute(
                task=task,
                content=request.query,
            )

            if self.analytics:
                self.analytics.record_request(
                    route="coding",
                    model=self.GROQ_MODEL,
                    duration=0,
                )

            return AgentResponse(
                success=True,
                output=result,
                agent=self.name,
                metadata={
                    "provider": "Groq",
                    "model": self.GROQ_MODEL,
                    "task": task.value,
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
