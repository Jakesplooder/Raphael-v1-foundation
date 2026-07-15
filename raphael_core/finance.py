import logging
from pydantic import BaseModel
from typing import Dict, Any
from .kernel.storage import KernelStorage
from .kernel.event_bus import emit

logger = logging.getLogger("rrk.executive.finance")
storage = KernelStorage()

class FinancialReport(BaseModel):
    venture_id: str
    revenue: float
    burn_rate: float
    runway_days: int

class FinanceIntelligence:
    def __init__(self):
        self.domain = "finance"

    def record_transaction(self, venture_id: str, amount: float, category: str):
        data = storage.load(self.domain, f"{venture_id}_ledger.json") or []
        data.append({"amount": amount, "category": category})
        storage.save(self.domain, f"{venture_id}_ledger.json", data)
        
        emit("TRANSACTION_RECORDED", "FinanceIntelligence", {
            "venture_id": venture_id,
            "amount": amount,
            "category": category
        })

    def generate_report(self, venture_id: str) -> FinancialReport:
        # Stub logic
        return FinancialReport(
            venture_id=venture_id,
            revenue=15000.0,
            burn_rate=2000.0,
            runway_days=180
        )
