import logging
import asyncio
from typing import Optional, Callable, Awaitable
from ..models.workflow import Workflow, WorkflowExecution, WorkflowStatus
from ..repositories.workflow_repository import WorkflowRepository
from ..providers.workflow.executor_provider import ExecutorProvider
from ..providers.workflow.scheduler_provider import SchedulerProvider

logger = logging.getLogger("rrk.workflow.service")

class WorkflowService:
    """
    Reasoning layer for Workflows.
    Manages logic, state transitions, and delegates actual execution to Providers.
    """
    def __init__(
        self, 
        repository: WorkflowRepository, 
        executor: ExecutorProvider, 
        scheduler: SchedulerProvider
    ):
        self.repository = repository
        self.executor = executor
        self.scheduler = scheduler
        
        # Register the execution callback with the scheduler
        self.scheduler.register_callback("default", self._run_execution_logic)
        
        # Callback for the Manager to emit events
        self.emit_event: Optional[Callable[[str, dict], Awaitable[None]]] = None
        
    async def recover_active_workflows(self):
        """
        Runs on Daemon boot. Finds all workflows that were RUNNING when the 
        process crashed, and re-queues them into the scheduler.
        Idempotency layer protects against duplicate execution.
        """
        logger.info("Initializing Workflow Recovery Routine...")
        # Since we use a simple dict repository mock for now, we scan it
        active_executions = [
            ex for ex in self.repository.executions.values() 
            if ex.status == WorkflowStatus.RUNNING
        ]
        
        if not active_executions:
            logger.info("No dangling workflows found.")
            return
            
        logger.warning(f"Found {len(active_executions)} dangling workflows. Initiating recovery.")
        for execution in active_executions:
            logger.info(f"Re-queuing execution {execution.id} for recovery...")
            self.scheduler.schedule_execution(execution.id)

    async def _emit(self, event_type: str, payload: dict):
        if self.emit_event:
            await self.emit_event(event_type, payload)

    async def create_workflow(self, name: str, steps: list, importance: str = "normal") -> Workflow:
        workflow = Workflow(name=name, steps=steps, importance=importance)
        self.repository.save_workflow(workflow)
        await self._emit("workflow_created", workflow.model_dump())
        return workflow

    async def trigger_workflow(self, workflow_id: str) -> Optional[WorkflowExecution]:
        workflow = self.repository.get_workflow(workflow_id)
        if not workflow:
            return None

        # Transition workflow state
        workflow.status = WorkflowStatus.QUEUED
        self.repository.save_workflow(workflow)

        execution = WorkflowExecution(workflow_id=workflow_id)
        self.repository.save_execution(execution)
        
        await self._emit("workflow_queued", {"workflow_id": workflow_id, "execution_id": execution.id})

        # Submit to scheduler pool
        self.scheduler.schedule_execution(execution.id)
        return execution

    async def _run_execution_logic(self, execution_id: str):
        execution = self.repository.get_execution(execution_id)
        if not execution:
            return
            
        workflow = self.repository.get_workflow(execution.workflow_id)
        if not workflow:
            return

        workflow.status = WorkflowStatus.RUNNING
        execution.status = WorkflowStatus.RUNNING
        self.repository.save_workflow(workflow)
        self.repository.save_execution(execution)
        
        await self._emit("workflow_started", {"execution_id": execution.id, "workflow_id": workflow.id})

        try:
            for step in workflow.steps:
                await self._emit("workflow_step_started", {"execution_id": execution.id, "step_id": step.id})
                
                # ExecutorProvider handles retries internally. It will either return COMPLETED or FAILED.
                step_status = await self.executor.execute_step(step, execution)
                
                if step_status == WorkflowStatus.FAILED:
                    execution.status = WorkflowStatus.FAILED
                    workflow.status = WorkflowStatus.FAILED
                    self.repository.save_execution(execution)
                    self.repository.save_workflow(workflow)
                    
                    payload = {
                        "execution_id": execution.id, 
                        "workflow_id": workflow.id, 
                        "importance": workflow.importance,
                        "error": execution.error
                    }
                    await self._emit("workflow_failed", payload)
                    return
                
                await self._emit("workflow_step_completed", {"execution_id": execution.id, "step_id": step.id, "result": execution.result.get(step.id)})

            execution.status = WorkflowStatus.COMPLETED
            workflow.status = WorkflowStatus.COMPLETED
            self.repository.save_execution(execution)
            self.repository.save_workflow(workflow)
            
            payload = {
                "execution_id": execution.id, 
                "workflow_id": workflow.id, 
                "importance": workflow.importance,
                "result": execution.result
            }
            await self._emit("workflow_completed", payload)

        except Exception as e:
            logger.error(f"Execution {execution.id} crashed unhandled: {e}")
            execution.status = WorkflowStatus.FAILED
            workflow.status = WorkflowStatus.FAILED
            execution.error = str(e)
            self.repository.save_execution(execution)
            self.repository.save_workflow(workflow)
            await self._emit("workflow_failed", {"execution_id": execution.id, "workflow_id": workflow.id, "importance": workflow.importance, "error": str(e)})
