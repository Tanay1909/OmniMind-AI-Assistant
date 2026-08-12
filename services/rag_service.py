"""
=========================================================
OmniMind AI Assistant
Retrieval Augmented Generation (RAG) Service
=========================================================

Responsibilities
----------------
• Split documents into chunks
• Generate embeddings
• Store vectors
• Retrieve relevant chunks
• Build context for the LLM
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from services.embedding_service import EmbeddingService

# ==========================================================
# DOCUMENT CHUNK
# ==========================================================


@dataclass(slots=True)
class DocumentChunk:

    id: str

    text: str

    source: str

    metadata: dict[str, Any]


# ==========================================================
# SIMPLE VECTOR STORE
# ==========================================================


class InMemoryVectorStore:
    """
    Temporary vector store.

    Replace later with:
        • ChromaDB
        • FAISS
        • Pinecone
        • Weaviate
    """

    def __init__(self):

        self.documents = []

    def add(
        self,
        embedding: list[float],
        chunk: DocumentChunk,
    ):

        self.documents.append(
            (
                embedding,
                chunk,
            )
        )

    def search(
        self,
        query_embedding: list[float],
        embedding_service: EmbeddingService,
        top_k: int = 5,
    ) -> list[DocumentChunk]:

        scored = []

        for embedding, chunk in self.documents:

            score = embedding_service.cosine_similarity(
                query_embedding,
                embedding,
            )

            scored.append(
                (
                    score,
                    chunk,
                )
            )

        scored.sort(
            reverse=True,
            key=lambda x: x[0],
        )

        return [chunk for _, chunk in scored[:top_k]]


# ==========================================================
# CHUNKER
# ==========================================================


class DocumentChunker:
    """
    Splits long text into overlapping chunks.
    """

    def __init__(
        self,
        chunk_size: int = 800,
        overlap: int = 150,
    ):

        self.chunk_size = chunk_size

        self.overlap = overlap

    def split(
        self,
        text: str,
    ) -> list[str]:

        chunks = []

        start = 0

        while start < len(text):

            end = start + self.chunk_size

            chunks.append(text[start:end])

            start += self.chunk_size - self.overlap

        return chunks


# ==========================================================
# RAG SERVICE
# ==========================================================


class RAGService:

    def __init__(
        self,
        embedding_service: EmbeddingService,
    ):

        self.embedding_service = embedding_service

        self.chunker = DocumentChunker()

        self.vector_store = InMemoryVectorStore()

    # ------------------------------------------------------

    def index_document(
        self,
        text: str,
        source: str,
    ):

        chunks = self.chunker.split(text)

        embeddings = self.embedding_service.embed_batch(chunks)

        for index, (chunk, embedding) in enumerate(
            zip(
                chunks,
                embeddings,
            )
        ):

            self.vector_store.add(
                embedding,
                DocumentChunk(
                    id=f"{source}_{index}",
                    text=chunk,
                    source=source,
                    metadata={},
                ),
            )

    # ------------------------------------------------------

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
    ) -> list[DocumentChunk]:

        query_embedding = self.embedding_service.embed(query)

        return self.vector_store.search(
            query_embedding,
            self.embedding_service,
            top_k,
        )

    # ------------------------------------------------------

    def build_context(
        self,
        query: str,
        top_k: int = 5,
    ) -> str:

        chunks = self.retrieve(
            query,
            top_k,
        )

        return "\n\n".join(chunk.text for chunk in chunks)

    # ------------------------------------------------------

    def clear(self):

        self.vector_store = InMemoryVectorStore()
