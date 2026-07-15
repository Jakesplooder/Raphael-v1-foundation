from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any, Union
from enum import Enum
import uuid
import time

class ConfidenceState(str, Enum):
    ACTIVE = "active"
    REVIEW_CANDIDATE = "review_candidate"
    DORMANT = "dormant"
    DEPRECATED = "deprecated"

class NodeStatus(str, Enum):
    ACTIVE = "active"
    PAUSED = "paused"
    ARCHIVED = "archived"
    DEPRECATED = "deprecated"
    CONFLICTED = "conflicted"

class WorldNode(BaseModel):
    """A fundamental entity in the World Model."""
    node_id: str
    node_type: str
    name: str
    summary: str
    status: str = "active"
    priority: str = "medium"
    created_at: Union[float, str] = Field(default_factory=time.time)
    updated_at: Union[float, str] = Field(default_factory=time.time)
    source_system: str
    source_reference: str
    confidence: float = 0.82
    confidence_state: ConfidenceState = ConfidenceState.ACTIVE
    tags: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)

class WorldRelationship(BaseModel):
    """A directed semantic edge between two WorldNodes."""
    relationship_id: str
    from_node: str
    to_node: str
    relationship_type: str
    summary: str
    confidence: float = 0.82
    confidence_state: ConfidenceState = ConfidenceState.ACTIVE
    evidence: List[Dict[str, Any]] = Field(default_factory=list)
    source_system: str
    source_reference: str
    source_trust: str = "C"
    created_at: Union[float, str] = Field(default_factory=time.time)
    updated_at: Union[float, str] = Field(default_factory=time.time)
    status: str = "active"

class WorldEvent(BaseModel):
    """An observation or historical milestone affecting the World."""
    event_id: str
    event_type: str
    event_time: Union[float, str] = Field(default_factory=time.time)
    cause: str
    effect: str
    outcome: str
    related_entities: List[str] = Field(default_factory=list)
    source_system: str
    source_reference: str
    confidence: float = 0.82
    importance_level: str = "important"
    status: str = "active"

class WorldHypothesis(BaseModel):
    """An uncertain proposition that the World Model tracks evidence for."""
    hypothesis_id: str
    statement: str
    generated_by: str
    confidence: float = 0.55
    supporting_evidence: List[Dict[str, Any]] = Field(default_factory=list)
    contradicting_evidence: List[Dict[str, Any]] = Field(default_factory=list)
    created_at: Union[float, str] = Field(default_factory=time.time)
    updated_at: Union[float, str] = Field(default_factory=time.time)
    status: str = "active"
