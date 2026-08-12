"""
=========================================================
OmniMind AI Assistant
Services Package
=========================================================

This package contains all external service integrations.

Services include:
- LLM providers
- Embedding generation
- RAG
- OCR
- PDF processing
- Image processing
- Speech processing
- Translation
- Web search
- Export utilities
- Analytics

Only service classes should be imported here.
Avoid creating instances inside this file.
"""

from .llm_service import BaseLLMService
from .gemini_service import GeminiService
from .groq_service import GroqService
from .embedding_service import EmbeddingService
from .rag_service import RAGService
from .ocr_service import OCRService
from .pdf_service import PDFService
from .image_service import ImageService
from .speech_service import SpeechService
from .translation_service import TranslationService
from .web_search_service import WebSearchService
from .export_service import ExportService
from .analytics_service import AnalyticsService

__all__ = [
    "BaseLLMService",
    "GeminiService",
    "GroqService",
    "EmbeddingService",
    "RAGService",
    "OCRService",
    "PDFService",
    "ImageService",
    "SpeechService",
    "TranslationService",
    "WebSearchService",
    "ExportService",
    "AnalyticsService",
]

__version__ = "1.0.0"
