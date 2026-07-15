import abc
from typing import List

class KnowledgeEmbeddingProvider(abc.ABC):
    """Abstract interface for embedding factual knowledge items."""
    
    @abc.abstractmethod
    async def embed(self, text: str) -> List[float]:
        pass


class LocalKnowledgeEmbeddingProvider(KnowledgeEmbeddingProvider):
    """Implementation for embedding (proxies to Gateway)."""
    
    async def embed(self, text: str) -> List[float]:
        # Dummy implementation for now; would call Model Router / Gateway
        return [0.0] * 1536
