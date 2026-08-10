import logging
import uuid
from typing import Dict, Any, List
from ..core.models import DeliberationDecision, Argument
from .perspective_generator import PerspectiveGenerator
from .alternative_generator import AlternativeGenerator
from .executive_context import ExecutiveContextEngine
from ..strategies.resolution_strategies import ResolutionStrategy
from ..memory.deliberation_memory import DeliberationMemoryService

logger = logging.getLogger("rrk.deliberation.runtime")

class DeliberationRuntime:
    def __init__(self, context_engine: ExecutiveContextEngine, memory_service: DeliberationMemoryService, strategy: ResolutionStrategy):
        self.context_engine = context_engine
        self.memory_service = memory_service
        self.strategy = strategy
        self.perspective_gen = PerspectiveGenerator()
        self.alternative_gen = AlternativeGenerator()
        
    async def run_deliberation(self, original_action: str, council_arguments: List[Argument]) -> DeliberationDecision:
        decision_id = f"DEC-{uuid.uuid4().hex[:4].upper()}"
        logger.info(f"[{decision_id}] Starting deliberation for: {original_action}")
        
        # 1. Context & Perspectives
        context = self.context_engine.get_context()
        logger.info(f"[{decision_id}] Retrieved Executive Context. Active Goals: {context['active_goals']}")
        
        perspectives = self.perspective_gen.generate_perspectives({"task": original_action}, context['active_goals'])
        all_arguments = council_arguments + perspectives
        
        # 2. Alternatives
        logger.info(f"[{decision_id}] Generating alternatives...")
        options = self.alternative_gen.generate_options(original_action, all_arguments)
        
        # 3. Simulation
        logger.info(f"[{decision_id}] Simulating outcomes for {len(options)} options...")
        # Mocked simulation hook
        
        # 4. Resolve
        logger.info(f"[{decision_id}] Evaluating options via Resolution Strategy...")
        chosen_option = self.strategy.resolve(all_arguments, options, context)
        
        decision = DeliberationDecision(
            decision_id=decision_id,
            original_action=original_action,
            conflicts=["Identified from arguments"],
            options=options,
            final_resolution=chosen_option.description,
            confidence=0.88,
            uncertainty=["Simulated outcomes are probabilistic"],
            information_needed=["Run deeper market simulation"]
        )
        
        # 5. Memory
        self.memory_service.save_decision(decision)
        logger.info(f"[{decision_id}] Deliberation complete. Final Decision: {decision.final_resolution}")
        return decision
