from typing import Dict, Any
from .near_miss_logger import get_recent_near_misses

class SafetyAuditorAgent:
    """
    Reviews what happened. Retroactive analysis of near-misses.
    Part of the Security Council.
    """
    def generate_audit_report(self, days: int = 7) -> Dict[str, Any]:
        misses = get_recent_near_misses(hours=days * 24)
        
        report = {
            "period_days": days,
            "total_near_misses": len(misses),
            "findings": []
        }
        
        if len(misses) > 10:
            report["findings"].append("High volume of near-misses detected. Recommend tightening thresholds.")
            
        return report

def run_safety_audit() -> Dict[str, Any]:
    auditor = SafetyAuditorAgent()
    return auditor.generate_audit_report()
