import asyncio
import uuid
import time
import logging
from typing import Dict, Any, Optional

from ..interfaces import ServiceModule, ModuleHealth, Event, EventType, EventPriority
from ..event_bus import global_event_bus
from ..state import store
from ..storage import KernelStorage
from pydantic import BaseModel, Field

logger = logging.getLogger("kernel.mission_dispatcher")

class MissionRecord(BaseModel):
    id: str
    business_id: Optional[str] = None
    initiative_id: Optional[str] = None
    objective: str
    business_impact: Optional[str] = None
    status: str = "planning" # planning, running, paused, completed, failed
    owner_council: Optional[str] = None
    assigned_agents: list[str] = Field(default_factory=list)
    current_workflow_stage: Optional[str] = None
    
    # Execution & Telemetry Layer
    assets_created: list[str] = Field(default_factory=list) # Asset IDs
    distribution_channels: list[str] = Field(default_factory=list)
    metrics: Dict[str, float] = Field(default_factory=lambda: {
        "reach": 0,
        "ctr": 0.0,
        "clicks": 0
    })
    experiments: list[str] = Field(default_factory=list) # Experiment IDs
    lessons: list[str] = Field(default_factory=list) # Lesson IDs
    revenue_impact: float = 0.0
    roi_expected: Optional[float] = None
    
    # Internal state
    external_resources: list[str] = Field(default_factory=list)
    outputs: dict[str, str] = Field(default_factory=dict)
    logs: list[str] = Field(default_factory=list)
    decisions: list[str] = Field(default_factory=list)
    human_approvals_needed: list[str] = Field(default_factory=list)
    recovery_state: dict[str, Any] = Field(default_factory=dict)
    start_time: float = Field(default_factory=time.time)
    
