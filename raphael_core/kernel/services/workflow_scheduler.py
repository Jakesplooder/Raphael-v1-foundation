from typing import List, Dict, Any
from .execution_queue import ExecutionQueue
from ..models.workflow_plan import WorkflowPlan, WorkflowStep, StepStatus
from ..providers.workflow_providers import CapabilityRegistry, ExecutionProvider

class WorkflowScheduler:
    def __init__(self, queue: ExecutionQueue, registry: CapabilityRegistry):
        self.queue = queue
        self.registry = registry
        
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
        Sorts by plan priority, but in a real system would sort across all plans.
        """
        ready_steps = self.get_next_ready_steps(plan)
        
        # In a real scheduler, we'd sort by priority, weight, estimated cost, etc.
        # For now, just enqueue them.
        for step in ready_steps:
            self.queue.enqueue(plan, step)
            
        return ready_steps

    async def dispatch(self) -> None:
        """
        Pulls pending steps from the queue and dispatches them to ExecutionProviders.
        """
        pending = self.queue.get_pending()
        
        for step in pending:
            # Check capabilities
            provider = None
            for cap in step.required_capabilities:
                provider = self.registry.resolve_best(cap)
                if provider:
                    break
                    
            if provider and isinstance(provider, ExecutionProvider):
                # We have a provider, mark running and dispatch
                # In a real system, we'd check `self.resources` here before dispatching.
                self.queue.mark_running(step.step_id)
                # Dispatching would be async: asyncio.create_task(provider.execute_step(step, {}))
                # For this skeletal layer, we just rely on Epic J to actually do this.
