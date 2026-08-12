"""
=========================================================
OmniMind AI Assistant
Memory Models
=========================================================

Shared memory models used across the application.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field

# ==========================================================
# MEMORY TYPE
# ==========================================================


class MemoryType(str, Enum):
    """
    Types of memories.
    """

    CONVERSATION = "conversation"
    FACT = "fact"
    PREFERENCE = "preference"
    PROFILE = "profile"
    TASK = "task"
    DOCUMENT = "document"
    SUMMARY = "summary"
    CUSTOM = "custom"


# ==========================================================
# MEMORY IMPORTANCE
# ==========================================================


class MemoryImportance(str, Enum):
    """
    Importance level.
    """

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


# ==========================================================
# MEMORY ITEM
# ==========================================================


class MemoryItem(BaseModel):
    """
    One memory entry.
    """

    model_config = ConfigDict(validate_assignment=True)

    id: str = Field(default_factory=lambda: str(uuid4()))

    memory_type: MemoryType

    content: str

    importance: MemoryImportance = MemoryImportance.MEDIUM

    created_at: datetime = Field(default_factory=datetime.utcnow)

    updated_at: datetime = Field(default_factory=datetime.utcnow)

    source: str | None = None

    embedding: list[float] | None = None

    tags: list[str] = Field(default_factory=list)

    metadata: dict[str, Any] = Field(default_factory=dict)

    access_count: int = 0

    last_accessed: datetime | None = None

    expires_at: datetime | None = None

    def access(self) -> None:
        """
        Update access statistics.
        """

        self.access_count += 1
        self.last_accessed = datetime.utcnow()


# ==========================================================
# MEMORY SUMMARY
# ==========================================================


class MemorySummary(BaseModel):
    """
    Conversation summary.
    """

    model_config = ConfigDict(validate_assignment=True)

    id: str = Field(default_factory=lambda: str(uuid4()))

    summary: str

    generated_at: datetime = Field(default_factory=datetime.utcnow)

    message_count: int = 0

    metadata: dict[str, Any] = Field(default_factory=dict)


# ==========================================================
# MEMORY RETRIEVAL RESULT
# ==========================================================


class MemoryRetrievalResult(BaseModel):
    """
    Retrieved memory.
    """

    model_config = ConfigDict(validate_assignment=True)

    memory: MemoryItem

    similarity_score: float = 1.0

    rank: int = 1


# ==========================================================
# MEMORY COLLECTION
# ==========================================================


class MemoryCollection(BaseModel):
    """
    Collection of memories.
    """

    model_config = ConfigDict(validate_assignment=True)

    id: str = Field(default_factory=lambda: str(uuid4()))

    name: str = "Default"

    memories: list[MemoryItem] = Field(default_factory=list)

    summaries: list[MemorySummary] = Field(default_factory=list)

    metadata: dict[str, Any] = Field(default_factory=dict)

    created_at: datetime = Field(default_factory=datetime.utcnow)

    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # =====================================================
    # METHODS
    # =====================================================

    def add_memory(
        self,
        memory: MemoryItem,
    ) -> None:

        self.memories.append(memory)
        self.updated_at = datetime.utcnow()

    def remove_memory(
        self,
        memory_id: str,
    ) -> None:

        self.memories = [m for m in self.memories if m.id != memory_id]

        self.updated_at = datetime.utcnow()

    def add_summary(
        self,
        summary: MemorySummary,
    ) -> None:

        self.summaries.append(summary)
        self.updated_at = datetime.utcnow()

    def clear(self) -> None:

        self.memories.clear()
        self.summaries.clear()
        self.updated_at = datetime.utcnow()

    @property
    def memory_count(self) -> int:
        return len(self.memories)

    @property
    def summary_count(self) -> int:
        return len(self.summaries)

    @property
    def high_priority_memories(self) -> list[MemoryItem]:

        return [
            memory
            for memory in self.memories
            if memory.importance
            in (
                MemoryImportance.HIGH,
                MemoryImportance.CRITICAL,
            )
        ]

    def get_by_type(
        self,
        memory_type: MemoryType,
    ) -> list[MemoryItem]:

        return [memory for memory in self.memories if memory.memory_type == memory_type]
