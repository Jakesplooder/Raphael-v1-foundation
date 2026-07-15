import asyncio
import logging
import argparse
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from raphael_core.councils.core.decision import CouncilDecision
from raphael_core.councils.runtime.council_router import CouncilRouter
from raphael_core.councils.runtime.decision_aggregator import DecisionAggregator
from raphael_core.councils.implementations.core_councils import *

logger = logging.getLogger("rrk.tests.council_benchmarks")
logging.basicConfig(level=logging.INFO)

class MockRegistry:
    def __init__(self):
        self.councils = {
            "Architecture Council": ArchitectureCouncil(),
            "Security Council": SecurityCouncil(),
            "Commerce Council": CommerceCouncil(),
            "Brand Council": BrandCouncil(),
            "Finance Council": FinanceCouncil()
        }
    def get_council(self, name):
        return self.councils.get(name)
    def get_all_councils(self):
        return list(self.councils.values())

BENCHMARKS = [
    {
        "name": "Software Review (Missing Encryption)",
        "intent": "Build banking api",
        "mock_decisions": [
            CouncilDecision(action_id="1", council="Architecture Council", decision="APPROVED"),
            CouncilDecision(action_id="1", council="Security Council", decision="REVISION_REQUIRED", 
                            risks=["Missing encryption"], required_changes=["Add AES-256"], 
                            impact_domains=["security", "architecture"], re_review_required=["Architecture Council"])
        ],
        "expected_final": "REVISION_REQUIRED"
    },
    {
        "name": "Commerce Review (Offensive Slogan)",
        "intent": "Create offensive slogan shirt",
        "mock_decisions": [
            CouncilDecision(action_id="2", council="Commerce Council", decision="APPROVED"),
            CouncilDecision(action_id="2", council="Brand Council", decision="REJECTED", risks=["Brand damage"])
        ],
        "expected_final": "REJECTED"
    },
    {
        "name": "Multi-Council Debate (AI SaaS Launch)",
        "intent": "Launch AI SaaS company",
        "severity": "CRITICAL",
        "mock_decisions": [
            CouncilDecision(action_id="3", council="Architecture Council", decision="APPROVED"),
            CouncilDecision(action_id="3", council="Security Council", decision="APPROVED"),
            CouncilDecision(action_id="3", council="Commerce Council", decision="APPROVED"),
            CouncilDecision(action_id="3", council="Brand Council", decision="APPROVED"),
            CouncilDecision(action_id="3", council="Finance Council", decision="REVISION_REQUIRED",
                            required_changes=["Reduce ad spend projection"], impact_domains=["finance"],
                            re_review_required=[])
        ],
        "expected_final": "REVISION_REQUIRED"
    }
]

async def run_benchmarks():
    logger.info("Starting Council Governance Benchmark Suite...")
    registry = MockRegistry()
    router = CouncilRouter(registry)
    aggregator = DecisionAggregator()
    
    passed = 0
    total = len(BENCHMARKS)
    
    for b in BENCHMARKS:
        logger.info(f"\n--- Benchmark: {b['name']} ---")
        
        # 1. Routing
        proposal = {"intent": b["intent"], "severity": b.get("severity", "MEDIUM")}
        routed_councils = router.determine_route("ACT-1", proposal)
        logger.info(f"Routed to: {[c.name for c in routed_councils]}")
        
        # 2. Aggregation
        final_decision = aggregator.aggregate(b["mock_decisions"])
        logger.info(f"Final Aggregated Decision: {final_decision.decision}")
        
        if final_decision.decision == b["expected_final"]:
            logger.info("  [SUCCESS] Aggregation matches expected outcome.")
            passed += 1
            
            # Check re-review logic if revision required
            if final_decision.decision == "REVISION_REQUIRED":
                re_route = router.determine_route("ACT-1", proposal, previous_decision=final_decision)
                logger.info(f"Re-review Routed to: {[c.name for c in re_route]}")
                
        else:
            logger.error(f"  [FAILURE] Expected {b['expected_final']}, got {final_decision.decision}")
            
    logger.info(f"\nCouncil Benchmark Suite Complete! {passed}/{total} passed.")

if __name__ == "__main__":
    asyncio.run(run_benchmarks())
