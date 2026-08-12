"""
=========================================================
OmniMind AI Assistant
Chat Models
=========================================================

Shared chat-related models used across the application.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field, ConfigDict

# ==========================================================
# MESSAGE ROLE
# ==========================================================


class MessageRole(str, Enum):
    """
    Supported chat roles.
    """

    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"


# ==========================================================
# CHAT MESSAGE
# ==========================================================


class ChatMessage(BaseModel):
    """
    Represents a single chat message.
    """

    model_config = ConfigDict(
        validate_assignment=True,
        use_enum_values=True,
    )

    id: str = Field(default_factory=lambda: str(uuid4()))

    role: MessageRole

    content: str

    timestamp: datetime = Field(default_factory=datetime.utcnow)

    metadata: dict[str, Any] = Field(default_factory=dict)

    tokens: int | None = None

    model_name: str | None = None


# ==========================================================
# CONVERSATION
# ==========================================================


class Conversation(BaseModel):
    """
    Represents a complete conversation.
    """

    model_config = ConfigDict(validate_assignment=True)

    id: str = Field(default_factory=lambda: str(uuid4()))

    title: str = "New Conversation"

    created_at: datetime = Field(default_factory=datetime.utcnow)

    updated_at: datetime = Field(default_factory=datetime.utcnow)

    messages: list[ChatMessage] = Field(default_factory=list)

    metadata: dict[str, Any] = Field(default_factory=dict)

    archived: bool = False

    # =====================================================
    # METHODS
    # =====================================================

    def add_message(
        self,
        message: ChatMessage,
    ) -> None:
        """
        Add a message to the conversation.
        """

        self.messages.append(message)
        self.updated_at = datetime.utcnow()

    def last_message(
        self,
    ) -> ChatMessage | None:
        """
        Return the latest message.
        """

        if not self.messages:
            return None

        return self.messages[-1]

    def clear(self) -> None:
        """
        Remove all messages.
        """

        self.messages.clear()
        self.updated_at = datetime.utcnow()

    @property
    def message_count(self) -> int:
        """
        Number of messages.
        """

        return len(self.messages)

    @property
    def user_messages(self) -> list[ChatMessage]:
        """
        User-only messages.
        """

        return [m for m in self.messages if m.role == MessageRole.USER]

    @property
    def assistant_messages(self) -> list[ChatMessage]:
        """
        Assistant-only messages.
        """

        return [m for m in self.messages if m.role == MessageRole.ASSISTANT]

    def to_llm_messages(
        self,
    ) -> list[dict[str, str]]:
        """
        Convert conversation into
        LLM-compatible message format.
        """

        return [
            {
                "role": msg.role.value,
                "content": msg.content,
            }
            for msg in self.messages
        ]
