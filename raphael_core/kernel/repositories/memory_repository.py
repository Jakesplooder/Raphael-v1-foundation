import uuid
from typing import List, Dict, Any, Optional
import json

from raphael_core.kernel.models.memory import MemoryRecord, MemoryType

try:
    from qdrant_client import QdrantClient
    from qdrant_client.models import Distance, VectorParams, PointStruct, Filter, FieldCondition, MatchValue
    HAS_QDRANT = True
except ImportError:
    HAS_QDRANT = False


class MemoryIndex:
    """Abstract interface for Semantic Vector Operations"""
    def upsert(self, records: List[MemoryRecord]) -> None:
        raise NotImplementedError

    def search(self, query_vector: List[float], limit: int = 10, filters: Dict[str, Any] = None) -> List[MemoryRecord]:
        raise NotImplementedError
        
    def delete(self, record_ids: List[str]) -> None:
        raise NotImplementedError


class QdrantMemoryIndex(MemoryIndex):
    def __init__(self, url: str = "http://127.0.0.1:6333", collection_name: str = "raphael_rrk_memory"):
        if not HAS_QDRANT:
            raise RuntimeError("qdrant-client is required for QdrantMemoryIndex")
        
        self.client = QdrantClient(url=url)
        self.collection_name = collection_name
        self._ensure_collection()
        
    def _ensure_collection(self):
        try:
            collections = self.client.get_collections().collections
            if not any(c.name == self.collection_name for c in collections):
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(size=1536, distance=Distance.COSINE) # Assuming standard 1536 OpenAI/compatible
                )
        except Exception as e:
            print(f"[Qdrant] Warning: Failed to ensure collection: {e}")

    def upsert(self, records: List[MemoryRecord]) -> None:
        if not records:
            return
            
        points = []
        for r in records:
            if not r.embedding:
                continue
            
            payload = r.model_dump()
            # Remove embedding from payload to save space in storage
            payload.pop("embedding", None)
            
            points.append(
                PointStruct(
                    id=r.id,
                    vector=r.embedding,
                    payload=payload
                )
            )
            
        if points:
            self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )

    def search(self, query_vector: List[float], limit: int = 10, filters: Dict[str, Any] = None) -> List[MemoryRecord]:
        qdrant_filter = None
        if filters:
            must_conditions = []
            for k, v in filters.items():
                must_conditions.append(FieldCondition(key=k, match=MatchValue(value=v)))
            qdrant_filter = Filter(must=must_conditions)
            
        results = self.client.query_points(
            collection_name=self.collection_name,
            query=query_vector,
            query_filter=qdrant_filter,
            limit=limit,
            with_payload=True
        ).points
        
        records = []
        for res in results:
            data = res.payload
            # Note: We aren't reconstructing the exact embedding back into the object for now
            # as it's rarely needed downstream and saves memory, but we could.
            records.append(MemoryRecord(**data))
            
        return records

    def delete(self, record_ids: List[str]) -> None:
        if not record_ids:
            return
        self.client.delete(
            collection_name=self.collection_name,
            points_selector=record_ids
        )


class MemoryRepository:
    """
    Handles physical IO for MemoryRecords via the configured Semantic Index.
    """
    def __init__(self, index: MemoryIndex):
        self.index = index
        
    def save_batch(self, records: List[MemoryRecord]) -> None:
        self.index.upsert(records)
        
    def save(self, record: MemoryRecord) -> None:
        self.save_batch([record])
        
    def search_similar(self, query_vector: List[float], limit: int = 20, filters: Dict[str, Any] = None) -> List[MemoryRecord]:
        return self.index.search(query_vector=query_vector, limit=limit, filters=filters)
        
    def archive(self, record_id: str) -> None:
        # In a real implementation, we might move this to an archive collection or change its tier payload
        pass
        
    def forget(self, record_ids: List[str]) -> None:
        self.index.delete(record_ids)
