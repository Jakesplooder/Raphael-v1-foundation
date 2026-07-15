import logging
from typing import Dict, Any, List
from pathlib import Path

from ..interfaces import ServiceModule, Event, EventType, ModuleHealth
from ..repositories.agent_repository import AgentRepository
from ..providers.agents.llm_provider import LLMProvider
from ..providers.agents.tool_provider import ToolProvider
from ..services.agent_service import AgentService
from ..services.agent_reasoning_service import AgentReasoningService
from ..models.agent import MemoryScope

logger = logging.getLogger("rrk.managers.agent")

class AgentManager(ServiceModule):
    def __init__(self, event_bus, config):
        self.event_bus = event_bus
        self.config = config
        
        vault_path = Path(getattr(self.config, "vault", "./vault")) / "00_Raphael/Agents"
        self.repository = AgentRepository(vault_path)
        
        self.agent_service = AgentService(self.repository)
        self.llm_provider = LLMProvider()
        self.tool_provider = ToolProvider()
        self.reasoning_service = AgentReasoningService(self.llm_provider, self.tool_provider)
        
        # Inject Event emitter
        async def _emit_event(event_type_str: str, payload: dict):
            enum_type = EventType(event_type_str)
            event = Event(source=self.name, type=enum_type, payload=payload)
            self.event_bus.publish(event)
            
        self.reasoning_service.emit_event = _emit_event
        self._is_initialized = False

    @property
    def name(self) -> str:
        return "Agents"

    @property
    def depends_on(self) -> List[str]:
        return ["EventBus"]

    async def initialize(self) -> None:
        # Pre-seed for testing if no definitions exist
        if not self.agent_service.get_definition("TestAgent"):
            self.agent_service.create_definition(
                name="TestAgent",
                role="Tester",
                description="A test agent",
                capabilities=["echo", "python"],
                permissions=["testing"]
            )
        
        if not self.agent_service.get_definition("MarketingAgent"):
            self.agent_service.create_definition(
                name="MarketingAgent",
                role="Marketing Strategist",
                description="Marketing campaigns",
                capabilities=["market_research", "campaign_design"],
                permissions=["marketing"]
            )
            
        self._is_initialized = True
        logger.info("AgentManager initialized.")

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
        return ModuleHealth(status="OK", details={"agents_tracked": len(self.repository.instances)})

    async def metrics(self) -> dict:
        return {}

    async def handle_request(self, method: str, endpoint: str, payload: Dict[str, Any]) -> Any:
        if method == "POST" and endpoint == "/api/agents/spawn":
            def_name = payload.get("definition")
            scope_str = payload.get("memory_scope", "none")
            scope = MemoryScope(scope_str)
            inst = self.agent_service.spawn_agent(def_name, scope)
            
            # Emit AGENT_CREATED
            self.event_bus.publish(Event(
                source=self.name,
                type=EventType.AGENT_CREATED,
                payload={"agent_id": inst.id, "definition": inst.definition}
            ))
            return {"agent_id": inst.id}
            
        elif method == "POST" and endpoint == "/api/agents/assign":
            agent_id = payload.get("agent_id")
            goal = payload.get("goal")
            inst = self.agent_service.get_agent(agent_id)
            if not inst:
                raise ValueError("Agent not found")
                
            df = self.agent_service.get_definition(inst.definition)
            
            self.event_bus.publish(Event(
                source=self.name,
                type=EventType.AGENT_TASK_ASSIGNED,
                payload={"agent_id": inst.id, "goal": goal}
            ))
            
            # Start reasoning loop (async for now, wait for it to complete in test script though)
            await self.reasoning_service.reason_about_goal(inst, df, goal)
            return {"status": "reasoning_started"}
            
        return {"error": "Unknown endpoint"}
