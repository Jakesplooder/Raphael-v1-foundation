import abc
from typing import List
from .models import MarketSignal

class MarketSignalProvider(abc.ABC):
    @abc.abstractmethod
    def fetch_signals(self) -> List[MarketSignal]: pass
