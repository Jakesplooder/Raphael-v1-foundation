from typing import List, Dict, Any, Optional

from raphael_core.kernel.interfaces import ServiceModule, EventType, Event, ModuleHealth
from raphael_core.kernel.models.memory import MemoryType
from raphael_core.kernel.repositories.memory_repository import MemoryRepository, QdrantMemoryIndex
from raphael_core.kernel.providers.memory_providers import LocalEmbeddingProvider, LocalSummarizationProvider
from raphael_core.kernel.services.memory_service import MemoryService


class MemoryManager(ServiceModule):
    """
    RRK Entrypoint for the Memory domain (Cognitive Layer).
    """
    def __init__(self, event_bus):
        self.event_bus = event_bus
        
        # Assemble internal architecture
        # In a fully Dependency Injected environment, these would be passed in,
        # but the Manager acts as the root composer for the module.
        self.index = QdrantMemoryIndex()
        self.repository = MemoryRepository(self.index)
        self.embedding = LocalEmbeddingProvider()
        self.summarizer = LocalSummarizationProvider()
        
        self.service = MemoryService(
            repository=self.repository,
            embedding_provider=self.embedding,
            summarization_provider=self.summarizer
        )
        
        self._is_initialized = False

    @property
    def name(self) -> str:
        return "Memory"
        
    @property
    def depends_on(self) -> List[str]:
        return ["EventBus", "Gateway"]

    async def initialize(self) -> None:
        """Subscribe to passive cognitive events."""
        # Passive cognitive observation
        self.event_bus.subscribe(EventType.GOAL_CREATED, self._handle_cognitive_event)
        self.event_bus.subscribe(EventType.TASK_COMPLETED, self._handle_cognitive_event)
        self.event_bus.subscribe(EventType.PROJECT_CREATED, self._handle_cognitive_event)
        self.event_bus.subscribe(EventType.USER_DECISION, self._handle_cognitive_event)
        self.event_bus.subscribe(EventType.ERROR_OCCURRED, self._handle_cognitive_event)
        self.event_bus.subscribe(EventType.BUILD_GENERATION_FINISHED, self._handle_cognitive_event)
        self.event_bus.subscribe(EventType.PLAN_APPROVED, self._handle_cognitive_event)
        
        # Memory Promotion Gate
        self.event_bus.subscribe(EventType.KNOWLEDGE_CREATED, self._handle_knowledge_promotion)
        
        # Promotion Gate for Workflows
        self.event_bus.subscribe(EventType.WORKFLOW_COMPLETED, self._handle_workflow_promotion)
        self.event_bus.subscribe(EventType.WORKFLOW_FAILED, self._handle_workflow_promotion)
        
        # Promotion Gate for Agents
        self.event_bus.subscribe(EventType.AGENT_STRATEGIC_OUTCOME, self._handle_agent_promotion)
        self.event_bus.subscribe(EventType.AGENT_LESSON_LEARNED, self._handle_agent_promotion)
        self.event_bus.subscribe(EventType.AGENT_FAILED, self._handle_agent_promotion)
        
        # Promotion Gate for Goals (Strategic memory)
        self.event_bus.subscribe(EventType.OBJECTIVE_COMPLETED, self._handle_goal_promotion)
        self.event_bus.subscribe(EventType.GOAL_COMPLETED, self._handle_goal_promotion)
        
        self._is_initialized = True

    async def start(self) -> None:
        pass
        
    async def stop(self) -> None:
        pass
        
    def metrics(self) -> Dict[str, Any]:
        return {"memories_stored": 0, "memories_retrieved": 0}
        
    async def shutdown(self) -> None:
        self._is_initialized = False

    def health(self) -> ModuleHealth:
        return ModuleHealth.OK if self._is_initialized else ModuleHealth.ERROR

    def status(self) -> str:
        return "running" if self._is_initialized else "initialized"

    async def heartbeat(self) -> bool | Dict[str, Any]:
        return True

    async def handle_request(self, method: str, path: str, payload: Dict[str, Any] = None) -> Any:
        """
        Gateway HTTP routing
        """
        if method == "POST" and path == "/api/memory/search":
            query = payload.get("query", "")
            limit = payload.get("limit", 5)
            filters = payload.get("filters", {})
            results = await self.service.retrieve_memories(query, limit, filters)
            
            # Emit event
            self.event_bus.publish(Event(
                source=self.name,
                type=EventType.MEMORY_RETRIEVED,
                payload={"query": query, "returned": len(results)}
            ))
            
            return {"status": "success", "data": [r.model_dump() for r in results]}
            
        elif method == "POST" and path == "/api/memory/store":
            content = payload.get("content")
            if not content:
                raise ValueError("content is required")
                
            record = await self.service.store_memory(
                content=content,
                source=payload.get("source", "API"),
                type=MemoryType(payload.get("type", MemoryType.FACT.value)),
                importance=payload.get("importance", 0.5)
            )
            
            self.event_bus.publish(Event(
                source=self.name,
                type=EventType.MEMORY_STORED,
                payload={"id": record.id}
            ))
            
            return {"status": "success", "data": record.model_dump()}

        return {"status": "error", "message": f"Unknown endpoint {method} {path}"}

    async def _handle_cognitive_event(self, event: Event) -> None:
        """
        Passive listener that intercepts events and stores them in cognitive memory.
        """
        content = f"Event {event.type.value} occurred in {event.source}: {event.payload}"
        
        mem_type = MemoryType.OBSERVATION
        importance = 0.4
        
        if event.type == EventType.USER_DECISION:
            mem_type = MemoryType.DECISION
            importance = 0.9
        elif event.type == EventType.ERROR_OCCURRED:
            mem_type = MemoryType.ERROR
            importance = 0.8
            
        await self.service.store_memory(
            content=content,
            source=f"EventBus.{event.source}",
            type=mem_type,
            importance=importance
        )

    async def _handle_workflow_promotion(self, event: Event) -> None:
        payload = event.payload
        importance = payload.get("importance", "normal")
        
        # Memory is earned: Promote strategic successes OR any failures (which are valuable learning opportunities)
        if importance == "strategic" or event.type == EventType.WORKFLOW_FAILED:
            await self.service.store_memory(
                content=f"Workflow execution {payload.get('execution_id')} resulted in {event.type.value}. Error: {payload.get('error', 'None')}",
                source="WorkflowRunner",
                type=MemoryType.OBSERVATION
            )
            # Emit that a memory was formed (reusing KNOWLEDGE_PROMOTED_TO_MEMORY or similar, we'll just log it here for now or emit it)
            self.event_bus.publish(Event(
                source=self.name,
                type=EventType.KNOWLEDGE_PROMOTED_TO_MEMORY,  # Reusing this for general promotion visibility
                payload={"execution_id": payload.get("execution_id")}
            ))

    async def _handle_agent_promotion(self, event: Event) -> None:
        payload = event.payload
        importance = payload.get("importance", "normal")
        
        if importance == "strategic" or event.type == EventType.AGENT_FAILED:
            await self.service.store_memory(
                content=f"Agent {payload.get('agent_id')} reasoning result: {event.type.value}. Error: {payload.get('error', 'None')}",
                source="AgentManager",
                type=MemoryType.OBSERVATION
            )
            self.event_bus.publish(Event(
                source=self.name,
                type=EventType.KNOWLEDGE_PROMOTED_TO_MEMORY,
                payload={"agent_id": payload.get("agent_id")}
            ))

    async def _handle_goal_promotion(self, event: Event) -> None:
        payload = event.payload
        importance = payload.get("importance", "normal")
        
        # Only store if strategic milestone reached
        if importance == "strategic":
            await self.service.store_memory(
                content=f"Strategic milestone reached: {event.type.value} - ID {payload.get('objective_id') or payload.get('goal_id')}",
                source="GoalsManager",
                type=MemoryType.OBSERVATION
            )
            self.event_bus.publish(Event(
                source=self.name,
                type=EventType.KNOWLEDGE_PROMOTED_TO_MEMORY,
                payload={"goal_related_id": payload.get("objective_id") or payload.get("goal_id")}
            ))

    async def _handle_knowledge_promotion(self, event: Event) -> None:
        """
        Memory Promotion Gate.
        Evaluates explicit knowledge for experiential/executive relevance.
        Only promotes to Semantic Memory if importance is STRATEGIC.
        """
        payload = event.payload or {}
        importance = payload.get("importance", "normal").lower()
        
        if importance == "strategic":
            content = f"Promoted Strategic Knowledge: {payload.get('title')} ({payload.get('summary', '')})"
            
            await self.service.store_memory(
                content=content,
                source=f"Knowledge.PromotionGate",
                type=MemoryType.FACT,
                importance=0.9
            )
            
            # Emit promotion event
            self.event_bus.publish(Event(
                source=self.name,
                type=EventType.KNOWLEDGE_PROMOTED_TO_MEMORY,
                payload={"knowledge_id": payload.get("id")}
            ))