class MissionDispatcher(ServiceModule):
    """
    80.9 Mission Dispatcher
    Handles executable COMMAND intents. Coordinates the mission lifecycle
    and emits rich OS-level events to drive the Matrix View UI.
    """
    def __init__(self):
        self._running = False
        self._active_missions: Dict[str, MissionRecord] = {}
        self.storage = KernelStorage(base_dir="raphael_storage")
        self._load_persisted_missions()
        
    def _load_persisted_missions(self):
        mission_files = self.storage.query("missions")
        for filename in mission_files:
            data = self.storage.load("missions", filename)
            if data:
                try:
                    record = MissionRecord(**data)
                    self._active_missions[record.id] = record
                except Exception as e:
                    logger.error(f"Failed to load mission {filename}: {e}")
                    
    def _save_mission(self, mission_id: str):
        if mission_id in self._active_missions:
            record = self._active_missions[mission_id]
            self.storage.save("missions", f"{mission_id}.json", record.model_dump())
        
    @property
    def name(self) -> str:
        return "MissionDispatcher"
        
    @property
    def depends_on(self) -> list[str]:
        return ["EventBus", "IntentRouter"]
        
    async def initialize(self) -> None:
        store.set_state(self.name, "status", "initialized")
        
    async def start(self) -> None:
        self._running = True
        store.set_state(self.name, "status", "running")
        
    async def heartbeat(self) -> bool:
        return self._running
        
    async def stop(self) -> None:
        self._running = False
        store.set_state(self.name, "status", "stopped")
        
    async def shutdown(self) -> None:
        pass
        
    def health(self) -> ModuleHealth:
        return ModuleHealth.OK if self._running else ModuleHealth.FAILED
        
    def status(self) -> str:
        return f"Online. {len(self._active_missions)} active missions."
        
    def metrics(self) -> Dict[str, Any]:
        return {"active_missions": len(self._active_missions)}
        
    async def dispatch_mission(self, prompt: str) -> str:
        """
        Takes a COMMAND prompt, creates a MissionID, and starts the lifecycle sequence.
        Returns the MissionID immediately so the Gateway can respond.
        """
        mission_id = str(uuid.uuid4())
        record = MissionRecord(
            id=mission_id,
            objective=prompt,
            status="planning"
        )
        self._active_missions[mission_id] = record
        self._save_mission(mission_id)
        
        # Fire and forget the background orchestration
        asyncio.create_task(self._orchestrate_mission(mission_id, prompt))
        return mission_id

    async def _orchestrate_mission(self, mission_id: str, prompt: str):
        """
        Simulates or drives the real mission execution lifecycle, emitting events 
        at each stage for the UI timeline.
        """
        try:
            # 1. Intent Received / Planning
            await self._emit_state(
                mission_id=mission_id,
                event_type=EventType.WORKFLOW_STARTED,
                council="Executive Council",
                agent="Mission Planner",
                payload={"message": f"Planning mission: '{prompt}'", "state": "Listening"}
            )
            await asyncio.sleep(1.5)
            
            # 2. Assigning to Councils
            # We derive a pseudo-council based on keyword for simulation 
            # (In production, this talks to Executor/Planner)
            assigned_council = "Research Council"
            assigned_agent = "Data Analyst"
            if "build" in prompt.lower() or "generate" in prompt.lower():
                assigned_council = "Business Council"
                assigned_agent = "Creative Director"
            elif "deploy" in prompt.lower():
                assigned_council = "Operations Council"
                assigned_agent = "DevOps Engineer"
                
            await self._emit_state(
                mission_id=mission_id,
                event_type=EventType.AGENT_TASK_ASSIGNED,
                council=assigned_council,
                agent=assigned_agent,
                payload={"message": f"Delegated to {assigned_council}", "state": "Delegating"}
            )
            await asyncio.sleep(2.0)
            
            # 3. Executing (Working on it)
            await self._emit_state(
                mission_id=mission_id,
                event_type=EventType.AGENT_REASONING_STARTED,
                council=assigned_council,
                agent=assigned_agent,
                payload={"message": f"{assigned_agent} is executing tasks...", "state": "Executing"}
            )
            await asyncio.sleep(2.5)
            
            # 4. QA / Review
            await self._emit_state(
                mission_id=mission_id,
                event_type=EventType.BUILD_REVIEW_REQUESTED,
                council="Executive Council",
                agent="QA Lead",
                payload={"message": "Performing Quality Assurance check.", "state": "Reasoning"}
            )
            await asyncio.sleep(1.5)
            
            # 5. Completed
            self._active_missions[mission_id].status = "completed"
            self._save_mission(mission_id)
            await self._emit_state(
                mission_id=mission_id,
                event_type=EventType.WORKFLOW_COMPLETED,
                council="Executive Council",
                agent="Mission Planner",
                payload={"message": "Mission successfully completed and finalized.", "state": "Completed"}
            )
            
            # 6. Memory Update
            await self._emit_state(
                mission_id=mission_id,
                event_type=EventType.MEMORY_UPDATED,
                council="Memory",
                agent="Archivist",
                payload={"message": "Mission outcomes persisted to Long-Term Memory", "state": "Learning"}
            )
            
        except Exception as e:
            logger.error(f"Mission {mission_id} failed: {e}")
            self._active_missions[mission_id].status = "failed"
            self._active_missions[mission_id].logs.append(str(e))
            self._save_mission(mission_id)
            await self._emit_state(
                mission_id=mission_id,
                event_type=EventType.WORKFLOW_FAILED,
                council="Executive Council",
                agent="Mission Planner",
                payload={"message": f"Mission Failed: {str(e)}", "state": "Failed"}
            )

    async def _emit_state(
        self, 
        mission_id: str, 
        event_type: EventType, 
        council: str, 
        agent: str, 
        payload: Dict[str, Any]
    ):
        event = Event(
            source="MissionDispatcher",
            type=event_type,
            mission_id=mission_id,
            council=council,
            agent=agent,
            payload=payload
        )
        await global_event_bus.publish(event)
