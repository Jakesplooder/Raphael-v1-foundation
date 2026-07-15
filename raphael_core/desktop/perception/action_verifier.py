import logging

logger = logging.getLogger("rrk.desktop.perception.verifier")

class ActionVerifier:
    """After every desktop action, confirms the expected UI state was achieved."""
    
    def verify(self, expected: str, actual_screen: dict) -> dict:
        current_app = actual_screen.get("application", "unknown")
        if expected in str(actual_screen):
            logger.info(f"[ActionVerifier] Verification PASSED. Expected state confirmed in '{current_app}'.")
            return {"verified": True, "application": current_app}
        else:
            logger.warning(f"[ActionVerifier] Verification FAILED. Expected '{expected}' not found in '{current_app}'.")
            return {"verified": False, "application": current_app}
