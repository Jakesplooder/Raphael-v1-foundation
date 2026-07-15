from typing import List, Dict, Any, Optional
from pathlib import Path

from raphael_core.kernel.interfaces import ServiceModule, EventType, Event, ModuleHealth
from raphael_core.kernel.models.knowledge import KnowledgeImportance
from raphael_core.kernel.repositories.knowledge_repository import KnowledgeRepository
from raphael_core.kernel.providers.knowledge.extraction_provider import BasicMarkdownExtractionProvider
from raphael_core.kernel.providers.knowledge.summarization_provider import LocalKnowledgeSummarizationProvider
from raphael_core.kernel.providers.knowledge.embedding_provider import LocalKnowledgeEmbeddingProvider
from raphael_core.kernel.services.knowledge_service import KnowledgeService


class KnowledgeManager(ServiceModule):
    """
    RRK Entrypoint for the Knowledge domain (Explicit Facts).
    """
    def __init__(self, event_bus, config):
        self.event_bus = event_bus
        self.config = config
        
        self.vault_root = getattr(config, "vault", Path("C:/Users/cyber/Downloads/RalphaelOS/Ralphael"))
        self.repository = KnowledgeRepository(self.vault_root)
        self.extractor = BasicMarkdownExtractionProvider()
        self.summarizer = LocalKnowledgeSummarizationProvider()
        self.embedder = LocalKnowledgeEmbeddingProvider()
        
        self.service = KnowledgeService(
            repository=self.repository,
            extractor=self.extractor,
            summarizer=self.summarizer,
            embedder=self.embedder
        )
        
        self._is_initialized = False

    @property
    def name(self) -> str:
        return "Knowledge"
        
    @property
    def depends_on(self) -> List[str]:
        return ["EventBus", "Gateway"]

    async def initialize(self) -> None:
        self._is_initialized = True

    async def start(self) -> None:
        pass
        
    async def stop(self) -> None:
        pass
        
    def metrics(self) -> Dict[str, Any]:
        return {"items_scanned": 0, "items_ingested": 0}
        
    async def shutdown(self) -> None:
        self._is_initialized = False

    def health(self) -> ModuleHealth:
        return ModuleHealth.OK if self._is_initialized else ModuleHealth.ERROR

    def status(self) -> str:
        return "running" if self._is_initialized else "initialized"

    async def heartbeat(self) -> bool | Dict[str, Any]:
        return True

    async def handle_request(self, method: str, path: str, payload: Dict[str, Any] = None) -> Any:
        if method == "POST" and path == "/api/knowledge/ingest":
            file_path_str = payload.get("file_path")
            if not file_path_str:
                raise ValueError("file_path is required")
                
            importance_str = payload.get("importance", "normal").lower()
            importance = KnowledgeImportance(importance_str)
            
            item = await self.service.ingest_file(Path(file_path_str), importance=importance)
            
            # Publish KNOWLEDGE_CREATED
            # MemoryManager will act as the Memory Promotion Gate
            self.event_bus.publish(Event(
                source=self.name,
                type=EventType.KNOWLEDGE_CREATED,
                payload={
                    "id": item.id,
                    "title": item.title,
                    "category": item.category.value,
                    "importance": item.importance.value,
                    "summary": item.summary
                }
            ))
            
            return {"status": "success", "data": item.model_dump()}

        return {"status": "error", "message": f"Unknown endpoint {method} {path}"}
