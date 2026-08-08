import os
import json
from pathlib import Path
from typing import List, Optional, Protocol, Dict, Any
from .state_models import PendingMission, WorkflowExecution

class MissionRepository(Protocol):
    def save(self, mission: PendingMission) -> None: ...
    def get(self, mission_id: str) -> Optional[PendingMission]: ...
    def get_latest_for_session(self, session_id: str) -> Optional[PendingMission]: ...
    def list(self) -> List[PendingMission]: ...

class ExecutionRepository(Protocol):
    def save(self, execution: WorkflowExecution) -> None: ...
    def get(self, execution_id: str) -> Optional[WorkflowExecution]: ...
    def get_latest_for_session(self, session_id: str) -> Optional[WorkflowExecution]: ...
    def list(self) -> List[WorkflowExecution]: ...

class JsonMissionRepository:
    def __init__(self, storage_dir: Optional[str] = None):
        root = storage_dir or os.environ.get("RAPHAEL_DATA_DIR", "C:/Users/cyber/Downloads/RalphaelOS")
        self.path = Path(root) / "raphael_storage" / "operations" / "missions"
        self.path.mkdir(parents=True, exist_ok=True)

    def save(self, mission: PendingMission) -> None:
        file_path = self.path / f"{mission.mission_id}.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(mission.to_dict(), f, indent=2)

    def get(self, mission_id: str) -> Optional[PendingMission]:
        file_path = self.path / f"{mission_id}.json"
        if not file_path.exists():
            return None
        with open(file_path, "r", encoding="utf-8") as f:
            return PendingMission.from_dict(json.load(f))
            
    def get_latest_for_session(self, session_id: str) -> Optional[PendingMission]:
        missions = self.list()
        session_missions = [m for m in missions if m.context.session_id == session_id]
        if not session_missions:
            return None
        return max(session_missions, key=lambda m: m.created_at)

    def list(self) -> List[PendingMission]:
        missions = []
        for file_path in self.path.glob("*.json"):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    missions.append(PendingMission.from_dict(data))
            except Exception:
                pass
        return missions

class JsonExecutionRepository:
    def __init__(self, storage_dir: Optional[str] = None):
        root = storage_dir or os.environ.get("RAPHAEL_DATA_DIR", "C:/Users/cyber/Downloads/RalphaelOS")
        self.path = Path(root) / "raphael_storage" / "operations" / "executions"
        self.path.mkdir(parents=True, exist_ok=True)

    def save(self, execution: WorkflowExecution) -> None:
        file_path = self.path / f"{execution.execution_id}.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(execution.to_dict(), f, indent=2)

    def get(self, execution_id: str) -> Optional[WorkflowExecution]:
        file_path = self.path / f"{execution_id}.json"
        if not file_path.exists():
            return None
        with open(file_path, "r", encoding="utf-8") as f:
            return WorkflowExecution.from_dict(json.load(f))

    def get_latest_for_session(self, session_id: str) -> Optional[WorkflowExecution]:
        executions = self.list()
        session_executions = [e for e in executions if e.context.session_id == session_id]
        if not session_executions:
            return None
        return max(session_executions, key=lambda e: e.updated_at)

    def list(self) -> List[WorkflowExecution]:
        executions = []
        for file_path in self.path.glob("*.json"):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    executions.append(WorkflowExecution.from_dict(data))
            except Exception:
                pass
        return executions
