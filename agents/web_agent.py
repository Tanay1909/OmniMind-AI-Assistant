"""
=========================================================
OmniMind AI Assistant
Web Agent
=========================================================

Responsibilities
----------------
- Search the web
- Summarize search results
- Answer current-event questions
- Cite sources
"""

from __future__ import annotations

import traceback

from agents.base_agent import (
    BaseAgent,
    AgentRequest,
    AgentResponse,
)

from services.analytics_service import AnalyticsService
from services.gemini_service import GeminiService
from services.llm_service import (
    BaseLLMService,
    LLMRequest,
)
from services.web_search_service import (
    WebSearchService,
    SearchResult,
)


class WebAgent(BaseAgent):
    """
    Agent responsible for searching the web
    and generating answers from search results.
    """

    def __init__(
        self,
        search_service: WebSearchService | None = None,
        llm: BaseLLMService | None = None,
        analytics: AnalyticsService | None = None,
    ) -> None:

        super().__init__(
            name="Web Agent",
            description="Searches the web and summarizes search results.",
        )

        # -----------------------------------------
        # Default Services
        # -----------------------------------------

        self.search_service = (
            search_service if search_service is not None else WebSearchService()
        )

        self.llm = llm if llm is not None else GeminiService()

        self.analytics = analytics

    # =====================================================
    # SEARCH
    # =====================================================

    def search(
        self,
        query: str,
        max_results: int = 5,
    ) -> list[SearchResult]:

        return self.search_service.search(
            query=query,
            max_results=max_results,
        )

    # =====================================================
    # BUILD CONTEXT
    # =====================================================

    def build_context(
        self,
        results: list[SearchResult],
    ) -> str:

        if not results:
            return "No search results were found."

        context = []

        for i, result in enumerate(results, start=1):

            context.append(f"""
Result {i}

Title:
{result.title}

URL:
{result.url}

Snippet:
{result.snippet}
""")

        return "\n".join(context)

    # =====================================================
    # GENERATE ANSWER
    # =====================================================

    def answer(
        self,
        query: str,
        results: list[SearchResult],
    ) -> str:

        context = self.build_context(results)

        prompt = f"""
You are OmniMind AI.

Answer the user's question using ONLY the information below.

Question:
{query}

Search Results:

{context}
"""

        request = LLMRequest(
            model="gemini-2.5-flash",
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            temperature=0.3,
            max_tokens=2048,
        )

        response = self.llm.generate(request)

        return response.content

    # =====================================================
    # MAIN
    # =====================================================

    def run(
        self,
        request: AgentRequest,
    ) -> AgentResponse:

        try:

            self.validate(request)

            results = self.search(request.query)

            answer = self.answer(
                request.query,
                results,
            )

            if self.analytics:

                self.analytics.record_request(
                    route="web",
                    model="gemini-2.5-flash",
                    duration=0,
                )

                self.analytics.record_tool("web_search")

            return AgentResponse(
                success=True,
                output=answer,
                agent=self.name,
                metadata={
                    "sources": [
                        {
                            "title": r.title,
                            "url": r.url,
                        }
                        for r in results
                    ],
                    "result_count": len(results),
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
