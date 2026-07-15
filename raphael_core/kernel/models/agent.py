from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
import datetime

class AgentStatus(str, Enum):
    CREATED = "created"
    INITIALIZING = "initializing"
    ACTIVE = "active"
    PAUSED = "paused"
    SUSPENDED = "suspended"
    FAILED = "failed"
    RETIRED = "retired"

class MemoryScope(str, Enum):
    NONE = "none"
    PERSONAL = "personal"
    BUSINESS = "business"
    DOMAIN = "domain"
    GLOBAL = "global"

class AgentDefinition(BaseModel):
    name: str
    role: str
    description: str
    capabilities: List[str] = Field(default_factory=list)
    permissions: List[str] = Field(default_factory=list)
    default_model: str = "default"

class AgentInstance(BaseModel):
    id: str
    definition: str  # References AgentDefinition.name (or ID)
    status: AgentStatus = AgentStatus.CREATED
    created_at: str = Field(default_factory=lambda: datetime.datetime.now().isoformat())
    memory_scope: MemoryScope = MemoryScope.NONE
    context: Dict[str, Any] = Field(default_factory=dict)
