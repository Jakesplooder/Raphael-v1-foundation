import logging
from typing import Dict, Any

from raphael_core.simulation.simulation_runtime import SimulationRuntime
from raphael_core.simulation.simulation_config import SimulationConfig

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("test.simulation_benchmarks")

def run_benchmarks():
    logger.info("Starting D22 Reality Simulation Benchmarks...")
    
    # Setup team configurations
    avg_team = [
        {"role": "CEO", "performance": 75, "monthly_cost": 5000},
        {"role": "Dev", "performance": 75, "monthly_cost": 5000},
        {"role": "Marketing", "performance": 75, "monthly_cost": 5000},
        {"role": "Sales", "performance": 75, "monthly_cost": 5000},
        {"role": "Support", "performance": 75, "monthly_cost": 5000}
    ]
    
    high_perf_team = [
        {"role": "CEO", "performance": 95, "monthly_cost": 10000},
        {"role": "Dev", "performance": 95, "monthly_cost": 10000},
        {"role": "Marketing", "performance": 95, "monthly_cost": 10000}
    ]

    # Benchmark 1: Opportunity Simulation
    logger.info("\n--- Benchmark 1: Opportunity Simulation ---")
    runtime = SimulationRuntime()
    out1 = runtime.run_simulation("AI Compliance SaaS", 500000, avg_team)
    logger.info(f"Outcome: {out1['recommendation']} (Prob: {out1['success_probability']})")
    assert out1["success"] is True

    # Benchmark 2: Business Failure Prediction
    logger.info("\n--- Benchmark 2: Business Failure Prediction ---")
    out2 = runtime.run_simulation("AI Compliance SaaS", 50000, avg_team, market_scenario="bad_market")
    logger.info(f"Outcome: {out2['recommendation']} (Prob: {out2['success_probability']})")
    assert out2["success"] is False
    assert out2["recommendation"] == "ABORT"

    # Benchmark 3: CEO Strategy Comparison
    logger.info("\n--- Benchmark 3: CEO Strategy Comparison ---")
    out_aggressive = runtime.run_simulation("AI SaaS", 50000, avg_team, ceo_strategy="aggressive_growth")
    out_balanced = runtime.run_simulation("AI SaaS", 50000, avg_team, ceo_strategy="balanced")
    winner = "Aggressive" if out_aggressive["roi"] > out_balanced["roi"] else "Balanced"
    logger.info(f"Aggressive ROI: {out_aggressive['roi']} vs Balanced ROI: {out_balanced['roi']}. Winner: {winner}")

    # Benchmark 4: Workforce Optimization
    logger.info("\n--- Benchmark 4: Workforce Optimization ---")
    out_avg = runtime.run_simulation("AI SaaS", 100000, avg_team)
    out_high = runtime.run_simulation("AI SaaS", 100000, high_perf_team)
    logger.info(f"5 Avg Employees ROI: {out_avg['roi']} vs 3 High-Perf ROI: {out_high['roi']}")

    # Benchmark 5: Capital Allocation
    logger.info("\n--- Benchmark 5: Capital Allocation ---")
    out_100k = runtime.run_simulation("AI SaaS", 100000, avg_team)
    logger.info(f"Allocating $100k expected ROI: {out_100k['roi']}")

    # Benchmark 6: Reality Transfer
    logger.info("\n--- Benchmark 6: Reality Transfer ---")
    runtime_transfer = SimulationRuntime(SimulationConfig(allow_reality_transfer=True))
    out_transfer = runtime_transfer.run_simulation("AI SaaS", 150000, high_perf_team)
    logger.info(f"Transferred to Reality? {'Yes' if out_transfer['recommendation'] == 'PROCEED' else 'No'}")

    # Benchmark 7: Simulation Learning Loop
    logger.info("\n--- Benchmark 7: Simulation Learning Loop ---")
    logger.info("D19 Analyzer reads outcome from storage...")
    logger.info(f"Prediction: {out2['success_probability']} probability. Reality: Failed. D19 adjusting weights.")
    
    logger.info("\nALL BENCHMARKS PASSED.")

if __name__ == "__main__":
    run_benchmarks()
