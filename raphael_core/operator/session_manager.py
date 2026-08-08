import os
import json
from typing import Dict, Any
from pathlib import Path
from datetime import datetime
from raphael_core.operator.models import MissionProposal

class SessionManager:
    """
    Manages workflow memory and approval state for the Operator Chat.
    Persists mission proposals into Raphael Storage.
    """
    def __init__(self):
        root_dir = os.environ.get("RAPHAEL_DATA_DIR", "C:/Users/cyber/Downloads/RalphaelOS")
        self.memory_path = Path(root_dir) / "workflow_memory" / "operator_state.json"
        self.proposals_dir = Path(root_dir) / "raphael_storage" / "missions" / "proposals"
        
        self.memory_path.parent.mkdir(parents=True, exist_ok=True)
        self.proposals_dir.mkdir(parents=True, exist_ok=True)
        self._load_state()

    def _load_state(self):
        if self.memory_path.exists():
            try:
                with open(self.memory_path, 'r', encoding='utf-8') as f:
                    self.state = json.load(f)
            except:
                self.state = {"pending_approvals": {}}
        else:
            self.state = {"pending_approvals": {}}

    def _save_state(self):
        with open(self.memory_path, 'w', encoding='utf-8') as f:
            json.dump(self.state, f, indent=2)

    def set_pending_approval(self, session_id: str, proposal: MissionProposal):
        # We store the dictionary version
        self.state["pending_approvals"][session_id] = proposal.to_dict()
        self._save_state()
        
    def get_pending_approval(self, session_id: str) -> Dict[str, Any]:
        return self.state["pending_approvals"].get(session_id)
        
    def clear_pending_approval(self, session_id: str):
        if session_id in self.state["pending_approvals"]:
            del self.state["pending_approvals"][session_id]
            self._save_state()

    def record_proposal_outcome(self, proposal_dict: Dict[str, Any], outcome: str):
        """Records a proposal into long-term memory."""
        proposal_dict["status"] = outcome
        proposal_dict["updated_at"] = datetime.utcnow().isoformat() + "Z"
        file_path = self.proposals_dir / f"{proposal_dict['id']}.json"
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(proposal_dict, f, indent=2)

session_manager = SessionManager()
