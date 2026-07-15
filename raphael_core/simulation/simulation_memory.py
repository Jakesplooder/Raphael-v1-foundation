import os
import json
import logging
from typing import Dict, Any

logger = logging.getLogger("rrk.simulation.memory")

class SimulationMemory:
    """
    Hybrid persistent simulation memory.
    Saves isolated simulation data to raphael_storage/simulations/ to avoid polluting real memory.
    """
    def __init__(self, base_dir: str = "raphael_storage/simulations"):
        self.base_dir = base_dir
        for sub in ["active", "completed", "failed", "transferred", "analytics"]:
            os.makedirs(os.path.join(self.base_dir, sub), exist_ok=True)

    def initialize_simulation(self, sim_id: str, venture_type: str, initial_conditions: Dict[str, Any]):
        sim_dir = os.path.join(self.base_dir, "active", sim_id)
        os.makedirs(sim_dir, exist_ok=True)
        
        data = {
            "simulation_id": sim_id,
            "venture_type": venture_type,
            "initial_conditions": initial_conditions,
            "decisions": [],
            "outcome": {}
        }
        self.save_state(sim_id, data, status="active")

    def save_state(self, sim_id: str, state: Dict[str, Any], status: str = "active"):
        dir_path = os.path.join(self.base_dir, status, sim_id)
        os.makedirs(dir_path, exist_ok=True)
        filepath = os.path.join(dir_path, "world_state.json")
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(state, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save simulation state for {sim_id}: {e}")

    def load_state(self, sim_id: str, status: str = "active") -> Dict[str, Any]:
        filepath = os.path.join(self.base_dir, status, sim_id, "world_state.json")
        if not os.path.exists(filepath):
            return {}
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load simulation state for {sim_id}: {e}")
            return {}

    def log_decision(self, sim_id: str, decision: Dict[str, Any], status: str = "active"):
        state = self.load_state(sim_id, status)
        if state:
            state.setdefault("decisions", []).append(decision)
            self.save_state(sim_id, state, status)
            
    def finalize_simulation(self, sim_id: str, outcome: Dict[str, Any], status: str = "completed"):
        state = self.load_state(sim_id, "active")
        if state:
            state["outcome"] = outcome
            
            # Move from active to final status directory
            import shutil
            active_dir = os.path.join(self.base_dir, "active", sim_id)
            final_dir = os.path.join(self.base_dir, status, sim_id)
            
            self.save_state(sim_id, state, "active") # Save one last time in active
            if os.path.exists(active_dir):
                shutil.move(active_dir, final_dir)
