import json
from pathlib import Path
from typing import Dict, List, Optional
from ..models.workflow import Workflow, WorkflowExecution

class WorkflowRepository:
    """
    Pure I/O handler for Workflows and WorkflowExecutions.
    In a full production environment, this would hit PostgreSQL or similar.
    For now, it stores state in-memory and optionally syncs to disk.
    """
    def __init__(self, data_dir: Path):
        self.data_dir = data_dir
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.workflows: Dict[str, Workflow] = {}
        self.executions: Dict[str, WorkflowExecution] = {}

    def save_workflow(self, workflow: Workflow):
        self.workflows[workflow.id] = workflow

    def get_workflow(self, workflow_id: str) -> Optional[Workflow]:
        return self.workflows.get(workflow_id)
        
    def list_workflows(self) -> List[Workflow]:
        return list(self.workflows.values())

    def save_execution(self, execution: WorkflowExecution):
        self.executions[execution.id] = execution

    def get_execution(self, execution_id: str) -> Optional[WorkflowExecution]:
        return self.executions.get(execution_id)

    def list_executions_for_workflow(self, workflow_id: str) -> List[WorkflowExecution]:
        return [ex for ex in self.executions.values() if ex.workflow_id == workflow_id]
