from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum

class ImprovementType(str, Enum):
    MEMORY_OPTIMIZATION = "MEMORY_OPTIMIZATION"
    PROMPT_OPTIMIZATION = "PROMPT_OPTIMIZATION"
    SKILL_IMPROVEMENT = "SKILL_IMPROVEMENT"
    WORKFLOW_OPTIMIZATION = "WORKFLOW_OPTIMIZATION"
    AGENT_BEHAVIOR_CHANGE = "AGENT_BEHAVIOR_CHANGE"
    ARCHITECTURE_CHANGE = "ARCHITECTURE_CHANGE"

# Maps ImprovementType → minimum authority level required
IMPROVEMENT_AUTHORITY = {
    ImprovementType.MEMORY_OPTIMIZATION: 1,
    ImprovementType.PROMPT_OPTIMIZATION: 2,
    ImprovementType.SKILL_IMPROVEMENT: 2,
    ImprovementType.WORKFLOW_OPTIMIZATION: 2,
    ImprovementType.AGENT_BEHAVIOR_CHANGE: 3,
    ImprovementType.ARCHITECTURE_CHANGE: 4,
}

class ImprovementLineage(BaseModel):
    improvement_id: str
    target_component: str
    proposal_id: str
    simulation_id: Optional[str] = None
    council_decision_id: Optional[str] = None
    deployment_id: Optional[str] = None
    result_id: Optional[str] = None

class ImprovementProposal(BaseModel):
    id: str
    improvement_type: ImprovementType
    target: str
    problem: str
    proposed_change: str
    expected_gain: str
    risk_level: str = "LOW"
    authority_required: int = 1
    lineage: Optional[ImprovementLineage] = None
    
    def __init__(self, **data):
        super().__init__(**data)
        self.authority_required = IMPROVEMENT_AUTHORITY.get(self.improvement_type, 4)
