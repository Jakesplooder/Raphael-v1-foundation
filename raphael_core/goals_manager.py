import re
import os
from typing import Dict, Any, List
from pathlib import Path

from .kernel.interfaces import ServiceModule, ModuleHealth
from .kernel.observability import ObservabilityLayer
from .kernel.state import store
from .repositories.goals import MarkdownGoalRepository
from .services.goals import GoalService

class GoalsManager(ServiceModule):
    """
    Native RRK GoalsManager.
    Replaces legacy_adapter.goals()
    """
    def __init__(self):
        self._running = False
        self.vault_path = Path(os.environ.get("RAPHAEL_DATA_DIR", r"C:\RaphaelOS"))
        
        # In a real DI system, this would be injected.
        self.repository = MarkdownGoalRepository(self.vault_path)
        self.service = GoalService(self.repository)

    @property
    def name(self) -> str:
        return "GoalsManager"

    @property
    def depends_on(self) -> List[str]:
        return ["RuntimeStateStore", "HealthMonitor"]

    async def initialize(self) -> None:
        store.set_state(self.name, "status", "initialized")
        ObservabilityLayer.info(self.name, "GoalsManager initialized.")

    async def start(self) -> None:
        self._running = True
        store.set_state(self.name, "status", "running")
        ObservabilityLayer.info(self.name, "GoalsManager started.")

    async def stop(self) -> None:
        self._running = False
        store.set_state(self.name, "status", "stopped")
        ObservabilityLayer.info(self.name, "GoalsManager stopped.")

    async def shutdown(self) -> None:
        store.set_state(self.name, "status", "shutdown")
        ObservabilityLayer.info(self.name, "GoalsManager shutdown.")

    async def heartbeat(self) -> bool:
        return self._running

    def health(self) -> ModuleHealth:
        return ModuleHealth.OK if self._running else ModuleHealth.FAILED

    def metrics(self) -> Dict[str, Any]:
        return {}

    def status(self) -> str:
        return "GoalsManager running"

    # --- Goals Domain Logic ---
    
    def get_all_goals(self) -> List[Dict[str, str]]:
        return self.service.get_all_goals()


