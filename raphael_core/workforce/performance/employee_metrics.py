import logging

logger = logging.getLogger("rrk.workforce.performance")

class EmployeeMetrics:
    """
    Employee Intelligence Score:
    
    Task Success        25%
    Decision Quality    20%
    Resource Efficiency 15%
    Learning Rate       15%
    Customer Impact     10%
    Autonomy Growth     15%
    """
    
    def calculate(self, task_success: float, decision_quality: float,
                  resource_efficiency: float, learning_rate: float,
                  customer_impact: float, autonomy_growth: float) -> float:
        score = (task_success * 0.25) + \
                (decision_quality * 0.20) + \
                (resource_efficiency * 0.15) + \
                (learning_rate * 0.15) + \
                (customer_impact * 0.10) + \
                (autonomy_growth * 0.15)
        return round(score, 2)
