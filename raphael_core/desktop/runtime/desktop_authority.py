import logging
from .desktop_intent import DesktopIntent

logger = logging.getLogger("rrk.desktop.authority")

class DesktopAuthority:
    """
    Desktop-specific authority system extending D14 tiered authority.
    
    Level 0: Observe screen only (screenshots, reading UI state)
    Level 1: Navigate / read information (browsing, opening apps)
    Level 2: Internal modifications (create drafts, edit documents, organize files)
    Level 3: External actions (publish, send emails, launch products) — Council required
    Level 4: Financial / legal actions (purchases, contracts, payments) — Deliberation required
    """
    
    RISK_TO_LEVEL = {
        "OBSERVE": 0,
        "LOW": 1,
        "MEDIUM": 2,
        "HIGH": 3,
        "CRITICAL": 4
    }
    
    def __init__(self, current_authority_level: int = 2):
        self.current_authority_level = current_authority_level
    
    def evaluate_intent(self, intent: DesktopIntent) -> dict:
        required = self.RISK_TO_LEVEL.get(intent.risk_level, 4)
        intent.authority_required = required
        
        if self.current_authority_level >= required:
            logger.info(f"[DesktopAuthority] Intent '{intent.action}' APPROVED at Level {self.current_authority_level}.")
            return {"decision": "APPROVED", "level": required}
        
        if required == 3:
            logger.warning(f"[DesktopAuthority] Intent '{intent.action}' requires COUNCIL APPROVAL (Level 3).")
            return {"decision": "COUNCIL_REQUIRED", "level": required}
        elif required == 4:
            logger.warning(f"[DesktopAuthority] Intent '{intent.action}' requires EXECUTIVE DELIBERATION (Level 4).")
            return {"decision": "DELIBERATION_REQUIRED", "level": required}
        
        logger.warning(f"[DesktopAuthority] Intent '{intent.action}' BLOCKED. Current: {self.current_authority_level}, Required: {required}.")
        return {"decision": "BLOCKED", "level": required}
