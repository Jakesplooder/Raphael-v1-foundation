from typing import Dict, Any, List
import json
import asyncio
from fastapi import APIRouter
from pydantic import BaseModel

from ..interfaces import ServiceModule, Event, EventType
from ...config import RaphaelConfig
from ..event_bus import EventBus

from ..models.workflow_plan import WorkflowPlan
from ..repositories.workflow_plan_repository import WorkflowPlanRepository
from ..providers.workflow_providers import CapabilityRegistry
from ..services.workflow_plan_service import WorkflowPlanService
from ..services.execution_queue import ExecutionQueue
from ..services.workflow_scheduler import WorkflowScheduler

class WorkflowPlanManager(ServiceModule):
    def __init__(self, config: RaphaelConfig):
        self.config = config
        self._health = "pending"
        self._router = APIRouter(prefix="/api/workflowplans")
        
        # Instantiate layer
        self.repository = WorkflowPlanRepository(config)
        self.registry = CapabilityRegistry()
        self.service = WorkflowPlanService(self.repository, self.registry)
        self.queue = ExecutionQueue()
        self.scheduler = WorkflowScheduler(self.queue, self.registry)
        
        self.event_bus = None

    @property
    def name(self) -> str:
        return "WorkflowPlans"

    @property
    def depends_on(self) -> List[str]:
        return ["EventBus", "Gateway"]

    async def initialize(self, **kwargs) -> None:
        self.event_bus = kwargs.get("event_bus")
        self._setup_routes()
        self._health = "initialized"

    async def start(self) -> None:
        self._health = "running"
        if self.event_bus:
            # We would subscribe to events here if needed
            pass

    async def stop(self) -> None:
        self._health = "stopped"

    async def shutdown(self) -> None:
        self._health = "shutdown"

    async def heartbeat(self) -> bool | Dict[str, Any]:
        return {"alive": True, "type": "basic", "latency_sec": 0.0}

    async def handle_request(self, method: str, path: str, payload: Dict[str, Any] = None) -> Any:
        return None

    def health(self) -> Any:
        from ..interfaces import ModuleHealth
        return ModuleHealth.OK if self._health == "running" else ModuleHealth.DEGRADED

    def status(self) -> str:
        return f"Queue Pending: {len(self.queue.get_pending())}, Running: {len(self.queue.get_running())}"

    def metrics(self) -> Dict[str, Any]:
        return {}

    def snapshot(self) -> Dict[str, Any]:
        return {}

    def api_router(self) -> APIRouter:
        return self._router

    def _setup_routes(self):
        @self._router.get("/list")
        async def list_plans():
            plans = self.repository.list_plans()
            return {"plans": [json.loads(p.model_dump_json()) for p in plans]}

        @self._router.post("/validate")
        async def validate_plan(plan: WorkflowPlan):
            is_valid, errors = self.service.validate_plan(plan)
            if self.event_bus:
                await self.event_bus.publish(Event(
                    type=EventType.SYSTEM_INFO,
                    source=self.name,
                    payload={"action": "validate", "plan_id": plan.plan_id, "is_valid": is_valid}
                ))
            return {"is_valid": is_valid, "errors": errors}
