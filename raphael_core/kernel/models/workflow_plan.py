from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
import time
import uuid

class WorkflowStatus(str, Enum):
    PENDING = "pending"
    VALIDATING = "validating"
    READY = "ready"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    ARCHIVED = "archived"

class StepStatus(str, Enum):
    PENDING = "pending"
    READY = "ready"
    STARTED = "started"
    COMPLETED = "completed"
    FAILED = "failed"
    BLOCKED = "blocked"
    SKIPPED = "skipped"
    RETRIED = "retried"
    CANCELLED = "cancelled"

class WorkflowContext(BaseModel):
    goal: Optional[str] = None
    project: Optional[str] = None
    workspace: Optional[str] = None
    builder_request: Optional[str] = None
    priority: int = 1
    owner: str = "system"
    created_by: str = "system"

class FailureRecovery(BaseModel):
    retry_policy: str = "none"  # none, linear, exponential
    rollback_policy: str = "none"  # none, automatic, manual
    timeout: int = 3600  # seconds
    max_retries: int = 0

class WorkflowStep(BaseModel):
    step_id: str
    name: str
    description: str = ""
    required_capabilities: List[str] = Field(default_factory=list)
    dependencies: List[str] = Field(default_factory=list)
    status: StepStatus = StepStatus.PENDING
    confidence: float = 0.0
    result: Dict[str, Any] = Field(default_factory=dict)
    recovery: FailureRecovery = Field(default_factory=FailureRecovery)
    metrics: Dict[str, Any] = Field(default_factory=dict)

class WorkflowPhase(BaseModel):
    phase_id: str
    name: str
    steps: Dict[str, WorkflowStep] = Field(default_factory=dict)

    @property
    def confidence(self) -> float:
        if not self.steps:
            return 0.0
        return sum(s.confidence for s in self.steps.values()) / len(self.steps)

class WorkflowTemplate(BaseModel):
    template_id: str
    name: str
    description: str = ""
    phases: Dict[str, WorkflowPhase] = Field(default_factory=dict)

class WorkflowPlan(BaseModel):
    plan_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    template_id: Optional[str] = None
    version: str = "1.0.0"
    parent_version: Optional[str] = None
    revision: int = 1
    status: WorkflowStatus = WorkflowStatus.PENDING
    phases: Dict[str, WorkflowPhase] = Field(default_factory=dict)
    context: WorkflowContext = Field(default_factory=WorkflowContext)
    estimated_time: str = "0h"
    risk: str = "Low"

    @property
    def confidence(self) -> float:
        if not self.phases:
            return 0.0
        return sum(p.confidence for p in self.phases.values()) / len(self.phases)

    def metrics(self) -> Dict[str, Any]:
        all_steps = [s for p in self.phases.values() for s in p.steps.values()]
        total = len(all_steps)
        if total == 0:
            return {}
        
        completed = sum(1 for s in all_steps if s.status == StepStatus.COMPLETED)
        failed = sum(1 for s in all_steps if s.status == StepStatus.FAILED)
        running = sum(1 for s in all_steps if s.status == StepStatus.STARTED)
        blocked = sum(1 for s in all_steps if s.status == StepStatus.BLOCKED)
        ready = sum(1 for s in all_steps if s.status == StepStatus.READY)
        
        return {
            "progress_percent": (completed / total) * 100,
            "completed_percent": (completed / total) * 100,
            "remaining_percent": ((total - completed) / total) * 100,
            "risk_percent": (failed / total) * 100 if total > 0 else 0,
            "confidence_percent": self.confidence * 100,
            "blocked_steps": blocked,
            "running_steps": running,
            "ready_steps": ready
        }

    def export_mermaid(self) -> str:
        lines = ["graph TD"]
        for p_id, phase in self.phases.items():
            lines.append(f"    subgraph {p_id} [{phase.name}]")
            for s_id, step in phase.steps.items():
                lines.append(f"        {s_id}[{step.name}]")
            lines.append("    end")
            
        for phase in self.phases.values():
            for s_id, step in phase.steps.items():
                for dep in step.dependencies:
                    lines.append(f"    {dep} --> {s_id}")
        return "\\n".join(lines)

    def export_graphviz(self) -> str:
        # Simplistic dot representation
        lines = ["digraph G {"]
        for phase in self.phases.values():
            for s_id, step in phase.steps.items():
                lines.append(f'    "{s_id}" [label="{step.name}"];')
                for dep in step.dependencies:
                    lines.append(f'    "{dep}" -> "{s_id}";')
        lines.append("}")
        return "\\n".join(lines)
