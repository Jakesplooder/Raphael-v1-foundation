from typing import List
from ..core.interfaces import MarketSignalProvider
from ..core.models import MarketSignal

class MockMarketSignalProvider(MarketSignalProvider):
    def fetch_signals(self) -> List[MarketSignal]:
        return [
            MarketSignal(
                signal_id="SIGNAL-001",
                category="cybersecurity",
                source="market_research",
                observation="SMB compliance demand increased 40%",
                confidence=0.82,
                timestamp="2026-07-14"
            )
        ]
