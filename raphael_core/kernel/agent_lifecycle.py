import json
import os
import time
import asyncio
from typing import Dict, Any, List

from .interfaces import ServiceModule, ModuleHealth, Event, EventType, AgentState, JobState, Job
from .observability import ObservabilityLayer
from .registry import registry
from .state import store

class AgentLifecycleManager(ServiceModule):
    """
    Orchestrates agent spawning, state sync, and termination.
    Maintains the runtime/agent_runtime.json snapshot.
    """
    
    def __init__(self, data_dir: str = os.environ.get("RAPHAEL_DATA_DIR", r"R:\RaphaelOS")):
        self.runtime_dir = os.path.join(data_dir, "runtime")
        self.history_dir = os.path.join(data_dir, "history")
        self.runtime_file = os.path.join(self.runtime_dir, "agent_runtime.json")
        self.history_file = os.path.join(self.history_dir, "agent_history.json")
        
        os.makedirs(self.runtime_dir, exist_ok=True)
        os.makedirs(self.history_dir, exist_ok=True)
        
        from ..agents.runtime.agent_runtime import AgentRuntime
        self.agent_runtime = AgentRuntime(event_bus=None, workflow_manager=None) # will be set in initialize
        
        self._running = False
        self._task = None
        self._runtime_cache = {
            "schema": "2.0",
            "runtime_schema_version": "70.3",
            "agents": {}
        }
        self._history_cache = {"agents": {}}
        
    @property
    def name(self) -> str:
        return "AgentLifecycleManager"
        
    @property
    def depends_on(self) -> list[str]:
        return ["EventBus"]
        
    async def initialize(self) -> None:
        if os.path.exists(self.runtime_file):
            try:
                with open(self.runtime_file, 'r', encoding='utf-8') as f:
                    self._runtime_cache = json.load(f)
            except Exception:
                pass
                
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    self._history_cache = json.load(f)
            except Exception:
                pass
                
    async def start(self) -> None:
        self._running = True
        
        # Subscribe to agent state transitions
        bus = registry.get_service("EventBus")
        if bus:
            bus.subscribe(EventType.AGENT_STATE_TRANSITION.value, self._on_agent_transition)
            bus.subscribe(EventType.JOB_STATE_CHANGED.value, self._on_job_changed)
            
        self._task = asyncio.create_task(self._sync_loop())
        ObservabilityLayer.info(self.name, "AgentLifecycleManager started")
        
    async def _on_agent_transition(self, event: Event) -> None:
        agent_name = event.source
        new_state = event.payload.get("new_state")
        agent_id = event.payload.get("agent_id")
        
        if agent_name not in self._runtime_cache["agents"]:
            self._runtime_cache["agents"][agent_name] = {}
            
        self._runtime_cache["agents"][agent_name]["state"] = new_state
        self._runtime_cache["agents"][agent_name]["agent_id"] = agent_id
        self._runtime_cache["agents"][agent_name]["last_transition"] = time.time()
        
        # Trigger CheckpointManager
        chk_mgr = registry.get_service("CheckpointManager")
        if chk_mgr:
            chk_mgr.trigger_checkpoint(agent_name)
            
    async def _on_job_changed(self, event: Event) -> None:
        agent_name = event.source
        state = event.payload.get("state")
        
        if state in ("completed", "failed"):
            # Update history
            if agent_name not in self._history_cache["agents"]:
                self._history_cache["agents"][agent_name] = {
                    "jobs_completed": 0, "jobs_failed": 0
                }
            
            if state == "completed":
                self._history_cache["agents"][agent_name]["jobs_completed"] += 1
            else:
                self._history_cache["agents"][agent_name]["jobs_failed"] += 1
                
            self._save_history()

    async def _sync_loop(self) -> None:
        while self._running:
            try:
                await asyncio.sleep(5)
                # Pull full heartbeat data into runtime cache
                heartbeats = store.get_module_state("Heartbeats") or {}
                for agent_name, data in heartbeats.items():
                    if data.get("type") == "agent":
                        if agent_name not in self._runtime_cache["agents"]:
                            self._runtime_cache["agents"][agent_name] = {}
                        self._runtime_cache["agents"][agent_name].update(data)
                        
                with open(self.runtime_file, 'w', encoding='utf-8') as f:
                    json.dump(self._runtime_cache, f, indent=2)
            except asyncio.CancelledError:
                break
            except Exception as e:
                ObservabilityLayer.error(self.name, f"Sync error: {e}")
                await asyncio.sleep(1)

    def _save_history(self) -> None:
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self._history_cache, f, indent=2)
        except Exception as e:
            ObservabilityLayer.error(self.name, f"History save error: {e}")

    async def heartbeat(self) -> bool:
        return self._running
        
    async def stop(self) -> None:
        self._running = False
        if self._task:
            self._task.cancel()
            
    async def shutdown(self) -> None:
        pass
        
    def health(self) -> ModuleHealth:
        return ModuleHealth.OK if self._running else ModuleHealth.FAILED
        
    def status(self) -> str:
        return "Managing lifecycles and snapshots"
        
    def metrics(self) -> Dict[str, Any]:
        return {}


