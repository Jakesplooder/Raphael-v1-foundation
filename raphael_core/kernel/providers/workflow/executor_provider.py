import asyncio
import logging
from typing import Dict, Any
from ...models.workflow import WorkflowExecution, WorkflowStatus, WorkflowStep
from .automation_provider import AutomationProvider
from ...repositories.idempotency_store import IdempotencyStore

logger = logging.getLogger("rrk.workflow.executor")

# Steps that represent external/unsafe actions that MUST be idempotent.
# In a full system, this would read from the Architecture Spec capability definitions.
IDEMPOTENT_ACTIONS = {"commerce.publish", "commerce.spend", "voice.call", "notifications.send"}

class ExecutorProvider:
    """
    Controls execution lifecycle for a given WorkflowExecution.
    It manages retries, pauses, timeouts, and interacting with the AutomationProvider.
    """
    def __init__(self, provider: AutomationProvider):
        self.provider = provider
        self.max_retries = 3
        self.idempotency_store = IdempotencyStore()

    async def execute_step(self, step: WorkflowStep, execution: WorkflowExecution) -> WorkflowStatus:
        """
        Executes a single workflow step with retry logic and idempotency.
        """
        idempotency_key = f"{execution.id}:{step.id}"
        
        # 1. Idempotency Check
        if step.action in IDEMPOTENT_ACTIONS:
            existing_result = self.idempotency_store.get(idempotency_key)
            if existing_result:
                logger.info(f"[IDEMPOTENCY] Step {step.id} already completed. Skipping execution.")
                execution.step_executions[step.id] = WorkflowStatus.COMPLETED
                if execution.result is None:
                    execution.result = {}
                execution.result[step.id] = existing_result
                return WorkflowStatus.COMPLETED
                
        retries = 0
        while retries <= self.max_retries:
            try:
                # Update status
                execution.step_executions[step.id] = WorkflowStatus.RUNNING
                
                # Execute via the specific AutomationProvider
                result = await self.provider.execute_step(step.action, step.parameters, idempotency_key=idempotency_key)
                
                # Success
                execution.step_executions[step.id] = WorkflowStatus.COMPLETED
                if execution.result is None:
                    execution.result = {}
                execution.result[step.id] = result
                
                # 2. Save to Idempotency Store
                if step.action in IDEMPOTENT_ACTIONS:
                    self.idempotency_store.set(idempotency_key, result)
                    
                return WorkflowStatus.COMPLETED
                
            except Exception as e:
                retries += 1
                logger.warning(f"Step {step.id} failed (attempt {retries}/{self.max_retries + 1}): {e}")
                
                if retries <= self.max_retries:
                    execution.step_executions[step.id] = WorkflowStatus.RETRYING
                    # exponential backoff
                    await asyncio.sleep(2 ** retries)
                else:
                    execution.step_executions[step.id] = WorkflowStatus.FAILED
                    execution.error = f"Step {step.id} failed after {retries} attempts: {e}"
                    return WorkflowStatus.FAILED
                    
        return WorkflowStatus.FAILED
