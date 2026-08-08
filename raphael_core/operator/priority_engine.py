from typing import List
from .executive_state import ExecutiveSnapshot
from .executive_analysis import ObjectivePriority

class PriorityEngine:
    """
    Scores and sorts pending tasks, blocked workflows, and initiatives 
    based on the ExecutiveSnapshot.
    Formula: (Business Impact * Urgency * Confidence * Strategic Alignment) / Estimated Cost
    """
    def evaluate(self, snapshot: ExecutiveSnapshot) -> List[ObjectivePriority]:
        priorities = []
        state = snapshot.state
        
        # 1. Look at pending tasks (missions)
        tasks = state.executions.get("tasks", {}).get("pending_approval", [])
        for t in tasks:
            # In a real scenario, these metrics would come from the Task/Proposal metadata
            # or the Knowledge Graph. We mock the computation for now.
            impact = 80.0
            urgency = 90.0 if "error" in str(t).lower() else 50.0
            confidence = 85.0
            alignment = 1.0
            cost = 10.0 # arbitrary relative cost
            
            score = (impact * urgency * confidence * alignment) / max(cost, 1.0)
            
            priorities.append(
                ObjectivePriority(
                    id=t.get("mission_id", "UNKNOWN"),
                    title=f"Review Pending Mission: {t.get('mission_id')}",
                    score=score,
                    urgency=urgency,
                    confidence=confidence,
                    business_impact=impact,
                    estimated_cost=cost,
                    reasoning="Task requires executive approval to unblock execution."
                )
            )
            
        # 2. Look at failed workflows
        failed_wfs = state.executions.get("workflows", {}).get("failed", [])
        for fw in failed_wfs:
            impact = 95.0
            urgency = 100.0  # Failed workflows are highly urgent
            confidence = 90.0
            alignment = 1.0
            cost = 5.0
            
            score = (impact * urgency * confidence * alignment) / cost
            
            priorities.append(
                ObjectivePriority(
                    id=fw.get("execution_id", "UNKNOWN"),
                    title=f"Resolve Failed Workflow: {fw.get('execution_id')}",
                    score=score,
                    urgency=urgency,
                    confidence=confidence,
                    business_impact=impact,
                    estimated_cost=cost,
                    reasoning="A critical workflow has failed and requires intervention."
                )
            )
            
        # Sort descending by score
        priorities.sort(key=lambda x: x.score, reverse=True)
        return priorities
