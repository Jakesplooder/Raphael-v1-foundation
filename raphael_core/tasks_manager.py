import os
from typing import Dict, Any, List
from pathlib import Path

from .kernel.interfaces import ServiceModule, ModuleHealth
from .kernel.observability import ObservabilityLayer
from .kernel.state import store
from .repositories.tasks import MarkdownTaskRepository
from .services.tasks import TaskService

class TasksManager(ServiceModule):
    """
    Native RRK TasksManager.
    Replaces legacy_adapter.tasks() and legacy_adapter.council_task_entries()
    """
    def __init__(self):
        self._running = False
        
        # Load vault path from settings
        import json
        settings_path = Path(os.environ.get("RAPHAEL_DATA_DIR", r"C:\RaphaelOS")) / "config" / "settings.json"
        if not settings_path.exists():
            # Fallback to local config for testing
            settings_path = Path(__file__).parent.parent / "config" / "settings.json"
            
        try:
            with open(settings_path, "r", encoding="utf-8") as f:
                settings = json.load(f)
                self.vault_path = Path(settings.get("vault_path", r"C:\Users\cyber\Downloads\RalphaelOS\Ralphael"))
        except Exception:
            self.vault_path = Path(r"C:\Users\cyber\Downloads\RalphaelOS\Ralphael")
        
        # In a real DI system, this would be injected.
        self.repository = MarkdownTaskRepository(self.vault_path)
        self.service = TaskService(self.repository)

    @property
    def name(self) -> str:
        return "TasksManager"

    @property
    def depends_on(self) -> List[str]:
        return ["RuntimeStateStore", "HealthMonitor"]

    async def initialize(self) -> None:
        store.set_state(self.name, "status", "initialized")
        ObservabilityLayer.info(self.name, "TasksManager initialized.")

    async def start(self) -> None:
        self._running = True
        store.set_state(self.name, "status", "running")
        ObservabilityLayer.info(self.name, "TasksManager started.")

    async def stop(self) -> None:
        self._running = False
        store.set_state(self.name, "status", "stopped")
        ObservabilityLayer.info(self.name, "TasksManager stopped.")

    async def shutdown(self) -> None:
        store.set_state(self.name, "status", "shutdown")
        ObservabilityLayer.info(self.name, "TasksManager shutdown.")

    async def heartbeat(self) -> bool:
        return self._running

    def health(self) -> ModuleHealth:
        return ModuleHealth.OK if self._running else ModuleHealth.FAILED

    def metrics(self) -> Dict[str, Any]:
        return {}

    def status(self) -> str:
        return "TasksManager running"

    # --- Tasks Domain Logic ---
    
    def get_tasks(self, scope: str = "all") -> List[Dict[str, str]]:
        return self.service.get_tasks(scope)
