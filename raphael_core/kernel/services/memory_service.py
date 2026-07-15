import time
from typing import List, Dict, Any, Optional

from raphael_core.kernel.models.memory import MemoryRecord, MemoryType
from raphael_core.kernel.interfaces import MemoryTier
from raphael_core.kernel.repositories.memory_repository import MemoryRepository
from raphael_core.kernel.providers.memory_providers import EmbeddingProvider, SummarizationProvider


class MemoryService:
    """
    Cognitive Brain for Raphael.
    Manages meaning storage, semantic retrieval, lifecycle pruning, and summarization.
    """
    def __init__(
        self, 
        repository: MemoryRepository, 
        embedding_provider: EmbeddingProvider,
        summarization_provider: SummarizationProvider
    ):
        self.repository = repository
        self.embedding = embedding_provider
        self.summarizer = summarization_provider

    async def store_memory(
        self, 
        content: str, 
        source: str, 
        type: MemoryType = MemoryType.OBSERVATION,
        project: Optional[str] = None,
        goal: Optional[str] = None,
        importance: float = 0.5,
        confidence: float = 0.8,
        tags: List[str] = None
    ) -> MemoryRecord:
        """
        Embed and persist a new cognitive meaning vector.
        """
        vector = await self.embedding.embed(content)
        
        # Decide the initial tier
        tier = MemoryTier.WORKING
        if importance > 0.8:
            tier = MemoryTier.LONG_TERM
        elif type in (MemoryType.DECISION, MemoryType.PREFERENCE):
            tier = MemoryTier.LONG_TERM
            
        record = MemoryRecord(
            content=content,
            type=type,
            source=source,
            project=project,
            goal=goal,
            importance=importance,
            confidence=confidence,
            tags=tags or [],
            embedding=vector,
            tier=tier
        )
        
        self.repository.save(record)
        return record

    async def retrieve_memories(
        self, 
        query: str, 
        limit: int = 5,
        filters: Dict[str, Any] = None
    ) -> List[MemoryRecord]:
        """
        Semantic retrieval enriched by cognitive heuristics.
        Final score = similarity × importance × recency × confidence
        """
        query_vector = await self.embedding.embed(query)
        
        # We fetch more than limit from vector DB, then rerank cognitively
        candidates = self.repository.search_similar(query_vector, limit=limit*3, filters=filters)
        
        now = time.time()
        scored_candidates = []
        
        for record in candidates:
            # Reconstruct the vector-similarity distance (Mocked as 1.0 if not returned by DB natively)
            # In a real implementation, the vector DB returns distance alongside payload.
            # Assuming a default semantic similarity of 0.8 for matched candidates for now.
            semantic_similarity = 0.8 
            
            recency = record.decay_score(now)
            
            # Cognitive Scoring Formula
            final_score = semantic_similarity * record.importance * recency * record.confidence
            
            scored_candidates.append((final_score, record))
            
            # Update access tracking (side effect to keep it fresh)
            record.access()
            # self.repository.save(record) # In a heavily used system, we might debounce this save
            
        # Sort by final score descending
        scored_candidates.sort(key=lambda x: x[0], reverse=True)
        
        return [record for score, record in scored_candidates[:limit]]

    async def consolidate_session(self, project: str = None) -> MemoryRecord:
        """
        Compress working memory into a session summary and archive the originals.
        """
        filters = {"tier": MemoryTier.WORKING}
        if project:
            filters["project"] = project
            
        # Mock retrieval of working tier items (Vector index might not support pure filter without query,
        # but in production we'd use a pure filter lookup or maintain a DB of active records)
        candidates = self.repository.search_similar([0.0]*1536, limit=100, filters=filters)
        
        if not candidates:
            return None
            
        texts = [f"[{c.type}] {c.content}" for c in candidates]
        summary = await self.summarizer.summarize(texts)
        
        # Store new summary
        summary_record = await self.store_memory(
            content=summary,
            source="MemoryService.Consolidation",
            type=MemoryType.SUMMARY,
            project=project,
            importance=0.9, # Summaries carry structural importance
            tier=MemoryTier.SESSION
        )
        
        # Archive originals
        archived_ids = []
        for c in candidates:
            archived_ids.append(c.id)
            c.tier = MemoryTier.ARCHIVE
            self.repository.save(c) # Real implementation: update payload or move collection
            
        return summary_record
