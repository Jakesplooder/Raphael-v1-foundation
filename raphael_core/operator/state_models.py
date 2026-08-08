from typing import Dict, Any, List, Optional
from datetime import datetime

class Artifact:
    def __init__(self, name: str, path: str, type: str, size: Optional[int] = None):
        self.name = name
        self.path = path
        self.type = type
        self.size = size

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "path": self.path,
            "type": self.type,
            "size": self.size
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Artifact':
        return cls(
            name=data.get("name", ""),
            path=data.get("path", ""),
            type=data.get("type", "unknown"),
            size=data.get("size")
        )

class ExecutionContext:
    def __init__(self, source: str, session_id: str, initiated_by: str, workflow_id: Optional[str] = None):
        self.source = source
        self.session_id = session_id
        self.initiated_by = initiated_by
        self.workflow_id = workflow_id

    def to_dict(self) -> Dict[str, Any]:
        return {
            "source": self.source,
            "session_id": self.session_id,
            "initiated_by": self.initiated_by,
            "workflow_id": self.workflow_id
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ExecutionContext':
        return cls(
            source=data.get("source", "unknown"),
            session_id=data.get("session_id", ""),
            initiated_by=data.get("initiated_by", "system"),
            workflow_id=data.get("workflow_id")
        )

class PendingMission:
    def __init__(
        self,
        mission_id: str,
        proposal: Dict[str, Any],
        context: ExecutionContext,
        status: str = "PENDING_APPROVAL",
        created_at: Optional[str] = None
    ):
        self.mission_id = mission_id
        self.proposal = proposal
        self.context = context
        self.status = status
        self.created_at = created_at or datetime.utcnow().isoformat() + "Z"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "mission_id": self.mission_id,
            "proposal": self.proposal,
            "context": self.context.to_dict(),
            "status": self.status,
            "created_at": self.created_at
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PendingMission':
        return cls(
            mission_id=data["mission_id"],
            proposal=data["proposal"],
            context=ExecutionContext.from_dict(data.get("context", {})),
            status=data.get("status", "PENDING_APPROVAL"),
            created_at=data.get("created_at")
        )

class WorkflowExecution:
    def __init__(
        self,
        execution_id: str,
        mission_id: str,
        correlation_id: str,
        workflow_id: str,
        context: ExecutionContext,
        status: str = "QUEUED",
        progress_percent: int = 0,
        current_node: str = "",
        completed_nodes: Optional[List[str]] = None,
        failed_nodes: Optional[List[str]] = None,
        started_at: Optional[str] = None,
        updated_at: Optional[str] = None,
        completed_at: Optional[str] = None,
        logs: Optional[List[Dict[str, Any]]] = None,
        artifacts: Optional[List[Artifact]] = None,
        metrics: Optional[Dict[str, Any]] = None
    ):
        self.execution_id = execution_id
        self.mission_id = mission_id
        self.correlation_id = correlation_id
        self.workflow_id = workflow_id
        self.context = context
        
        self.status = status
        self.progress_percent = progress_percent
        self.current_node = current_node
        self.completed_nodes = completed_nodes or []
        self.failed_nodes = failed_nodes or []
        
        self.started_at = started_at or datetime.utcnow().isoformat() + "Z"
        self.updated_at = updated_at or self.started_at
        self.completed_at = completed_at
        
        self.logs = logs or []
        self.artifacts = artifacts or []
        self.metrics = metrics or {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "execution_id": self.execution_id,
            "mission_id": self.mission_id,
            "correlation_id": self.correlation_id,
            "workflow_id": self.workflow_id,
            "context": self.context.to_dict(),
            "status": self.status,
            "progress_percent": self.progress_percent,
            "current_node": self.current_node,
            "completed_nodes": self.completed_nodes,
            "failed_nodes": self.failed_nodes,
            "started_at": self.started_at,
            "updated_at": self.updated_at,
            "completed_at": self.completed_at,
            "logs": self.logs,
            "artifacts": [a.to_dict() for a in self.artifacts],
            "metrics": self.metrics
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'WorkflowExecution':
        return cls(
            execution_id=data["execution_id"],
            mission_id=data["mission_id"],
            correlation_id=data["correlation_id"],
            workflow_id=data["workflow_id"],
            context=ExecutionContext.from_dict(data.get("context", {})),
            status=data.get("status", "QUEUED"),
            progress_percent=data.get("progress_percent", 0),
            current_node=data.get("current_node", ""),
            completed_nodes=data.get("completed_nodes", []),
            failed_nodes=data.get("failed_nodes", []),
            started_at=data.get("started_at"),
            updated_at=data.get("updated_at"),
            completed_at=data.get("completed_at"),
            logs=data.get("logs", []),
            artifacts=[Artifact.from_dict(a) for a in data.get("artifacts", [])],
            metrics=data.get("metrics", {})
        )
