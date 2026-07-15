import logging
from typing import List
from .world_events import WorldEventBus
from .confidence.signal_confidence import SignalConfidenceEngine
from .providers.world_provider import WorldProvider
from .world_entities import WorldSignal

logger = logging.getLogger("rrk.world.runtime")

class WorldRuntime:
    def __init__(self, event_bus: WorldEventBus):
        self.event_bus = event_bus
        self.confidence_engine = SignalConfidenceEngine()
        self.providers: List[WorldProvider] = []
        
    def register_provider(self, provider: WorldProvider):
        self.providers.append(provider)
        
    async def run_cycle(self):
        all_signals = []
        for provider in self.providers:
            signals = await provider.collect_signals()
            all_signals.extend(signals)
            
        for signal in all_signals:
            conf = self.confidence_engine.evaluate(signal)
            if conf < 0.5:
                logger.info(f"Signal ignored due to LOW CONFIDENCE ({conf}): {signal.content}")
                continue
                
            # Broadcast events based on signal type
            if signal.type == "MARKET_TREND":
                self.event_bus.publish("MARKET_TREND_DETECTED", signal.model_dump())
            elif signal.type == "COMPETITOR_THREAT":
                self.event_bus.publish("COMPETITOR_THREAT", signal.model_dump())
            elif signal.type == "OPPORTUNITY_SIGNAL":
                self.event_bus.publish("OPPORTUNITY_SIGNAL", signal.model_dump())
