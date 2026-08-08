import json
from pathlib import Path
from typing import Dict, Any, List
from .lifecycle import BusinessLifecycle, LifecycleState

class BaseTwin:
    def __init__(self, business_id: str, name: str, category: str, domain: str, storage_path: Path):
        self.business_id = business_id
        self.storage_path = storage_path
        self.version = 1
        
        # Core Contract
        self.identity = {
            "business_id": business_id,
            "name": name,
            "category": category,
            "domain": domain
        }
        
        self.lifecycle = BusinessLifecycle()
        
        self.financials = {
            "revenue": 0.0,
            "expenses": 0.0,
            "profit": 0.0,
            "roi": 0.0
        }
        
        self.operations = {
            "missions_attempted": 0,
            "missions_successful": 0,
            "approval_rate": 0.0,
            "average_quality": 0.0
        }
        
        self.strategy = {
            "active_strategies": [],
            "retired_strategies": []
        }
        
        self.learning = {
            "experiments_run": 0,
            "knowledge_base_size": 0
        }
        
        self.knowledge = {
            "observations": [],
            "hypotheses": [],
            "experiments": [],
            "strategies": []
        }
        
        self.growth = {
            "metrics": {}
        }
        
        self.risk = {
            "operational_risk": 0.10,
            "financial_risk": 0.10
        }
        
        self.confidence = 0.50
        
        self.venture_metadata = {
            "parent_portfolio": "Raphael Holdings",
            "founder": "Raphael OS",
            "incubation_budget": 0,
            "validation_deadline": "",
            "success_threshold": 0.0
        }
        
        self.decision_journal = []
        
        self._load()
        
    def _load(self):
        if self.storage_path.exists():
            data = json.loads(self.storage_path.read_text())
            self.version = data.get("version", 1)
            self.identity = data.get("identity", self.identity)
            
            state = data.get("lifecycle_state", "PROPOSED")
            self.lifecycle.transition(LifecycleState(state))
            
            # Map new or old keys
            self.financials = data.get("financials", data.get("financial_intelligence", self.financials))
            self.operations = data.get("operations", data.get("operational_intelligence", self.operations))
            self.strategy = data.get("strategy", data.get("strategic_intelligence", self.strategy))
            self.learning = data.get("learning", data.get("learning_intelligence", self.learning))
            
            knowledge_data = data.get("knowledge", {})
            self.knowledge = {
                "observations": knowledge_data.get("observations", self.knowledge["observations"]),
                "hypotheses": knowledge_data.get("hypotheses", self.knowledge["hypotheses"]),
                "experiments": knowledge_data.get("experiments", self.knowledge["experiments"]),
                "strategies": knowledge_data.get("strategies", self.knowledge["strategies"])
            }
            
            self.growth = data.get("growth", self.growth)
            self.risk = data.get("risk", self.risk)
            self.confidence = data.get("confidence", self.confidence)
            if isinstance(self.confidence, dict):
                self.confidence = self.confidence.get("business_model_confidence", 0.50)
            self.venture_metadata = data.get("venture_metadata", self.venture_metadata)
            self.decision_journal = data.get("decision_journal", self.decision_journal)

    def save(self):
        self.version += 1
        data = {
            "version": self.version,
            "identity": self.identity,
            "lifecycle_state": self.lifecycle.get_state(),
            "financials": self.financials,
            "operations": self.operations,
            "strategy": self.strategy,
            "learning": self.learning,
            "knowledge": self.knowledge,
            "growth": self.growth,
            "risk": self.risk,
            "confidence": self.confidence,
            "venture_metadata": self.venture_metadata,
            "decision_journal": self.decision_journal
        }
        self.storage_path.write_text(json.dumps(data, indent=2))
        
    def log_decision(self, decision: str, reasoning: List[str], expected_outcome: str):
        self.decision_journal.append({
            "decision": decision,
            "reasoning": reasoning,
            "expected_outcome": expected_outcome
        })
        self.save()
