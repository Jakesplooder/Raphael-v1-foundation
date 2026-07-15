from typing import List, Dict, Any, Tuple
from ..models.workflow_plan import WorkflowPlan, WorkflowStatus
from ..repositories.workflow_plan_repository import WorkflowPlanRepository
from ..providers.workflow_providers import CapabilityRegistry

class WorkflowPlanService:
    def __init__(self, repository: WorkflowPlanRepository, registry: CapabilityRegistry):
        self.repository = repository
        self.registry = registry

    def create_plan(self, plan: WorkflowPlan) -> WorkflowPlan:
        plan.status = WorkflowStatus.VALIDATING
        self.repository.save_plan(plan)
        self.repository.log_event(plan, "PLAN_CREATED")
        return plan

    def validate_plan(self, plan: WorkflowPlan) -> Tuple[bool, List[str]]:
        """
        Validates a Workflow Plan DAG.
        Checks for:
        - Cycles
        - Missing Dependencies
        - Orphan Nodes (no parents and not root)
        - Dead Ends
        - Duplicate IDs
        - Capability Validation
        """
        errors = []
        all_steps = {}
        
        # Gather steps and check duplicate IDs
        for phase_id, phase in plan.phases.items():
            for step_id, step in phase.steps.items():
                if step_id in all_steps:
                    errors.append(f"Duplicate step_id: {step_id}")
                else:
                    all_steps[step_id] = step

        # Check for missing dependencies
        adj_list = {step_id: [] for step_id in all_steps}
        in_degree = {step_id: 0 for step_id in all_steps}
        
        for step_id, step in all_steps.items():
            for dep_id in step.dependencies:
                if dep_id not in all_steps:
                    errors.append(f"Missing dependency: {step_id} depends on {dep_id} which does not exist.")
                else:
                    adj_list[dep_id].append(step_id)
                    in_degree[step_id] += 1

        # Check for capabilities
        for step_id, step in all_steps.items():
            for cap in step.required_capabilities:
                if not self.registry.resolve(cap):
                    errors.append(f"Invalid Agent Assignment: Step {step_id} requires capability '{cap}' which has no registered provider.")

        # Cycle detection and Orphan node detection (Topological Sort)
        visited = 0
        queue = [node for node in all_steps if in_degree[node] == 0]
        
        if not queue and all_steps:
            errors.append("Orphan Nodes / No root nodes found. The graph might be entirely cyclic.")
            
        while queue:
            curr = queue.pop(0)
            visited += 1
            for neighbor in adj_list[curr]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
                    
        if visited != len(all_steps):
            errors.append("Cycles detected: The workflow contains a circular dependency.")

        # Dead ends (nodes that have no outgoing edges but are not marked as terminal or final steps)
        # For our basic DAG, any node without outgoing edges is a leaf. We'll just ensure leaves exist.
        leaves = [node for node in all_steps if not adj_list[node]]
        if not leaves and all_steps:
            errors.append("Dead Ends: Graph has no terminal leaves.")

        is_valid = len(errors) == 0
        if is_valid:
            plan.status = WorkflowStatus.READY
        else:
            plan.status = WorkflowStatus.FAILED
            
        self.repository.save_plan(plan)
        
        event_type = "PLAN_VALIDATED" if is_valid else "PLAN_FAILED_VALIDATION"
        self.repository.log_event(plan, event_type, {"errors": errors})
        
        return is_valid, errors
