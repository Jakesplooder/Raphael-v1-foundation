from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
from enum import Enum
import time

class GenerationStatus(str, Enum):
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class GenerationRequest(BaseModel):
    """Renderer-agnostic request to generate an asset."""
    request_id: str
    business_id: Optional[str] = None
    mission_id: Optional[str] = None
    asset_type: str
    prompt: str
    style: Optional[str] = None
    dimensions: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    parent_asset_id: Optional[str] = None
    
class GenerationJob(BaseModel):
    """Tracks the execution of a generation request."""
    job_id: str
    request: GenerationRequest
    status: GenerationStatus = GenerationStatus.QUEUED
    progress: float = 0.0
    retry_count: int = 0
    max_retries: int = 3
    error_message: Optional[str] = None
    started_at: Optional[float] = None
    completed_at: Optional[float] = None
    asset_id: Optional[str] = None
    telemetry: Dict[str, Any] = Field(default_factory=dict)
