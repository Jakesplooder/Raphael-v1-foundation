from pydantic import BaseModel, Field
from enum import Enum
from typing import List, Optional
import datetime

class GoalPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class GoalStatus(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    COMPLETED = "completed"
    FAILED = "failed"
    ABANDONED = "abandoned"

class TaskStatus(str, Enum):
    CREATED = "created"
    QUEUED = "queued"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    BLOCKED = "blocked"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class Goal(BaseModel):
    id: str
    title: str
    description: str
    priority: GoalPriority = GoalPriority.MEDIUM
    importance: str = "normal"  # normal, strategic
    status: GoalStatus = GoalStatus.DRAFT
    created_at: str = Field(default_factory=lambda: datetime.datetime.now().isoformat())

class Objective(BaseModel):
    id: str
    goal_id: str
    title: str
    status: GoalStatus = GoalStatus.DRAFT
    created_at: str = Field(default_factory=lambda: datetime.datetime.now().isoformat())

class Task(BaseModel):
    id: str
    objective_id: str
    title: str
    description: str
    status: TaskStatus = TaskStatus.CREATED
    assigned_agent_id: Optional[str] = None
    created_at: str = Field(default_factory=lambda: datetime.datetime.now().isoformat())
