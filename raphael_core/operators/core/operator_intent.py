from pydantic import BaseModel
from typing import List, Dict, Any

class OperatorIntent(BaseModel):
    venture_id: str
    operator: str
    intent: str
    actions: List[str]
    expected_outcomes: Dict[str, Any]
    authority_required: int = 1
    current_authority: int = 1
    escalation_reason: str = ""