class CheckpointManager(ServiceModule):
    """
    Listens to lifecycle events and writes agent volatile state 
    to checkpoint/<agent>.json.
    """
    
    def __init__(self, data_dir: str = os.environ.get("RAPHAEL_DATA_DIR", r"R:\RaphaelOS")):
        self.checkpoint_dir = os.path.join(data_dir, "checkpoint")
        os.makedirs(self.checkpoint_dir, exist_ok=True)
        self._running = False
        
    @property
    def name(self) -> str:
        return "CheckpointManager"
        
    @property
    def depends_on(self) -> list[str]:
        return []
        
    async def initialize(self) -> None:
        pass
        
    async def start(self) -> None:
        self._running = True
        
    def trigger_checkpoint(self, agent_name: str) -> None:
        if not self._running:
            return
            
        agent = registry.get_service(agent_name)
        if not agent or not hasattr(agent, "current_context"):
            return
            
        try:
            cp_file = os.path.join(self.checkpoint_dir, f"{agent_name}.json")
            data = {
                "timestamp": time.time(),
                "agent_id": agent.agent_id,
                "generation": agent.generation,
                "state": agent.state.value,
                "current_job": agent.current_job.model_dump() if agent.current_job else None,
                "current_context": agent.current_context,
                "conversation_ids": agent.conversation_ids,
                "pending_events": agent.pending_events,
                "open_jobs": agent.open_jobs,
                "loaded_hypotheses": agent.loaded_hypotheses
            }
            with open(cp_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            ObservabilityLayer.debug(self.name, f"Checkpoint saved for {agent_name}")
        except Exception as e:
            ObservabilityLayer.error(self.name, f"Checkpoint failure for {agent_name}: {e}")

    async def heartbeat(self) -> bool:
        return self._running
        
    async def stop(self) -> None:
        self._running = False
        
    async def shutdown(self) -> None:
        pass
        
    def health(self) -> ModuleHealth:
        return ModuleHealth.OK if self._running else ModuleHealth.FAILED
        
    def status(self) -> str:
        return "Ready"
        
    def metrics(self) -> Dict[str, Any]:
        return {}


class RecoveryManager(ServiceModule):
    """
    Detects crashed jobs on boot and restores them to Step N/M using checkpoints.
    """
    
    def __init__(self, data_dir: str = os.environ.get("RAPHAEL_DATA_DIR", r"R:\RaphaelOS")):
        self.checkpoint_dir = os.path.join(data_dir, "checkpoint")
        self._running = False
        self._recovered_count = 0
        
    @property
    def name(self) -> str:
        return "RecoveryManager"
        
    @property
    def depends_on(self) -> list[str]:
        return ["CheckpointManager", "JobSystem"]
        
    async def initialize(self) -> None:
        pass
        
    async def start(self) -> None:
        self._running = True
        self._recover_agents()
        
    def _recover_agents(self) -> None:
        if not os.path.exists(self.checkpoint_dir):
            return
            
        for file in os.listdir(self.checkpoint_dir):
            if file.endswith(".json"):
                agent_name = file[:-5]
                agent = registry.get_service(agent_name)
                if not agent:
                    continue
                    
                try:
                    with open(os.path.join(self.checkpoint_dir, file), 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        
                    state_val = data.get("state")
                    if state_val in (AgentState.EXECUTING.value, AgentState.THINKING.value, AgentState.WAITING.value):
                        # Agent crashed during active work.
                        ObservabilityLayer.info(self.name, f"Recovering crashed agent: {agent_name}")
                        
                        agent.current_context = data.get("current_context", {})
                        agent.conversation_ids = data.get("conversation_ids", [])
                        agent.pending_events = data.get("pending_events", [])
                        agent.open_jobs = data.get("open_jobs", [])
                        agent.loaded_hypotheses = data.get("loaded_hypotheses", [])
                        
                        job_data = data.get("current_job")
                        if job_data:
                            from .interfaces import Job
                            job = Job(**job_data)
                            agent.current_job = job
                            
                            # Re-queue the job via JobSystem so it naturally restarts
                            job_sys = registry.get_service("JobSystem")
                            if job_sys:
                                asyncio.create_task(job_sys.submit_job(job))
                                self._recovered_count += 1
                                ObservabilityLayer.info(self.name, f"Re-queued job {job.id} for {agent_name}")
                except Exception as e:
                    ObservabilityLayer.error(self.name, f"Failed to recover {agent_name}: {e}")

    async def heartbeat(self) -> bool:
        return self._running
        
    async def stop(self) -> None:
        self._running = False
        
    async def shutdown(self) -> None:
        pass
        
    def health(self) -> ModuleHealth:
        return ModuleHealth.OK if self._running else ModuleHealth.FAILED
        
    def status(self) -> str:
        return f"Recovered {self._recovered_count} agents"
        
    def metrics(self) -> Dict[str, Any]:
        return {"recovered_count": self._recovered_count}
