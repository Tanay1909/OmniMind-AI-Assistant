
"""
=========================================================
OmniMind AI Assistant
Prompt Manager
=========================================================

Responsible for:
- Loading prompt templates
- Formatting prompts
- Managing system prompts
- Injecting variables
- Building final prompts for LLM providers
"""

from __future__ import annotations

from string import Formatter
from typing import Any

from config.prompts import (
    get_chat_prompt,
    get_document_prompt,
    get_image_prompt,
    get_system_prompt,
)

from core.exceptions import ValidationError


class PromptManager:
    """
    Handles prompt retrieval and formatting.
    """

    def __init__(self):
        self._formatter = Formatter()

    # =====================================================
    # SYSTEM PROMPTS
    # =====================================================

    def system_prompt(
        self,
        role: str = "assistant",
    ) -> str:
        """
        Return the system prompt for a role.
        """

        return get_system_prompt(role)

    # =====================================================
    # CHAT PROMPTS
    # =====================================================

    def chat_prompt(
        self,
        template: str,
        **kwargs,
    ) -> str:
        """
        Format a chat prompt.
        """

        prompt = get_chat_prompt(template)

        return self.format_prompt(
            prompt,
            **kwargs,
        )

    # =====================================================
    # DOCUMENT PROMPTS
    # =====================================================

    def document_prompt(
        self,
        template: str,
        **kwargs,
    ) -> str:

        prompt = get_document_prompt(template)

        return self.format_prompt(
            prompt,
            **kwargs,
        )

    # =====================================================
    # IMAGE PROMPTS
    # =====================================================

    def image_prompt(
        self,
        template: str,
        **kwargs,
    ) -> str:

        prompt = get_image_prompt(template)

        return self.format_prompt(
            prompt,
            **kwargs,
        )

    # =====================================================
    # FORMATTER
    # =====================================================

    def format_prompt(
        self,
        template: str,
        **kwargs: Any,
    ) -> str:
        """
        Safely format a prompt template.
        """

        required_fields = {
            field_name
            for _, field_name, _, _
            in self._formatter.parse(template)
            if field_name
        }

        missing = required_fields - kwargs.keys()

        if missing:
            raise ValidationError(
                "Missing prompt variables: "
                + ", ".join(sorted(missing))
            )

        return template.format(**kwargs)

    # =====================================================
    # COMBINE PROMPTS
    # =====================================================

    def build_messages(
        self,
        system_prompt: str,
        conversation: list[dict[str, str]],
    ) -> list[dict[str, str]]:
        """
        Build LLM-compatible message list.
        """

        messages = [
            {
                "role": "system",
                "content": system_prompt,
            }
        ]

        messages.extend(conversation)

        return messages

    # =====================================================
    # CUSTOM PROMPTS
    # =====================================================

    @staticmethod
    def custom_prompt(text: str) -> str:
        """
        Return a user-defined prompt.
        """

        return text.strip()


# ==========================================================
# GLOBAL INSTANCE
# ==========================================================

prompt_manager = PromptManager()
