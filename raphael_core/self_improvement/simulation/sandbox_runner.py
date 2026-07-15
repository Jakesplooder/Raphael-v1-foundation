import logging

logger = logging.getLogger("rrk.self_improvement.simulation")

class SandboxRunner:
    """
    Runs 'Current Raphael vs Improved Raphael' benchmark comparisons.
    Includes A/B experiment engine for measurable gain validation.
    """
    
    def run_ab_experiment(self, current_score: float, improved_score: float,
                          current_samples: int = 100, improved_samples: int = 100) -> dict:
        gain = improved_score - current_score
        gain_pct = (gain / current_score * 100) if current_score > 0 else 0
        
        passed = improved_score > current_score
        
        result = {
            "current_score": current_score,
            "improved_score": improved_score,
            "gain": round(gain, 2),
            "gain_pct": round(gain_pct, 2),
            "current_samples": current_samples,
            "improved_samples": improved_samples,
            "passed": passed,
            "recommendation": "DEPLOY" if passed else "REJECT"
        }
        
        if passed:
            logger.info(f"[SandboxRunner] A/B PASSED: {current_score} → {improved_score} (+{gain_pct:.1f}%)")
        else:
            logger.warning(f"[SandboxRunner] A/B FAILED: {current_score} → {improved_score} ({gain_pct:.1f}%)")
            
        return result
