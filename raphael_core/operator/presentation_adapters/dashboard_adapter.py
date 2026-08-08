from typing import List
from ..executive_analysis import ExecutiveAnalysis, ExecutiveRecommendation
from .dashboard_view_model import (
    DashboardViewModel, HealthCard, PriorityCard, InitiativeCard, 
    AgentCard, RecommendationCard, TimelineEvent
)
from ..notification_engine import notification_engine

class DashboardAdapter:
    """
    Transforms an ExecutiveAnalysis into a UI-friendly DashboardViewModel.
    """
    def adapt(self, analysis: ExecutiveAnalysis) -> DashboardViewModel:
        
        # 1. Adapt Health
        overall_score = f"{int(analysis.health.business_health)}%" # Assuming business is the primary metric for now
        trend = "Stable"
        status = "Healthy" if analysis.health.strategic_risk in ("Low", "Medium") else "Degraded"
        
        components = [
            {"label": "Business", "value": analysis.health.business_health},
            {"label": "Execution", "value": analysis.health.execution_health},
            {"label": "Workflow", "value": analysis.health.workflow_health},
            {"label": "Agent", "value": analysis.health.agent_health}
        ]
        
        health_card = HealthCard(
            overall_score=overall_score,
            trend=trend,
            status=status,
            components=components
        )
        
        # 2. Adapt Priorities
        priorities = []
        for p in analysis.priorities[:5]: # Take top 5
            priorities.append(
                PriorityCard(
                    title=p.title,
                    reason=p.reasoning,
                    score=p.score,
                    recommended_action="Review", # Could map based on type
                    estimated_time="N/A"
                )
            )
            
        # 3. Adapt Recommendations (filtered)
        raw_recs = analysis.recommendations
        filtered_recs = notification_engine.filter(raw_recs)
        
        recommendation_cards = []
        for r in filtered_recs:
            recommendation_cards.append(
                RecommendationCard(
                    id=r.id,
                    title=r.action,
                    impact=r.impact,
                    action_type=r.target
                )
            )
            
        # 4. Extract simple metrics for now (mocked until Initiative/Agent models catch up)
        initiatives = [] 
        agents = []
        timeline = []
        
        return DashboardViewModel(
            health=health_card,
            priorities=priorities,
            initiatives=initiatives,
            running_workflows=0, # Should come from analysis
            agent_activity=agents,
            alerts=analysis.risks,
            recommendations=recommendation_cards,
            timeline=timeline
        )

# Global singleton
dashboard_adapter = DashboardAdapter()
