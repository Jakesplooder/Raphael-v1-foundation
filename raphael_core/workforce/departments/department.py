import logging
from typing import List, Optional
from ..employees.employee import DigitalEmployee

logger = logging.getLogger("rrk.workforce.departments")

class Department:
    def __init__(self, name: str, department_id: str, venture_id: str, capacity: int = 10):
        self.name = name
        self.department_id = department_id
        self.venture_id = venture_id
        self.capacity = capacity
        self.roster: List[DigitalEmployee] = []
        
    @property
    def head_count(self) -> int:
        return len(self.roster)
        
    def hire(self, employee: DigitalEmployee) -> bool:
        if self.head_count >= self.capacity:
            logger.warning(f"[{self.name}] At capacity ({self.capacity}). Cannot hire.")
            return False
        employee.department = self.name
        self.roster.append(employee)
        logger.info(f"[{self.name}] Hired {employee.role}: {employee.id}")
        return True
        
    def reassign(self, employee_id: str) -> Optional[DigitalEmployee]:
        for i, emp in enumerate(self.roster):
            if emp.id == employee_id:
                removed = self.roster.pop(i)
                logger.info(f"[{self.name}] Reassigned {removed.role}: {removed.id}")
                return removed
        return None
        
    def retire(self, employee_id: str) -> bool:
        emp = self.reassign(employee_id)
        if emp:
            from ..employees.employee_state import EmployeeState
            emp.transition(EmployeeState.RETIRED)
            logger.info(f"[{self.name}] Retired {emp.role}: {emp.id}")
            return True
        return False

class EngineeringDept(Department):
    def __init__(self, venture_id: str):
        super().__init__("Engineering", f"DEPT-ENG-{venture_id}", venture_id)

class MarketingDept(Department):
    def __init__(self, venture_id: str):
        super().__init__("Marketing", f"DEPT-MKT-{venture_id}", venture_id)

class SalesDept(Department):
    def __init__(self, venture_id: str):
        super().__init__("Sales", f"DEPT-SAL-{venture_id}", venture_id)

class FinanceDept(Department):
    def __init__(self, venture_id: str):
        super().__init__("Finance", f"DEPT-FIN-{venture_id}", venture_id)

class OperationsDept(Department):
    def __init__(self, venture_id: str):
        super().__init__("Operations", f"DEPT-OPS-{venture_id}", venture_id)

class CustomerSuccessDept(Department):
    def __init__(self, venture_id: str):
        super().__init__("Customer Success", f"DEPT-CS-{venture_id}", venture_id)
