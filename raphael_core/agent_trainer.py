import uuid
import datetime
from typing import Dict, Any, List

class ConstitutionalViolationError(Exception):
    pass

VALID_LEVERS = {
    "prompt_improvement",
    "retrieval_tuning",
    "tool_access_calibration",
    "model_routing_optimization"
}

class TrainingProposer:
    def propose_training(self, agent_id: str, lever: str, performance_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Proposes a training modification based on recent performance data.
        """
        if lever not in VALID_LEVERS:
            raise ConstitutionalViolationError(f"Lever {lever} is not a constitutionally valid training lever.")
            
        proposal_id = f"TRAIN-{str(uuid.uuid4())[:8].upper()}"
        
        # Build hypothesis based on the lever
        if lever == "prompt_improvement":
            hypothesis = "Refining core instructions will improve accuracy by 10% without degrading speed."
        elif lever == "retrieval_tuning":
            hypothesis = "Increasing context window will improve semantic matching reliability."
        elif lever == "tool_access_calibration":
            hypothesis = "Granting Tool X will increase task completion speed by 20%."
        elif lever == "model_routing_optimization":
            hypothesis = "Upgrading default model will improve complex reasoning accuracy."
            
        return {
            "training_id": proposal_id,
            "agent_id": agent_id,
            "lever": lever,
            "hypothesis": hypothesis,
            "status": "proposed",
            "baseline_metrics": performance_data,
            "created_at": datetime.datetime.utcnow().isoformat()
        }

class ABTestTracker:
    def __init__(self, registry: Any = None):
        self.registry = registry
        
    def evaluate_test(self, training_record: Dict[str, Any], current_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluates a training modification against its baseline.
        """
        baseline = training_record.get("baseline_metrics", {})
        # Simple evaluation: did composite score improve?
        base_comp = baseline.get("composite", 0)
        curr_comp = current_metrics.get("composite", 0)
        
        passed = curr_comp > base_comp
        return {
            "passed": passed,
            "delta": round(curr_comp - base_comp, 2),
            "baseline": base_comp,
            "current": curr_comp
        }

class TrainingLifecycleManager:
    def __init__(self, registry: Any = None):
        self.registry = registry
        self.active_trainings = {}
        
    def activate_training(self, training_id: str, proposal: Dict[str, Any]) -> bool:
        """
        Activates a training. STRICTLY requires explicit invocation (simulating Aaron's approval).
        """
        if proposal["status"] != "proposed":
            return False
            
        proposal["status"] = "active"
        proposal["activated_at"] = datetime.datetime.utcnow().isoformat()
        self.active_trainings[training_id] = proposal
        
        # In a real scenario, this applies the config changes to the AgentRuntimeRegistry
        if self.registry:
            agents = self.registry.load_registry()
            agent = agents.get(proposal["agent_id"])
            if agent:
                # Evolve the agent version
                curr_version = agent.get("training_version")
                agent["training_version"] = (curr_version if curr_version is not None else 1) + 1
                self.registry.update_agent(proposal["agent_id"], agent)
                
        return True
        
    def list_trainings(self) -> List[Dict[str, Any]]:
        return list(self.active_trainings.values())
