import logging
from typing import List, Dict, Any
from ..core.models import Argument, Option

logger = logging.getLogger("rrk.deliberation.strategies")

class ResolutionStrategy:
    def resolve(self, arguments: List[Argument], options: List[Option], context: Dict[str, Any]) -> Option:
        pass

class RiskWeightedStrategy(ResolutionStrategy):
    def resolve(self, arguments: List[Argument], options: List[Option], context: Dict[str, Any]) -> Option:
        for opt in options:
            if "safe" in opt.description.lower() or "delay" in opt.description.lower() or "risk-adjusted" in opt.description.lower():
                opt.score += 50
        options.sort(key=lambda x: x.score, reverse=True)
        return options[0] if options else Option(option_id="UNKNOWN", description="None")

class UtilityAnalysisStrategy(ResolutionStrategy):
    def resolve(self, arguments: List[Argument], options: List[Option], context: Dict[str, Any]) -> Option:
        for opt in options:
            if "scale" in opt.description.lower():
                opt.score += 100
            elif "acquire" in opt.description.lower() or "business" in opt.description.lower():
                opt.score += 80
            elif "launch" in opt.description.lower() and "delay" not in opt.description.lower():
                opt.score += 40
        options.sort(key=lambda x: x.score, reverse=True)
        return options[0] if options else Option(option_id="UNKNOWN", description="None")
