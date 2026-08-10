from raphael_core.performance_reviewer import PerformanceEvaluator, ReviewCadenceManager, TrustTierAssessor
from raphael_core.world_model_emitter import get_performance_reviews, acknowledge_review
import os

def test_score_calculation():
    evaluator = PerformanceEvaluator()
    metrics = {
        "productivity_raw": 80.0,
        "accuracy_raw": 90.0,
        "reliability_raw": 100.0,
        "cost_efficiency_raw": 70.0
    }
    
    scores = evaluator.calculate_scores("AGENT-DEV", metrics)
    
    assert scores["productivity"] == 80.0
    assert scores["accuracy"] == 90.0
    assert scores["reliability"] == 100.0
    assert scores["cost_efficiency"] == 70.0
    
    # 80 * 0.35 = 28
    # 90 * 0.30 = 27
    # 100 * 0.25 = 25
    # 70 * 0.10 = 7
    # 28 + 27 + 25 + 7 = 87.0
    assert scores["composite"] == 87.0

def test_weekly_snapshot_suppression():
    rcm = ReviewCadenceManager()
    metrics = {"productivity_raw": 80.0, "accuracy_raw": 90.0, "reliability_raw": 100.0, "cost_efficiency_raw": 70.0} # composite 87.0
    
    # Delta of 5 (87.0 - 82.0). Suppressed.
    res1 = rcm.generate_weekly_snapshot("AGENT-DEV", metrics, 82.0)
    assert res1["surfaced"] is False
    
    # Delta of -15 (87.0 - 102.0) triggers. (Drop of 15)
    res2 = rcm.generate_weekly_snapshot("AGENT-DEV", metrics, 102.0)
    assert res2["surfaced"] is True
    assert res2["initiative_item"]["signal"] == "weekly_performance_anomaly"

def test_monthly_review_generation():
    rcm = ReviewCadenceManager()
    metrics = {"productivity_raw": 80.0, "accuracy_raw": 90.0, "reliability_raw": 100.0, "cost_efficiency_raw": 70.0} # composite 87.0
    
    record = rcm.generate_monthly_review("AGENT-DEV", metrics, 80.0)
    
    assert record["agent_id"] == "AGENT-DEV"
    assert record["reviewed_by_aaron"] is False
    assert record["trend"] == "improving"
    
    # Verify in world model
    reviews = get_performance_reviews()
    assert any(r["review_id"] == record["review_id"] for r in reviews)

def test_trust_tier_recommendation():
    assessor = TrustTierAssessor()
    
    reviews = [
        {"review_id": "r1", "scores": {"composite": 86.0}},
        {"review_id": "r2", "scores": {"composite": 88.0}},
        {"review_id": "r3", "scores": {"composite": 87.0}},
    ]
    pressure_history = [{"trend": "improving"}]
    
    rec = assessor.assess_trust_tier_recommendation("AGENT-DEV", 2, reviews, pressure_history)
    
    assert rec["action"] == "promote"
    assert rec["confidence"] == 0.78
    assert len(rec["evidence"]) == 3

def test_data_isolation():
    # Verify that scorelines for one agent do not depend on or reference another agent.
    evaluator = PerformanceEvaluator()
    scores_a = evaluator.calculate_scores("AGENT-A", {"productivity_raw": 80.0})
    scores_b = evaluator.calculate_scores("AGENT-B", {"productivity_raw": 80.0})
    
    assert scores_a == scores_b
    # If the system were ranking or adjusting scores based on peer performance, these wouldn't be identical isolated functions.

def test_performance_acknowledge():
    rcm = ReviewCadenceManager()
    metrics = {"productivity_raw": 80.0, "accuracy_raw": 90.0, "reliability_raw": 100.0, "cost_efficiency_raw": 70.0}
    record = rcm.generate_monthly_review("AGENT-ACK", metrics, 80.0)
    
    rid = record["review_id"]
    
    # Assert False initially
    revs = get_performance_reviews()
    for r in revs:
        if r["review_id"] == rid:
            assert r["reviewed_by_aaron"] is False
            
    # Acknowledge
    assert acknowledge_review(rid) is True
    
    # Assert True after
    revs2 = get_performance_reviews()
    for r in revs2:
        if r["review_id"] == rid:
            assert r["reviewed_by_aaron"] is True
            break
            
    # Clean up mock file
    fp = r"R:\RaphaelOS\world_model\performance_reviews.json"
    if os.path.exists(fp):
        os.remove(fp)
