import abc
import asyncio
from typing import Dict, Any, Optional

DEPRECATED = True
REPLACED_BY = "raphael_core.agents"

from .interfaces import ServiceModule, Job, JobState
from .observability import ObservabilityLayer
from .job_system import JobSystem


class AgentService(ServiceModule):
    """
    Base class for all Digital Workforce agents.
    Every agent is a first-class RRK service.
    """
    
    def __init__(self):
        super().__init__()
        import uuid
        from .interfaces import AgentState
        from .state import store
        
        self.agent_id = str(uuid.uuid4())
        self.generation = int(store.get_state(self.name, "generation", 0)) + 1
        store.set_state(self.name, "generation", self.generation)
        
        self._state = AgentState.CREATED
        self.current_job: Optional[Job] = None
        self.current_context: Dict[str, Any] = {}
        self.previous_context: Dict[str, Any] = {}
        self.conversation_ids: list[str] = []
        self.loaded_hypotheses: list[str] = []
        self.pending_events: list[Any] = []
        self.open_jobs: list[str] = []
        
        # Performance/Health metrics
        self.tokens_processed = 0
        self.last_latency = 0.0
        self.queue_depth = 0
    
    @property
    def state(self):
        return self._state
        
    def transition_to(self, new_state) -> None:
        """
        Transition the agent to a new lifecycle state.
        Emits AGENT_STATE_TRANSITION, triggering the AgentLifecycleManager to checkpoint.
        """
        from .interfaces import EventType
        old_state = self._state
        self._state = new_state
        self._publish_event(EventType.AGENT_STATE_TRANSITION, {
            "old_state": old_state.value,
            "new_state": new_state.value,
            "agent_id": self.agent_id,
            "generation": self.generation
        }, trace_id=self.agent_id)
        ObservabilityLayer.debug(self.name, f"Transitioned {old_state.value} -> {new_state.value}")

    def capabilities(self) -> Dict[str, Any]:
        """
        Rich capability profile for routing.
        """
        return {
            "general_reasoning": {
                "confidence": 0.8,
                "specialties": ["logic", "planning"]
            }
        }
    
    @property
    def depends_on(self) -> list[str]:
        # Agents now depend on the new 70.3 managers and SkillRegistry
        return ["WorldModelService", "EventBus", "JobSystem", "AgentLifecycleManager", "CheckpointManager", "RuntimeMetricsManager", "SkillRegistry"]
        
    async def initialize(self) -> None:
        from .interfaces import AgentState
        self.transition_to(AgentState.INITIALIZING)
        ObservabilityLayer.info(self.name, f"Initializing Agent: {self.name} (Gen {self.generation})")
        self.transition_to(AgentState.READY)
        
    async def start(self) -> None:
        from .interfaces import AgentState
        self.transition_to(AgentState.IDLE)
        ObservabilityLayer.info(self.name, f"Starting Agent: {self.name}")
        
    async def stop(self) -> None:
        from .interfaces import AgentState
        self.transition_to(AgentState.STOPPED)
        ObservabilityLayer.info(self.name, f"Stopping Agent: {self.name}")
        
    async def heartbeat(self) -> Dict[str, Any]:
        """
        Phase 70.3 Rich Heartbeat.
        Returns full state telemetry.
        """
        import sys
        
        return {
            "type": "agent",
            "generation": self.generation,
            "state": self._state.value,
            "last_job": self.current_job.id if self.current_job else None,
            "latency_sec": self.last_latency,
            "memory_mb": sys.getsizeof(self.current_context) / (1024 * 1024),
            "queue_depth": self.queue_depth,
            "reasoning_mode": "standard",
            "provider": "default",
            "tokens": self.tokens_processed,
            "context_size": len(str(self.current_context)),
            "temperature": 0.7,
            "last_exception": None
        }
        
    async def shutdown(self) -> None:
        pass
        
    def health(self) -> Any:
        from .interfaces import ModuleHealth
        if self._state.value in ("failed", "stopped"):
            return ModuleHealth.FAILED
        return ModuleHealth.OK
        
    def status(self) -> str:
        return f"State: {self._state.value} (Gen {self.generation})"
        
    def metrics(self) -> Dict[str, Any]:
        return {
            "performance_score": 100.0,
            "pressure_score": 0.0,
            "active_tasks": len(self.open_jobs),
            "trust_tier": "unknown",
            "lifecycle_state": self._state.value
        }

    def _publish_event(self, event_type, payload: Dict[str, Any], trace_id: str) -> None:
        from .registry import registry
        from .interfaces import Event, EventPriority
        bus = registry.get_service("EventBus")
        if bus:
            evt = Event(source=self.name, type=event_type, payload=payload, trace_id=trace_id, priority=EventPriority.NORMAL)
            asyncio.create_task(bus.publish(evt))

    async def execute_skill(self, skill_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Natively execute a shared skill via the SkillRegistry.
        Automatically propagates the current job's trace_id and agent's trust tier.
        """
        from .registry import registry
        skill_registry = registry.get_service("SkillRegistry")
        if not skill_registry:
            return {"success": False, "error": "SkillRegistry is not available in the kernel."}
            
        trace_id = self.current_job.trace_id if self.current_job else self.agent_id
        
        # We assume tier 1 for base agents until explicit trust tier properties are mapped from World Model
        agent_tier = 1 
        
        return await skill_registry.invoke(skill_name, params, trace_id=trace_id, agent_tier=agent_tier)

    async def execute_job(self, job: Job) -> Dict[str, Any]:
        """
        Wrapper around process_job to emit required telemetry and state transitions.
        """
        from .interfaces import EventType, AgentState
        import time
        
        start_time = time.time()
        self.current_job = job
        self.transition_to(AgentState.EXECUTING)
        self._publish_event(EventType.JOB_STATE_CHANGED, {"job_id": job.id, "state": "started"}, job.trace_id)
        
        try:
            self.transition_to(AgentState.THINKING)
            result = await self.process_job(job)
            self.last_latency = time.time() - start_time
            self.transition_to(AgentState.IDLE)
            self._publish_event(EventType.JOB_STATE_CHANGED, {"job_id": job.id, "state": "completed", "result": result}, job.trace_id)
            self.current_job = None
            return result
        except Exception as e:
            self.last_latency = time.time() - start_time
            self.transition_to(AgentState.FAILED)
            self._publish_event(EventType.JOB_STATE_CHANGED, {"job_id": job.id, "state": "failed", "error": str(e)}, job.trace_id)
            self.current_job = None
            # Recovering immediately for OS resilience
            self.transition_to(AgentState.RECOVERING)
            self.transition_to(AgentState.IDLE)
            raise e

    @abc.abstractmethod
    async def process_job(self, job: Job) -> Dict[str, Any]:
        """
        Core agent execution loop. All outputs logged via ObservabilityLayer.
        Should return a dictionary containing the result or state update.
        """
        pass
