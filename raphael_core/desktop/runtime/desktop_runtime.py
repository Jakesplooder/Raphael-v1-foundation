import logging
from .desktop_state import DesktopState
from .desktop_intent import DesktopIntent
from .desktop_authority import DesktopAuthority
from ..providers.desktop_provider import DesktopProvider

logger = logging.getLogger("rrk.desktop.runtime")

class DesktopRuntime:
    """
    The main perception-action loop for desktop interaction.
    Observe → Plan → Authority Check → Execute → Verify → Learn.
    """
    
    def __init__(self, authority: DesktopAuthority):
        self.state = DesktopState.IDLE
        self.authority = authority
        self.provider = None
        self.action_log = []
        
    def set_provider(self, provider: DesktopProvider):
        self.provider = provider
        
    def transition(self, new_state: DesktopState):
        logger.info(f"[DesktopRuntime] {self.state.value} -> {new_state.value}")
        self.state = new_state
        
    async def execute_intent(self, intent: DesktopIntent) -> dict:
        if not self.provider:
            raise ValueError("No DesktopProvider registered")
        
        # 1. Observe
        self.transition(DesktopState.OBSERVING)
        screen_state = await self.provider.observe()
        
        # 2. Plan
        self.transition(DesktopState.PLANNING)
        
        # 3. Authority Check
        self.transition(DesktopState.AUTHORITY_CHECK)
        auth_result = self.authority.evaluate_intent(intent)
        
        if auth_result["decision"] != "APPROVED":
            self.transition(DesktopState.BLOCKED)
            self.action_log.append({"intent": intent.action, "result": "BLOCKED", "reason": auth_result["decision"]})
            return {"status": "BLOCKED", "reason": auth_result["decision"]}
        
        # 4. Execute
        self.transition(DesktopState.EXECUTING)
        exec_result = await self.provider.execute_action(intent)
        
        # 5. Verify
        self.transition(DesktopState.VERIFYING)
        verification = await self.provider.verify_result(intent)
        
        # 6. Learn
        self.transition(DesktopState.LEARNING)
        outcome = {
            "status": "SUCCESS" if verification.get("verified", False) else "FAILED",
            "intent": intent.action,
            "steps_completed": exec_result.get("steps_completed", 0),
            "verification": verification
        }
        self.action_log.append(outcome)
        
        self.transition(DesktopState.IDLE)
        return outcome
