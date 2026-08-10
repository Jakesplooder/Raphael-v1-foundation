"""
Phase 9.4: Commerce Venture Launch — AI Store
==============================================

This script proves Raphael Holdings can manage a portfolio of competing ventures.

Pipeline:
1. Submit AI Store proposal through the Venture Council
2. Generate Investment Memo (independently scored from MentorMap)
3. CEO Approval Gate
4. Create AIStoreTwin
5. Run 3-business portfolio allocation:
   - Focus Marketing (ACTIVE → Exploitation Pool)
   - MentorMap (INCUBATING → Exploration Pool)
   - AI Store (INCUBATING → Exploration Pool)
6. Venture Competition Telemetry
7. Portfolio-Level Learning
8. CEO Holdings Brief
"""

import sys
from pathlib import Path
sys.path.insert(0, r"R:\RalphaelOS_Repo")

from raphael_core.kernel.services.business_registry.proposals.proposal import BusinessProposal
from raphael_core.kernel.services.business_registry.proposals.proposal_manager import proposal_manager
from raphael_domains.venture_council.council import venture_council
from raphael_core.kernel.services.notification_gateway.notification_service import notification_service
from raphael_core.kernel.services.business_registry.registry import business_registry
from raphael_core.kernel.services.portfolio_manager.allocation_engine import AllocationEngine
from raphael_core.kernel.services.portfolio_manager.resource_scheduler import ResourceScheduler
from raphael_core.kernel.services.portfolio_manager.portfolio_report import PortfolioReport
from raphael_core.kernel.services.portfolio_manager.portfolio_learning import PortfolioLearning

# --- Clean state ---
for f in ["fm_phase94.json", "mm_phase94.json", "as_phase94.json"]:
    p = Path(f)
    if p.exists():
        p.unlink()


