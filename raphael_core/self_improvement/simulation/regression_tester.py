import logging
from typing import Dict

logger = logging.getLogger("rrk.self_improvement.simulation")

class RegressionTester:
    """Ensures an improvement does not degrade existing capabilities."""
    
    def test(self, baseline_scores: Dict[str, float], post_change_scores: Dict[str, float],
             tolerance: float = 2.0) -> dict:
        regressions = []
        for component, baseline in baseline_scores.items():
            post = post_change_scores.get(component, 0)
            if post < baseline - tolerance:
                regressions.append({
                    "component": component,
                    "baseline": baseline,
                    "post_change": post,
                    "regression": round(baseline - post, 2)
                })
                
        passed = len(regressions) == 0
        
        if passed:
            logger.info(f"[RegressionTester] No regressions detected across {len(baseline_scores)} components.")
        else:
            logger.warning(f"[RegressionTester] {len(regressions)} regression(s) detected!")
            
        return {
            "passed": passed,
            "regressions": regressions,
            "components_tested": len(baseline_scores)
        }
