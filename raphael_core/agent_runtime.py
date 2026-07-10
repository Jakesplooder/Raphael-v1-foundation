import json
import os
import uuid
import time
from typing import Dict, Any, List, Optional
from datetime import datetime

from .kernel.interfaces import ServiceModule, Event, EventType
from .kernel.observability import ObservabilityLayer
from .kernel.registry import registry

class WorkforceManager(ServiceModule):
    """
    Manages the lifecycle and state synchronization of all Digital Workforce agents.
    Syncs authoritative state from World Model down to agent_runtime.json cache.
    """
    
    def __init__(self, filepath: str = os.path.join(os.environ.get("RAPHAEL_DATA_DIR", r"C:\RaphaelOS"), r"workforce\agent_runtime.json")):
        self.filepath = filepath
        self._cache: Dict[str, Any] = {}
        self._running = False
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
        
    @property
    def name(self) -> str:
        return "WorkforceManager"

    @property
    def depends_on(self) -> list[str]:
        return ["WorldModelService", "EventBus"]
        
    async def initialize(self) -> None:
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, 'r', encoding='utf-8') as f:
                    self._cache = json.load(f)
            except Exception:
                self._cache = {}
        else:
            self._cache = {}
            self._save_cache()

    async def start(self) -> None:
        self._running = True
        ObservabilityLayer.info(self.name, "Started WorkforceManager")
        
        # In a full implementation, we'd spawn a background task to sync every N seconds.
        # For now, we do an initial sync on boot.
        self._sync_to_world_model()
        
    async def stop(self) -> None:
        self._running = False

    async def heartbeat(self) -> bool:
        return self._running
        
    async def shutdown(self) -> None:
        self._save_cache()
        
    def health(self) -> Any:
        from .kernel.interfaces import ModuleHealth
        return ModuleHealth.OK if self._running else ModuleHealth.OFFLINE
        
    def status(self) -> str:
        return f"Tracking {len(self._cache)} agents"
        
    def metrics(self) -> Dict[str, Any]:
        return {"tracked_agents": len(self._cache)}

    def _save_cache(self) -> None:
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump(self._cache, f, indent=2)

    def _sync_to_world_model(self) -> None:
        """
        Authoritative flow: World Model -> agent_runtime.json cache
        Never: agent_runtime.json -> World Model
        """
        wm_svc = registry.get_service("WorldModelService")
        if not wm_svc:
            return
            
        # For Phase 70.0 simulation, we mock the extraction since the World Model
        # schema for agents isn't fully robust yet. But the directional pattern holds.
        # Ideally, we query WM for each agent and rebuild the cache.
        # Here we just log the sync pattern and save the current cache.
        trace_id = str(uuid.uuid4())
        ObservabilityLayer.info(self.name, "Syncing agent states from World Model", trace_id=trace_id)
        
        # In a real implementation:
        # wm_node = wm_svc.query(agent_id="WorkforceManager", purpose="cache_sync", question=f"Current state of agents")
        # self._cache = self._extract_runtime_record(wm_node)
        
        self._save_cache()

    def write_lifecycle_transition(self, agent_id: str, new_state: str, reason: str, trace_id: str) -> None:
        """
        Lifecycle transitions write to World Model first.
        Cache is updated by the next sync cycle.
        Never write directly to agent_runtime.json for state changes.
        """
        wm_svc = registry.get_service("WorldModelService")
        if wm_svc:
            # We would use wm_svc to update the node if the API supported it.
            pass
            
        ObservabilityLayer.info(
            self.name,
            f"Lifecycle transition recorded for {agent_id}: -> {new_state}",
            trace_id=trace_id
        )
        
        # Emulate the subsequent sync picking it up:
        if agent_id in self._cache:
            self._cache[agent_id]["previous_state"] = self._cache[agent_id].get("current_state")
            self._cache[agent_id]["current_state"] = new_state
            self._cache[agent_id]["state_entered_at"] = datetime.utcnow().isoformat()
            self._save_cache()

    def get_agent_state(self, agent_id: str) -> Optional[Dict[str, Any]]:
        return self._cache.get(agent_id)
