"""
RRK Workflow State Primitives.

Defines the state machine vocabulary, recovery event model, and workflow memory
used by the generic WorkflowEngine and all concrete workflow implementations
(POD, App, Website, Business, etc.).
"""

import time
import uuid
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Workflow-level state (the lifecycle of a workflow execution)
# ---------------------------------------------------------------------------

class WorkflowPhase(str, Enum):
    """High-level lifecycle phase of a workflow execution."""
    PENDING = "pending"
    RUNNING = "running"
    RECOVERING = "recovering"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


# ---------------------------------------------------------------------------
# Recovery event model — exceptions become structured data
# ---------------------------------------------------------------------------

class RecoverySeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class RecoveryStrategy(str, Enum):
    """What the engine should do when a quality failure occurs."""
    RETRY_SAME = "retry_same"           # Re-run the same state with identical inputs
    REGENERATE = "regenerate"           # Rewind to a generation state
    MODIFY_PROMPT = "modify_prompt"     # Rewrite the prompt before regeneration
    ESCALATE = "escalate"              # Requires human intervention
    ABORT = "abort"                    # Unrecoverable — stop the workflow


class WorkflowEvent(BaseModel):
    """
    Structured recovery event.  Exceptions are converted into these so the
    engine can reason about *why* something failed and *how* to recover,
    rather than just catching a generic exception and retrying blindly.
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: float = Field(default_factory=time.time)
    event_type: str                     # e.g. "QUALITY_FAILURE", "GENERATION_ERROR"
    source: str                         # e.g. "typography_scan", "comfyui_provider"
    severity: RecoverySeverity = RecoverySeverity.MEDIUM
    recovery: RecoveryStrategy = RecoveryStrategy.REGENERATE
    detail: str = ""                    # Human-readable description
    metadata: Dict[str, Any] = Field(default_factory=dict)


# ---------------------------------------------------------------------------
# Workflow step definition — what each concrete workflow declares
# ---------------------------------------------------------------------------

class StepDefinition(BaseModel):
    """
    A single state in a workflow's pipeline.
    Concrete workflows (PodWorkflow, AppWorkflow, ...) declare a list of these.
    """
    name: str                           # e.g. "concept_analysis"
    display_name: str = ""              # e.g. "Concept Analysis" (for Dashboard)
    rewind_target: Optional[str] = None # On failure, rewind to this step name
    max_retries: int = 3
    recoverable: bool = True            # If False, failure is always fatal


# ---------------------------------------------------------------------------
# Workflow execution record — tracks runtime state of a single execution
# ---------------------------------------------------------------------------

class WorkflowExecution(BaseModel):
    """
    The runtime record of a workflow execution.
    Persisted by the engine so recovery survives restarts.
    """
    execution_id: str = Field(default_factory=lambda: f"WFEXEC-{uuid.uuid4().hex[:10].upper()}")
    workflow_type: str                  # e.g. "pod_generation", "app_build"
    phase: WorkflowPhase = WorkflowPhase.PENDING
    current_step: int = 0
    step_retries: Dict[str, int] = Field(default_factory=dict)
    total_rewinds: int = 0
    max_total_rewinds: int = 6
    context: Dict[str, Any] = Field(default_factory=dict)
    events: List[WorkflowEvent] = Field(default_factory=list)
    created_at: float = Field(default_factory=time.time)
    completed_at: Optional[float] = None
    result: Optional[str] = None        # Final status message or output path


# ---------------------------------------------------------------------------
# Workflow memory — learn from failures
# ---------------------------------------------------------------------------

class WorkflowMemoryEntry(BaseModel):
    """
    A single lesson learned from a workflow execution.
    Stored so future executions can pre-emptively avoid known failure modes.
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: float = Field(default_factory=time.time)
    workflow_type: str
    failure_source: str                 # e.g. "typography_scan"
    failure_type: str                   # e.g. "TypographyContaminationError"
    original_context: Dict[str, Any] = Field(default_factory=dict)
    resolution: str = ""                # e.g. "Added negative prompt: avoid readable text"
    recovery_strategy_used: RecoveryStrategy = RecoveryStrategy.REGENERATE
    success: bool = False               # Did the recovery actually work?


class WorkflowMemory:
    """
    In-memory store of lessons learned from past workflow executions.
    Consulted by the engine before generation to pre-emptively avoid known failures.
    """

    def __init__(self):
        self._entries: List[WorkflowMemoryEntry] = []

    def record(self, entry: WorkflowMemoryEntry) -> None:
        self._entries.append(entry)

    def query(self, workflow_type: str, failure_source: str = "") -> List[WorkflowMemoryEntry]:
        """Find past lessons relevant to this workflow type and failure source."""
        results = [e for e in self._entries if e.workflow_type == workflow_type]
        if failure_source:
            results = [e for e in results if e.failure_source == failure_source]
        return results

    def successful_resolutions(self, workflow_type: str, failure_type: str) -> List[str]:
        """Return resolution strings that actually worked for this failure type."""
        return [
            e.resolution for e in self._entries
            if e.workflow_type == workflow_type
            and e.failure_type == failure_type
            and e.success
        ]
