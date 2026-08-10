from typing import List, Dict, Any
import asyncio
import logging
from .execution_queue import ExecutionQueue
from ..event_bus import EventBus
from ..interfaces import Event, EventType
from ..models.workflow_plan import WorkflowPlan, WorkflowStep, StepStatus, WorkflowStatus
from ..providers.workflow_providers import CapabilityRegistry
from ..providers.workflow.automation_provider import AutomationProvider

logger = logging.getLogger("rrk.services.workflow_scheduler")

class WorkflowScheduler:
    def __init__(self, queue: ExecutionQueue, registry: CapabilityRegistry, event_bus: EventBus = None, max_concurrent_jobs: int = 1):
        self.queue = queue
        self.registry = registry
        self.event_bus = event_bus
        self.max_concurrent_jobs = max_concurrent_jobs
        self._active_tasks: Dict[str, asyncio.Task] = {}
        
        # Mock resource awareness
        self.resources = {
            "cpu": 100,
            "gpu": 100,
            "memory": 100,
            "docker": True,
            "n8n": True,
            "comfyui": True,
            "internet": True
        }

    def update_resources(self, updates: Dict[str, Any]) -> None:
        self.resources.update(updates)

    def get_next_ready_steps(self, plan: WorkflowPlan) -> List[WorkflowStep]:
        """
        Determines which steps in the plan are ready to execute based on DAG topology.
        """
        ready_steps = []
        all_steps = {}
        
        for phase in plan.phases.values():
            for step_id, step in phase.steps.items():
                all_steps[step_id] = step

        for step in all_steps.values():
            if step.status != StepStatus.PENDING:
                continue
                
            # Check dependencies
            dependencies_met = True
            for dep_id in step.dependencies:
                dep_step = all_steps.get(dep_id)
                if not dep_step or dep_step.status != StepStatus.COMPLETED:
                    dependencies_met = False
                    break
                    
            if dependencies_met:
                step.status = StepStatus.READY
                ready_steps.append(step)
                
        return ready_steps

    def schedule(self, plan: WorkflowPlan) -> List[WorkflowStep]:
        """
        Schedules ready steps into the execution queue.
        """
        if plan.status == WorkflowStatus.FAILED:
            return []
            
        ready_steps = self.get_next_ready_steps(plan)
        
        for step in ready_steps:
            self.queue.enqueue(plan, step)
            
        return ready_steps

    def _resolve_parameters(self, step: WorkflowStep, plan: WorkflowPlan) -> Dict[str, Any]:
        """
        Resolves string templates like ${step_id.result.key} into actual values.
        """
        all_steps = {}
        for phase in plan.phases.values():
            for s_id, s in phase.steps.items():
                all_steps[s_id] = s
                
        resolved = {}
        for k, v in step.parameters.items():
            if isinstance(v, str) and v.startswith("${") and v.endswith("}"):
                path = v[2:-1].split(".")
                if len(path) >= 3 and path[1] == "result":
                    dep_step_id = path[0]
                    key = path[2]
                    
                    dep_step = all_steps.get(dep_step_id)
                    if dep_step and dep_step.status == StepStatus.COMPLETED:
                        resolved[k] = dep_step.result.get(key)
                    else:
                        resolved[k] = None # Will likely cause step failure, which is correct
                else:
                    resolved[k] = v
            else:
                resolved[k] = v
                
        return resolved

    async def _execute_step_task(self, provider: AutomationProvider, plan: WorkflowPlan, step: WorkflowStep, resolved_params: Dict[str, Any]):
        """Background task to execute a step."""
        try:
            logger.info(f"Executing step {step.step_id} with action '{step.action}'")
            if self.event_bus:
                await self.event_bus.publish(Event(
                    type=EventType.JOB_STARTED,
                    source="WorkflowScheduler",
                    payload={"job_id": step.step_id, "status": "started", "action": step.action, "parameters": resolved_params}
                ))

            result = await provider.execute_step(
                action=step.action,
                parameters=resolved_params,
                idempotency_key=f"{plan.plan_id}-{step.step_id}"
            )
            
            if result.get("status") == "success":
                # Lightweight Guard: Check verified status if an asset was generated
                if "asset_id" in result and "is_verified" in result:
                    if not result["is_verified"]:
                        logger.error(f"Step {step.step_id} returned an unverified asset. Guard validation failed.")
                        step.status = StepStatus.FAILED
                        step.result = {"error": "Asset failed verification guard."}
                        self.queue.mark_failed(step.step_id)
                        self._handle_plan_failure(plan)
                        if self.event_bus:
                            await self.event_bus.publish(Event(type=EventType.JOB_PROGRESS, source="WorkflowScheduler", payload={"job_id": step.step_id, "status": "failed", "result": step.result}))
                        return
                
                step.status = StepStatus.COMPLETED
                step.result = result
                self.queue.mark_completed(step.step_id)
                if self.event_bus:
                    await self.event_bus.publish(Event(type=EventType.JOB_PROGRESS, source="WorkflowScheduler", payload={"job_id": step.step_id, "status": "completed", "result": result}))
            else:
                step.status = StepStatus.FAILED
                step.result = result
                self.queue.mark_failed(step.step_id)
                self._handle_plan_failure(plan)
                if self.event_bus:
                    await self.event_bus.publish(Event(type=EventType.JOB_PROGRESS, source="WorkflowScheduler", payload={"job_id": step.step_id, "status": "failed", "result": result}))
                
        except Exception as e:
            logger.exception(f"Exception during step {step.step_id} execution: {e}")
            step.status = StepStatus.FAILED
            step.result = {"error": str(e)}
            self.queue.mark_failed(step.step_id)
            self._handle_plan_failure(plan)
            if self.event_bus:
                await self.event_bus.publish(Event(type=EventType.JOB_PROGRESS, source="WorkflowScheduler", payload={"job_id": step.step_id, "status": "failed", "result": step.result}))

    def _handle_plan_failure(self, plan: WorkflowPlan):
        """Halt the plan and cancel running steps."""
        plan.status = WorkflowStatus.FAILED
        logger.error(f"WorkflowPlan {plan.plan_id} FAILED. Halting and cancelling in-flight steps.")
        
        # Cancel any running steps belonging to this plan
        for phase in plan.phases.values():
            for step in phase.steps.values():
                if step.status == StepStatus.STARTED:
                    task = self._active_tasks.get(step.step_id)
                    if task and not task.done():
                        logger.warning(f"Cancelling in-flight task for step {step.step_id}")
                        task.cancel()
                        step.status = StepStatus.CANCELLED
                        self.queue.mark_cancelled(step.step_id)
                        
        # We don't have a direct reference to the active providers here to cancel,
        # but emitting a PLAN_FAILED event would let the manager/providers handle cleanup.
        pass

    async def dispatch(self, plans: List[WorkflowPlan]) -> None:
        """
        Pulls pending steps from the queue and dispatches them to ExecutionProviders.
        Enforces concurrency ceiling.
        """
        running_count = len(self.queue.get_running())
        if running_count >= self.max_concurrent_jobs:
            return
            
        pending = self.queue.get_pending()
        
        for step in pending:
            if running_count >= self.max_concurrent_jobs:
                break
                
            # Find the parent plan
            plan = next((p for p in plans if any(s_id == step.step_id for phase in p.phases.values() for s_id in phase.steps)), None)
            if not plan:
                logger.warning(f"Orphaned step {step.step_id} in queue.")
                self.queue.dequeue(step.step_id)
                continue
                
            if plan.status == WorkflowStatus.FAILED:
                # Discard steps for failed plans
                self.queue.dequeue(step.step_id)
                continue

            # Check capabilities
            provider = None
            for cap in step.required_capabilities:
                provider = self.registry.resolve_best(cap)
                if provider:
                    break
                    
            if provider and isinstance(provider, AutomationProvider):
                resolved_params = self._resolve_parameters(step, plan)
                self.queue.mark_running(step.step_id)
                step.status = StepStatus.STARTED
                running_count += 1
                
                task = asyncio.create_task(self._execute_step_task(provider, plan, step, resolved_params))
                self._active_tasks[step.step_id] = task
                task.add_done_callback(lambda t, sid=step.step_id: self._active_tasks.pop(sid, None))
