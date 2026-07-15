import logging
import asyncio
from typing import List, Dict, Any

from ..intelligence.signal_fusion import SignalFusionEngine
from ..intelligence.opportunity_ranker import OpportunityRanker
from ..intelligence.opportunity_state import OpportunityState
from raphael_core.simulation.simulation_event_bus import SimulationEventBus

logger = logging.getLogger("rrk.market.runtime")

class IntelligenceRuntime:
    """
    Orchestrates the Discovery -> Generation -> Ranking -> Simulation pipeline.
    """
    def __init__(self, event_bus: SimulationEventBus):
        self.event_bus = event_bus
        self.fusion_engine = SignalFusionEngine()
        self.ranker = OpportunityRanker()
        self.signal_buffer = []

    def process_fast_signal(self, signal: dict):
        """Tier 1: Immediate routing or buffer addition"""
        self.signal_buffer.append(signal)

    def run_daily_discovery(self) -> List[Dict[str, Any]]:
        """Tier 2: Fuse signals, rank, and submit to council"""
        logger.info("Starting Daily Discovery Cycle...")
        
        # 1. Fuse
        fused_opp = self.fusion_engine.fuse_signals(self.signal_buffer)
        opportunities = []
        if fused_opp:
            opportunities.append(fused_opp)
            
        # Clear buffer
        self.signal_buffer = []
        
        if not opportunities:
            logger.info("No viable opportunities discovered today.")
            return []
            
        # 2. Rank
        ranked = self.ranker.rank_opportunities(opportunities)
        
        # 3. Submit to Council (Top Ranked)
        for opp in ranked[:3]:
            opp["state"] = OpportunityState.COUNCIL_REVIEW
            logger.info(f"Submitting {opp['name']} to Market Intelligence Council. OIS: {opp['ois_score']}")
            
            # Emit for Simulation Approval
            self.event_bus.emit("OPPORTUNITY_DISCOVERED", "IntelligenceRuntime", {"opportunity": opp})
            
        return ranked
