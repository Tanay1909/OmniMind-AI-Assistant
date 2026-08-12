
"""
=========================================================
OmniMind AI Assistant
Application Initializer
=========================================================

Bootstraps the application by creating and wiring
all core components.

Responsibilities:
- Initialize session
- Create managers
- Register tools
- Create workflow engine
- Create assistant facade
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from core.assistant import OmniMindAssistant
from core.context import ContextBuilder
from core.history import HistoryManager
from core.memory import MemoryManager
from core.planner import Planner
from core.prompt_manager import PromptManager
from core.reasoning import ReasoningEngine
from core.router import Router
from core.session import SessionManager
from core.tool_executor import ToolExecutor
from core.tools import ToolRegistry
from core.workflow import WorkflowEngine

# ----------------------------------------------------------
# These imports will be replaced with your real implementations
# when the services package is completed.
# ----------------------------------------------------------
#
# from services.openai_service import OpenAIService
# from services.gemini_service import GeminiService
# from services.pdf_service import PDFService
# from services.ocr_service import OCRService
# from services.search_service import SearchService
# ----------------------------------------------------------


# ==========================================================
# APPLICATION CONTAINER
# ==========================================================

@dataclass(slots=True)
class ApplicationContainer:
    """
    Holds references to all initialized components.
    """

    session: SessionManager
    router: Router
    planner: Planner
    reasoning: ReasoningEngine
    memory: MemoryManager
    history: HistoryManager
    context: ContextBuilder
    prompts: PromptManager
    tool_registry: ToolRegistry
    tool_executor: ToolExecutor
    workflow: WorkflowEngine
    assistant: OmniMindAssistant


# ==========================================================
# PLACEHOLDER LLM
# ==========================================================

class DummyLLMProvider:
    """
    Temporary provider until actual AI services are added.
    """

    def generate(self, messages, **kwargs):
        from core.response_parser import AIResponse

        return AIResponse(
            content="LLM provider is not configured.",
            provider="Dummy",
            model="None",
        )


# ==========================================================
# INITIALIZER
# ==========================================================

class ApplicationInitializer:
    """
    Creates and wires all application components.
    """

    def __init__(self):

        self.session = SessionManager()

        self.router = Router()

        self.planner = Planner()

        self.reasoning = ReasoningEngine()

        self.memory = MemoryManager()

        self.history = HistoryManager()

        self.context = ContextBuilder()

        self.prompts = PromptManager()

        self.tool_registry = ToolRegistry()

        self.tool_executor = ToolExecutor()

    # ======================================================
    # TOOL REGISTRATION
    # ======================================================

    def register_tools(self) -> None:
        """
        Register application tools.

        Add real tools here after the services package
        is implemented.
        """

        pass

    # ======================================================
    # LLM PROVIDER
    # ======================================================

    def create_llm_provider(self):
        """
        Return the default LLM provider.
        """

        return DummyLLMProvider()

    # ======================================================
    # WORKFLOW
    # ======================================================

    def create_workflow(self) -> WorkflowEngine:

        return WorkflowEngine(
            tool_executor=self.tool_executor,
            reasoning=self.reasoning,
            llm=self.create_llm_provider(),
        )

    # ======================================================
    # ASSISTANT
    # ======================================================

    def create_assistant(
        self,
        workflow: WorkflowEngine,
    ) -> OmniMindAssistant:

        return OmniMindAssistant(
            workflow=workflow,
            tool_executor=self.tool_executor,
        )

    # ======================================================
    # BUILD
    # ======================================================

    def build(self) -> ApplicationContainer:
        """
        Build the complete application.
        """

        SessionManager.initialize()

        self.register_tools()

        workflow = self.create_workflow()

        assistant = self.create_assistant(
            workflow
        )

        return ApplicationContainer(
            session=self.session,
            router=self.router,
            planner=self.planner,
            reasoning=self.reasoning,
            memory=self.memory,
            history=self.history,
            context=self.context,
            prompts=self.prompts,
            tool_registry=self.tool_registry,
            tool_executor=self.tool_executor,
            workflow=workflow,
            assistant=assistant,
        )


# ==========================================================
# PUBLIC FACTORY
# ==========================================================

def initialize_application() -> ApplicationContainer:
    """
    Public application bootstrap.
    """

    initializer = ApplicationInitializer()

    return initializer.build()
