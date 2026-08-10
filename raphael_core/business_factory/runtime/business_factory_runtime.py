import logging
from ..genesis.venture_generator import VentureGenerator
from ..lifecycle.venture_lifecycle import VentureLifecycle, VentureState
from ..validation.market_validator import MarketValidator
from ..boards.venture_board import VentureBoard
from ..memory.business_memory import BusinessMemory

logger = logging.getLogger("rrk.business_factory.runtime")

class BusinessFactoryRuntime:
    """
    The complete autonomous enterprise loop:
    
    World Signal → Opportunity → Validate → Create Venture → Assign CEO →
    Form Departments → Hire Employees → Build Product → Launch →
    Measure KPIs → Board Review → Scale/Pivot/Shutdown → Learn → Repeat
    """
    
    def __init__(self):
        self.lifecycle = VentureLifecycle()
        self.generator = VentureGenerator(self.lifecycle)
        self.validator = MarketValidator()
        self.memory = BusinessMemory()
        self.ventures_created = 0
        self.ventures_failed = 0
        self.ventures_scaled = 0
        
    def discover_and_create(self, opportunity_name: str, venture_type: str,
                             market_score: float, confidence: float) -> dict:
        """Full autonomous venture creation pipeline."""
        
        # 1. Validate market
        validation = self.validator.validate(opportunity_name, market_score, confidence)
        if not validation["validated"]:
            return {"status": "REJECTED", "reason": validation["issues"]}
            
        # 2. Generate venture
        blueprint = self.generator.generate(
            opportunity_name, venture_type, market_score, confidence
        )
        self.ventures_created += 1
        
        # 3. Transition to LAUNCHING
        self.lifecycle.transition(blueprint.venture_id, VentureState.LAUNCHING)
        
        # 4. Board formation
        board = VentureBoard(blueprint.venture_id)
        
        logger.info(f"[BusinessFactory] Autonomous venture created: {blueprint.venture_id} "
                     f"({blueprint.name}, CEO: {blueprint.ceo_type})")
        
        return {
            "status": "CREATED",
            "venture_id": blueprint.venture_id,
            "blueprint": blueprint.model_dump(),
            "board": board
        }
        
    def evaluate_and_decide(self, venture_id: str, revenue_trend: str,
                             kpi_health: str, market_score: float) -> dict:
        """Board evaluates venture health and decides next action."""
        
        board = VentureBoard(venture_id)
        evaluation = board.evaluate_venture(revenue_trend, kpi_health, market_score)
        decision = evaluation["decision"]
        
        # Track outcomes
        if decision == "SHUTDOWN":
            self.ventures_failed += 1
            self.lifecycle.transition(venture_id, VentureState.FAILED)
            self.memory.store("failed", venture_id, {
                "reason": "Board shutdown decision",
                "revenue_trend": revenue_trend,
                "kpi_health": kpi_health
            })
        elif decision == "SCALE":
            self.ventures_scaled += 1
            self.lifecycle.transition(venture_id, VentureState.SCALING)
            self.memory.store("successful", venture_id, {
                "outcome": "Scaled",
                "revenue_trend": revenue_trend,
                "market_score": market_score
            })
        elif decision == "PIVOT":
            self.lifecycle.transition(venture_id, VentureState.PIVOTING)
            
        return {
            "venture_id": venture_id,
            "decision": decision,
            "state": self.lifecycle.get_state(venture_id).value
        }
        
    def run_factory_loop(self, opportunities: list) -> dict:
        """Run one complete factory iteration across multiple opportunities."""
        results = []
        
        for opp in opportunities:
            result = self.discover_and_create(
                opp["name"], opp["type"],
                opp["market_score"], opp["confidence"]
            )
            results.append(result)
            
        return {
            "opportunities_processed": len(opportunities),
            "ventures_created": sum(1 for r in results if r["status"] == "CREATED"),
            "ventures_rejected": sum(1 for r in results if r["status"] == "REJECTED"),
            "results": results
        }
