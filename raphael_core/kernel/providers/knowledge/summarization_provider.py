import abc
from typing import List

class KnowledgeSummarizationProvider(abc.ABC):
    """Abstract interface for summarizing explicit knowledge."""
    
    @abc.abstractmethod
    async def summarize(self, text: str) -> str:
        pass


class LocalKnowledgeSummarizationProvider(KnowledgeSummarizationProvider):
    """Implementation for knowledge summarization (proxies to Gateway)."""
    
    async def summarize(self, text: str) -> str:
        # Mock summarization for now
        if len(text) > 100:
            return text[:97] + "..."
        return text
