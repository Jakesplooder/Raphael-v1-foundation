import logging
from ..employees.employee import DigitalEmployee
from ..employees.employee_state import EmployeeState

logger = logging.getLogger("rrk.workforce.training")

class EmployeeTraining:
    """
    When an employee's performance_score drops below threshold,
    they enter TRAINING state. Training improves their score
    based on historical failure analysis.
    """
    
    RETRAIN_THRESHOLD = 50.0
    TRAINING_BOOST = 15.0
    
    def needs_training(self, employee: DigitalEmployee) -> bool:
        return employee.performance_score < self.RETRAIN_THRESHOLD
        
    def train(self, employee: DigitalEmployee, mistakes: list) -> float:
        employee.transition(EmployeeState.TRAINING)
        
        # Boost proportional to how many mistakes were analyzed
        lesson_count = min(len(mistakes), 5)
        boost = self.TRAINING_BOOST + (lesson_count * 2)
        
        employee.performance_score = min(100.0, employee.performance_score + boost)
        employee.transition(EmployeeState.IMPROVING)
        
        logger.info(f"[Training] {employee.id} trained on {lesson_count} lessons. "
                     f"Score: {employee.performance_score:.1f}")
        return employee.performance_score
