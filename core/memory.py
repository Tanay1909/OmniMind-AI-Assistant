"""
=========================================================
OmniMind AI Assistant
Advanced Memory Manager
=========================================================

Provides short-term and long-term memory for OmniMind.

Features
--------
• Conversation Memory
• Long-Term Memory
• Categories
• Search
• Favorites
• Metadata
• Statistics
• Context Builder
• User Preferences
• Export / Import Ready
"""

from __future__ import annotations

import uuid

from dataclasses import asdict
from dataclasses import dataclass
from dataclasses import field

from datetime import datetime

from enum import Enum

from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from core.session import SessionManager

# ==========================================================
# MEMORY CATEGORY
# ==========================================================


class MemoryCategory(str, Enum):
    """
    Categories for stored memories.
    """

    GENERAL = "General"
    CHAT = "Chat"
    DOCUMENT = "Document"
    RESEARCH = "Research"
    CODING = "Coding"
    USER = "User"
    PREFERENCE = "Preference"


# ==========================================================
# MEMORY ITEM
# ==========================================================


@dataclass
class MemoryItem:
    """
    Single stored memory.
    """

    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    role: str = "user"

    content: str = ""

    category: MemoryCategory = MemoryCategory.GENERAL

    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())

    tags: List[str] = field(default_factory=list)

    metadata: Dict[str, Any] = field(default_factory=dict)

    favorite: bool = False

    archived: bool = False

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert object to dictionary.
        """

        data = asdict(self)

        data["category"] = self.category.value

        return data

    @classmethod
    def from_dict(
        cls,
        data: Dict[str, Any],
    ) -> "MemoryItem":

        category = data.get(
            "category",
            MemoryCategory.GENERAL,
        )

        if isinstance(category, str):
            category = MemoryCategory(category)

        return cls(
            id=data.get("id", str(uuid.uuid4())),
            role=data.get("role", "user"),
            content=data.get("content", ""),
            category=category,
            created_at=data.get(
                "created_at",
                datetime.now().isoformat(),
            ),
            updated_at=data.get(
                "updated_at",
                datetime.now().isoformat(),
            ),
            tags=data.get("tags", []),
            metadata=data.get("metadata", {}),
            favorite=data.get("favorite", False),
            archived=data.get("archived", False),
        )


# ==========================================================
# MEMORY STATISTICS
# ==========================================================


@dataclass
class MemoryStatistics:

    total_memories: int = 0

    active_memories: int = 0

    archived_memories: int = 0

    favorite_memories: int = 0

    total_categories: int = 0

    total_preferences: int = 0


# ==========================================================
# MEMORY MANAGER
# ==========================================================


class MemoryManager:
    """
    Advanced memory manager.
    """

    MEMORY_KEY = "omnimind_memory"

    SUMMARY_KEY = "conversation_summary"

    PREFERENCE_KEY = "user_preferences"

    HISTORY_KEY = "conversation_history"

    def __init__(self):

        SessionManager.initialize()

        self._initialize_storage()

    # =====================================================
    # STORAGE INITIALIZATION
    # =====================================================

    def _initialize_storage(self) -> None:

        defaults = {
            self.MEMORY_KEY: [],
            self.SUMMARY_KEY: "",
            self.PREFERENCE_KEY: {},
            self.HISTORY_KEY: [],
        }

        for key, value in defaults.items():

            if not SessionManager.exists(key):

                if isinstance(value, (list, dict)):
                    SessionManager.set(
                        key,
                        value.copy(),
                    )
                else:
                    SessionManager.set(
                        key,
                        value,
                    )

    # =====================================================
    # INTERNAL HELPERS
    # =====================================================

    def _load(self) -> List[MemoryItem]:

        data = SessionManager.get(
            self.MEMORY_KEY,
            [],
        )

        memories: List[MemoryItem] = []

        for item in data:

            if isinstance(item, MemoryItem):

                memories.append(item)

            elif isinstance(item, dict):

                memories.append(MemoryItem.from_dict(item))

        return memories

    def _save(
        self,
        memories: List[MemoryItem],
    ) -> None:

        SessionManager.set(
            self.MEMORY_KEY,
            [memory.to_dict() for memory in memories],
        )

    def _find(
        self,
        memory_id: str,
    ) -> Optional[MemoryItem]:

        for memory in self._load():

            if memory.id == memory_id:

                return memory

        return None
    # =====================================================
    # CREATE
    # =====================================================

    def add_memory(
        self,
        role: str,
        content: str,
        category: MemoryCategory = MemoryCategory.GENERAL,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> MemoryItem:
        """
        Add a new memory.
        """

        memory = MemoryItem(
            role=role,
            content=content,
            category=category,
            tags=tags or [],
            metadata=metadata or {},
        )

        memories = self._load()
        memories.append(memory)

        self._save(memories)

        return memory

    # =====================================================
    # CHAT COMPATIBILITY
    # =====================================================

    def add_message(
        self,
        role: str,
        content: str,
    ) -> None:
        """
        Compatible with existing ChatAgent.
        """

        self.add_memory(
            role=role,
            content=content,
            category=MemoryCategory.CHAT,
        )

    # =====================================================
    # READ
    # =====================================================

    def get_memories(
        self,
        include_archived: bool = False,
    ) -> List[MemoryItem]:

        memories = self._load()

        if include_archived:
            return memories

        return [memory for memory in memories if not memory.archived]

    def get_messages(self) -> List[MemoryItem]:
        """
        Backward compatibility.
        """

        return self.get_memories()

    def get_memory(
        self,
        memory_id: str,
    ) -> Optional[MemoryItem]:

        return self._find(memory_id)

    # =====================================================
    # UPDATE
    # =====================================================

    def update_memory(
        self,
        memory_id: str,
        *,
        content: Optional[str] = None,
        category: Optional[MemoryCategory] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        favorite: Optional[bool] = None,
    ) -> bool:

        memories = self._load()

        updated = False

        for memory in memories:

            if memory.id != memory_id:
                continue

            if content is not None:
                memory.content = content

            if category is not None:
                memory.category = category

            if tags is not None:
                memory.tags = tags

            if metadata is not None:
                memory.metadata = metadata

            if favorite is not None:
                memory.favorite = favorite

            memory.updated_at = datetime.now().isoformat()

            updated = True
            break

        if updated:
            self._save(memories)

        return updated

    # =====================================================
    # DELETE
    # =====================================================

    def delete_memory(
        self,
        memory_id: str,
    ) -> bool:

        memories = self._load()

        filtered = [memory for memory in memories if memory.id != memory_id]

        if len(filtered) == len(memories):
            return False

        self._save(filtered)

        return True

    # =====================================================
    # ARCHIVE
    # =====================================================

    def archive_memory(
        self,
        memory_id: str,
    ) -> bool:

        return self._set_archive(
            memory_id,
            True,
        )

    def restore_memory(
        self,
        memory_id: str,
    ) -> bool:

        return self._set_archive(
            memory_id,
            False,
        )

    def _set_archive(
        self,
        memory_id: str,
        state: bool,
    ) -> bool:

        memories = self._load()

        for memory in memories:

            if memory.id == memory_id:

                memory.archived = state

                memory.updated_at = datetime.now().isoformat()

                self._save(memories)

                return True

        return False

    # =====================================================
    # FAVORITES
    # =====================================================

    def favorite_memory(
        self,
        memory_id: str,
    ) -> bool:

        return self.update_memory(
            memory_id,
            favorite=True,
        )

    def unfavorite_memory(
        self,
        memory_id: str,
    ) -> bool:

        return self.update_memory(
            memory_id,
            favorite=False,
        )

    def favorite_memories(self) -> List[MemoryItem]:

        return [memory for memory in self.get_memories() if memory.favorite]

    # =====================================================
    # SEARCH
    # =====================================================

    def search_memory(
        self,
        query: str,
    ) -> List[MemoryItem]:

        query = query.lower().strip()

        if not query:
            return self.get_memories()

        results = []

        for memory in self.get_memories():

            searchable = " ".join(
                [
                    memory.content,
                    memory.role,
                    memory.category.value,
                    " ".join(memory.tags),
                ]
            ).lower()

            if query in searchable:
                results.append(memory)

        return results

    # =====================================================
    # CATEGORY
    # =====================================================

    def memories_by_category(
        self,
        category: MemoryCategory,
    ) -> List[MemoryItem]:

        return [memory for memory in self.get_memories() if memory.category == category]

    def categories(self) -> List[str]:

        return sorted({memory.category.value for memory in self.get_memories()})
    # =====================================================
    # SUMMARY
    # =====================================================

    def set_summary(
        self,
        summary: str,
    ) -> None:

        SessionManager.set(
            self.SUMMARY_KEY,
            summary,
        )

    def get_summary(self) -> str:

        return SessionManager.get(
            self.SUMMARY_KEY,
            "",
        )

    # =====================================================
    # USER PREFERENCES
    # =====================================================

    def save_preference(
        self,
        key: str,
        value: Any,
    ) -> None:

        preferences = SessionManager.get(
            self.PREFERENCE_KEY,
            {},
        )

        preferences[key] = value

        SessionManager.set(
            self.PREFERENCE_KEY,
            preferences,
        )

    def get_preference(
        self,
        key: str,
        default: Any = None,
    ) -> Any:

        preferences = SessionManager.get(
            self.PREFERENCE_KEY,
            {},
        )

        return preferences.get(
            key,
            default,
        )

    def get_all_preferences(self) -> Dict[str, Any]:

        return SessionManager.get(
            self.PREFERENCE_KEY,
            {},
        )

    # =====================================================
    # CONTEXT
    # =====================================================

    def build_context(
        self,
        max_messages: int = 10,
    ) -> List[Dict[str, str]]:
        """
        Return recent conversation in LLM format.
        """

        messages = self.get_memories()

        recent = messages[-max_messages:]

        return [
            {
                "role": memory.role,
                "content": memory.content,
            }
            for memory in recent
            if not memory.archived
        ]

    # =====================================================
    # EXPORT / IMPORT
    # =====================================================

    def export_memory(self) -> List[Dict[str, Any]]:
        """
        Export all memories as dictionaries.
        """

        return [memory.to_dict() for memory in self._load()]

    def import_memory(
        self,
        data: List[Dict[str, Any]],
    ) -> None:
        """
        Import memories from exported data.
        """

        memories = [MemoryItem.from_dict(item) for item in data]

        self._save(memories)

    # =====================================================
    # CLEAR
    # =====================================================

    def clear_memory(self) -> None:

        SessionManager.set(
            self.MEMORY_KEY,
            [],
        )

    # =====================================================
    # STATISTICS
    # =====================================================

    def statistics(self) -> MemoryStatistics:

        memories = self._load()

        return MemoryStatistics(
            total_memories=len(memories),
            active_memories=len([m for m in memories if not m.archived]),
            archived_memories=len([m for m in memories if m.archived]),
            favorite_memories=len([m for m in memories if m.favorite]),
            total_categories=len({m.category for m in memories}),
            total_preferences=len(self.get_all_preferences()),
        )

    # =====================================================
    # COMPATIBILITY
    # =====================================================

    def message_count(self) -> int:

        return len(self.get_memories())

    def has_memory(self) -> bool:

        return self.message_count() > 0

    def __len__(self):

        return self.message_count()

    def __iter__(self):

        return iter(self.get_memories())


# ==========================================================
# GLOBAL INSTANCE
# ==========================================================

memory = MemoryManager()
