import json
import os
import shutil
from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import datetime

from ..models.workflow_plan import WorkflowPlan, WorkflowStatus
from ...config import RaphaelConfig

class WorkflowPlanRepository:
    def __init__(self, config: RaphaelConfig):
        self.config = config
        self.base_dir = self.config.vault / "00_Raphael" / "Workflow Plans"
        
        # Ensure directories exist
        for state_dir in ["Templates", "Running", "Completed", "Archived"]:
            (self.base_dir / state_dir).mkdir(parents=True, exist_ok=True)

    def _get_state_dir(self, status: WorkflowStatus) -> Path:
        if status in (WorkflowStatus.PENDING, WorkflowStatus.VALIDATING, WorkflowStatus.READY, WorkflowStatus.ACTIVE, WorkflowStatus.PAUSED):
            return self.base_dir / "Running"
        elif status == WorkflowStatus.COMPLETED:
            return self.base_dir / "Completed"
        elif status in (WorkflowStatus.ARCHIVED, WorkflowStatus.CANCELLED, WorkflowStatus.FAILED):
            return self.base_dir / "Archived"
        return self.base_dir / "Running"

    def _get_plan_dir(self, plan: WorkflowPlan) -> Path:
        state_dir = self._get_state_dir(plan.status)
        return state_dir / plan.plan_id

    def save_plan(self, plan: WorkflowPlan) -> None:
        """Saves the plan to disk, handling state directory transitions."""
        # Find if it already exists in any state dir, and move it if status changed
        existing_path = None
        for state_dir in ["Running", "Completed", "Archived"]:
            potential_path = self.base_dir / state_dir / plan.plan_id
            if potential_path.exists():
                existing_path = potential_path
                break
                
        target_dir = self._get_plan_dir(plan)
        
        if existing_path and existing_path != target_dir:
            shutil.move(str(existing_path), str(target_dir))
            
        target_dir.mkdir(parents=True, exist_ok=True)
        (target_dir / "checkpoints").mkdir(parents=True, exist_ok=True)
        (target_dir / "artifacts").mkdir(parents=True, exist_ok=True)
        (target_dir / "logs").mkdir(parents=True, exist_ok=True)
        
        # Save JSON source of truth
        plan_json_path = target_dir / "plan.json"
        plan_json_path.write_text(plan.model_dump_json(indent=2), encoding="utf-8")
        
        # Save Markdown human-readable summary
        readme_path = target_dir / "README.md"
        readme_content = f"# Workflow Plan: {plan.plan_id}\\n\\n"
        readme_content += f"**Status**: {plan.status}\\n"
        readme_content += f"**Version**: {plan.version} (Rev {plan.revision})\\n\\n"
        readme_content += "## Graph\\n\\n```mermaid\\n"
        readme_content += plan.export_mermaid()
        readme_content += "\\n```\\n"
        readme_path.write_text(readme_content, encoding="utf-8")

    def save_checkpoint(self, plan: WorkflowPlan) -> None:
        """Saves a point-in-time checkpoint of the plan."""
        self.save_plan(plan)
        target_dir = self._get_plan_dir(plan)
        checkpoint_name = f"checkpoint-{plan.revision:03d}.json"
        checkpoint_path = target_dir / "checkpoints" / checkpoint_name
        checkpoint_path.write_text(plan.model_dump_json(indent=2), encoding="utf-8")

    def log_event(self, plan: WorkflowPlan, event_type: str, details: Dict[str, Any] = None) -> None:
        """Appends a transition event to the plan's event log."""
        target_dir = self._get_plan_dir(plan)
        events_path = target_dir / "logs" / "events.jsonl"
        
        event_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "event_type": event_type,
            "revision": plan.revision,
            "details": details or {}
        }
        
        with events_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(event_entry) + "\\n")

    def get_plan(self, plan_id: str) -> Optional[WorkflowPlan]:
        for state_dir in ["Running", "Completed", "Archived"]:
            plan_json_path = self.base_dir / state_dir / plan_id / "plan.json"
            if plan_json_path.exists():
                try:
                    content = plan_json_path.read_text(encoding="utf-8")
                    return WorkflowPlan.model_validate_json(content)
                except Exception:
                    pass
        return None

    def list_plans(self, state: str = "Running") -> List[WorkflowPlan]:
        plans = []
        state_dir = self.base_dir / state
        if not state_dir.exists():
            return plans
            
        for item in state_dir.iterdir():
            if item.is_dir():
                plan_json_path = item / "plan.json"
                if plan_json_path.exists():
                    try:
                        content = plan_json_path.read_text(encoding="utf-8")
                        plans.append(WorkflowPlan.model_validate_json(content))
                    except Exception:
                        pass
        return plans
