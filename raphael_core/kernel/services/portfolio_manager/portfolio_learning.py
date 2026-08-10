import json
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime
from raphael_core.kernel.event_bus import emit

class PortfolioLearning:
    """
    Portfolio-Level Learning Engine.
    
    Raphael doesn't just learn which videos win — it learns which business models win.
    Tracks cross-portfolio patterns, business model comparisons, and strategic insights.
    """
    def __init__(self):
        self.learning_dir = Path(r"R:\RaphaelOS\Portfolio\Learning")
        self.learning_dir.mkdir(parents=True, exist_ok=True)
        self.learning_file = self.learning_dir / "portfolio_intelligence.json"
        self.intelligence = self._load()
        
    def _load(self) -> Dict[str, Any]:
        if self.learning_file.exists():
            return json.loads(self.learning_file.read_text(encoding="utf-8"))
        return {
            "business_model_learning": [],
            "venture_comparisons": [],
            "allocation_history": [],
            "last_updated": None
        }
        
    def save(self):
        self.intelligence["last_updated"] = datetime.now().isoformat()
        self.learning_file.write_text(json.dumps(self.intelligence, indent=2), encoding="utf-8")
    
    def record_allocation_cycle(self, allocations: Dict[str, Dict[str, Any]], businesses: List[Dict[str, Any]]):
        """
        Records the result of an allocation cycle for historical tracking.
        """
        cycle_record = {
            "timestamp": datetime.now().isoformat(),
            "businesses": {}
        }
        
        for b in businesses:
            twin = b["twin"]
            bid = twin.identity["business_id"]
            alloc = allocations.get(bid, {})
            cycle_record["businesses"][bid] = {
                "name": twin.identity["name"],
                "domain": twin.identity.get("domain", "unknown"),
                "lifecycle": twin.lifecycle.get_state(),
                "score": alloc.get("score", 0),
                "allocation_pct": alloc.get("allocation_pct", 0),
                "pool": alloc.get("pool", "unknown"),
                "confidence": twin.confidence,
                "roi": twin.financials.get("roi", 0)
            }
            
        self.intelligence["allocation_history"].append(cycle_record)
        self.save()
    
    def learn_from_portfolio(self, businesses: List[Dict[str, Any]]):
        """
        Extracts cross-portfolio patterns by comparing business models.
        """
        patterns = []
        
        # Group by domain to find domain-level insights
        domains = {}
        for b in businesses:
            twin = b["twin"]
            domain = twin.identity.get("domain", "unknown")
            if domain not in domains:
                domains[domain] = []
            domains[domain].append(twin)
        
        # Pattern: Which business model type performs best?
        model_scores = {}
        for b in businesses:
            twin = b["twin"]
            model = twin.strategy.get("business_model", twin.identity.get("category", "unknown"))
            roi = twin.financials.get("roi", 0)
            conf = twin.confidence
            if model not in model_scores:
                model_scores[model] = {"total_roi": 0, "total_confidence": 0, "count": 0}
            model_scores[model]["total_roi"] += roi
            model_scores[model]["total_confidence"] += conf
            model_scores[model]["count"] += 1
            
        for model, stats in model_scores.items():
            avg_roi = stats["total_roi"] / stats["count"]
            avg_conf = stats["total_confidence"] / stats["count"]
            
            if avg_roi > 5.0:
                patterns.append({
                    "pattern": f"{model} businesses show strong ROI performance",
                    "confidence": min(0.95, avg_conf),
                    "evidence": f"Average ROI: {avg_roi:.1f}"
                })
            elif avg_conf < 0.50 and stats["count"] > 0:
                patterns.append({
                    "pattern": f"{model} businesses require longer validation periods",
                    "confidence": round(0.30 + (1 - avg_conf) * 0.40, 2),
                    "evidence": f"Average confidence: {avg_conf:.2f}"
                })
        
        # Pattern: AI-assisted businesses
        ai_businesses = [b for b in businesses if b["twin"].strategy.get("business_model", "") != "" or b["twin"].identity.get("domain", "") in ["creator", "commerce"]]
        if len(ai_businesses) > 1:
            avg_score = sum(b.get("score", b["twin"].confidence) for b in ai_businesses) / len(ai_businesses)
            if avg_score > 0.40:
                patterns.append({
                    "pattern": "AI-assisted content and commerce businesses scale faster than manual operations",
                    "confidence": round(min(0.85, avg_score + 0.20), 2),
                    "evidence": f"Average portfolio score across {len(ai_businesses)} AI businesses: {avg_score:.2f}"
                })
        
        # Pattern: Marketplace businesses
        marketplace_businesses = [b for b in businesses if b["twin"].identity.get("domain", "") == "career"]
        if marketplace_businesses:
            avg_conf = sum(b["twin"].confidence for b in marketplace_businesses) / len(marketplace_businesses)
            if avg_conf < 0.60:
                patterns.append({
                    "pattern": "Marketplaces require longer validation due to two-sided network effects",
                    "confidence": round(0.40 + (1 - avg_conf) * 0.30, 2),
                    "evidence": f"Career domain avg confidence: {avg_conf:.2f}"
                })
        
        # Record and deduplicate patterns
        existing = {p["pattern"] for p in self.intelligence["business_model_learning"]}
        for p in patterns:
            if p["pattern"] not in existing:
                self.intelligence["business_model_learning"].append(p)
                existing.add(p["pattern"])
            else:
                # Update confidence of existing pattern
                for ep in self.intelligence["business_model_learning"]:
                    if ep["pattern"] == p["pattern"]:
                        ep["confidence"] = p["confidence"]
                        ep["evidence"] = p["evidence"]
                        break
                        
        self.save()
        return patterns
    
    def record_venture_comparison(self, ventures: List[Dict[str, Any]]):
        """
        Records a head-to-head comparison when ventures compete for exploration capital.
        """
        comparison = {
            "timestamp": datetime.now().isoformat(),
            "ventures": ventures
        }
        self.intelligence["venture_comparisons"].append(comparison)
        self.save()

portfolio_learning = PortfolioLearning()
