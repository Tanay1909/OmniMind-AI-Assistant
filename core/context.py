
"""
=========================================================
OmniMind AI Assistant
Context Manager
=========================================================

Builds the complete context that will be sent
to the language model.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


# ==========================================================
# CONTEXT DATA MODEL
# ==========================================================

@dataclass
class Context:
    """
    Complete context passed to the LLM.
    """

    system_prompt: str = ""

    conversation: list[dict[str, str]] = field(default_factory=list)

    retrieved_documents: list[str] = field(default_factory=list)

    web_results: list[str] = field(default_factory=list)

    uploaded_files: list[str] = field(default_factory=list)

    user_preferences: dict[str, Any] = field(default_factory=dict)

    summary: str = ""

    metadata: dict[str, Any] = field(default_factory=dict)


# ==========================================================
# CONTEXT BUILDER
# ==========================================================

class ContextBuilder:
    """
    Collects information from different modules and
    builds a unified context object.
    """

    def __init__(self):

        self.context = Context()

    # =====================================================
    # SYSTEM PROMPT
    # =====================================================

    def set_system_prompt(
        self,
        prompt: str,
    ) -> None:

        self.context.system_prompt = prompt

    # =====================================================
    # MEMORY
    # =====================================================

    def set_conversation(
        self,
        messages: list[dict[str, str]],
    ) -> None:

        self.context.conversation = messages

    # =====================================================
    # SUMMARY
    # =====================================================

    def set_summary(
        self,
        summary: str,
    ) -> None:

        self.context.summary = summary

    # =====================================================
    # DOCUMENTS
    # =====================================================

    def add_document(
        self,
        document: str,
    ) -> None:

        self.context.retrieved_documents.append(document)

    def add_documents(
        self,
        documents: list[str],
    ) -> None:

        self.context.retrieved_documents.extend(documents)

    # =====================================================
    # WEB SEARCH
    # =====================================================

    def add_web_result(
        self,
        result: str,
    ) -> None:

        self.context.web_results.append(result)

    # =====================================================
    # FILES
    # =====================================================

    def add_uploaded_file(
        self,
        filename: str,
    ) -> None:

        self.context.uploaded_files.append(filename)

    # =====================================================
    # USER PREFERENCES
    # =====================================================

    def set_preferences(
        self,
        preferences: dict,
    ) -> None:

        self.context.user_preferences = preferences

    # =====================================================
    # METADATA
    # =====================================================

    def add_metadata(
        self,
        key: str,
        value: Any,
    ) -> None:

        self.context.metadata[key] = value

    # =====================================================
    # EXPORT
    # =====================================================

    def build(self) -> Context:
        """
        Return complete context.
        """

        return self.context

    # =====================================================
    # LLM FORMAT
    # =====================================================

    def to_messages(self) -> list[dict[str, str]]:
        """
        Convert context into OpenAI/Gemini-compatible
        chat messages.
        """

        messages = []

        if self.context.system_prompt:

            messages.append(
                {
                    "role": "system",
                    "content": self.context.system_prompt,
                }
            )

        if self.context.summary:

            messages.append(
                {
                    "role": "system",
                    "content":
                        f"Conversation Summary:\n"
                        f"{self.context.summary}",
                }
            )

        if self.context.retrieved_documents:

            document_text = "\n\n".join(
                self.context.retrieved_documents
            )

            messages.append(
                {
                    "role": "system",
                    "content":
                        "Relevant Documents:\n"
                        + document_text,
                }
            )

        if self.context.web_results:

            web_text = "\n\n".join(
                self.context.web_results
            )

            messages.append(
                {
                    "role": "system",
                    "content":
                        "Web Search Results:\n"
                        + web_text,
                }
            )

        messages.extend(self.context.conversation)

        return messages


# ==========================================================
# GLOBAL INSTANCE
# ==========================================================

context_builder = ContextBuilder()
