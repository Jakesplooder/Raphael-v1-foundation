from .desktop_provider import DesktopProvider
from ..runtime.desktop_intent import DesktopIntent

class MockDesktopProvider(DesktopProvider):
    def __init__(self):
        self.screen_state = {"application": "none", "elements": []}
        self.injected_results = {}
        self.injected_verifications = {}
        
    def set_screen(self, state: dict):
        self.screen_state = state
        
    def inject_result(self, action: str, result: dict):
        self.injected_results[action] = result
        
    def inject_verification(self, action: str, verification: dict):
        self.injected_verifications[action] = verification
        
    async def observe(self) -> dict:
        return self.screen_state
        
    async def execute_action(self, intent: DesktopIntent) -> dict:
        return self.injected_results.get(intent.action, {"steps_completed": len(intent.steps)})
        
    async def verify_result(self, intent: DesktopIntent) -> dict:
        return self.injected_verifications.get(intent.action, {"verified": True, "screenshot": "mock_screenshot.png"})
