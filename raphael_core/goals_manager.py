import re
import os
from typing import Dict, Any, List
from pathlib import Path

from .kernel.interfaces import ServiceModule, ModuleHealth
from .kernel.observability import ObservabilityLayer
from .kernel.state import store

def _read_text(path: Path) -> str:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return ""

def _subsection_value(text: str, heading: str) -> str:
    pattern = rf"^### {re.escape(heading)}[ \t]*\r?\n+(.*?)(?=^### |\Z)"
    match = re.search(pattern, text, flags=re.M | re.S)
    return match.group(1).strip() if match else ""

class GoalsManager(ServiceModule):
    """
    Native RRK GoalsManager.
    Replaces legacy_adapter.goals()
    """
    def __init__(self):
        self._running = False
        self.vault_path = Path(os.environ.get("RAPHAEL_DATA_DIR", r"C:\RaphaelOS")) / "vault"

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
        goals_file = self.vault_path / "00_Raphael" / "Goals.md"
        text = _read_text(goals_file)
        
        items: List[Dict[str, str]] = []
        for match in re.finditer(r"^## (GOAL-[A-Z0-9-]+)\s+(.+?)(?=^## GOAL-|\Z)", text, flags=re.M | re.S):
            body = match.group(2)
            items.append(
                {
                    "id": match.group(1),
                    "title": _subsection_value(body, "Title"),
                    "status": _subsection_value(body, "Status"),
                    "priority": _subsection_value(body, "Priority"),
                    "milestone": _subsection_value(body, "Next Milestone"),
                }
            )
        return items


