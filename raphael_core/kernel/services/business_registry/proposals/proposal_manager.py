from typing import Dict, List
from raphael_core.kernel.event_bus import emit
from .proposal import BusinessProposal

class ProposalManager:
    def __init__(self):
        self.proposals: Dict[str, BusinessProposal] = {}
        
    def submit_proposal(self, proposal: BusinessProposal):
        self.proposals[proposal.name] = proposal
        
        emit("BUSINESS.PROPOSED", "ProposalManager", {
            "name": proposal.name,
            "category": proposal.category,
            "resources_requested": proposal.initial_resources_requested
        })
        
        return proposal
        
    def get_proposal(self, name: str) -> BusinessProposal:
        return self.proposals.get(name)

proposal_manager = ProposalManager()
