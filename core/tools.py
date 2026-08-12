
"""
=========================================================
OmniMind AI Assistant
Tool Framework
=========================================================

Defines the base tool interface and registry used by
the ToolExecutor.

Every application tool should inherit from BaseTool.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


# ==========================================================
# TOOL METADATA
# ==========================================================

@dataclass(slots=True)
class ToolMetadata:
    """
    Metadata describing a tool.
    """

    name: str
    description: str

    category: str = "General"

    version: str = "1.0"

    enabled: bool = True

    requires_network: bool = False

    requires_file: bool = False

    supports_streaming: bool = False

    tags: list[str] = field(default_factory=list)


# ==========================================================
# BASE TOOL
# ==========================================================

class BaseTool(ABC):
    """
    Abstract base class for all tools.
    """

    metadata: ToolMetadata

    @abstractmethod
    def run(
        self,
        *args,
        **kwargs,
    ) -> Any:
        """
        Execute the tool.
        """
        raise NotImplementedError

    def validate(
        self,
        *args,
        **kwargs,
    ) -> bool:
        """
        Validate inputs before execution.

        Override if needed.
        """

        return True

    def cleanup(self) -> None:
        """
        Cleanup temporary resources.

        Override if needed.
        """

        return None


# ==========================================================
# TOOL REGISTRY
# ==========================================================

class ToolRegistry:
    """
    Stores all available tools.
    """

    def __init__(self):

        self._tools: dict[str, BaseTool] = {}

    # =====================================================
    # REGISTRATION
    # =====================================================

    def register(
        self,
        tool: BaseTool,
    ) -> None:

        self._tools[
            tool.metadata.name
        ] = tool

    def unregister(
        self,
        name: str,
    ) -> None:

        self._tools.pop(name, None)

    # =====================================================
    # LOOKUP
    # =====================================================

    def get(
        self,
        name: str,
    ) -> BaseTool | None:

        return self._tools.get(name)

    def exists(
        self,
        name: str,
    ) -> bool:

        return name in self._tools

    # =====================================================
    # FILTERS
    # =====================================================

    def list_tools(
        self,
    ) -> list[str]:

        return sorted(
            self._tools.keys()
        )

    def by_category(
        self,
        category: str,
    ) -> list[BaseTool]:

        return [
            tool
            for tool in self._tools.values()
            if tool.metadata.category == category
        ]

    def enabled_tools(
        self,
    ) -> list[BaseTool]:

        return [
            tool
            for tool in self._tools.values()
            if tool.metadata.enabled
        ]

    # =====================================================
    # INFORMATION
    # =====================================================

    def metadata(
        self,
    ) -> list[ToolMetadata]:

        return [
            tool.metadata
            for tool in self._tools.values()
        ]

    # =====================================================
    # RESET
    # =====================================================

    def clear(self):

        self._tools.clear()


# ==========================================================
# GLOBAL REGISTRY
# ==========================================================

tool_registry = ToolRegistry()

