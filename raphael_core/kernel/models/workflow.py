import uuid
import time
from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class WorkflowStatus(str, Enum):
    CREATED = "created"
    QUEUED = "queued"
    RETRYING = "retrying"
    RUNNING = "running"
    PAUSED = "paused"
    FAILED = "failed"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class WorkflowStep(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    action: str
    parameters: Dict[str, Any] = Field(default_factory=dict)
    depends_on: List[str] = Field(default_factory=list)

class Workflow(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str = ""
    trigger: str = "manual"
    steps: List[WorkflowStep] = Field(default_factory=list)
    status: WorkflowStatus = WorkflowStatus.CREATED
    priority: int = 0
    created_at: float = Field(default_factory=time.time)
    importance: str = "normal"  # low, normal, high, strategic

class WorkflowExecution(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    workflow_id: str
    execution_date: float = Field(default_factory=time.time)
    status: WorkflowStatus = WorkflowStatus.CREATED
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    step_executions: Dict[str, WorkflowStatus] = Field(default_factory=dict)
