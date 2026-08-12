
"""
=========================================================
OmniMind AI Assistant
Tool Executor
=========================================================

Centralized tool execution engine.

Responsibilities:
- Register tools
- Execute tools
- Validate tool availability
- Handle execution errors
- Return standardized results
"""

from __future__ import annotations

from dataclasses import dataclass, field
from time import perf_counter
from typing import Any, Callable

from core.exceptions import ToolExecutionError


# ==========================================================
# TOOL RESULT
# ==========================================================

@dataclass(slots=True)
class ToolResult:
    """
    Standardized tool execution result.
    """

    success: bool
    tool_name: str

    data: Any = None

    execution_time: float = 0.0

    error: str | None = None

    metadata: dict[str, Any] = field(default_factory=dict)


# ==========================================================
# TOOL EXECUTOR
# ==========================================================

class ToolExecutor:
    """
    Registers and executes application tools.
    """

    def __init__(self):

        self._tools: dict[str, Callable[..., Any]] = {}

    # =====================================================
    # REGISTRATION
    # =====================================================

    def register(
        self,
        name: str,
        tool: Callable[..., Any],
    ) -> None:
        """
        Register a callable tool.
        """

        self._tools[name] = tool

    def unregister(
        self,
        name: str,
    ) -> None:

        self._tools.pop(name, None)

    # =====================================================
    # INFORMATION
    # =====================================================

    def exists(
        self,
        name: str,
    ) -> bool:

        return name in self._tools

    def list_tools(self) -> list[str]:

        return sorted(self._tools.keys())

    # =====================================================
    # EXECUTION
    # =====================================================

    def execute(
        self,
        name: str,
        *args,
        **kwargs,
    ) -> ToolResult:
        """
        Execute a registered tool.
        """

        if name not in self._tools:
            raise ToolExecutionError(
                f"Tool '{name}' is not registered."
            )

        tool = self._tools[name]

        start = perf_counter()

        try:

            result = tool(
                *args,
                **kwargs,
            )

            elapsed = perf_counter() - start

            return ToolResult(
                success=True,
                tool_name=name,
                data=result,
                execution_time=elapsed,
            )

        except Exception as exc:

            elapsed = perf_counter() - start

            return ToolResult(
                success=False,
                tool_name=name,
                error=str(exc),
                execution_time=elapsed,
            )

    # =====================================================
    # RESET
    # =====================================================

    def clear(self) -> None:
        """
        Remove all registered tools.
        """

        self._tools.clear()


# ==========================================================
# GLOBAL INSTANCE
# ==========================================================

tool_executor = ToolExecutor()
