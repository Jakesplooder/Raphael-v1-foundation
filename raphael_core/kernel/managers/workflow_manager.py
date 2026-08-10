import logging
from typing import Dict, Any, List
from ..interfaces import Event, EventType, ModuleHealth, ServiceModule
from ..services.workflow_service import WorkflowService
from ..repositories.workflow_repository import WorkflowRepository
from ..providers.workflow.executor_provider import ExecutorProvider
from ..providers.workflow.scheduler_provider import SchedulerProvider
from ..providers.workflow.python_provider import PythonProvider
from pathlib import Path

logger = logging.getLogger("rrk.managers.workflow")

class WorkflowManager(ServiceModule):
    def __init__(self, event_bus, config):
        self.event_bus = event_bus
        self.config = config
        
        # Assemble domain components
        vault_path = Path(getattr(self.config, "vault", "./vault")) / "00_Raphael/Workflows"
        self.repository = WorkflowRepository(vault_path)
        
        # Provider stack
        self.automation_provider = PythonProvider()
        self.executor = ExecutorProvider(self.automation_provider)
        self.scheduler = SchedulerProvider()
        
        self.service = WorkflowService(self.repository, self.executor, self.scheduler)
        
        # Hook service emissions to EventBus
        async def _emit_event(event_type: str, payload: dict):
            # Map string event to Enum
            enum_type = EventType(event_type)
            event = Event(source=self.name, type=enum_type, payload=payload)
            await self.event_bus.publish(event)
            
        self.service.emit_event = _emit_event
        
        # Subscribe to Agent Intents
        self.event_bus.subscribe(EventType.AGENT_WORKFLOW_REQUESTED, self._handle_agent_intent)

    async def _handle_agent_intent(self, event: Event):
        payload = event.payload
        agent_id = payload.get("agent_id")
        wf_data = payload.get("workflow", {})
        importance = payload.get("importance", "normal")
        
        from ..models.workflow import WorkflowStep
        steps = [WorkflowStep(**s) for s in wf_data.get("steps", [])]
        
        # Create and trigger workflow automatically
        wf = await self.service.create_workflow(f"Agent {agent_id}: {wf_data.get('name', 'Task')}", steps, importance)
        await self.service.trigger_workflow(wf.id)
        
        logger.info(f"WorkflowManager received intent from agent {agent_id} and triggered workflow {wf.id}")

    @property
    def name(self) -> str:
        return "Workflowrunner"

    @property
    def depends_on(self) -> List[str]:
        return ["EventBus"]

    async def initialize(self) -> None:
        logger.info("WorkflowManager initialized.")

    async def start(self) -> None:
        pass

    async def stop(self) -> None:
        pass

    def health(self) -> ModuleHealth:
        return ModuleHealth.OK

    async def metrics(self) -> dict:
        return {}

    async def handle_request(self, method: str, endpoint: str, payload: Dict[str, Any]) -> Any:
        if method == "POST" and endpoint == "/api/workflow/create":
            name = payload.get("name")
            steps = payload.get("steps", [])
            importance = payload.get("importance", "normal")
            from ..models.workflow import WorkflowStep
            
            # Construct actual objects for safety (ignoring complex validation for now)
            parsed_steps = [WorkflowStep(**s) for s in steps]
            wf = await self.service.create_workflow(name, parsed_steps, importance)
            return {"workflow_id": wf.id}
            
        elif method == "POST" and endpoint == "/api/workflow/trigger":
            workflow_id = payload.get("workflow_id")
            execution = await self.service.trigger_workflow(workflow_id)
            if not execution:
                raise ValueError("Workflow not found")
            return {"execution_id": execution.id}
            
        return {"error": "Unknown endpoint"}

    async def heartbeat(self) -> bool | Dict[str, Any]:
        return True

    async def shutdown(self) -> None:
        pass

    def status(self) -> str:
        return "running"
