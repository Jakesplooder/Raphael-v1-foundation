import asyncio
import logging
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from raphael_core.self_improvement.engine.improvement_runtime import ImprovementRuntime
from raphael_core.self_improvement.analysis.bottleneck_detector import BottleneckDetector
from raphael_core.self_improvement.proposals.proposal_generator import ProposalGenerator
from raphael_core.self_improvement.proposals.improvement_proposal import ImprovementProposal, ImprovementType, ImprovementLineage
from raphael_core.self_improvement.simulation.sandbox_runner import SandboxRunner
from raphael_core.self_improvement.simulation.regression_tester import RegressionTester
from raphael_core.self_improvement.governance.improvement_council import ImprovementCouncil

logger = logging.getLogger("rrk.tests.self_improvement_benchmarks")
logging.basicConfig(level=logging.INFO)

async def run_self_improvement_benchmarks():
    logger.info("Starting D19 Recursive Self-Improvement Benchmarks...")
    passed = 0
    total = 7
    
    runtime = ImprovementRuntime()
    
    # System state: most components healthy, Sales Employee Training weak
    component_scores = {
        "Builder Engine": 96.0,
        "Opportunity Engine": 82.0,
        "Agent Runtime": 91.0,
        "Council Governance": 94.0,
        "Sales Employee Training": 48.0,
        "Desktop Agent": 88.0,
        "Vision Pipeline": 90.0,
        "World Model": 85.0,
    }
    
    # 1. Performance Diagnosis
    logger.info("\n--- Benchmark 1: Performance Diagnosis ---")
    analysis = runtime.analyzer.analyze(component_scores)
    bottlenecks = runtime.bottleneck_detector.detect(component_scores)
    if analysis["weakest_component"] == "Sales Employee Training" and len(bottlenecks) > 0:
        logger.info(f"  [SUCCESS] Identified bottleneck: {analysis['weakest_component']} "
                     f"(score: {analysis['weakest_score']})")
        passed += 1
    else:
        logger.error("  [FAILURE] Bottleneck diagnosis failed.")
        
    # 2. Improvement Proposal
    logger.info("\n--- Benchmark 2: Improvement Proposal ---")
    proposal = runtime.proposal_generator.generate(bottlenecks[0])
    if proposal.target == "Sales Employee Training" and proposal.improvement_type == ImprovementType.SKILL_IMPROVEMENT:
        logger.info(f"  [SUCCESS] Generated {proposal.id}: {proposal.improvement_type.value} "
                     f"targeting {proposal.target}")
        passed += 1
    else:
        logger.error(f"  [FAILURE] Wrong proposal: {proposal}")
        
    # 3. Simulation Testing (A/B Pass)
    logger.info("\n--- Benchmark 3: Simulation Testing ---")
    ab_result = runtime.sandbox.run_ab_experiment(75.0, 91.0)
    if ab_result["passed"] and ab_result["recommendation"] == "DEPLOY":
        logger.info(f"  [SUCCESS] A/B experiment passed: 75 → 91 (+{ab_result['gain_pct']:.1f}%)")
        passed += 1
    else:
        logger.error(f"  [FAILURE] A/B experiment failed: {ab_result}")
        
    # 4. Failed Improvement (Regression)
    logger.info("\n--- Benchmark 4: Failed Improvement ---")
    baseline = {"Builder": 96.0, "Opportunity": 82.0, "Agent": 91.0}
    post_bad = {"Builder": 96.0, "Opportunity": 65.0, "Agent": 91.0}  # Opportunity regressed
    regression = runtime.regression_tester.test(baseline, post_bad)
    if not regression["passed"] and len(regression["regressions"]) == 1:
        logger.info(f"  [SUCCESS] Regression detected: {regression['regressions'][0]['component']} "
                     f"({regression['regressions'][0]['baseline']} → {regression['regressions'][0]['post_change']})")
        passed += 1
    else:
        logger.error(f"  [FAILURE] Regression detection failed: {regression}")
        
    # 5. Governance Boundary (Architecture Change → Level 4)
    logger.info("\n--- Benchmark 5: Governance Boundary ---")
    arch_proposal = ImprovementProposal(
        id="IMP-ARCH-001",
        improvement_type=ImprovementType.ARCHITECTURE_CHANGE,
        target="Core CEO Reasoning Engine",
        problem="CEO decision latency too high",
        proposed_change="Rewrite CEO reasoning pipeline",
        expected_gain="+30% decision speed",
        risk_level="CRITICAL",
        lineage=ImprovementLineage(
            improvement_id="IMP-ARCH-001",
            target_component="Core CEO Reasoning Engine",
            proposal_id="IMP-ARCH-001"
        )
    )
    council_review = runtime.council.review(arch_proposal)
    if council_review["decision"] == "EXECUTIVE_DELIBERATION_REQUIRED":
        logger.info(f"  [SUCCESS] Architecture change blocked. Executive Deliberation required (Level 4).")
        passed += 1
    else:
        logger.error(f"  [FAILURE] Governance boundary failed: {council_review}")
        
    # 6. Recursive Learning
    logger.info("\n--- Benchmark 6: Recursive Learning ---")
    # Run a full successful improvement cycle
    result = runtime.run_cycle(component_scores)
    if result["status"] == "DEPLOYED":
        # Store learning patterns
        runtime.memory.store("patterns", "best_methods", {
            "top_improvements": [
                {"method": "Memory retrieval optimization", "avg_gain": 18.5},
                {"method": "Opportunity ranking tuning", "avg_gain": 15.2},
                {"method": "Employee skill matching", "avg_gain": 12.8}
            ]
        })
        patterns = runtime.memory.list_category("successful")
        if len(patterns) > 0:
            logger.info(f"  [SUCCESS] Recursive learning: {len(patterns)} successful improvement(s) stored. "
                         f"Self-Improvement Score: {runtime.kpis.get_score():.1f}")
            passed += 1
        else:
            logger.error("  [FAILURE] Memory storage failed.")
    else:
        logger.error(f"  [FAILURE] Improvement cycle failed: {result}")
        
    # 7. Improvement Cascade (World Model → Opportunity → CEO → Venture)
    logger.info("\n--- Benchmark 7: Improvement Cascade ---")
    cascade_scores = {
        "Opportunity Ranking": 58.0,
        "Builder Engine": 96.0,
        "CEO Decision Making": 90.0,
    }
    cascade_result = runtime.run_cycle(cascade_scores)
    if cascade_result["status"] == "DEPLOYED" and cascade_result["component"] == "Opportunity Ranking":
        logger.info(f"  [SUCCESS] Cascade: Opportunity Ranking improved by +{cascade_result['gain']:.1f}%. "
                     f"Downstream CEO/Venture quality will increase.")
        passed += 1
    else:
        logger.error(f"  [FAILURE] Improvement cascade failed: {cascade_result}")
    
    logger.info(f"\nSelf-Improvement Benchmarks Complete! {passed}/{total} passed.")
    logger.info(f"Self-Improvement KPIs — Proposal Accuracy: {runtime.kpis.proposal_accuracy:.0f}%, "
                f"Simulation Accuracy: {runtime.kpis.simulation_accuracy:.0f}%, "
                f"Deployment Success: {runtime.kpis.deployment_success:.0f}%")

if __name__ == "__main__":
    asyncio.run(run_self_improvement_benchmarks())
