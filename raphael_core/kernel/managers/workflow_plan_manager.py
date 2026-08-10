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
    def __init__(self, event_bus: EventBus, config: RaphaelConfig):
        self.config = config
        self.event_bus = event_bus
        self._health = "pending"
        self._router = APIRouter(prefix="/api/workflowplans")
        
        # Instantiate layer
        self.repository = WorkflowPlanRepository(config)
        self.registry = CapabilityRegistry()
        self.service = WorkflowPlanService(self.repository, self.registry)
        self.queue = ExecutionQueue()
        self.scheduler = WorkflowScheduler(self.queue, self.registry)
        

        self.active_plans = {}

    @property
    def name(self) -> str:
        return "WorkflowPlans"

    @property
    def depends_on(self) -> List[str]:
        return ["EventBus", "Gateway"]

    async def initialize(self, **kwargs) -> None:
        self._setup_routes()
        self._health = "initialized"

    async def start(self) -> None:
        self._health = "running"
        self._engine_task = None
        if self.event_bus:
            self.event_bus.subscribe(EventType.WORKFLOW_PLAN_REQUESTED, self._handle_plan_requested)
            self._engine_task = asyncio.create_task(self._engine_loop())

    async def _handle_plan_requested(self, event: Event) -> None:
        import logging
        from ..observability import ObservabilityLayer
        logger = logging.getLogger("workflow_plan_manager")
        logger.info(f"_handle_plan_requested received event: {event.id}")
        ObservabilityLayer.info("WorkflowPlanManager", f"_handle_plan_requested received event: {event.id}")
        
        payload = event.payload
        template_dump = payload.get("template")
        if not template_dump:
            logger.error("No template dump in payload!")
            ObservabilityLayer.error("WorkflowPlanManager", "No template dump in payload!")
            return
            
        from ..models.workflow_plan import WorkflowTemplate, WorkflowPlan
        template = WorkflowTemplate(**template_dump)
        plan = WorkflowPlan(
            template_id=template.template_id,
            phases=template.phases
        )
        self.active_plans[plan.plan_id] = plan
        
        try:
            self.repository.save_plan(plan)
            logger.info(f"Saved WorkflowPlan {plan.plan_id}")
            ObservabilityLayer.info("WorkflowPlanManager", f"Saved WorkflowPlan {plan.plan_id} to {self.repository.base_dir}")
        except Exception as e:
            ObservabilityLayer.error("WorkflowPlanManager", f"Failed to save plan: {e}")
        
    async def _engine_loop(self) -> None:
        import logging
        logger = logging.getLogger("rrk.managers.workflow_plan")
        
        # Load running plans from disk on startup
        for plan in self.repository.list_plans():
            self.active_plans[plan.plan_id] = plan
            
        while self._health == "running":
            try:
                plans = list(self.active_plans.values())
                # Schedule new steps
                for plan in plans:
                    self.scheduler.schedule(plan)
                    
                # Dispatch ready steps
                await self.scheduler.dispatch(plans)
                
                # Save state back to repository and cleanup finished plans
                finished_plans = []
                from ..models.workflow_plan import WorkflowStatus, StepStatus
                
                for plan_id, plan in self.active_plans.items():
                    # Check if all steps completed
                    if plan.status not in (WorkflowStatus.FAILED, WorkflowStatus.CANCELLED):
                        all_completed = True
                        for phase in plan.phases.values():
                            for step in phase.steps.values():
                                if step.status != StepStatus.COMPLETED:
                                    all_completed = False
                                    break
                        if all_completed and len(plan.phases) > 0:
                            plan.status = WorkflowStatus.COMPLETED
                            logger.info(f"WorkflowPlan {plan.plan_id} completed successfully.")
                            
                    self.repository.save_plan(plan)
                    
                    if plan.status in (WorkflowStatus.COMPLETED, WorkflowStatus.FAILED, WorkflowStatus.CANCELLED):
                        finished_plans.append(plan_id)
                        
                for plan_id in finished_plans:
                    del self.active_plans[plan_id]
                    
            except Exception as e:
                logger.error(f"Error in Workflow Engine loop: {e}")
                
            await asyncio.sleep(2)

    async def stop(self) -> None:
        self._health = "stopped"
        if hasattr(self, '_engine_task') and self._engine_task:
            self._engine_task.cancel()

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
