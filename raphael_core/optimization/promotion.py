from ..kernel.models.business_objects import Experiment, OptimizationRun

class PromotionCouncil:
    def __init__(self):
        pass

    def review_experiment(self, experiment: Experiment) -> bool:
        """
        In early Raphael, this flags for manual approval.
        Eventually (Phase 4D), this will be a full automated ROI/Risk scoring engine.
        Returns True if approved, False if rejected.
        """
        # Right now, we simulate manual review by just accepting it if it has a winner
        if experiment.winner == experiment.treatment_asset_id:
            return True
        return False

    def promote(self, run: OptimizationRun) -> str:
        """
        Executes the promotion of the treatment into production.
        """
        run.outcome = "success"
        run.improvement_score = 0.25 # Mocked 25% improvement
        return "Promoted successfully"
