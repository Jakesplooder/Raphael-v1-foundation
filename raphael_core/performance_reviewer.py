from typing import List, Dict, Any
from datetime import datetime
import json
import os
import uuid
import statistics

PERFORMANCE_WEIGHTS = {
    "productivity":    0.35,  
    "accuracy":        0.30,  
    "reliability":     0.25,  
    "cost_efficiency": 0.10,  
}

class PerformanceEvaluator:
    """
    Calculates the four dimensions of agent performance.
    """
    def calculate_scores(self, agent_id: str, raw_metrics: Dict[str, float]) -> Dict[str, float]:
        # raw_metrics provided by external mock for testing, 
        # in reality extracted from agent_runtime, llm_ledger, world_model, canary
        
        # Calculate individual dimension scores
        prod = min(100.0, max(0.0, raw_metrics.get("productivity_raw", 75.0)))
        acc = min(100.0, max(0.0, raw_metrics.get("accuracy_raw", 75.0)))
        rel = min(100.0, max(0.0, raw_metrics.get("reliability_raw", 75.0)))
        cost = min(100.0, max(0.0, raw_metrics.get("cost_efficiency_raw", 75.0)))
        
        # Composite score
        comp = (prod * PERFORMANCE_WEIGHTS["productivity"] +
                acc * PERFORMANCE_WEIGHTS["accuracy"] +
                rel * PERFORMANCE_WEIGHTS["reliability"] +
                cost * PERFORMANCE_WEIGHTS["cost_efficiency"])
                
        return {
            "productivity": round(prod, 1),
            "accuracy": round(acc, 1),
            "reliability": round(rel, 1),
            "cost_efficiency": round(cost, 1),
            "composite": round(comp, 1)
        }

class TrustTierAssessor:
    def assess_trust_tier_recommendation(
        self,
        agent_id: str,
        current_tier: int,
        reviews: List[Dict[str, Any]],
        safety_pressure_history: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        if len(reviews) < 3:
            return {"action": "none", "reason": "insufficient_history"}
            
        recent_3 = reviews[-3:]
        recent_composite = statistics.mean([r["scores"]["composite"] for r in recent_3])
        
        # Mock trend determination
        pressure_trend = safety_pressure_history[-1].get("trend", "stable") if safety_pressure_history else "stable"
        
        if recent_composite >= 85 and pressure_trend == "improving" and current_tier < 4:
            return {
                "action": "promote",
                "evidence": [r["review_id"] for r in recent_3],
                "confidence": 0.78
            }
            
        if recent_composite < 60 or pressure_trend == "critically_degrading":
            return {
                "action": "demote",
                "evidence": [r["review_id"] for r in recent_3],
                "confidence": 0.85
            }
            
        return {"action": "none", "reason": "within_acceptable_range"}

class ReviewCadenceManager:
    """
    Governs continuous collection, Weekly snapshots, and Monthly crystallizations.
    """
    def generate_weekly_snapshot(self, agent_id: str, raw_metrics: Dict[str, float], prev_composite: float) -> Dict[str, Any]:
        evaluator = PerformanceEvaluator()
        scores = evaluator.calculate_scores(agent_id, raw_metrics)
        delta = scores["composite"] - prev_composite
        
        if delta <= -15 or delta >= 20:
            # Significant deviation, surface as initiative queue item
            return {
                "surfaced": True,
                "initiative_item": {
                    "type": "workforce_lifecycle",
                    "signal": "weekly_performance_anomaly",
                    "entity": agent_id,
                    "current_state": "active",
                    "reason": f"Significant performance deviation detected: {delta:+.1f} points",
                    "evidence": [],
                    "authority_required": False,
                    "priority_score": 0.70,
                    "status": "Detected"
                }
            }
        return {"surfaced": False}

    def generate_monthly_review(self, agent_id: str, raw_metrics: Dict[str, float], prev_composite: float) -> Dict[str, Any]:
        evaluator = PerformanceEvaluator()
        scores = evaluator.calculate_scores(agent_id, raw_metrics)
        delta = scores["composite"] - prev_composite
        
        if delta > 0:
            trend = "improving"
        elif delta < 0:
            trend = "degrading"
        else:
            trend = "stable"
            
        period = datetime.utcnow().strftime("%Y-%m")
        rid = f"REVIEW-{agent_id}-{period}-{str(uuid.uuid4())[:4]}"
        
        record = {
            "review_id": rid,
            "agent_id": agent_id,
            "review_period": period,
            "review_type": "monthly",
            "scores": scores,
            "trend": trend,
            "trend_delta": round(delta, 1),
            "highlights": ["Calculated from simulated metrics."],
            "concerns": [],
            "trust_tier_recommendation": None,
            "trust_tier_evidence": [],
            "generated_by": "Raphael Core",
            "reviewed_by_aaron": False,
            "aaron_notes": None,
            "constitutional_compliance": True,
            "source_reference": "agent_runtime.json + llm_ledger.json + world_model",
            "confidence": 0.84,
        }
        
        from .world_model_emitter import emit_performance_review
        emit_performance_review(record)
        
        return record
