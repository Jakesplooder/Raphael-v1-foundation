import abc
from enum import Enum
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field
import uuid
import time


class ModuleHealth(str, Enum):
    OK = "ok"
    DEGRADED = "degraded"
    FAILED = "failed"
    UNKNOWN = "unknown"
    STARTING = "starting"
    SHUTDOWN = "shutdown"


class EventPriority(int, Enum):
    LOW = 0
    NORMAL = 1
    HIGH = 2
    CRITICAL = 3


class EventType(str, Enum):
    # Volatile
    HEARTBEAT = "heartbeat"
    METRIC_EMITTED = "metric_emitted"
    TOKEN_STREAMED = "token_streamed"
    MOUSE_MOVED = "mouse_moved"
    
    # Durable
    PLAN_APPROVED = "plan_approved"
    WORKFLOW_COMPLETED = "workflow_completed"
    PREDICTION_CREATED = "prediction_created"
    AUTHORITY_GRANTED = "authority_granted"
    JOB_STATE_CHANGED = "job_state_changed"
    AGENT_STATE_TRANSITION = "agent_state_transition"
    CHECKPOINT_REQUESTED = "checkpoint_requested"


class Event(BaseModel):
    """The strict event schema for the Hybrid Event Bus."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: float = Field(default_factory=time.time)
    trace_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    source: str
    target: Optional[str] = None
    type: EventType
    priority: EventPriority = EventPriority.NORMAL
    payload: Dict[str, Any] = Field(default_factory=dict)
    
    @property
    def is_durable(self) -> bool:
        """Determines if the event must survive a hard crash (SQLite) vs Memory queue."""
        # Define durable events vs volatile
        durable_types = {
            EventType.PLAN_APPROVED,
            EventType.WORKFLOW_COMPLETED,
            EventType.PREDICTION_CREATED,
            EventType.AUTHORITY_GRANTED,
            EventType.JOB_STATE_CHANGED,
            EventType.AGENT_STATE_TRANSITION
        }
        return self.type in durable_types


class AgentState(str, Enum):
    """The strict state machine for all agents."""
    CREATED = "created"
    INITIALIZING = "initializing"
    READY = "ready"
    IDLE = "idle"
    THINKING = "thinking"
    WAITING = "waiting"
    EXECUTING = "executing"
    BLOCKED = "blocked"
    PAUSED = "paused"
    FAILED = "failed"
    RECOVERING = "recovering"
    STOPPED = "stopped"


class JobState(str, Enum):
    QUEUED = "queued"
    RUNNING = "running"
    PAUSED = "paused"
    WAITING = "waiting"
    RETRYING = "retrying"
    FAILED = "failed"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class Job(BaseModel):
    """A rich unit of work managed by the Job System."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: float = Field(default_factory=time.time)
    state: JobState = JobState.QUEUED
    priority: int = 0
    owner: str
    module: str
    retry_count: int = 0
    max_retries: int = 3
    deadline: Optional[float] = None
    authority: str = "standard"
    cost: float = 0.0
    estimated_duration: Optional[float] = None
    payload: Dict[str, Any] = Field(default_factory=dict)
    trace_id: str


class ServiceModule(abc.ABC):
    """
    The universal Service Contract for all RRK Modules.
    No exceptions. Every module must expose these methods.
    """
    
    @property
    @abc.abstractmethod
    def name(self) -> str:
        """Unique identifier for this service."""
        pass

    @property
    def depends_on(self) -> list[str]:
        """List of service names this module requires to function."""
        return []

    def manifest(self) -> Dict[str, Any]:
        """
        Self-describing manifest of this runtime component.
        """
        return {
            "name": self.name,
            "dependencies": self.depends_on,
            "status": self.status(),
            "health": self.health().value
        }

    @abc.abstractmethod
    async def initialize(self) -> None:
        """One-time setup (e.g., creating DB tables). Does not start processing."""
        pass

    @abc.abstractmethod
    async def start(self) -> None:
        """Begin processing workloads (subscribe to events, start loops)."""
        pass

    @abc.abstractmethod
    async def heartbeat(self) -> bool | Dict[str, Any]:
        """Return True for simple liveness, or a dict for rich OS-level telemetry."""
        pass

    @abc.abstractmethod
    async def stop(self) -> None:
        """Gracefully stop processing new workloads. Drain current tasks."""
        pass

    @abc.abstractmethod
    async def shutdown(self) -> None:
        """Teardown resources (close sockets, files, DB connections)."""
        pass

    @abc.abstractmethod
    def health(self) -> ModuleHealth:
        """Return the current health evaluation of the module."""
        pass

    @abc.abstractmethod
    def status(self) -> str:
        """Return a human-readable status (e.g., 'Processing 5 active jobs')."""
        pass

    @abc.abstractmethod
    def metrics(self) -> Dict[str, Any]:
        """Return internal module metrics (e.g., event counters, memory)."""
        pass
