"""
=========================================================
OmniMind AI Assistant
Advanced Memory Agent
=========================================================

Responsibilities
----------------
• Store conversation memory
• Search memories
• Update memories
• Delete memories
• Manage user preferences
• Build conversation context
• Export memory
• Memory statistics
"""

from __future__ import annotations

from typing import Any

from agents.base_agent import (
    AgentRequest,
    AgentResponse,
    BaseAgent,
)

from core.history import HistoryManager
from core.memory import (
    MemoryCategory,
    MemoryManager,
)

from services.analytics_service import AnalyticsService


class MemoryAgent(BaseAgent):
    """
    Intelligent memory management agent.
    """

    def __init__(
        self,
        memory: MemoryManager | None = None,
        history: HistoryManager | None = None,
        analytics: AnalyticsService | None = None,
    ) -> None:

        super().__init__(
            name="Memory Agent",
            description="Advanced conversational memory manager.",
        )

        self.memory = memory or MemoryManager()
        self.history = history or HistoryManager()
        self.analytics = analytics

    # =====================================================
    # MEMORY
    # =====================================================

    def remember(
        self,
        role: str,
        content: str,
        category: MemoryCategory = MemoryCategory.CHAT,
        tags: list[str] | None = None,
        metadata: dict | None = None,
    ):

        return self.memory.add_memory(
            role=role,
            content=content,
            category=category,
            tags=tags,
            metadata=metadata,
        )

    def recall(self):

        return self.memory.get_memories()

    def get_context(
        self,
        max_messages: int = 10,
    ):

        return self.memory.build_context(
            max_messages=max_messages,
        )

    # =====================================================
    # SEARCH
    # =====================================================

    def search(
        self,
        query: str,
    ):

        return self.memory.search_memory(query)

    # =====================================================
    # UPDATE
    # =====================================================

    def update(
        self,
        memory_id: str,
        **kwargs,
    ) -> bool:

        return self.memory.update_memory(
            memory_id,
            **kwargs,
        )

    # =====================================================
    # DELETE
    # =====================================================

    def delete(
        self,
        memory_id: str,
    ) -> bool:

        return self.memory.delete_memory(
            memory_id,
        )

    # =====================================================
    # FAVORITES
    # =====================================================

    def favorite(
        self,
        memory_id: str,
    ) -> bool:

        return self.memory.favorite_memory(
            memory_id,
        )

    def unfavorite(
        self,
        memory_id: str,
    ) -> bool:

        return self.memory.unfavorite_memory(
            memory_id,
        )

    # =====================================================
    # CATEGORY
    # =====================================================

    def memories_by_category(
        self,
        category: MemoryCategory,
    ):

        return self.memory.memories_by_category(
            category,
        )

    def categories(self):

        return self.memory.categories()

    # =====================================================
    # SUMMARY
    # =====================================================

    def summarize(self):

        return self.memory.get_summary()

    def set_summary(
        self,
        summary: str,
    ):

        self.memory.set_summary(summary)

    # =====================================================
    # PREFERENCES
    # =====================================================

    def save_preference(
        self,
        key: str,
        value: Any,
    ):

        self.memory.save_preference(
            key,
            value,
        )

    def get_preference(
        self,
        key: str,
        default: Any = None,
    ):

        return self.memory.get_preference(
            key,
            default,
        )

    def preferences(self):

        return self.memory.get_all_preferences()

    # =====================================================
    # HISTORY
    # =====================================================

    def create_chat(
        self,
        title: str = "New Chat",
    ):

        return self.history.create_chat(
            title,
        )

    def list_chats(self):

        return self.history.list_chats()
    # =====================================================
    # EXPORT / IMPORT
    # =====================================================

    def export_memory(self):

        return self.memory.export_memory()

    def import_memory(
        self,
        data,
    ):

        self.memory.import_memory(data)

    # =====================================================
    # STATISTICS
    # =====================================================

    def statistics(self):

        return self.memory.statistics()

    # =====================================================
    # ARCHIVE
    # =====================================================

    def archive(
        self,
        memory_id: str,
    ) -> bool:

        return self.memory.archive_memory(
            memory_id,
        )

    def restore(
        self,
        memory_id: str,
    ) -> bool:

        return self.memory.restore_memory(
            memory_id,
        )

    # =====================================================
    # CLEAR
    # =====================================================

    def clear(self):

        self.memory.clear_memory()

    # =====================================================
    # COMPATIBILITY
    # =====================================================

    def message_count(self):

        return self.memory.message_count()

    def has_memory(self):

        return self.memory.has_memory()

    # =====================================================
    # MAIN EXECUTION
    # =====================================================

    def run(
        self,
        request: AgentRequest,
    ) -> AgentResponse:

        self.validate(request)

        context = request.context or {}

        action = context.get(
            "action",
            "recall",
        )

        try:

            if action == "remember":

                output = self.remember(
                    role=context.get(
                        "role",
                        "user",
                    ),
                    content=request.query,
                    category=context.get(
                        "category",
                        MemoryCategory.CHAT,
                    ),
                    tags=context.get(
                        "tags",
                    ),
                    metadata=context.get(
                        "metadata",
                    ),
                )

            elif action == "recall":

                output = self.recall()

            elif action == "search":

                output = self.search(
                    request.query,
                )

            elif action == "update":

                output = self.update(
                    context["memory_id"],
                    content=context.get("content"),
                    category=context.get("category"),
                    tags=context.get("tags"),
                    metadata=context.get("metadata"),
                    favorite=context.get("favorite"),
                )

            elif action == "delete":

                output = self.delete(
                    context["memory_id"],
                )

            elif action == "archive":

                output = self.archive(
                    context["memory_id"],
                )

            elif action == "restore":

                output = self.restore(
                    context["memory_id"],
                )

            elif action == "statistics":

                output = self.statistics()

            elif action == "summary":

                output = self.summarize()

            elif action == "set_summary":

                self.set_summary(
                    request.query,
                )

                output = "Summary updated."

            elif action == "save_preference":

                self.save_preference(
                    context["key"],
                    context["value"],
                )

                output = "Preference saved."

            elif action == "preferences":

                output = self.preferences()

            elif action == "export":

                output = self.export_memory()

            elif action == "import":

                self.import_memory(
                    context["data"],
                )

                output = "Memory imported."

            elif action == "clear":

                self.clear()

                output = "Memory cleared."

            else:

                raise ValueError(f"Unknown action: {action}")

            if self.analytics:

                self.analytics.record_request(
                    route="memory",
                    model="memory-agent",
                    duration=0,
                )

            return AgentResponse(
                success=True,
                output=output,
                agent=self.name,
                metadata={
                    "action": action,
                },
            )

        except Exception as exc:

            if self.analytics:

                self.analytics.record_error(type(exc).__name__)

            return AgentResponse(
                success=False,
                output=None,
                error=str(exc),
                agent=self.name,
            )
