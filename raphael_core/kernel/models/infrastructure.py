import time
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

class InfrastructureState(str, Enum):
    INITIALIZING = "initializing"
    READY = "ready"
    DEGRADED = "degraded"
    RECOVERING = "recovering"
    STOPPING = "stopping"
    OFFLINE = "offline"

class HealthSeverity(str, Enum):
    HEALTHY = "healthy"
    WARNING = "warning"
    DEGRADED = "degraded"
    CRITICAL = "critical"
    OFFLINE = "offline"

class DependencyState(str, Enum):
    SATISFIED = "satisfied"
    WAITING = "waiting"
    MISSING = "missing"
    DEGRADED = "degraded"
    BLOCKED = "blocked"

class ServiceCapability(str, Enum):
    IMAGE_GENERATION = "image_generation"
    VECTOR_SEARCH = "vector_search"
    VOICE_SYNTHESIS = "voice_synthesis"
    SPEECH_RECOGNITION = "speech_recognition"
    LLM_INFERENCE = "llm_inference"
    CONTAINER_ORCHESTRATION = "container_orchestration"
    HOST_EXECUTION = "host_execution"
    CREATIVE = "creative"
    BUILDER = "builder"
    RESEARCH = "research"
    RAG = "rag"
    EXECUTIVE = "executive"
    PREDICTION = "prediction"

class ServicePolicy(str, Enum):
    AUTO = "auto"
    MANUAL = "manual"
    ON_DEMAND = "on_demand"
    RECOVERY_ONLY = "recovery_only"
    DISABLED = "disabled"

class InfrastructureEvent(BaseModel):
    event_type: str
    timestamp: float = Field(default_factory=time.time)
    service_id: Optional[str] = None
    details: Dict[str, Any] = Field(default_factory=dict)

class DependencyInfo(BaseModel):
    service_id: str
    state: DependencyState
    message: str = ""

class HostProcess(BaseModel):
    pid: Optional[int] = None
    running: bool = False
    port_listening: Optional[bool] = None
    last_error: str = ""
    logs: str = ""
    metrics: Dict[str, Any] = Field(default_factory=dict)

class ContainerStatus(BaseModel):
    container_id: str = ""
    name: str = ""
    image: str = ""
    state: str = ""  # running, exited, etc.
    status: str = "" # "Up 2 hours", "Exited (1)"
    health: str = ""
    ports: List[str] = Field(default_factory=list)

class DockerHealth(BaseModel):
    available: bool = False
    version: str = ""
    containers: List[ContainerStatus] = Field(default_factory=list)
    images_count: int = 0
    volumes_count: int = 0
    networks_count: int = 0
    last_error: str = ""

class ServiceIdentity(BaseModel):
    service_id: str
    display_name: str
    category: str

class ServiceExecution(BaseModel):
    backend: str  # "docker", "host_agent", "internal"
    host_process: Optional[HostProcess] = None
    container: Optional[ContainerStatus] = None

class ServicePolicyState(BaseModel):
    startup: ServicePolicy = ServicePolicy.MANUAL
    notes: str = ""

class ServiceStatus(BaseModel):
    # Flattened representation of the 4 sections
    identity: ServiceIdentity
    execution: ServiceExecution
    policy: ServicePolicyState
    capabilities: List[ServiceCapability] = Field(default_factory=list)
    
    # State tracking
    severity: HealthSeverity = HealthSeverity.OFFLINE
    health_details: Dict[str, Any] = Field(default_factory=dict)
    dependencies: List[DependencyInfo] = Field(default_factory=list)
    display_url: str = ""

class InfrastructureSnapshot(BaseModel):
    timestamp: float = Field(default_factory=time.time)
    schema_version: str = "2.0"
    state: InfrastructureState = InfrastructureState.OFFLINE
    docker: DockerHealth = Field(default_factory=DockerHealth)
    services: Dict[str, ServiceStatus] = Field(default_factory=dict)
    capabilities: List[ServiceCapability] = Field(default_factory=list)
    overall_health: HealthSeverity = HealthSeverity.OFFLINE
    policies_active: Dict[str, int] = Field(default_factory=dict)
