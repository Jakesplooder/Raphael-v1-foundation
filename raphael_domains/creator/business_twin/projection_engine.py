from typing import Dict, Any
from raphael_core.kernel.event_bus import emit
from raphael_domains.creator.business_twin.twin import BusinessTwin

class CreatorProjectionEngine:
    def __init__(self, twin: BusinessTwin):
        self.twin = twin
        
    def handle_observation_captured(self, payload: Dict[str, Any]):
        print(f"DEBUG: Appending observation")
        self.twin.knowledge["observations"].append(payload)
        self.twin.save()

    def handle_hypothesis_created(self, payload: Dict[str, Any]):
        """
        Payload expects a hypothesis dict.
        We check if it exists, if not, we add it. We don't automatically change strategy.
        """
        hyp_id = payload.get("id")
        existing = [h for h in self.twin.knowledge["hypotheses"] if h.get("id") == hyp_id]
        
        if not existing:
            print(f"DEBUG: Appending hypothesis {hyp_id}")
            self.twin.knowledge["hypotheses"].append(payload)
            # Propose an experiment for this hypothesis
            exp_id = f"exp_{hyp_id}"
            experiment = {
                "experiment_id": exp_id,
                "hypothesis_id": hyp_id,
                "control_group": {"type": "AI Marketing", "missions": 1},
                "test_group": {"type": "Business Case Studies", "missions": 7},
                "metrics": {
                    "quality_score": True,
                    "approval_rate": True,
                    "production_time": True,
                    "human_feedback": True
                },
                "started_at": "",
                "completed_at": "",
                "result": "pending"
            }
            self.twin.knowledge["experiments"].append(experiment)
            self.twin.save()
            
            # The human acts as the gate here. When approved, STRATEGY.EXPERIMENT_STARTED is emitted.

    def handle_experiment_started(self, payload: Dict[str, Any]):
        """
        Payload expects:
        {
            "experiment_id": str,
            "hypothesis_id": str
        }
        """
        exp_id = payload.get("experiment_id")
        hyp_id = payload.get("hypothesis_id")
        
        # Update experiment state
        for exp in self.twin.knowledge["experiments"]:
            if exp["experiment_id"] == exp_id:
                exp["result"] = "running"
                break
                
        # Update hypothesis state
        for hyp in self.twin.knowledge["hypotheses"]:
            if hyp["id"] == hyp_id:
                hyp["state"] = "EXPERIMENT_RUNNING"
                break
                
        self.twin.save()
        
    def handle_experiment_completed(self, payload: Dict[str, Any]):
        """
        Payload expects:
        {
            "experiment_id": str,
            "hypothesis_id": str,
            "result": "validated" | "rejected",
            "new_evidence": {
                "sample_size": int,
                "avg_quality": float,
                "approval_rate": float
            }
        }
        """
        exp_id = payload.get("experiment_id")
        hyp_id = payload.get("hypothesis_id")
        result = payload.get("result")
        new_evidence = payload.get("new_evidence", {})
        
        self.twin.learning["experiments_run"] += 1
        
        for exp in self.twin.knowledge["experiments"]:
            if exp["experiment_id"] == exp_id:
                exp["result"] = result
                break
                
        for hyp in self.twin.knowledge["hypotheses"]:
            if hyp["id"] == hyp_id:
                hyp["state"] = "VALIDATED" if result == "validated" else "REJECTED"
                
                if result == "validated":
                    self.twin.learning["experiments_successful"] += 1
                    self.twin.strategy.setdefault("validated_strategies", 0)
                    self.twin.strategy["validated_strategies"] += 1
                    
                    # Bayesian update mock: confidence moves closer to 1.0 based on sample size
                    prior = hyp["confidence"]
                    sample_size = new_evidence.get("sample_size", 10)
                    bump = 0.05 + (0.1 * (sample_size / 30.0))
                    posterior = min(0.99, prior + bump)
                    hyp["confidence"] = round(posterior, 2)
                    
                    # Upgrade to formal strategy
                    strategy_name = hyp.get("strategy_action", {}).get("decision", hyp["name"])
                    strategy_obj = {
                        "strategy": strategy_name,
                        "state": "ACTIVE",
                        "confidence": hyp["confidence"],
                        "sample_size": sample_size,
                        "last_validated": "2026-07-16",
                        "decay_rate": 0.05,
                        "next_review_required": "2026-08-16",
                        "evidence_store": {
                            "prior_confidence": prior,
                            "new_evidence": new_evidence,
                            "posterior_confidence": hyp["confidence"],
                            "calculation": {
                                "method": "bayesian_update",
                                "timestamp": "2026-07-16"
                            }
                        }
                    }
                    self.twin.knowledge["strategies"].append(strategy_obj)
                    
                    self.twin.log_decision(
                        decision_id=f"decision_{exp_id}",
                        decision=strategy_name,
                        reasoning=[f"Experiment {exp_id} validated. Bayesian posterior: {hyp['confidence']} (n={sample_size})"],
                        confidence=hyp["confidence"],
                        expected_outcome="Improved engagement"
                    )
                else:
                    self.twin.learning.setdefault("experiments_failed", 0)
                    self.twin.learning["experiments_failed"] += 1
                    self.twin.strategy.setdefault("rejected_strategies", 0)
                    self.twin.strategy["rejected_strategies"] += 1
                break
                
        self.twin.save()

    def handle_quality_scored(self, payload: Dict[str, Any]):
        """
        Payload expects:
        {
            "mission_id": str,
            "scores": Dict[str, float]
        }
        """
        scores = payload.get("scores", {})
        if scores:
            self.twin.operations["missions_approved"] += 1
            self.twin.operations["missions_successful"] += 1
            self.twin.operations["missions_attempted"] += 1
            
            # Simple rolling average
            current_avg = self.twin.operations.get("average_quality", 0.0)
            current_count = self.twin.operations["missions_approved"]
            
            # Assuming score is in a 'quality' key or we just average all sub-scores
            avg_subscore = sum(scores.values()) / len(scores) if scores else 0
            
            new_avg = ((current_avg * (current_count - 1)) + avg_subscore) / current_count
            self.twin.operations["average_quality"] = round(new_avg, 2)
            self.twin.operations["approval_rate"] = 1.0 # Mocking 100% approval rate
            self.twin.save()

    def handle_finance_expense(self, payload: Dict[str, Any]):
        self.twin.financials["expenses"] += payload.get("amount", 0.0)
        self.twin.financials["profit"] = self.twin.financials["revenue"] - self.twin.financials["expenses"]
        
        # Update cost_per_mission
        if self.twin.operations["missions_attempted"] > 0:
            self.twin.financials.setdefault("cost_per_mission", 0.0)
            self.twin.financials["cost_per_mission"] = round(self.twin.financials["expenses"] / self.twin.operations["missions_attempted"], 2)
            
        self.twin.save()
        
    def handle_finance_revenue(self, payload: Dict[str, Any]):
        self.twin.financials["revenue"] += payload.get("amount", 0.0)
        self.twin.financials["profit"] = self.twin.financials["revenue"] - self.twin.financials["expenses"]
        self.twin.save()
