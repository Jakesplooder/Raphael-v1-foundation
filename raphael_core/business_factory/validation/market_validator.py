import logging

logger = logging.getLogger("rrk.business_factory.validation")

class MarketValidator:
    """
    Validates an opportunity before Raphael invests in creating a venture.
    Prevents 'cool idea, bad business.'
    """
    
    MINIMUM_MARKET_SCORE = 60.0
    MINIMUM_CONFIDENCE = 0.5
    
    def validate(self, opportunity_name: str, market_score: float,
                 confidence: float, competitor_count: int = 0) -> dict:
        issues = []
        
        if market_score < self.MINIMUM_MARKET_SCORE:
            issues.append(f"Market score {market_score} below minimum {self.MINIMUM_MARKET_SCORE}")
        if confidence < self.MINIMUM_CONFIDENCE:
            issues.append(f"Confidence {confidence} below minimum {self.MINIMUM_CONFIDENCE}")
        if competitor_count > 20:
            issues.append(f"Oversaturated market: {competitor_count} competitors")
            
        passed = len(issues) == 0
        
        if passed:
            logger.info(f"[MarketValidator] '{opportunity_name}' VALIDATED "
                         f"(score: {market_score}, confidence: {confidence})")
        else:
            logger.warning(f"[MarketValidator] '{opportunity_name}' REJECTED: {issues}")
            
        return {
            "validated": passed,
            "opportunity": opportunity_name,
            "issues": issues,
            "market_score": market_score,
            "confidence": confidence
        }
