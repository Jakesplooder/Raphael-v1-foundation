from typing import List
from .world_provider import WorldProvider
from ..world_entities import WorldSignal

class MockProvider(WorldProvider):
    def __init__(self):
        self.injected_signals = []
        
    def inject(self, signals: List[WorldSignal]):
        self.injected_signals.extend(signals)
        
    async def collect_signals(self) -> List[WorldSignal]:
        signals = self.injected_signals.copy()
        self.injected_signals.clear()
        return signals
