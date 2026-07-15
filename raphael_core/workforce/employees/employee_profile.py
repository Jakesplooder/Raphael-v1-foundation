from pydantic import BaseModel, Field
from typing import List, Dict

class EmployeeProfile(BaseModel):
    employee_id: str
    specialization_depth: Dict[str, float] = Field(default_factory=dict)
    task_history: List[Dict] = Field(default_factory=list)
    promotions: int = 0
    total_tasks: int = 0
    successful_tasks: int = 0
    
    @property
    def success_rate(self) -> float:
        if self.total_tasks == 0:
            return 0.0
        return (self.successful_tasks / self.total_tasks) * 100
