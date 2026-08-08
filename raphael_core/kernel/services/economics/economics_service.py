from typing import Dict, Any
import raphael_core.kernel.event_bus as event_bus

class EconomicsService:
    def __init__(self):
        self.total_revenue = 0.0
        self.total_expenses = 0.0
        
    def record_expense(self, amount: float, category: str, context: Dict[str, Any]):
        self.total_expenses += amount
        event_bus.emit("FINANCE.EXPENSE_RECORDED", "EconomicsService", {
            "amount": amount,
            "category": category,
            "context": context
        })
        
    def record_revenue(self, amount: float, source: str, context: Dict[str, Any]):
        self.total_revenue += amount
        event_bus.emit("FINANCE.REVENUE_RECORDED", "EconomicsService", {
            "amount": amount,
            "source": source,
            "context": context
        })
        
    def calculate_roi(self, expected_return: float, cost: float):
        roi = expected_return - cost
        event_bus.emit("FINANCE.ROI_CALCULATED", "EconomicsService", {
            "expected_return": expected_return,
            "cost": cost,
            "roi": roi
        })
        return roi

economics_service = EconomicsService()
