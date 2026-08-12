"""
=========================================================
OmniMind AI Assistant
Document Agent
=========================================================

Responsibilities
----------------
- Process uploaded documents
- Extract text
- Index documents into RAG
- Answer document questions
- Summarize documents
"""

from __future__ import annotations

import traceback
from pathlib import Path

from agents.base_agent import (
    AgentRequest,
    AgentResponse,
    BaseAgent,
)

from services.analytics_service import AnalyticsService
from services.embedding_service import EmbeddingService
from services.gemini_service import GeminiService
from services.llm_service import (
    BaseLLMService,
    LLMRequest,
)
from services.pdf_service import PDFService
from services.rag_service import RAGService


class DocumentAgent(BaseAgent):
    """
    Intelligent document processing agent.
    """

    GEMINI_MODEL = "gemini-3.1-flash-lite"

    def __init__(
        self,
        pdf_service: PDFService | None = None,
        rag_service: RAGService | None = None,
        llm: BaseLLMService | None = None,
        analytics: AnalyticsService | None = None,
    ) -> None:

        super().__init__(
            name="Document Agent",
            description="Document Understanding & RAG Agent",
        )

        self.pdf_service = pdf_service or PDFService()

        self.rag_service = rag_service or RAGService(
            embedding_service=EmbeddingService()
        )

        self.llm = llm or GeminiService()

        self.analytics = analytics

    # =====================================================
    # LOAD DOCUMENT
    # =====================================================

    def load_document(
        self,
        path: str | Path,
    ) -> str:

        document = self.pdf_service.load(path)

        self.rag_service.clear()

        self.rag_service.index_document(
            text=document.full_text,
            source=document.filename,
        )

        return document.full_text

    # =====================================================
    # EXTRACT TEXT
    # =====================================================

    def extract_text(
        self,
        path: str | Path,
    ) -> str:

        return self.load_document(path)

    # =====================================================
    # SUMMARIZE
    # =====================================================

    def summarize_document(self) -> str:

        context = self.rag_service.build_context("Summarize the entire document.")

        request = LLMRequest(
            model=self.GEMINI_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": f"Summarize the following document:\n\n{context}",
                }
            ],
            temperature=0.3,
            max_tokens=2048,
        )

        response = self.llm.generate(request)

        return response.content

    # Backward compatibility
    def summarize(
        self,
        path: str | Path,
    ) -> str:

        self.load_document(path)

        return self.summarize_document()

    # =====================================================
    # ANALYZE
    # =====================================================

    def analyze_document(self) -> str:

        context = self.rag_service.build_context("Analyze the document.")

        request = LLMRequest(
            model=self.GEMINI_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": (
                        "Analyze this document and provide:\n\n"
                        "- Main topics\n"
                        "- Important insights\n"
                        "- Key findings\n\n"
                        f"{context}"
                    ),
                }
            ],
            temperature=0.2,
            max_tokens=2048,
        )

        response = self.llm.generate(request)

        return response.content

    # Backward compatibility
    def analyze(
        self,
        path: str | Path,
    ) -> str:

        self.load_document(path)

        return self.analyze_document()

    # =====================================================
    # QUESTION ANSWERING
    # =====================================================

    def answer_question(
        self,
        question: str,
    ) -> str:

        context = self.rag_service.build_context(question)

        prompt = f"""
Use ONLY the provided document context.

If the answer is unavailable, reply:

I don't know.

Context:
{context}

Question:
{question}
"""

        request = LLMRequest(
            model=self.GEMINI_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            temperature=0.2,
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

            context = request.context or {}

            document_path = context.get("document_path")

            if document_path:
                self.load_document(document_path)

            result = self.answer_question(request.query)

            if self.analytics:

                self.analytics.record_request(
                    route="document",
                    model=self.GEMINI_MODEL,
                    duration=0,
                )

            return AgentResponse(
                success=True,
                output=result,
                agent=self.name,
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
