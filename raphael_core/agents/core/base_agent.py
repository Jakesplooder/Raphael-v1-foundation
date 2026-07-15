import json
import os
from typing import Dict, Any
from ..runtime.agent_state import AgentState

class BaseAgent:
    """The canonical BaseAgent utilizing the new declarative Manifest system."""
    def __init__(self, name: str, memory_service=None):
        self.name = name
        self.state = AgentState.IDLE
        self.memory_service = memory_service
        self.manifest = self._load_manifest()

    def _load_manifest(self) -> Dict[str, Any]:
        manifest_path = os.path.join(os.path.dirname(__file__), "..", "manifests", f"{self.name}.json")
        try:
            with open(manifest_path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def transition_to(self, new_state: AgentState):
        self.state = new_state
        
    async def reason_about(self, task: str) -> Dict[str, Any]:
        return {"intent": f"Fulfill: {task}"}
        
    async def create_plan(self, intent: Dict[str, Any]) -> Dict[str, Any]:
        return {"name": f"Plan for {intent['intent']}"}
        
    async def review_outcome(self, workflow_id: str) -> Dict[str, Any]:
        return {"status": "ok", "workflow_id": workflow_id}
        
    async def extract_lessons(self, review: Dict[str, Any]) -> None:
        if self.memory_service and self.manifest.get("memory", {}).get("enabled"):
            self.memory_service.save_memory(self.name, "strategy", "Lesson extracted")
        
    async def recover_from_failure(self, error: Exception) -> Dict[str, Any]:
        return {"name": "Recovery Plan", "error": str(error)}
