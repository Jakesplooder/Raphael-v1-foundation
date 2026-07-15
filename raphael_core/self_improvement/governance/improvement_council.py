import logging
from ..proposals.improvement_proposal import ImprovementProposal, IMPROVEMENT_AUTHORITY

logger = logging.getLogger("rrk.self_improvement.governance")

class ImprovementCouncil:
    """
    Reviews improvement proposals with tiered authority.
    
    Level 0: Analysis only
    Level 1: Memory/config updates
    Level 2: Prompt/behavior changes  
    Level 3: Agent behavior changes
    Level 4: Core architecture changes — Executive Deliberation required
    """
    
    def __init__(self, current_authority: int = 2):
        self.current_authority = current_authority
        
    def review(self, proposal: ImprovementProposal) -> dict:
        required = proposal.authority_required
        
        if self.current_authority >= required:
            logger.info(f"[ImprovementCouncil] Proposal {proposal.id} APPROVED "
                        f"({proposal.improvement_type.value}, Level {required})")
            return {"decision": "APPROVED", "level": required}
            
        if required == 4:
            logger.warning(f"[ImprovementCouncil] Proposal {proposal.id} requires "
                           f"EXECUTIVE DELIBERATION (Level 4: {proposal.improvement_type.value})")
            return {"decision": "EXECUTIVE_DELIBERATION_REQUIRED", "level": required}
            
        logger.warning(f"[ImprovementCouncil] Proposal {proposal.id} requires "
                       f"ESCALATION (Level {required}: {proposal.improvement_type.value})")
        return {"decision": "ESCALATION_REQUIRED", "level": required}
