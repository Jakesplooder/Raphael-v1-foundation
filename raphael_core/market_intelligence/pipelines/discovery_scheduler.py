import logging
import asyncio

logger = logging.getLogger("rrk.market.scheduler")

class DiscoveryScheduler:
    """
    Hybrid scheduler: Real-time event streams, 24h Discovery Cycles, 7d Strategic Reviews.
    """
    def __init__(self, event_bus, runtime):
        self.event_bus = event_bus
        self.runtime = runtime
        
        self.intervals = {
            "daily_discovery": 86400, # 24h
            "strategic_review": 604800 # 7d
        }
        
        # Subscribe to Tier 1 Real-time signals
        self.event_bus.subscribe("MARKET_SIGNAL_CREATED", self._handle_realtime_signal)

    def _handle_realtime_signal(self, event: dict):
        # Fast evaluation of urgent market shifts
        payload = event.get("payload", {})
        logger.info(f"Received fast-moving Tier 1 signal: {payload}")
        self.runtime.process_fast_signal(payload)
