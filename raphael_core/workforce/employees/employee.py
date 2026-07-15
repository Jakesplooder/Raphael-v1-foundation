from pydantic import BaseModel, Field
from typing import List, Optional
from .employee_state import EmployeeState

class EmployeeLineage(BaseModel):
    venture_id: str
    department_id: str
    employee_id: str
    created_by: str
    assigned_reason: str = ""

class DigitalEmployee(BaseModel):
    id: str
    role: str
    department: str
    skills: List[str] = Field(default_factory=list)
    authority_level: int = 1
    assigned_venture: str = ""
    performance_score: float = 50.0
    state: EmployeeState = EmployeeState.CREATED
    lineage: Optional[EmployeeLineage] = None
    
    def transition(self, new_state: EmployeeState):
        self.state = new_state
        
    def promote(self):
        self.authority_level = min(4, self.authority_level + 1)
        self.state = EmployeeState.PROMOTED
