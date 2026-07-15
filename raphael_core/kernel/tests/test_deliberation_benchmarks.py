import asyncio
import logging
import argparse
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from raphael_core.deliberation.core.models import Argument
from raphael_core.deliberation.core.mock_managers import MockGoalManager
from raphael_core.deliberation.runtime.executive_context import ExecutiveContextEngine
from raphael_core.deliberation.memory.deliberation_memory import DeliberationMemoryService
from raphael_core.deliberation.strategies.resolution_strategies import RiskWeightedStrategy, UtilityAnalysisStrategy
from raphael_core.deliberation.runtime.deliberation_runtime import DeliberationRuntime

logger = logging.getLogger("rrk.tests.deliberation_benchmarks")
logging.basicConfig(level=logging.INFO)

BENCHMARKS = [
    {
        "name": "Conflict Resolution (Commerce vs Finance vs Security)",
        "action": "Launch SaaS product",
        "arguments": [
            Argument(source="Commerce Council", position="Support", argument="Large market opportunity"),
            Argument(source="Finance Council", position="Modify", argument="Customer acquisition cost unknown"),
            Argument(source="Security Council", position="Reject", argument="No data isolation strategy")
        ],
        "strategy": RiskWeightedStrategy(),
        "expected_resolution": "Create safer lower-cost launch plan"
    },
    {
        "name": "Strategic Tradeoff",
        "action": "Spend money now for growth",
        "arguments": [
            Argument(source="Finance Council", position="Modify", argument="Too expensive")
        ],
        "strategy": RiskWeightedStrategy(),
        "expected_resolution": "Risk-adjusted recommendation"
    },
    {
        "name": "Architecture Decision",
        "action": "Migrate to microservices vs monolith",
        "arguments": [],
        "strategy": UtilityAnalysisStrategy(),
        "expected_resolution": "Decision based on scale requirements"
    }
]

async def run_benchmarks():
    logger.info("Starting Deliberation Engine Benchmark Suite...")
    goal_manager = MockGoalManager()
    context_engine = ExecutiveContextEngine(goal_manager)
    memory_service = DeliberationMemoryService()
    
    passed = 0
    total = len(BENCHMARKS)
    
    for b in BENCHMARKS:
        logger.info(f"\n--- Benchmark: {b['name']} ---")
        runtime = DeliberationRuntime(context_engine, memory_service, b["strategy"])
        decision = await runtime.run_deliberation(b["action"], b["arguments"])
        
        logger.info(f"Final Resolution: {decision.final_resolution}")
        if decision.final_resolution == b["expected_resolution"]:
            logger.info("  [SUCCESS] Deliberation resolution matches expected outcome.")
            passed += 1
        else:
            logger.error(f"  [FAILURE] Expected '{b['expected_resolution']}', got '{decision.final_resolution}'")
            
    logger.info(f"\nDeliberation Benchmark Suite Complete! {passed}/{total} passed.")

if __name__ == "__main__":
    asyncio.run(run_benchmarks())
