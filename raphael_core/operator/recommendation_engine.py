from typing import List
from .executive_state import ExecutiveSnapshot
from .executive_analysis import ExecutiveRecommendation
import uuid

class RecommendationEngine:
    """
    Analyzes the ExecutiveSnapshot to surface actionable executive recommendations.
    Provides proactive suggestions (e.g. Pause Initiative, Increase Compute).
    """
    def evaluate(self, snapshot: ExecutiveSnapshot) -> List[ExecutiveRecommendation]:
        recs = []
        state = snapshot.state
        
        # 1. Detect System Health Issues
        sys_health_raw = state.system.get("system_health_core", {})
        if sys_health_raw.get("overall") != "healthy":
            recs.append(
                ExecutiveRecommendation(
                    id=f"REC-{uuid.uuid4().hex[:6].upper()}",
                    action="Review System Health",
                    target="system_health",
                    confidence=0.95,
                    reasoning="System health is reporting as degraded or unhealthy.",
                    impact="High: Core subsystems may be failing."
                )
            )
            
        # 2. Detect Blocked/Pending Approval bottleneck
        tasks = state.executions.get("tasks", {}).get("pending_approval", [])
        if len(tasks) > 3:
            recs.append(
                ExecutiveRecommendation(
                    id=f"REC-{uuid.uuid4().hex[:6].upper()}",
                    action="Batch Review Pending Tasks",
                    target="mission_approval",
                    confidence=0.85,
                    reasoning=f"There are {len(tasks)} pending missions blocking execution pipelines.",
                    impact="Medium: Execution throughput is degraded."
                )
            )
            
        # 3. Detect Failed Workflows
        failed_wfs = state.executions.get("workflows", {}).get("failed", [])
        if failed_wfs:
            recs.append(
                ExecutiveRecommendation(
                    id=f"REC-{uuid.uuid4().hex[:6].upper()}",
                    action="Debug Failed Workflows",
                    target="workflow_engine",
                    confidence=0.98,
                    reasoning=f"{len(failed_wfs)} workflows have failed and require attention.",
                    impact="High: Operational output is halted for these workflows."
                )
            )
            
        return recs
