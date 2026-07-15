from abc import ABC, abstractmethod
from typing import Dict, Any

class AutomationProvider(ABC):
    """
    Abstract interface for all automation execution providers (e.g. Python, n8n, Docker).
    """

    @property
    @abstractmethod
    def provider_name(self) -> str:
        pass

    @abstractmethod
    async def execute_step(self, action: str, parameters: Dict[str, Any], idempotency_key: str = None) -> Dict[str, Any]:
        """
        Execute a single automation step.
        Must raise an exception or return a result dict indicating success/failure details.
        """
        pass
