from typing import Dict, List, Optional
import asyncio
from ..models.workflow_plan import WorkflowPlan, WorkflowStep, StepStatus

class ExecutionQueue:
    def __init__(self):
        self._pending: List[WorkflowStep] = []
        self._running: List[WorkflowStep] = []
        self._completed: List[WorkflowStep] = []
        self._failed: List[WorkflowStep] = []
        self._paused: List[WorkflowStep] = []
        
        # Track which plan each step belongs to
        self._step_to_plan: Dict[str, str] = {}

    def enqueue(self, plan: WorkflowPlan, step: WorkflowStep) -> None:
        self._step_to_plan[step.step_id] = plan.plan_id
        if step not in self._pending:
            self._pending.append(step)

    def mark_running(self, step_id: str) -> None:
        step = self._remove_from_all(step_id)
        if step:
            step.status = StepStatus.STARTED
            self._running.append(step)

    def mark_completed(self, step_id: str) -> None:
        step = self._remove_from_all(step_id)
        if step:
            step.status = StepStatus.COMPLETED
            self._completed.append(step)

    def mark_failed(self, step_id: str) -> None:
        step = self._remove_from_all(step_id)
        if step:
            step.status = StepStatus.FAILED
            self._failed.append(step)

    def get_pending(self) -> List[WorkflowStep]:
        return list(self._pending)

    def get_running(self) -> List[WorkflowStep]:
        return list(self._running)

    def _remove_from_all(self, step_id: str) -> Optional[WorkflowStep]:
        for q in [self._pending, self._running, self._completed, self._failed, self._paused]:
            for s in q:
                if s.step_id == step_id:
                    q.remove(s)
                    return s
        return None
