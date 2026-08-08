import uuid
from typing import Optional
from ..kernel.models.business_objects import MetricDiagnosis
from .builder_proposal import BuilderProposalGenerator

class FeedbackCouncil:
    def __init__(self):
        self.builder = BuilderProposalGenerator()

    def evaluate_diagnosis(self, diagnosis: MetricDiagnosis) -> Optional[str]:
        """
        Evaluates: Is this worth changing?
        Returns a BuilderProposal ID if action is needed, else None.
        """
        # Heuristic: If confidence is high and it's a known failure category
        impact = "High" if diagnosis.diagnosis_category == "PACKAGING_FAILURE" else "Low"
        
        if impact == "High" and diagnosis.confidence > 0.8:
            # We care. Formulate proposal.
            proposal = self.builder.generate_proposal(diagnosis)
            return proposal.id
            
        # We don't care enough to act
        return None
