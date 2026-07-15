import abc
from typing import List, Dict, Any

class MemoryProvider(abc.ABC):
    """Base interface for cognitive memory providers."""
    @property
    @abc.abstractmethod
    def name(self) -> str:
        pass


class EmbeddingProvider(MemoryProvider):
    """Provides semantic embedding vectors for memory items."""
    
    @abc.abstractmethod
    async def embed(self, text: str) -> List[float]:
        """Convert cognitive content into a semantic vector."""
        pass


class SummarizationProvider(MemoryProvider):
    """Provides cognitive compression (summarization) for archiving memories."""
    
    @abc.abstractmethod
    async def summarize(self, texts: List[str]) -> str:
        """Compress multiple memories into a single consolidated summary."""
        pass


class LocalEmbeddingProvider(EmbeddingProvider):
    """Implementation that proxies through Gateway/Model Router for embeddings."""
    @property
    def name(self) -> str:
        return "LocalEmbeddingProvider"
        
    async def embed(self, text: str) -> List[float]:
        # Dummy implementation for now; would call Model Router / Gateway
        return [0.0] * 1536


class LocalSummarizationProvider(SummarizationProvider):
    """Implementation that proxies through Gateway/Model Router for summarization."""
    @property
    def name(self) -> str:
        return "LocalSummarizationProvider"
        
    async def summarize(self, texts: List[str]) -> str:
        # Dummy implementation for now
        return f"Consolidated {len(texts)} memories into summary."
