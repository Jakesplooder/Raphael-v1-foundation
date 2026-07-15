from abc import ABC, abstractmethod
from ..runtime.desktop_intent import DesktopIntent

class DesktopProvider(ABC):
    @abstractmethod
    async def observe(self) -> dict:
        """Capture and return the current screen state."""
        pass
        
    @abstractmethod
    async def execute_action(self, intent: DesktopIntent) -> dict:
        """Execute the desktop action described by the intent."""
        pass
        
    @abstractmethod
    async def verify_result(self, intent: DesktopIntent) -> dict:
        """Verify that the action produced the expected result."""
        pass
