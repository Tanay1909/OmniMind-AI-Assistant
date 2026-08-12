"""
=========================================================
OmniMind AI Assistant
Research Agent
=========================================================

Responsibilities
----------------
- Multi-source research
- Web + Document synthesis
- Comparative analysis
- Structured report generation
"""

from __future__ import annotations

import traceback
from typing import Any

from agents.base_agent import (
    AgentRequest,
    AgentResponse,
    BaseAgent,
)

from agents.document_agent import DocumentAgent
from agents.web_agent import WebAgent

from services.analytics_service import AnalyticsService
from services.gemini_service import GeminiService
from services.llm_service import (
    BaseLLMService,
    LLMRequest,
)


class ResearchAgent(BaseAgent):
    """
    Multi-source research agent.
    """

    def __init__(
        self,
        web_agent: WebAgent | None = None,
        document_agent: DocumentAgent | None = None,
        llm: BaseLLMService | None = None,
        analytics: AnalyticsService | None = None,
    ) -> None:

        super().__init__(
            name="Research Agent",
            description="Conducts multi-step research.",
        )

        self.web_agent = web_agent if web_agent is not None else WebAgent()

        self.document_agent = (
            document_agent if document_agent is not None else DocumentAgent()
        )

        self.llm = llm if llm is not None else GeminiService()

        self.analytics = analytics

    # =====================================================
    # COLLECT EVIDENCE
    # =====================================================

    def collect_evidence(
        self,
        request: AgentRequest,
        max_results: int = 5,
    ) -> dict[str, Any]:
        """
        Collect evidence from web and documents.
        """

        evidence: dict[str, Any] = {}

        # -------------------------------------------------
        # Web Evidence
        # -------------------------------------------------

        try:

            web_request = AgentRequest(
                query=request.query,
                context=request.context,
                metadata={
                    **request.metadata,
                    "max_results": max_results,
                },
            )

            web_response = self.web_agent.run(web_request)

            if web_response.success:

                evidence["web"] = web_response.output

            else:

                evidence["web"] = None

        except Exception as exc:

            evidence["web"] = {"error": str(exc)}

        # -------------------------------------------------
        # Document Evidence
        # -------------------------------------------------

        if self.document_agent:

            try:

                document_response = self.document_agent.run(request)

                if document_response.success:

                    evidence["documents"] = document_response.output

                else:

                    evidence["documents"] = None

            except Exception as exc:

                evidence["documents"] = {"error": str(exc)}

        return evidence

    # =====================================================
    # SYNTHESIZE
    # =====================================================

    def synthesize(
        self,
        query: str,
        evidence: dict[str, Any],
        summarize: bool = True,
    ) -> str:
        """
        Synthesize collected evidence into
        a structured research report.
        """

        if summarize:

            prompt = f"""
You are an AI research assistant.

Create a professional research report.

Requirements:

1. Executive Summary
2. Key Findings
3. Supporting Evidence
4. Conflicting Information
5. Final Conclusion

Question:

{query}

Evidence:

{evidence}

Use the available evidence carefully.

Do not invent facts that are not supported
by the evidence.
"""

        else:

            prompt = f"""
You are an AI research assistant.

Analyze the following research question
using only the supplied evidence.

Question:

{query}

Evidence:

{evidence}

Return:

1. Key Findings
2. Supporting Evidence
3. Important Observations
4. Conclusion

Do not invent unsupported facts.
"""

        request = LLMRequest(
            model=GeminiService.DEFAULT_MODEL,
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
    # PUBLIC RESEARCH METHOD
    # =====================================================

    def research(
        self,
        query: str,
        max_results: int = 5,
        summarize: bool = True,
    ) -> dict[str, Any]:
        """
        Public research method used by ResearchPage.

        Parameters
        ----------
        query:
            Research question.

        max_results:
            Maximum number of web sources requested.

        summarize:
            Whether to generate a summarized report.

        Returns
        -------
        dict
            Structured research result.
        """

        if not query or not query.strip():

            raise ValueError("Research query cannot be empty.")

        max_results = max(
            1,
            min(int(max_results), 50),
        )

        request = AgentRequest(
            query=query.strip(),
            metadata={
                "max_results": max_results,
                "summarize": summarize,
            },
        )

        response = self.run(request)

        if not response.success:

            raise RuntimeError(response.error or "Research failed.")

        return response.output

    # =====================================================
    # MAIN AGENT RUN
    # =====================================================

    def run(
        self,
        request: AgentRequest,
    ) -> AgentResponse:
        """
        Execute the complete research workflow.
        """

        try:

            # ---------------------------------------------
            # Validate
            # ---------------------------------------------

            self.validate(request)

            # ---------------------------------------------
            # Options
            # ---------------------------------------------

            max_results = int(
                request.metadata.get(
                    "max_results",
                    5,
                )
            )

            summarize = bool(
                request.metadata.get(
                    "summarize",
                    True,
                )
            )

            # ---------------------------------------------
            # Collect Evidence
            # ---------------------------------------------

            evidence = self.collect_evidence(
                request,
                max_results=max_results,
            )

            # ---------------------------------------------
            # Generate Report
            # ---------------------------------------------

            report = self.synthesize(
                request.query,
                evidence,
                summarize=summarize,
            )

            # ---------------------------------------------
            # Convert to Page Structure
            # ---------------------------------------------

            result = {
                "summary": report,
                "findings": [],
                "sources": [],
            }

            # ---------------------------------------------
            # Web Sources
            # ---------------------------------------------

            web_data = evidence.get("web")

            if isinstance(web_data, list):

                for item in web_data:

                    if isinstance(item, dict):

                        result["sources"].append(
                            {
                                "title": item.get(
                                    "title",
                                    "Web Source",
                                ),
                                "url": item.get(
                                    "url",
                                    "",
                                ),
                                "snippet": item.get(
                                    "snippet",
                                    item.get(
                                        "description",
                                        "",
                                    ),
                                ),
                            }
                        )

            elif isinstance(web_data, dict):

                sources = web_data.get(
                    "sources",
                    [],
                )

                if isinstance(sources, list):

                    result["sources"].extend(sources[:max_results])

            # ---------------------------------------------
            # Analytics
            # ---------------------------------------------

            if self.analytics:

                self.analytics.record_request(
                    route="research",
                    model=GeminiService.DEFAULT_MODEL,
                    duration=0,
                )

            # ---------------------------------------------
            # Success
            # ---------------------------------------------

            return AgentResponse(
                success=True,
                output=result,
                agent=self.name,
                metadata={
                    "sources": list(evidence.keys()),
                    "max_results": max_results,
                    "summarize": summarize,
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
