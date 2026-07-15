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


class MemoryTier(str, Enum):
    """Semantic isolation tiers for memory cognitive layering."""
    WORKING = "working"      # TTL: minutes (Current workflow/conversation)
    SESSION = "session"      # TTL: days (Today's work/project context)
    LONG_TERM = "long_term"  # TTL: forever (Preferences, design decisions, projects)
    ARCHIVE = "archive"      # Rarely searched, highly compressed


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
    INFRASTRUCTURE_ALERT = "infrastructure_alert"
    
    # Builder Lifecycle
    BUILD_REQUESTED = "build_requested"
    BUILD_CLASSIFIED = "build_classified"
    BUILD_PLANNED = "build_planned"
    BUILD_GENERATION_STARTED = "build_generation_started"
    BUILD_GENERATION_FINISHED = "build_generation_finished"
    BUILD_REVIEW_REQUESTED = "build_review_requested"
    BUILD_APPROVED = "build_approved"
    BUILD_FAILED = "build_failed"
    
    # Cognitive / Observation
    GOAL_CREATED = "goal_created"
    TASK_COMPLETED = "task_completed"
    PROJECT_CREATED = "project_created"
    USER_DECISION = "user_decision"
    ERROR_OCCURRED = "error_occurred"
    
    # Memory Lifecycle
    MEMORY_STORED = "memory_stored"
    MEMORY_RETRIEVED = "memory_retrieved"
    MEMORY_UPDATED = "memory_updated"
    MEMORY_ARCHIVED = "memory_archived"
    MEMORY_FORGOTTEN = "memory_forgotten"
    
    # Knowledge Lifecycle
    KNOWLEDGE_CREATED = "knowledge_created"
    KNOWLEDGE_UPDATED = "knowledge_updated"
    KNOWLEDGE_DELETED = "knowledge_deleted"
    KNOWLEDGE_ANALYZED = "knowledge_analyzed"
    KNOWLEDGE_PROMOTED_TO_MEMORY = "knowledge_promoted_to_memory"
    
    # Workflow Execution Lifecycle
    WORKFLOW_CREATED = "workflow_created"
    WORKFLOW_QUEUED = "workflow_queued"
    WORKFLOW_STARTED = "workflow_started"
    WORKFLOW_STEP_STARTED = "workflow_step_started"
    WORKFLOW_STEP_COMPLETED = "workflow_step_completed"
    WORKFLOW_RETRYING = "workflow_retrying"
    WORKFLOW_FAILED = "workflow_failed"
    WORKFLOW_CANCELLED = "workflow_cancelled"
    
    # Agent Lifecycle
    AGENT_CREATED = "agent_created"
    AGENT_ACTIVATED = "agent_activated"
    AGENT_DEACTIVATED = "agent_deactivated"
    AGENT_TASK_ASSIGNED = "agent_task_assigned"
    AGENT_REASONING_STARTED = "agent_reasoning_started"
    AGENT_REASONING_COMPLETED = "agent_reasoning_completed"
    AGENT_FAILED = "agent_failed"
    AGENT_PERMISSION_DENIED = "agent_permission_denied"
    AGENT_WORKFLOW_REQUESTED = "agent_workflow_requested"
    AGENT_MEMORY_PROMOTION_REQUESTED = "agent_memory_promotion_requested"
    AGENT_MODEL_CHANGED = "agent_model_changed"
    
    # Agent Outcomes
    AGENT_TASK_COMPLETED = "agent_task_completed"
    AGENT_LESSON_LEARNED = "agent_lesson_learned"
    AGENT_STRATEGIC_OUTCOME = "agent_strategic_outcome"
    
    # Motivational Layer
    GOAL_COMPLETED = "goal_completed"
    GOAL_FAILED = "goal_failed"
    
    OBJECTIVE_CREATED = "objective_created"
    OBJECTIVE_COMPLETED = "objective_completed"
    OBJECTIVE_FAILED = "objective_failed"
    
    TASK_CREATED = "task_created"
    TASK_ASSIGNED = "task_assigned"
    TASK_FAILED = "task_failed"
    
    # World Model Lifecycle
    WORLD_NODE_CREATED = "world_node_created"
    WORLD_NODE_UPDATED = "world_node_updated"
    WORLD_RELATIONSHIP_CREATED = "world_relationship_created"
    WORLD_CONFLICT_DETECTED = "world_conflict_detected"
    
    # World Model Epistemics
    WORLD_OBSERVATION_RECEIVED = "world_observation_received"
    WORLD_HYPOTHESIS_CREATED = "world_hypothesis_created"
    WORLD_HYPOTHESIS_CONFIRMED = "world_hypothesis_confirmed"
    WORLD_HYPOTHESIS_REJECTED = "world_hypothesis_rejected"
    
    # Commerce & POD Lifecycle
    COMMERCE_PRODUCT_REQUESTED = "commerce_product_requested"
    COMMERCE_CONCEPT_READY = "commerce_concept_ready"
    COMMERCE_IMAGE_GENERATED = "commerce_image_generated"
    COMMERCE_UPSCALE_COMPLETED = "commerce_upscale_completed"
    COMMERCE_MOCKUP_READY = "commerce_mockup_ready"
    COMMERCE_SEO_READY = "commerce_seo_ready"
    COMMERCE_LISTING_CREATED = "commerce_listing_created"
    COMMERCE_PRODUCT_PUBLISHED = "commerce_product_published"
    COMMERCE_SALES_SYNCED = "commerce_sales_synced"

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
        try:
            health_val = self.health().value
        except AttributeError:
            health_val = str(self.health())
            
        return {
            "name": self.name,
            "dependencies": self.depends_on() if callable(self.depends_on) else self.depends_on,
            "status": self.status(),
            "health": health_val,
            "metadata": self.version()
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

    def snapshot(self) -> Dict[str, Any]:
        """Return a point-in-time state snapshot of this module."""
        return {}

    def version(self) -> Dict[str, Any]:
        """Return module versioning metadata."""
        return {
            "module": self.name.lower().replace("manager", ""),
            "version": "1.0.0",
            "schema": 1,
            "migration": "Legacy",
            "owner": self.name
        }
