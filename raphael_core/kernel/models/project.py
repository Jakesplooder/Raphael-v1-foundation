from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
import time
import uuid

class ProjectStatus(str, Enum):
    PLANNED = "planned"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    ARCHIVED = "archived"

class ProjectHealth(str, Enum):
    ON_TRACK = "on_track"
    AT_RISK = "at_risk"
    OFF_TRACK = "off_track"
    UNKNOWN = "unknown"

class ProjectContext(BaseModel):
    goals: List[str] = Field(default_factory=list)
    requirements: List[str] = Field(default_factory=list)
    risks: List[str] = Field(default_factory=list)
    last_updated: float = Field(default_factory=time.time)

class Project(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    slug: str
    path: str
    status: ProjectStatus = ProjectStatus.PLANNED
    health: ProjectHealth = ProjectHealth.UNKNOWN
    type: str = "Standard"
    context: ProjectContext = Field(default_factory=ProjectContext)
    files: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
