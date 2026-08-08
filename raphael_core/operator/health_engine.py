from typing import Any
from .executive_state import ExecutiveSnapshot
from .executive_analysis import HealthMetrics

class HealthEngine:
    """
    Computes overall executive health by interpreting the raw facts in the ExecutiveSnapshot.
    """
    def evaluate(self, snapshot: ExecutiveSnapshot) -> HealthMetrics:
        state = snapshot.state
        
        # Base system health
        sys_health_raw = state.system.get("system_health_core", {})
        is_healthy = sys_health_raw.get("overall") == "healthy"
        
        # Analyze workflows
        workflows = state.executions.get("workflows", {})
        running_wfs = len(workflows.get("running", []))
        failed_wfs = len(workflows.get("failed", []))
        total_wfs = running_wfs + failed_wfs + len(workflows.get("paused", []))
        
        workflow_health = 100.0
        if total_wfs > 0:
            workflow_health = 100.0 * (1.0 - (failed_wfs / total_wfs))
            
        # Overall Execution Health (Missions/Tasks + Workflows)
        tasks = state.executions.get("tasks", {})
        pending = len(tasks.get("pending_approval", []))
        execution_health = 100.0
        if pending > 10:  # Arbitrary threshold: too many pending means blocked execution
            execution_health = 50.0
        elif pending > 0:
            execution_health = 90.0
            
        # Business Health (mocked for now until Finance/Commerce producers exist)
        business_health = 85.0
        
        # Agent Health (mocked until Agent producer exists)
        agent_health = 100.0
        
        risk = "Low"
        if failed_wfs > 0:
            risk = "Medium"
        if not is_healthy:
            risk = "High"
            
        return HealthMetrics(
            business_health=business_health,
            execution_health=execution_health,
            workflow_health=workflow_health,
            agent_health=agent_health,
            financial_health=None,
            strategic_risk=risk
        )
