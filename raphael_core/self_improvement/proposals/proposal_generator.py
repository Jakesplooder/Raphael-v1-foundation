import logging
from .improvement_proposal import ImprovementProposal, ImprovementType, ImprovementLineage

logger = logging.getLogger("rrk.self_improvement.proposals")

class ProposalGenerator:
    """Given a bottleneck diagnosis, generates a concrete improvement proposal."""
    
    _next_id = 1
    
    def generate(self, bottleneck: dict) -> ImprovementProposal:
        prop_id = f"IMP-{self._next_id:03d}"
        self._next_id += 1
        
        component = bottleneck["component"]
        gap = bottleneck["gap"]
        severity = bottleneck["severity"]
        
        # Determine improvement type from component name
        if "Memory" in component or "memory" in component:
            imp_type = ImprovementType.MEMORY_OPTIMIZATION
        elif "Training" in component or "Employee" in component:
            imp_type = ImprovementType.SKILL_IMPROVEMENT
        elif "Workflow" in component or "Desktop" in component:
            imp_type = ImprovementType.WORKFLOW_OPTIMIZATION
        elif "CEO" in component or "Operator" in component:
            imp_type = ImprovementType.AGENT_BEHAVIOR_CHANGE
        elif "Architecture" in component or "Core" in component:
            imp_type = ImprovementType.ARCHITECTURE_CHANGE
        else:
            imp_type = ImprovementType.PROMPT_OPTIMIZATION
            
        proposal = ImprovementProposal(
            id=prop_id,
            improvement_type=imp_type,
            target=component,
            problem=f"{component} underperforming by {gap} points ({severity})",
            proposed_change=f"Optimize {component} targeting +{gap:.0f}% improvement",
            expected_gain=f"+{gap:.0f}% {component} score",
            risk_level="HIGH" if severity == "CRITICAL" else "MEDIUM",
            lineage=ImprovementLineage(
                improvement_id=prop_id,
                target_component=component,
                proposal_id=prop_id
            )
        )
        
        logger.info(f"[ProposalGenerator] Generated {prop_id}: {imp_type.value} for {component}")
        return proposal
