
"""
=========================================================
OmniMind AI Assistant
Conversation History Manager
=========================================================

Handles persistent conversation history.

Storage is abstracted so the backend can be changed
(SQLite, PostgreSQL, MongoDB, etc.) without affecting
the rest of the application.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional
from uuid import uuid4


# ==========================================================
# DATA MODEL
# ==========================================================

@dataclass
class Conversation:
    """
    Represents a stored conversation.
    """

    id: str = field(default_factory=lambda: str(uuid4()))
    title: str = "New Chat"
    created_at: str = field(
        default_factory=lambda: datetime.now().isoformat()
    )
    updated_at: str = field(
        default_factory=lambda: datetime.now().isoformat()
    )
    messages: List[Dict[str, str]] = field(default_factory=list)


# ==========================================================
# STORAGE INTERFACE
# ==========================================================

class HistoryStorage:
    """
    Abstract storage interface.

    Implementations:
        - SQLiteHistoryStorage
        - PostgreSQLHistoryStorage
        - MongoHistoryStorage
    """

    def save(self, conversation: Conversation) -> None:
        raise NotImplementedError

    def load(self, conversation_id: str) -> Optional[Conversation]:
        raise NotImplementedError

    def delete(self, conversation_id: str) -> None:
        raise NotImplementedError

    def list_all(self) -> List[Conversation]:
        raise NotImplementedError


# ==========================================================
# IN-MEMORY STORAGE
# ==========================================================

class InMemoryHistoryStorage(HistoryStorage):
    """
    Temporary storage used during development.

    Replace with SQLite implementation later.
    """

    def __init__(self):
        self._conversations: Dict[str, Conversation] = {}

    def save(self, conversation: Conversation) -> None:
        conversation.updated_at = datetime.now().isoformat()
        self._conversations[conversation.id] = conversation

    def load(self, conversation_id: str):
        return self._conversations.get(conversation_id)

    def delete(self, conversation_id: str):
        self._conversations.pop(conversation_id, None)

    def list_all(self):
        return sorted(
            self._conversations.values(),
            key=lambda x: x.updated_at,
            reverse=True,
        )


# ==========================================================
# HISTORY MANAGER
# ==========================================================

class HistoryManager:
    """
    Manages stored conversations.
    """

    def __init__(
        self,
        storage: HistoryStorage | None = None,
    ):
        self.storage = storage or InMemoryHistoryStorage()

    def create_chat(
        self,
        title: str = "New Chat",
    ) -> Conversation:

        conversation = Conversation(title=title)

        self.storage.save(conversation)

        return conversation

    def save_chat(
        self,
        conversation: Conversation,
    ) -> None:

        self.storage.save(conversation)

    def load_chat(
        self,
        conversation_id: str,
    ) -> Optional[Conversation]:

        return self.storage.load(conversation_id)

    def delete_chat(
        self,
        conversation_id: str,
    ) -> None:

        self.storage.delete(conversation_id)

    def rename_chat(
        self,
        conversation_id: str,
        new_title: str,
    ) -> bool:

        conversation = self.storage.load(conversation_id)

        if conversation is None:
            return False

        conversation.title = new_title

        self.storage.save(conversation)

        return True

    def list_chats(self) -> List[Conversation]:

        return self.storage.list_all()

    def append_message(
        self,
        conversation_id: str,
        role: str,
        content: str,
    ) -> bool:

        conversation = self.storage.load(conversation_id)

        if conversation is None:
            return False

        conversation.messages.append(
            {
                "role": role,
                "content": content,
            }
        )

        self.storage.save(conversation)

        return True


# ==========================================================
# GLOBAL INSTANCE
# ==========================================================

history = HistoryManager()
