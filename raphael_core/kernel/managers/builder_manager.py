from typing import Dict, Any, Type, Optional
from pathlib import Path
import os

from ..interfaces import ServiceModule, Event, EventType
from ..event_bus import EventBus
from ..observability import ObservabilityLayer
from ..repositories.builder_repository import MarkdownBuildRepository
from ..services.builder_service import BuilderService
from ..providers.build_provider import BuildProvider, LocalBuildProvider

class BuilderManager(ServiceModule):
    """
    RRK ServiceModule for the Builder Subsystem.
    Manages the lifecycle of application builds, coordinating the repository, service, and providers.
    """
    
    def __init__(self, root_dir: str):
        super().__init__()
        self.repository = MarkdownBuildRepository(Path(root_dir))
        self.service = BuilderService(self.repository)
        self.providers: Dict[str, BuildProvider] = {}
        self.generators: Dict[str, Any] = {}
        self.validators: Dict[str, Any] = {}
        self.templates: Dict[str, Any] = {}
        
        # Register default local provider
        self.register_provider("local", LocalBuildProvider(os.path.join(root_dir, "workspaces")))

    @property
    def name(self) -> str:
        return "BuilderManager"

    def register_provider(self, name: str, provider: BuildProvider):
        self.providers[name] = provider

    def register_generator(self, name: str, generator: Any):
        self.generators[name] = generator
        
    def register_validator(self, name: str, validator: Any):
        self.validators[name] = validator
        
    def register_template(self, name: str, template: Any):
        self.templates[name] = template

    async def initialize(self) -> None:
        from ..registry import registry
        self.bus = registry.get_service("EventBus")
        if self.bus:
            self.bus.subscribe(EventType.BUILD_REQUESTED, self._handle_build_requested)
            ObservabilityLayer.info(self.name, "BuilderManager initialized and subscribed to BUILD_REQUESTED.")
        else:
            ObservabilityLayer.warning(self.name, "EventBus not found during initialization.")
            
    async def start(self) -> None:
        pass
        
    async def stop(self) -> None:
        pass
        
    async def shutdown(self) -> None:
        pass
        
    async def heartbeat(self) -> bool | Dict[str, Any]:
        return True
        
    def health(self) -> Any:
        from ..interfaces import ModuleHealth
        return ModuleHealth.OK
        
    def status(self) -> str:
        return "Idle"
        
    def metrics(self) -> Dict[str, Any]:
        return {}

    async def handle_request(self, method: str, path: str, payload: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
        # This will be routed via the API Gateway e.g. POST /api/builder/request
        if method == "POST" and path == "/api/builder/request":
            description = payload.get("description", "")
            req = self.service.process_request(description, metadata=payload.get("metadata"))
            
            # Emit Event to EventBus
            await self.bus.publish(Event(
                type=EventType.BUILD_REQUESTED,
                source=self.name,
                payload={"request_id": req.id}
            ))
            
            return {"status": "accepted", "request_id": req.id}
            
        elif method == "GET" and path.startswith("/api/builder/request/"):
            req_id = path.split("/")[-1]
            req = self.repository.get_request(req_id)
            if req:
                return req.model_dump()
            return {"error": "Not Found"}

        return None

    async def _handle_build_requested(self, event: Event):
        req_id = event.payload.get("request_id")
        req = self.repository.get_request(req_id)
        if not req:
            ObservabilityLayer.error(self.name, f"Request {req_id} not found in repository.")
            return
            
        ObservabilityLayer.info(self.name, f"Processing BUILD_REQUESTED for {req_id}")
        
        # 1. Classify
        classification = self.service.classify_request(req)
        
        # 2. Emit Classified
        await self.bus.publish(Event(
            type=EventType.BUILD_CLASSIFIED,
            source=self.name,
            payload={"classification_id": classification.id, "request_id": req_id}
        ))
        
        ObservabilityLayer.info(self.name, f"Classification {classification.id} completed (Level {classification.complexity_level})")
        
        # 3. Trigger the appropriate Workflow Template
        # In a real scenario we use classification details to pick the template, here we default to React
        templates = self.service.get_workflow_templates()
        chosen_template = templates.get("Create React App")
        
        await self.bus.publish(Event(
            source=self.name,
            type=EventType.WORKFLOW_PLAN_REQUESTED,
            payload={
                "name": f"Builder Execution: {req_id}",
                "template": chosen_template,
                "context": {"request_id": req_id}
            }
        ))
        ObservabilityLayer.info(self.name, f"Triggered WorkflowPlan for {req_id}")
