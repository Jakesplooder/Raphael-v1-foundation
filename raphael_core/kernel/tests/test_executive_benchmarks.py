import asyncio
import logging
import argparse
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from raphael_core.executive.core.models import *
from raphael_core.executive.core.events import ExecutiveEventBus, ExecutiveEventType
from raphael_core.executive.managers.goal_manager import GoalManager
from raphael_core.executive.managers.kpi_manager import KPIManager
from raphael_core.executive.managers.portfolio_manager import PortfolioManager
from raphael_core.executive.opportunities.providers import MockMarketSignalProvider
from raphael_core.executive.opportunities.pipeline import SignalProcessor, OpportunityGenerator, OpportunityRanker

logger = logging.getLogger("rrk.tests.executive_benchmarks")
logging.basicConfig(level=logging.INFO)

async def run_benchmarks():
    logger.info("Starting Executive Intelligence Benchmark Suite...")
    passed = 0
    total = 4
    
    # 1. Goal Retrieval & Ownership
    logger.info("\n--- Benchmark 1: Goal Retrieval & Ownership ---")
    goal_manager = GoalManager()
    mission = Mission(
        statement="Build profitable autonomous businesses",
        objectives=[
            StrategicObjective(
                name="Launch cybersecurity venture",
                initiatives=[
                    Initiative(
                        name="Build security assessment platform",
                        owner="DeveloperAgent",
                        contributors=["ResearchAgent", "CommerceAgent"]
                    )
                ]
            )
        ]
    )
    goal_manager.set_mission(mission)
    owner = goal_manager.get_initiative_owner("Build security assessment platform")
    if owner == "DeveloperAgent":
        logger.info("  [SUCCESS] Initiative owner correctly resolved.")
        passed += 1
    else:
        logger.error(f"  [FAILURE] Owner was {owner}")
        
    # 2. KPI Trend & Event Emission
    logger.info("\n--- Benchmark 2: KPI Trend & Event Emission ---")
    bus = ExecutiveEventBus()
    event_emitted = []
    
    def on_kpi_risk(event):
        event_emitted.append(event)
        
    bus.subscribe(ExecutiveEventType.GOAL_AT_RISK, on_kpi_risk)
    
    kpi_manager = KPIManager(bus)
    kpi_manager.update_metric("CyberSecurity", "Customer_Acquisition_Cost", 100, 150)
    kpi_manager.update_metric("CyberSecurity", "Customer_Acquisition_Cost", 130, 150)
    kpi_manager.update_metric("CyberSecurity", "Customer_Acquisition_Cost", 180, 150)
    
    if len(event_emitted) > 0 and event_emitted[0].payload["trend"] == "POSITIVE" and event_emitted[0].payload["value"] > 150:
        logger.info("  [SUCCESS] KPI trend detected and GOAL_AT_RISK emitted.")
        passed += 1
    else:
        logger.error("  [FAILURE] KPI event not emitted correctly.")
        
    # 3. Portfolio Lifecycle
    logger.info("\n--- Benchmark 3: Portfolio Lifecycle ---")
    portfolio = PortfolioManager()
    v = Venture(name="Ocean Apparel")
    portfolio.register_venture(v)
    portfolio.update_venture_stage("Ocean Apparel", VentureStage.VALIDATING)
    portfolio.allocate_agent("Ocean Apparel", "CommerceAgent")
    
    if portfolio.ventures["Ocean Apparel"].stage == VentureStage.VALIDATING and "CommerceAgent" in portfolio.ventures["Ocean Apparel"].agents_assigned:
        logger.info("  [SUCCESS] Venture lifecycle and resources tracked.")
        passed += 1
    else:
        logger.error("  [FAILURE] Portfolio state incorrect.")
        
    # 4. Opportunity Pipeline
    logger.info("\n--- Benchmark 4: Opportunity Pipeline ---")
    provider = MockMarketSignalProvider()
    signals = provider.fetch_signals()
    
    processor = SignalProcessor()
    insights = processor.process(signals)
    
    generator = OpportunityGenerator()
    opps = generator.generate(insights)
    
    ranker = OpportunityRanker()
    ranked_opps = ranker.rank(opps)
    
    if len(ranked_opps) > 0 and ranked_opps[0].recommendation == "Explore":
        logger.info("  [SUCCESS] Opportunity generated and ranked with capability fit.")
        passed += 1
    else:
        logger.error("  [FAILURE] Opportunity pipeline failed.")
        
    logger.info(f"\nExecutive Benchmark Suite Complete! {passed}/{total} passed.")

if __name__ == "__main__":
    asyncio.run(run_benchmarks())
