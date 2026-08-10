import logging
from ..core.venture_operator import VentureOperator

logger = logging.getLogger("rrk.operators.runtime")

class OperatorRuntime:
    def __init__(self):
        pass
        
    def run_cycle(self, operator: VentureOperator):
        # A simple synchronous wrapper for the tick method
        operator.tick()
        
    async def async_run_cycle(self, operator: VentureOperator):
        # Future concurrency readiness
        self.run_cycle(operator)
