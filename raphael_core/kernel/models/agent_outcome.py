from pydantic import BaseModel, Field
import datetime
from typing import Optional

class AgentOutcome(BaseModel):
    agent_id: str
    workflow_id: Optional[str] = None
    outcome_type: str
    importance: str = "normal"
    summary: str
    created_at: str = Field(default_factory=lambda: datetime.datetime.now().isoformat())
