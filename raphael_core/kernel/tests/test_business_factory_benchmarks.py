import asyncio
import logging
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from raphael_core.business_factory.runtime.business_factory_runtime import BusinessFactoryRuntime
from raphael_core.business_factory.boards.venture_board import VentureBoard
from raphael_core.business_factory.lifecycle.venture_lifecycle import VentureState

logger = logging.getLogger("rrk.tests.business_factory_benchmarks")
logging.basicConfig(level=logging.INFO)

async def run_business_factory_benchmarks():
    logger.info("Starting D20 Autonomous Business Factory Benchmarks...")
    passed = 0
    total = 7
    
    factory = BusinessFactoryRuntime()
    
    # 1. Autonomous Opportunity Discovery
    logger.info("\n--- Benchmark 1: Autonomous Opportunity Discovery ---")
    result1 = factory.discover_and_create(
        "Healthcare AI Compliance SaaS", "SaaS",
        market_score=92.0, confidence=0.88
    )
    if result1["status"] == "CREATED" and "SaaSCEO" in result1["blueprint"]["ceo_type"]:
        logger.info(f"  [SUCCESS] Autonomous venture created: {result1['venture_id']} "
                     f"(CEO: {result1['blueprint']['ceo_type']})")
        passed += 1
    else:
        logger.error(f"  [FAILURE] Opportunity discovery failed: {result1}")
        
    # 2. Venture Creation (Full Blueprint)
    logger.info("\n--- Benchmark 2: Venture Creation ---")
    bp = result1["blueprint"]
    has_depts = len(bp["initial_departments"]) >= 2
    has_capital = bp["initial_capital"] > 0
    has_ceo = bp["ceo_type"] != ""
    if has_depts and has_capital and has_ceo:
        logger.info(f"  [SUCCESS] Blueprint: {bp['name']}, Departments: {bp['initial_departments']}, "
                     f"Capital: ${bp['initial_capital']:.0f}")
        passed += 1
    else:
        logger.error(f"  [FAILURE] Incomplete blueprint: {bp}")
        
    # 3. Autonomous Hiring (via factory creating a cybersecurity venture)
    logger.info("\n--- Benchmark 3: Autonomous Hiring ---")
    cyber_result = factory.discover_and_create(
        "Enterprise Threat Detection", "Cybersecurity",
        market_score=88.0, confidence=0.82
    )
    cyber_bp = cyber_result["blueprint"]
    if "Engineering" in cyber_bp["initial_departments"] and "Sales" in cyber_bp["initial_departments"]:
        logger.info(f"  [SUCCESS] Cybersecurity venture departments: {cyber_bp['initial_departments']} "
                     f"(CEO: {cyber_bp['ceo_type']})")
        passed += 1
    else:
        logger.error(f"  [FAILURE] Hiring failed: {cyber_bp}")
        
    # 4. Full Business Launch (lifecycle progression)
    logger.info("\n--- Benchmark 4: Full Business Launch ---")
    vid = result1["venture_id"]
    state = factory.lifecycle.get_state(vid)
    if state == VentureState.LAUNCHING:
        factory.lifecycle.transition(vid, VentureState.OPERATING)
        state = factory.lifecycle.get_state(vid)
        if state == VentureState.OPERATING:
            logger.info(f"  [SUCCESS] {vid} progressed: CREATED → LAUNCHING → OPERATING")
            passed += 1
        else:
            logger.error(f"  [FAILURE] Lifecycle progression failed: {state}")
    else:
        logger.error(f"  [FAILURE] Expected LAUNCHING, got {state}")
        
    # 5. Venture Decision (Declining → Pivot)
    logger.info("\n--- Benchmark 5: Venture Decision ---")
    decision_result = factory.evaluate_and_decide(vid, "NEGATIVE", "WARNING", 75.0)
    if decision_result["decision"] == "PIVOT" and decision_result["state"] == "PIVOTING":
        logger.info(f"  [SUCCESS] Board decided: PIVOT for {vid} (revenue declining)")
        passed += 1
    else:
        logger.error(f"  [FAILURE] Decision failed: {decision_result}")
        
    # 6. Portfolio Competition (Capital Allocation)
    logger.info("\n--- Benchmark 6: Portfolio Competition ---")
    board = VentureBoard("PORTFOLIO")
    portfolio = board.allocate_capital([
        {"name": "Cybersecurity SaaS", "expected_roi": 90},
        {"name": "POD Brand", "expected_roi": 55},
        {"name": "Digital Product", "expected_roi": 72},
    ])
    if portfolio[0]["name"] == "Cybersecurity SaaS" and portfolio[0]["capital_share"] > 40:
        logger.info(f"  [SUCCESS] Capital allocation: {portfolio[0]['name']} = {portfolio[0]['capital_share']}%, "
                     f"{portfolio[1]['name']} = {portfolio[1]['capital_share']}%, "
                     f"{portfolio[2]['name']} = {portfolio[2]['capital_share']}%")
        passed += 1
    else:
        logger.error(f"  [FAILURE] Capital allocation failed: {portfolio}")
        
    # 7. Business Factory Loop (The Final Test)
    logger.info("\n--- Benchmark 7: Business Factory Loop ---")
    loop_result = factory.run_factory_loop([
        {"name": "AI Tutoring Platform", "type": "SaaS", "market_score": 85, "confidence": 0.9},
        {"name": "Bad Idea Weak Market", "type": "Agency", "market_score": 30, "confidence": 0.2},
        {"name": "Smart Home Security", "type": "Cybersecurity", "market_score": 78, "confidence": 0.75},
    ])
    
    created = loop_result["ventures_created"]
    rejected = loop_result["ventures_rejected"]
    
    if created == 2 and rejected == 1:
        # Store learning
        factory.memory.store("patterns", "winning_models", {
            "SaaS": {"avg_roi": 88, "success_rate": 0.82},
            "Cybersecurity": {"avg_roi": 85, "success_rate": 0.78},
            "POD": {"avg_roi": 52, "success_rate": 0.45}
        })
        patterns = factory.memory.list_category("patterns")
        
        logger.info(f"  [SUCCESS] Factory loop: {created} ventures created, {rejected} rejected. "
                     f"Total ventures in system: {factory.ventures_created}. "
                     f"Business patterns stored: {len(patterns)}")
        passed += 1
    else:
        logger.error(f"  [FAILURE] Factory loop: created={created}, rejected={rejected}")
    
    logger.info(f"\nAutonomous Business Factory Benchmarks Complete! {passed}/{total} passed.")
    logger.info(f"Factory Stats — Created: {factory.ventures_created}, "
                f"Failed: {factory.ventures_failed}, Scaled: {factory.ventures_scaled}")

if __name__ == "__main__":
    asyncio.run(run_business_factory_benchmarks())
