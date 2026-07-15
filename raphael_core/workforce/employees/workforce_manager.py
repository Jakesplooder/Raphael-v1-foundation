import logging
from typing import List, Optional
from ..employees.employee import DigitalEmployee, EmployeeLineage
from ..employees.employee_state import EmployeeState
from ..departments.department import Department
from ..skills.skill_registry import SkillRegistry

logger = logging.getLogger("rrk.workforce.manager")

class WorkforceManager:
    """
    CEO Intent → WorkforceManager → Skill Matching → Hire/Create/Train.
    
    CEOs do not directly create employees. They express capability needs.
    The WorkforceManager resolves those needs from the labor pool.
    """
    
    def __init__(self, skill_registry: SkillRegistry):
        self.skill_registry = skill_registry
        self.employee_pool: List[DigitalEmployee] = []
        self._next_id = 1
        
    def request_capability(self, venture_id: str, department: Department, 
                           role: str, required_skills: List[str], 
                           requested_by: str) -> Optional[DigitalEmployee]:
        """
        CEO requests a capability. WorkforceManager attempts to:
        1. Find existing employee with matching skills
        2. Create new employee if none available
        """
        # 1. Search pool for best match
        best_match = None
        best_score = -1
        for emp in self.employee_pool:
            if emp.state == EmployeeState.RETIRED:
                continue
            if emp.assigned_venture and emp.assigned_venture != venture_id:
                continue
            match_score = len(set(emp.skills) & set(required_skills))
            if match_score > best_score:
                best_score = match_score
                best_match = emp
                
        if best_match and best_score > 0:
            best_match.assigned_venture = venture_id
            best_match.transition(EmployeeState.ACTIVE)
            department.hire(best_match)
            logger.info(f"[WorkforceManager] Matched existing employee {best_match.id} for {role}")
            return best_match
            
        # 2. Create new employee
        emp_id = f"EMP-{self._next_id:03d}"
        self._next_id += 1
        new_emp = DigitalEmployee(
            id=emp_id,
            role=role,
            department=department.name,
            skills=required_skills,
            authority_level=1,
            assigned_venture=venture_id,
            performance_score=50.0,
            state=EmployeeState.CREATED,
            lineage=EmployeeLineage(
                venture_id=venture_id,
                department_id=department.department_id,
                employee_id=emp_id,
                created_by=requested_by,
                assigned_reason=f"CEO requested {role} capability"
            )
        )
        new_emp.transition(EmployeeState.TRAINING)
        department.hire(new_emp)
        self.employee_pool.append(new_emp)
        logger.info(f"[WorkforceManager] Created new employee {emp_id}: {role}")
        return new_emp
        
    def select_best_for_task(self, skill_name: str) -> Optional[DigitalEmployee]:
        """Select the highest-performing employee with the required skill."""
        candidates = [e for e in self.employee_pool 
                      if skill_name in e.skills and e.state != EmployeeState.RETIRED]
        if not candidates:
            return None
        return max(candidates, key=lambda e: e.performance_score)
