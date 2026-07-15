from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime
import uuid

class BuildRequest(BaseModel):
    id: str = Field(default_factory=lambda: f"BUILD-{uuid.uuid4().hex[:8].upper()}")
    description: str
    requester: str = "User"
    timestamp: float = Field(default_factory=datetime.now().timestamp)
    metadata: Dict[str, Any] = Field(default_factory=dict)

class BuildClassification(BaseModel):
    id: str = Field(default_factory=lambda: f"BCLASS-{uuid.uuid4().hex[:8].upper()}")
    request_id: str
    complexity_level: int
    complexity_label: str
    build_type: str
    recommended_route: str
    required_councils: List[str] = Field(default_factory=list)
    assigned_agent: str = "Developer Agent"
    external_risk_flags: List[str] = Field(default_factory=list)

class BuildPlan(BaseModel):
    id: str = Field(default_factory=lambda: f"BPLAN-{uuid.uuid4().hex[:8].upper()}")
    request_id: str
    architecture: str
    files: List[str]
    steps: List[str]
    dependencies: List[str] = Field(default_factory=list)

class BuildArtifact(BaseModel):
    id: str = Field(default_factory=lambda: f"BART-{uuid.uuid4().hex[:8].upper()}")
    request_id: str
    path: str
    file_type: str
    hash: Optional[str] = None

from enum import Enum

class WorkspaceState(str, Enum):
    EMPTY = "EMPTY"
    SCAFFOLDED = "SCAFFOLDED"
    GENERATED = "GENERATED"
    BUILDING = "BUILDING"
    FAILED = "FAILED"
    PATCHING = "PATCHING"
    REVIEWING = "REVIEWING"
    COMPLETE = "COMPLETE"

class BuildWorkspace(BaseModel):
    id: str = Field(default_factory=lambda: f"BWS-{uuid.uuid4().hex[:8].upper()}")
    request_id: str
    provider: str
    location: str
    status: WorkspaceState = WorkspaceState.EMPTY

class BuildReview(BaseModel):
    id: str = Field(default_factory=lambda: f"BREV-{uuid.uuid4().hex[:8].upper()}")
    request_id: str
    reviewer: str
    approved: bool
    feedback: str
    timestamp: float = Field(default_factory=datetime.now().timestamp)

class BuildExecution(BaseModel):
    id: str = Field(default_factory=lambda: f"BEXEC-{uuid.uuid4().hex[:8].upper()}")
    request_id: str
    provider: str
    status: str = "pending"
    logs: List[str] = Field(default_factory=list)
    error: Optional[str] = None
