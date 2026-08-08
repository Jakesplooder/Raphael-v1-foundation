import uuid
from ..kernel.models.business_objects import BuilderProposal, MetricDiagnosis

class BuilderProposalGenerator:
    def __init__(self):
        pass

    def generate_proposal(self, diagnosis: MetricDiagnosis) -> BuilderProposal:
        """
        Takes a MetricDiagnosis and formulates a specific BuilderProposal.
        """
        # In reality, this would be an LLM call answering "What should we try?"
        
        changes = {}
        expected_impact = ""
        
        if "thumbnail redesign" in diagnosis.recommended_actions:
            changes["thumbnail"] = "Increase human emotion"
            expected_impact = "CTR +25%"
            
        return BuilderProposal(
            id=f"prop_{uuid.uuid4().hex[:8]}",
            business_id=diagnosis.business_id,
            asset_id=diagnosis.asset_id,
            diagnosis_id=diagnosis.id,
            proposed_changes=changes,
            expected_impact=expected_impact,
            status="draft"
        )
