import json
import os
from datetime import datetime
from typing import Dict, Any, List

class ConstitutionalViolationError(Exception):
    pass

class AgentRuntimeRegistry:
    def __init__(self, filepath: str = os.path.join(os.environ.get("RAPHAEL_DATA_DIR", r"C:\RaphaelOS"), r"\workforce\agent_runtime.json")):
        self.filepath = filepath
        # Ensure dir exists
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
        if not os.path.exists(self.filepath):
            self.save_registry({})
            
    def load_registry(self) -> Dict[str, Any]:
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {}

    def save_registry(self, data: Dict[str, Any]):
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
            
    def get_agent(self, agent_id: str) -> Dict[str, Any]:
        data = self.load_registry()
        return data.get(agent_id)
        
    def update_agent(self, agent_id: str, record: Dict[str, Any]):
        data = self.load_registry()
        data[agent_id] = record
        self.save_registry(data)
        
    def create_agent_record(self, agent_id: str, display_name: str, trust_tier: int, council: str, capabilities: List[str], model: str) -> Dict[str, Any]:
        record = {
            "agent_id": agent_id,
            "display_name": display_name,
            "trust_tier": trust_tier,
            "current_state": "created",
            "state_entered_at": datetime.utcnow().isoformat(),
            "previous_state": None,
            "active_task_count": 0,
            "safety_pressure_score": 0.0,
            "consecutive_days_overloaded": 0,
            "last_activity_at": datetime.utcnow().isoformat(),
            "onboarding_completed_at": None,
            "council": council,
            "capabilities": capabilities,
            "assigned_model": model,
            "world_model_node_id": f"{agent_id}-NODE",
            "performance_baseline": None,
            "training_version": None,
            "onboarding_checklist": {}
        }
        self.update_agent(agent_id, record)
        return record

class AgentLifecycleManager:
    VALID_TRANSITIONS = {
        "created":      ["onboarding"],
        "onboarding":   ["active", "suspended"],
        "active":       ["overloaded", "under_review", "suspended"],
        "overloaded":   ["active", "recovering", "under_review"],
        "recovering":   ["active", "under_review"],
        "under_review": ["active", "suspended", "retired"],
        "suspended":    ["under_review", "retired"],
        "retired":      [],  # terminal state
    }
    
    AUTHORITY_REQUIRED_TRANSITIONS = {
        "retired",      # always requires Aaron
        "suspended",    # requires Aaron (significant action)
    }
    
    OPERATIONAL_TRANSITIONS = {
        "onboarding",
        "active", 
        "overloaded",
        "recovering",
        "under_review",  # Raphael recommends, Aaron reviews
    }

    def __init__(self, registry: AgentRuntimeRegistry):
        self.registry = registry

    def request_transition(self, agent_id: str, target_state: str, reason: str, evidence: List[str]) -> Dict[str, Any]:
        agent = self.registry.get_agent(agent_id)
        if not agent:
            raise ValueError(f"Agent {agent_id} not found in runtime registry.")
            
        current_state = agent.get("current_state", "created")
        
        # Validate transition
        if target_state not in self.VALID_TRANSITIONS.get(current_state, []):
            raise ConstitutionalViolationError(f"Invalid transition from {current_state} to {target_state}")
            
        # Emergency Suspension Circuit Breaker
        if target_state == "suspended" and agent.get("safety_pressure_score", 0) >= 80:
            return self._execute_transition(agent, "suspended", reason, evidence)
            
        # Enforce Authority Boundries
        if target_state in self.AUTHORITY_REQUIRED_TRANSITIONS:
            # Generate Initiative Queue Item
            return self._create_lifecycle_initiative(agent, target_state, reason, evidence)
            
        return self._execute_transition(agent, target_state, reason, evidence)

    def _execute_transition(self, agent: Dict[str, Any], target_state: str, reason: str, evidence: List[str]) -> Dict[str, Any]:
        # Emit World Model Event
        from .world_model_emitter import emit_lifecycle_event
        emit_lifecycle_event(agent["agent_id"], agent["current_state"], target_state, reason, evidence)
        
        agent["previous_state"] = agent["current_state"]
        agent["current_state"] = target_state
        agent["state_entered_at"] = datetime.utcnow().isoformat()
        self.registry.update_agent(agent["agent_id"], agent)
        
        return {"status": "success", "agent_id": agent["agent_id"], "new_state": target_state}

    def _create_lifecycle_initiative(self, agent: Dict[str, Any], target_state: str, reason: str, evidence: List[str]) -> Dict[str, Any]:
        # Mock initiative queue insertion
        # In full implementation this writes to initiative_queue.json
        item = {
            "type": "workforce_lifecycle",
            "signal": f"agent_{target_state}_recommended",
            "entity": agent["agent_id"],
            "current_state": agent["current_state"],
            "recommended_transition": target_state,
            "reason": reason,
            "evidence": evidence,
            "alternative_interpretation": "Performance issues may reflect task complexity spike rather than agent capability decline.",
            "authority_required": True,
            "priority_score": 0.89,
            "status": "Detected"
        }
        return {"status": "initiative_created", "item": item}

class OnboardingProtocol:
    def __init__(self, registry: AgentRuntimeRegistry, lifecycle: AgentLifecycleManager):
        self.registry = registry
        self.lifecycle = lifecycle
        
    def start_onboarding(self, agent_id: str) -> Dict[str, Any]:
        self.lifecycle.request_transition(agent_id, "onboarding", "Commencing structured onboarding checklist", [])
        return self.resume_onboarding(agent_id)
        
    def run_checklist_item(self, agent_id: str, item_name: str) -> Dict[str, Any]:
        agent = self.registry.get_agent(agent_id)
        
        if item_name == "world_model_node":
            if not agent.get("world_model_node_id"):
                return {"status": "failed", "error": "Missing World Model node"}
            return {"status": "passed"}
            
        elif item_name == "trust_tier":
            if agent.get("trust_tier", -1) < 0:
                return {"status": "failed", "error": "Invalid Trust Tier"}
            return {"status": "passed"}
            
        elif item_name == "canary_baseline":
            # Mocking the 7-day Canary initialization
            return {"status": "passed"}
            
        # Other items mocked as passed
        return {"status": "passed"}

    def resume_onboarding(self, agent_id: str) -> Dict[str, Any]:
        agent = self.registry.get_agent(agent_id)
        checklist = agent.get("onboarding_checklist", {})
        
        required_items = ["world_model_node", "trust_tier", "canary_baseline", "council_assignment"]
        
        for item_name in required_items:
            current_status = checklist.get(item_name, {}).get("status")
            if current_status != "passed":
                result = self.run_checklist_item(agent_id, item_name)
                checklist[item_name] = result
                agent["onboarding_checklist"] = checklist
                self.registry.update_agent(agent_id, agent)
                
                if result["status"] == "failed":
                    return {"status": "halted", "failed_item": item_name, "error": result.get("error")}
        
        # All passed
        agent["onboarding_completed_at"] = datetime.utcnow().isoformat()
        self.registry.update_agent(agent_id, agent)
        self.lifecycle.request_transition(agent_id, "active", "Onboarding complete, observation window passed", [])
        
        return {"status": "completed"}
