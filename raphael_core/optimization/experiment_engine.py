import uuid
from ..kernel.models.business_objects import Experiment, BuilderProposal

class ExperimentEngine:
    def __init__(self):
        pass

    def create_experiment(self, proposal: BuilderProposal) -> Experiment:
        """
        Takes a BuilderProposal and structures a measurable Experiment.
        """
        # Formulate baseline and treatment
        baseline = "thumbnail_v1"
        treatment = "thumbnail_v2"
        
        return Experiment(
            id=f"exp_{uuid.uuid4().hex[:8]}",
            business_id=proposal.business_id,
            hypothesis=f"Test {list(proposal.proposed_changes.keys())[0]} to improve {proposal.expected_impact}",
            control_asset_id=proposal.asset_id,
            treatment_asset_id=f"{proposal.asset_id}_v2",
            metric_goal=proposal.expected_impact
        )
