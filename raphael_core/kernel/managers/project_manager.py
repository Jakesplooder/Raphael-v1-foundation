from typing import Dict, Any, Optional, List
import asyncio
from ..interfaces import ServiceModule, Event, EventType, ModuleHealth
from ..event_bus import EventBus
from ..observability import ObservabilityLayer
from ..repositories.project_repository import MarkdownProjectRepository
from ..services.project_service import ProjectService
from ...config import RaphaelConfig

class ProjectManager(ServiceModule):
    def __init__(self, config: RaphaelConfig):
        self.config = config
        self.repository = MarkdownProjectRepository(config)
        self.service = ProjectService(self.repository)
        self.bus: Optional[EventBus] = None

    @property
    def name(self) -> str:
        return "ProjectManager"

    @property
    def depends_on(self) -> List[str]:
        return ["EventBus", "InfrastructureManager"]

    async def initialize(self) -> None:
        from ..registry import registry
        self.bus = registry.get_service("EventBus")
        if self.bus:
            # We could subscribe to events like PROJECT_CREATED here
            pass
        ObservabilityLayer.info(self.name, "ProjectManager initialized.")

    async def start(self) -> None:
        ObservabilityLayer.info(self.name, "ProjectManager started.")
        
    async def stop(self) -> None:
        ObservabilityLayer.info(self.name, "ProjectManager stopped.")
        
    async def shutdown(self) -> None:
        ObservabilityLayer.info(self.name, "ProjectManager shutdown.")

    async def heartbeat(self) -> bool | Dict[str, Any]:
        return True

    def health(self) -> ModuleHealth:
        return ModuleHealth.OK

    def status(self) -> str:
        return "Active"

    def metrics(self) -> Dict[str, Any]:
        return {
            "projects_count": len(self.service.list_projects())
        }

    async def handle_request(self, method: str, path: str, payload: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
        if path.startswith("/api/projects"):
            return self.service.process_request(payload or {})
        return None
