import logging
from typing import Dict, Any, List
from pathlib import Path

from ..interfaces import ServiceModule, Event, EventType, ModuleHealth
from ..repositories.world_repository import WorldRepository
from ..services.world_service import WorldService

logger = logging.getLogger("rrk.managers.world")

class WorldManager(ServiceModule):
    """Event-driven Hybrid World Model Graph Manager."""
    
    def __init__(self, event_bus, config):
        self.event_bus = event_bus
        self.config = config
        
        # Legacy World Model stored in OS root
        os_root = getattr(self.config, "os_root", Path("C:/RaphaelOS"))
        runtime_path = os_root / "world_model"
        
        self.repository = WorldRepository(runtime_path)
        self.service = WorldService(self.repository)
        self._is_initialized = False

    @property
    def name(self) -> str:
        return "WorldModelService"

    @property
    def depends_on(self) -> List[str]:
        return ["EventBus"]

    async def initialize(self) -> None:
        # Phase 1 of Hybrid Model: Vault Ingestion Sweep
        self._ingest_from_vault()
        
        # Phase 2 of Hybrid Model: EventBus Runtime Updates
        self.event_bus.subscribe(EventType.GOAL_CREATED, self._handle_goal_created)
        self.event_bus.subscribe(EventType.AGENT_TASK_ASSIGNED, self._handle_agent_assigned)
        self.event_bus.subscribe(EventType.WORLD_OBSERVATION_RECEIVED, self._handle_observation)
        self.event_bus.subscribe(EventType.WORLD_HYPOTHESIS_CREATED, self._handle_hypothesis)
        self.event_bus.subscribe(EventType.CAREER_SKILL_VERIFIED, self._handle_career_skill_verified)
        self.event_bus.subscribe(EventType.MARKET_SIGNAL_ACQUIRED, self._handle_market_signal_acquired)
        
        self._is_initialized = True
        logger.info("WorldManager initialized.")

    def _ingest_from_vault(self) -> None:
        """Simulates sweeping the Vault to establish base nodes."""
        self.service.add_node("Aaron", "Aaron", "Owner and final decision authority", "Vault", "constitutional_authority", 0.99)
        self.service.add_node("Raphael", "Raphael Core", "Local OS", "Vault", "core_system", 0.99)
        self.service.add_relationship("AARON-AARON", "RAPHAEL-RAPHAEL CORE", "OWNS", "Aaron owns Raphael", "Vault", "constitutional_authority", 0.99)
        # Note: A real implementation would parse the Markdown vault here.
        
    async def _handle_goal_created(self, event: Event):
        goal_id = event.payload.get("goal_id")
        if goal_id:
            # Create a Goal node in the World Model (representing Reality)
            n = self.service.add_node("Goal", goal_id, "Generated Goal Node", "EventBus", str(event.id))
            await self.event_bus.publish(Event(
                source=self.name,
                type=EventType.WORLD_NODE_CREATED,
                payload={"node_id": n.node_id}
            ))

    async def _handle_agent_assigned(self, event: Event):
        agent_id = event.payload.get("agent_id")
        task_id = event.payload.get("task_id")
        if agent_id and task_id:
            # Ensure nodes exist
            self.service.add_node("Agent", agent_id, f"Agent {agent_id}", "EventBus", str(event.id))
            self.service.add_node("Task", task_id, f"Task {task_id}", "EventBus", str(event.id))
            
            # Create Edge
            r = self.service.add_relationship(
                f"AGENT-{agent_id}", f"TASK-{task_id}", "WORKS_ON",
                f"{agent_id} assigned to {task_id}", "EventBus", str(event.id)
            )
            await self.event_bus.publish(Event(
                source=self.name,
                type=EventType.WORLD_RELATIONSHIP_CREATED,
                payload={"relationship_id": r.relationship_id}
            ))

    async def _handle_observation(self, event: Event):
        # E.g. "Tesla released product X"
        self.service.add_event(
            event_type=event.payload.get("event_type", "observation"),
            cause=event.payload.get("cause", "unknown"),
            effect=event.payload.get("effect", "unknown"),
            outcome=event.payload.get("observation", ""),
            related=[],
            source_system="EventBus",
            source_ref=str(event.id)
        )

    async def _handle_hypothesis(self, event: Event):
        self.service.add_hypothesis(
            statement=event.payload.get("statement", ""),
            generated_by=event.payload.get("agent_id", "Unknown"),
            confidence=0.55
        )

    async def _handle_career_skill_verified(self, event: Event):
        person_id = event.payload.get("person_id")
        skill_name = event.payload.get("skill_name")
        confidence = event.payload.get("confidence", 0.8)
        if person_id and skill_name:
            s = self.service.add_node("Skill", skill_name, f"{skill_name} skill", "EventBus", str(event.id), confidence=confidence)
            r = self.service.add_relationship(person_id, s.node_id, "HAS_SKILL", f"User acquired {skill_name}", "EventBus", str(event.id), confidence=confidence)
            await self.event_bus.publish(Event(source=self.name, type=EventType.WORLD_RELATIONSHIP_CREATED, payload={"relationship_id": r.relationship_id}))

    async def _handle_market_signal_acquired(self, event: Event):
        signal_type = event.payload.get("signal_type")
        content = event.payload.get("content")
        role = event.payload.get("role")
        if signal_type and content:
            n = self.service.add_node("MarketSignal", f"Signal-{str(event.id)[:8]}", content, "EventBus", str(event.id))
            if role:
                r = self.service.add_node("Role", role, role, "EventBus", str(event.id))
                self.service.add_relationship(n.node_id, r.node_id, "AFFECTS", f"Signal affects {role}", "EventBus", str(event.id))

    async def start(self) -> None:
        pass

    async def stop(self) -> None:
        pass
        
    async def shutdown(self) -> None:
        self._is_initialized = False

    def status(self) -> str:
        return "running" if self._is_initialized else "stopped"

    async def heartbeat(self) -> bool | Dict[str, Any]:
        return True

    async def health(self) -> ModuleHealth:
        return ModuleHealth(status="OK", details={
            "nodes": len(self.repository.get_nodes()),
            "relationships": len(self.repository.get_relationships())
        })

    async def metrics(self) -> dict:
        return {}

    async def handle_request(self, method: str, endpoint: str, payload: Dict[str, Any]) -> Any:
        if method == "POST" and endpoint == "/api/world/query":
            return self.service.query_model(
                agent_id=payload.get("agent_id", "Unknown Agent"),
                purpose=payload.get("purpose", "General query"),
                question=payload.get("question", "")
            )
        elif method == "GET" and endpoint == "/api/world/nodes":
            return {"nodes": [n.model_dump() for n in self.repository.get_nodes()]}
            
        return {"error": "Unknown endpoint"}
