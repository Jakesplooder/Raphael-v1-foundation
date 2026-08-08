from typing import Dict, Any, List
import uuid
from ..kernel.models.business_objects import MetricDiagnosis, AssetPerformance, AnalyticsSnapshot

class MetricDiagnosisEngine:
    def __init__(self):
        # Eventually inject reasoning engine here
        pass

    def evaluate_rules(self, current: AssetPerformance) -> Dict[str, Any]:
        """Step 1 & 2: KPI Rules and Pattern Detection"""
        flags = []
        if current.views > 50000:
            flags.append("HIGH_IMPRESSIONS")
        if current.ctr < 2.0:
            flags.append("LOW_CTR")
        if current.retention > 50.0:
            flags.append("GOOD_RETENTION")
            
        category = "UNKNOWN"
        if "HIGH_IMPRESSIONS" in flags and "LOW_CTR" in flags and "GOOD_RETENTION" in flags:
            category = "PACKAGING_FAILURE"
            
        return {
            "flags": flags,
            "category": category
        }

    def _call_llm(self, rule_results: Dict[str, Any], current: AssetPerformance) -> Dict[str, Any]:
        """Step 4: LLM Explanation Layer (Mocked for now)"""
        # In a real system, we pass rule_results and current metrics to LLM
        if rule_results["category"] == "PACKAGING_FAILURE":
            return {
                "explanation": "Content quality appears acceptable (retention is strong), but low CTR indicates a title/thumbnail mismatch or weak hook.",
                "confidence": 0.85,
                "evidence": ["Strong distribution", "Weak click-through", "Content retention acceptable"],
                "recommended_actions": ["thumbnail redesign", "title variation"]
            }
        
        return {
            "explanation": "Unable to diagnose specific mechanical failure.",
            "confidence": 0.3,
            "evidence": rule_results["flags"],
            "recommended_actions": []
        }

    def run_diagnosis(self, asset_id: str, current_metrics: AssetPerformance, history: List[AnalyticsSnapshot]) -> MetricDiagnosis:
        """Runs the full diagnosis pipeline."""
        
        # 1. & 2. Rule evaluation
        rule_results = self.evaluate_rules(current_metrics)
        
        # 3. Historical comparison (Stubbed)
        # e.g., check if CTR is trending down over `history`
        
        # 4. LLM Explanation
        llm_results = self._call_llm(rule_results, current_metrics)
        
        # 5. Emit Diagnosis Object
        return MetricDiagnosis(
            id=f"diag_{uuid.uuid4().hex[:8]}",
            business_id=current_metrics.business_id,
            asset_id=asset_id,
            failed_metric="ctr" if "LOW_CTR" in rule_results["flags"] else "unknown",
            observed_metrics={
                "views": current_metrics.views,
                "ctr": current_metrics.ctr,
                "retention": current_metrics.retention
            },
            diagnosis_category=rule_results["category"],
            explanation=llm_results["explanation"],
            confidence=llm_results["confidence"],
            evidence=llm_results["evidence"],
            recommended_actions=llm_results["recommended_actions"]
        )
