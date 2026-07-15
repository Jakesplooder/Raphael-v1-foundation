import logging
from typing import Dict, Any, List
from pathlib import Path

from ..interfaces import ServiceModule, Event, EventType, ModuleHealth
from ..repositories.goal_repository import GoalRepository
from ..services.goal_service import GoalService
from ..models.goal import GoalStatus, TaskStatus

logger = logging.getLogger("rrk.managers.goal")

class GoalManager(ServiceModule):
    def __init__(self, event_bus, config):
        self.event_bus = event_bus
        self.config = config
        
        vault_path = Path(getattr(self.config, "vault", "./vault")) / "00_Raphael/Goals"
        self.repository = GoalRepository(vault_path)
        self.service = GoalService(self.repository)
        
        self._is_initialized = False

    @property
    def name(self) -> str:
        return "Goals"

    @property
    def depends_on(self) -> List[str]:
        return ["EventBus"]

    async def initialize(self) -> None:
        self.event_bus.subscribe(EventType.WORKFLOW_FAILED, self._handle_workflow_failed)
        # Note: We also track agent failures if they fail before triggering workflows
        self.event_bus.subscribe(EventType.AGENT_FAILED, self._handle_agent_failed)
        
        self._is_initialized = True
        logger.info("GoalManager initialized.")

    async def start(self) -> None:
        pass

    async def stop(self) -> None:
        pass
        
    async def shutdown(self) -> None:
        self._is_initialized = False

    def status(self) -> str:
        return "running" if self._is_initialized else "stopped"

    async def heartbeat(self) -> bool | Dict[str, Any]:
        return True

    async def health(self) -> ModuleHealth:
        return ModuleHealth(status="OK", details={"goals_tracked": len(self.repository.goals)})

    async def metrics(self) -> dict:
        return {}

    async def _handle_workflow_failed(self, event: Event):
        # We don't automatically rethink objectives. We mark task as FAILED and let agent rethink.
        wf_id = event.payload.get("workflow_id")
        
        # In a real system, we need a mapping of workflow_id -> task_id.
        # For simplicity in this D10 MVP, if payload has task_id, we fail it.
        task_id = event.payload.get("task_id")
        if task_id:
            self.service.update_task_status(task_id, TaskStatus.FAILED)
            self.event_bus.publish(Event(
                source=self.name,
                type=EventType.TASK_FAILED,
                payload={"task_id": task_id, "reason": "Workflow failed"}
            ))

    async def _handle_agent_failed(self, event: Event):
        agent_id = event.payload.get("agent_id")
        # Mark tasks assigned to this agent as FAILED if they are IN_PROGRESS
        # (MVP Implementation limits checking all tasks for simplicity, focusing on contract)
        for t in self.repository.tasks.values():
            if t.assigned_agent_id == agent_id and t.status in (TaskStatus.ASSIGNED, TaskStatus.IN_PROGRESS):
                self.service.update_task_status(t.id, TaskStatus.FAILED)
                self.event_bus.publish(Event(
                    source=self.name,
                    type=EventType.TASK_FAILED,
                    payload={"task_id": t.id, "reason": "Agent failed"}
                ))

    async def handle_request(self, method: str, endpoint: str, payload: Dict[str, Any]) -> Any:
        if method == "POST" and endpoint == "/api/goals":
            g = self.service.create_goal(
                title=payload.get("title"),
                description=payload.get("description"),
                priority=payload.get("priority", "medium"),
                importance=payload.get("importance", "normal")
            )
            self.event_bus.publish(Event(
                source=self.name,
                type=EventType.GOAL_CREATED,
                payload={"goal_id": g.id}
            ))
            return {"goal_id": g.id}
            
        elif method == "POST" and endpoint == "/api/objectives":
            o = self.service.create_objective(
                goal_id=payload.get("goal_id"),
                title=payload.get("title")
            )
            self.event_bus.publish(Event(
                source=self.name,
                type=EventType.OBJECTIVE_CREATED,
                payload={"objective_id": o.id}
            ))
            return {"objective_id": o.id}
            
        elif method == "POST" and endpoint == "/api/tasks":
            t = self.service.create_task(
                objective_id=payload.get("objective_id"),
                title=payload.get("title"),
                description=payload.get("description")
            )
            self.event_bus.publish(Event(
                source=self.name,
                type=EventType.TASK_CREATED,
                payload={"task_id": t.id}
            ))
            return {"task_id": t.id}
            
        elif method == "POST" and endpoint == "/api/tasks/assign":
            t = self.service.assign_task(
                task_id=payload.get("task_id"),
                agent_id=payload.get("agent_id")
            )
            # The crucial event that bridges Motivation to Agent Reasoning
            self.event_bus.publish(Event(
                source=self.name,
                type=EventType.AGENT_TASK_ASSIGNED,
                payload={"task_id": t.id, "agent_id": t.assigned_agent_id, "goal": t.description}
            ))
            return {"status": "assigned"}
            
        elif method == "POST" and endpoint == "/api/tasks/complete":
            task_id = payload.get("task_id")
            t = self.service.update_task_status(task_id, TaskStatus.COMPLETED)
            if t:
                self.event_bus.publish(Event(
                    source=self.name,
                    type=EventType.TASK_COMPLETED,
                    payload={"task_id": t.id}
                ))
            return {"status": "completed"}

        elif method == "POST" and endpoint == "/api/objectives/complete":
            obj_id = payload.get("objective_id")
            o = self.service.update_objective_status(obj_id, GoalStatus.COMPLETED)
            if o:
                g = self.service.get_goal(o.goal_id)
                self.event_bus.publish(Event(
                    source=self.name,
                    type=EventType.OBJECTIVE_COMPLETED,
                    payload={"objective_id": o.id, "importance": g.importance if g else "normal"}
                ))
            return {"status": "completed"}

        return {"error": "Unknown endpoint"}