def divider(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")


# ============================================================
# STEP 1: AI Store Business Proposal
# ============================================================
divider("STEP 1: AI STORE BUSINESS PROPOSAL")

ai_store_proposal = BusinessProposal(
    name="AI Store",
    category="commerce_technology",
    type="e_commerce_platform",
    problem="Finding reliable AI hardware and curated software tools is difficult for AI professionals.",
    solution="A curated e-commerce store with AI-powered product recommendations for AI professionals.",
    target_customer="AI engineers, ML researchers, data scientists, AI hobbyists",
    revenue_model=["E-commerce product sales", "Affiliate revenue", "Premium curation subscriptions"],
    strategic_alignment={
        "commerce_domain": True,
        "ai_advantage": True,
        "portfolio_synergy": True,
        "automation_potential": True
    },
    initial_resources_requested={
        "gpu_hours": 15,
        "agent_hours": 40,
        "budget": 300
    }
)

proposal_manager.submit_proposal(ai_store_proposal)


# ============================================================
# STEP 2: Venture Council Evaluation
# ============================================================
divider("STEP 2: VENTURE COUNCIL EVALUATION")

ai_store_votes = venture_council.evaluate_proposal(ai_store_proposal)

print(f"Venture: {ai_store_votes['venture']}")
print(f"VentureScore: {ai_store_votes['confidence']}")
print(f"Recommendation: {ai_store_votes['recommendation']}")
print(f"Agent Verdicts: {ai_store_votes['agent_verdicts']}")
print(f"Risks: {ai_store_votes['risks']}")


# ============================================================
# STEP 3: CEO Approval Gate
# ============================================================
divider("STEP 3: CEO APPROVAL GATE (TELEGRAM)")

notification_service.handle_event("VENTURE.APPROVAL_REQUIRED", "Kernel", ai_store_votes)
print("Mocking CEO Approval: [YES]")


# ============================================================
# STEP 4: Create AI Store Twin
# ============================================================
divider("STEP 4: CREATING AI STORE TWIN")

from raphael_domains.commerce.ai_store.twin import AIStoreTwin

ai_store_twin = AIStoreTwin(storage_path=Path("as_phase94.json"))
ai_store_twin.save()

business_registry.register(ai_store_twin, requirements={
    "opportunity_score": ai_store_votes["confidence"],
    "strategic_importance": 0.85
})

print(f"Twin: {ai_store_twin.identity['name']}")
print(f"Division: {ai_store_twin.venture_metadata['division']}")
print(f"Lifecycle: {ai_store_twin.lifecycle.get_state()}")
print(f"Capital Source: {ai_store_twin.venture_metadata['capital_source']}")


# ============================================================
# STEP 5: Multi-Venture Portfolio Allocation
# ============================================================
divider("STEP 5: PORTFOLIO ALLOCATION — 3 BUSINESSES")

# Create Focus Marketing (ACTIVE — established)
from raphael_domains.creator.business_twin.twin import BusinessTwin as FocusMarketingTwin
focus_mktg = FocusMarketingTwin(business_id="focus_mktg", storage_path=Path("fm_phase94.json"))
focus_mktg.financials["roi"] = 8.4
focus_mktg.strategy["business_model"] = "attention_economy"

# Create MentorMap (INCUBATING — exploring)
from raphael_domains.career.mentormap.twin import MentorMapTwin
mentormap = MentorMapTwin(storage_path=Path("mm_phase94.json"))
mentormap.strategy["business_model"] = "network_effects_marketplace"

# Portfolio
portfolio = [
    {"twin": focus_mktg, "requirements": {"opportunity_score": 0.50, "strategic_importance": 0.80}},
    {"twin": mentormap, "requirements": {"opportunity_score": 0.69, "strategic_importance": 0.90}},
    {"twin": ai_store_twin, "requirements": {"opportunity_score": ai_store_votes["confidence"], "strategic_importance": 0.85}}
]

engine = AllocationEngine()
scheduler = ResourceScheduler(engine)

allocations = scheduler.schedule_cycle(portfolio, 100, 500.0)

print("\nRAPHAEL HOLDINGS — RESOURCE ALLOCATION")
print("-" * 45)
print(f"{'Business':<20} {'Pool':<15} {'Score':<8} {'Alloc %':<8} {'GPU':<8} {'Budget':<8}")
print("-" * 45)
for bid, alloc in allocations.items():
    name = bid
    for b in portfolio:
        if b["twin"].identity["business_id"] == bid:
            name = b["twin"].identity["name"]
            break
    print(f"{name:<20} {alloc['pool']:<15} {alloc['score']:<8.4f} {alloc['allocation_pct']*100:<8.1f} {alloc['gpu_hours']:<8.1f} ${alloc['budget']:<7.1f}")


# ============================================================
# STEP 6: Portfolio-Level Learning
# ============================================================
divider("STEP 6: PORTFOLIO-LEVEL LEARNING")

learning = PortfolioLearning()
learning.record_allocation_cycle(allocations, portfolio)
patterns = learning.learn_from_portfolio(portfolio)

# Record venture competition
venture_rankings = sorted(
    [{"name": b["twin"].identity["name"], "score": allocations[b["twin"].identity["business_id"]]["score"],
      "allocation_pct": allocations[b["twin"].identity["business_id"]]["allocation_pct"]}
     for b in portfolio if b["twin"].lifecycle.get_state() in ["INCUBATING", "VALIDATING"]],
    key=lambda x: x["score"],
    reverse=True
)
learning.record_venture_comparison(venture_rankings)

print("Business Model Patterns Discovered:")
for p in learning.intelligence["business_model_learning"]:
    print(f"  📊 {p['pattern']}")
    print(f"     Confidence: {p['confidence']}")
    print(f"     Evidence: {p['evidence']}")
    print()


# ============================================================
# STEP 7: CEO Holdings Report
# ============================================================
divider("STEP 7: CEO HOLDINGS REPORT")

report = PortfolioReport().generate_report(allocations, portfolio)
print(report)


# ============================================================
# STEP 8: Venture Competition Summary
# ============================================================
divider("STEP 8: VENTURE COMPETITION — EXPLORATION POOL")

print("Exploration Pool Ventures (20% of total capital):")
print()
for v in venture_rankings:
    pct_of_pool = round(v["allocation_pct"] / 0.20 * 100, 1) if 0.20 > 0 else 0
    print(f"  {'🥇' if v == venture_rankings[0] else '🥈'} {v['name']}")
    print(f"    Score: {v['score']:.4f}")
    print(f"    Total Allocation: {v['allocation_pct']*100:.1f}%")
    print(f"    Share of Exploration Pool: {pct_of_pool}%")
    print()

winner = venture_rankings[0] if venture_rankings else None
if winner:
    print(f"CEO Brief:")
    print(f"  Best Opportunity: {winner['name']}")
    print(f"  Reason: Higher VentureScore ({winner['score']:.4f})")
    print(f"  Recommendation: Approve validation budget")

print("\n✅ Phase 9.4 Complete — Raphael Holdings is managing a diversified portfolio.")
