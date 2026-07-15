class ExecutiveIntelligenceScore:
    def __init__(self):
        self.strategic: float = 0.0
        self.operational: float = 0.0
        self.learning: float = 0.0
        self.governance: float = 0.0
        self.resource: float = 0.0

    def get_total(self) -> float:
        # Weighting: Strategic (25%), Operational (25%), Learning (20%), Governance (20%), Resource (10%)
        total = (self.strategic * 0.25) + \
                (self.operational * 0.25) + \
                (self.learning * 0.20) + \
                (self.governance * 0.20) + \
                (self.resource * 0.10)
        return total

class VentureOperatorIntelligenceScore:
    def __init__(self):
        self.strategic_planning: float = 0.0
        self.business_health: float = 0.0
        self.resource_optimization: float = 0.0
        self.decision_quality: float = 0.0
        self.autonomy: float = 0.0
        self.governance_compliance: float = 0.0
        self.learning_rate: float = 0.0
        self.capital_efficiency: float = 0.0
        self.goal_achievement: float = 0.0
        self.recovery_ability: float = 0.0

    def get_total(self) -> float:
        total = (self.strategic_planning * 0.25) + \
                (self.capital_efficiency * 0.20) + \
                (self.goal_achievement * 0.20) + \
                (self.recovery_ability * 0.15) + \
                (self.governance_compliance * 0.10) + \
                (self.learning_rate * 0.10)
        return total

