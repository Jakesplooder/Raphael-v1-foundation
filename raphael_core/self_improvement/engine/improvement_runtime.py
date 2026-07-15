import logging
from ..analysis.performance_analyzer import PerformanceAnalyzer
from ..analysis.bottleneck_detector import BottleneckDetector
from ..proposals.proposal_generator import ProposalGenerator
from ..simulation.sandbox_runner import SandboxRunner
from ..simulation.regression_tester import RegressionTester
from ..governance.improvement_council import ImprovementCouncil
from ..memory.improvement_memory import ImprovementMemory

logger = logging.getLogger("rrk.self_improvement.engine")

class SelfImprovementKPIs:
    """Tracks how well Raphael improves itself."""
    
    def __init__(self):
        self.proposals_generated = 0
        self.proposals_approved = 0
        self.simulations_passed = 0
        self.simulations_failed = 0
        self.deployments_successful = 0
        self.regressions_detected = 0
        
    @property
    def proposal_accuracy(self) -> float:
        if self.proposals_generated == 0:
            return 0
        return (self.proposals_approved / self.proposals_generated) * 100
        
    @property
    def simulation_accuracy(self) -> float:
        total = self.simulations_passed + self.simulations_failed
        if total == 0:
            return 0
        return (self.simulations_passed / total) * 100
        
    @property
    def deployment_success(self) -> float:
        if self.proposals_approved == 0:
            return 0
        return (self.deployments_successful / self.proposals_approved) * 100
        
    def get_score(self) -> float:
        return (self.proposal_accuracy * 0.25 +
                self.simulation_accuracy * 0.25 +
                self.deployment_success * 0.25 +
                (100 - (self.regressions_detected * 10)) * 0.25)

class ImprovementRuntime:
    """
    Orchestrates the full self-improvement cycle:
    Analyze → Propose → Simulate → Govern → Deploy → Measure → Learn
    """
    
    def __init__(self):
        self.analyzer = PerformanceAnalyzer()
        self.bottleneck_detector = BottleneckDetector()
        self.proposal_generator = ProposalGenerator()
        self.sandbox = SandboxRunner()
        self.regression_tester = RegressionTester()
        self.council = ImprovementCouncil(current_authority=2)
        self.memory = ImprovementMemory()
        self.kpis = SelfImprovementKPIs()
        
    def run_cycle(self, component_scores: dict, 
                  improved_scores: dict = None,
                  improvement_delta: float = 0) -> dict:
        """Run one full self-improvement cycle."""
        
        # 1. Analyze
        analysis = self.analyzer.analyze(component_scores)
        
        # 2. Detect bottlenecks
        bottlenecks = self.bottleneck_detector.detect(component_scores)
        if not bottlenecks:
            return {"status": "NO_IMPROVEMENTS_NEEDED", "analysis": analysis}
            
        # 3. Generate proposal for worst bottleneck
        worst = bottlenecks[0]
        proposal = self.proposal_generator.generate(worst)
        self.kpis.proposals_generated += 1
        
        # 4. Governance review
        review = self.council.review(proposal)
        if review["decision"] != "APPROVED":
            return {"status": review["decision"], "proposal": proposal.id}
            
        self.kpis.proposals_approved += 1
        
        # 5. Simulate A/B
        current = worst["score"]
        improved = current + improvement_delta if improvement_delta else current + worst["gap"] * 0.6
        ab_result = self.sandbox.run_ab_experiment(current, improved)
        
        if not ab_result["passed"]:
            self.kpis.simulations_failed += 1
            self.memory.store("failed", proposal.id, {"proposal": proposal.model_dump(), "ab": ab_result})
            return {"status": "SIMULATION_REJECTED", "proposal": proposal.id}
            
        self.kpis.simulations_passed += 1
        
        # 6. Regression test
        post_scores = improved_scores or component_scores.copy()
        post_scores[worst["component"]] = improved
        regression = self.regression_tester.test(component_scores, post_scores)
        
        if not regression["passed"]:
            self.kpis.regressions_detected += 1
            self.memory.store("failed", proposal.id, {"proposal": proposal.model_dump(), "regression": regression})
            return {"status": "REGRESSION_DETECTED", "proposal": proposal.id, "regressions": regression["regressions"]}
            
        # 7. Deploy & Learn
        self.kpis.deployments_successful += 1
        self.memory.store("successful", proposal.id, {
            "proposal": proposal.model_dump(),
            "gain": ab_result["gain_pct"],
            "component": worst["component"]
        })
        
        logger.info(f"[ImprovementRuntime] Successfully deployed {proposal.id}: "
                     f"+{ab_result['gain_pct']:.1f}% on {worst['component']}")
        
        return {
            "status": "DEPLOYED",
            "proposal": proposal.id,
            "component": worst["component"],
            "gain": ab_result["gain_pct"],
            "self_improvement_score": self.kpis.get_score()
        }
