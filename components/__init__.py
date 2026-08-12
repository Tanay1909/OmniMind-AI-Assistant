def __init__(self) -> None:

    from core.prompt_manager import PromptManager
    from core.memory import MemoryManager
    from core.history import HistoryManager
    from core.context import ContextBuilder
    from core.analytics import analytics

    from services.analytics_service import AnalyticsService
    from services.gemini_service import GeminiService

    self.prompt_manager = PromptManager()

    self.memory = MemoryManager()

    self.history = HistoryManager()

    self.context_builder = ContextBuilder()

    self.analytics = AnalyticsService(analytics)

    self.llm = GeminiService()

    self.agent = ChatAgent(
        llm=self.llm,
        prompt_manager=self.prompt_manager,
        memory=self.memory,
        history=self.history,
        context_builder=self.context_builder,
        analytics=self.analytics,
    )
