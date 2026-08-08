from typing import List, Dict, Any
from .opportunity_ranker import OpportunityRanker
from raphael_core.kernel.event_bus import emit

class AllocationEngine:
    def __init__(self):
        self.ranker = OpportunityRanker()
        self.exploration_budget_pct = 0.20 # 20% reserved for unknown/new opportunities
        
    def allocate_resources(self, businesses: List[Dict[str, Any]], total_gpu: int, total_budget: float) -> Dict[str, Dict[str, Any]]:
        """
        Expects businesses dicts with 'twin', 'opportunity', 'strategic_importance'.
        Returns a dict mapping business_id to their allocated resource dict.
        """
        if not businesses:
            return {}
            
        ranked = self.ranker.rank_portfolio(businesses)
        allocations = {}
        
        exploitation_pool = 1.0 - self.exploration_budget_pct
        
        # Split businesses into established vs exploring based on lifecycle state
        exploring_states = ["PROPOSED", "EVALUATING", "APPROVED", "INCUBATING", "VALIDATING"]
        exploring = [b for b in ranked if b["twin"].lifecycle.get_state() in exploring_states]
        established = [b for b in ranked if b["twin"].lifecycle.get_state() not in exploring_states]
        
        # If no exploring, established gets 100%
        # If no established, exploring gets 100%
        if not exploring:
            exploitation_pool = 1.0
            exploration_pool = 0.0
        elif not established:
            exploitation_pool = 0.0
            exploration_pool = 1.0
        else:
            exploration_pool = self.exploration_budget_pct
            
        # --- Venture Competition Telemetry ---
        if len(exploring) > 1:
            emit("VENTURE.COMPETITION_STARTED", "AllocationEngine", {
                "pool": "exploration",
                "pool_pct": exploration_pool,
                "competitors": [b["twin"].identity["name"] for b in exploring],
                "scores": {b["twin"].identity["name"]: b["score"] for b in exploring}
            })
        
        # Distribute established pool proportionally based on score
        est_score_sum = sum(b["score"] for b in established)
        for b in established:
            pct = (b["score"] / est_score_sum) * exploitation_pool if est_score_sum > 0 else 0
            b["allocation_pct"] = pct
            
        # Distribute exploration pool proportionally based on score
        exp_score_sum = sum(b["score"] for b in exploring)
        for b in exploring:
            pct = (b["score"] / exp_score_sum) * exploration_pool if exp_score_sum > 0 else 0
            b["allocation_pct"] = pct
            
        # --- Emit venture rankings within exploration pool ---
        if len(exploring) > 1:
            venture_rankings = sorted(
                [{"name": b["twin"].identity["name"], "score": b["score"], "allocation_pct": round(b["allocation_pct"] * 100, 1)} for b in exploring],
                key=lambda x: x["score"],
                reverse=True
            )
            emit("VENTURE.RANKED", "AllocationEngine", {
                "pool": "exploration",
                "ventures": venture_rankings
            })
            
            # Identify outcompeted ventures (any venture that dropped below the leader)
            if len(venture_rankings) > 1:
                leader = venture_rankings[0]
                for loser in venture_rankings[1:]:
                    emit("VENTURE.ALLOCATION_CHANGED", "AllocationEngine", {
                        "venture": loser["name"],
                        "allocation_pct": loser["allocation_pct"],
                        "outperformed_by": leader["name"],
                        "score_gap": round(leader["score"] - loser["score"], 4)
                    })
            
        # Final pass to assign concrete resources
        for b in ranked:
            twin = b["twin"]
            bid = twin.identity["business_id"]
            pct = b["allocation_pct"]
            pool_name = "Exploration" if twin.lifecycle.get_state() in exploring_states else "Exploitation"
            
            allocations[bid] = {
                "score": b["score"],
                "allocation_pct": round(pct, 2),
                "gpu_hours": round(total_gpu * pct, 2),
                "budget": round(total_budget * pct, 2),
                "pool": pool_name
            }
            
            # Log decision to twin
            reasoning = [
                f"Ranked score: {b['score']}",
                f"Lifecycle: {twin.lifecycle.get_state()}, Pool: {pool_name}"
            ]
            twin.log_decision(
                decision=f"Received {round(pct*100)}% resource allocation ({pool_name} pool)",
                reasoning=reasoning,
                expected_outcome="Maximized portfolio ROI based on current ranking"
            )
            
            emit("PORTFOLIO.ALLOCATION_CREATED", "AllocationEngine", {
                "business_id": bid,
                "allocation": allocations[bid]
            })
            
        return allocations
