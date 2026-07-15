import logging
from typing import Dict, Any, List
from pydantic import BaseModel, Field

logger = logging.getLogger("rrk.councils.memory.decision")

class DecisionRecord(BaseModel):
    action_id: str
    revision: int = 1
    previous_decisions: List[str] = Field(default_factory=list)
    new_changes: List[str] = Field(default_factory=list)

class DecisionMemoryService:
    """Bridges Agent Memory and World Model by tracking the 'Why' behind decisions."""
    def __init__(self):
        self.records: Dict[str, DecisionRecord] = {}
        
    def track_revision(self, action_id: str, previous_decision: str, new_change: str):
        if action_id not in self.records:
            self.records[action_id] = DecisionRecord(action_id=action_id)
        
        record = self.records[action_id]
        record.revision += 1
        record.previous_decisions.append(previous_decision)
        record.new_changes.append(new_change)
        
        logger.info(f"[{action_id}] Decision revision tracked (v{record.revision}).")
