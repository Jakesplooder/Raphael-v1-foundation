"""
Phase 9.5: Agency Venture Launch — Diversified AI Holding Company
=================================================================

This script proves Raphael Holdings can manage 4 economically distinct businesses:

  Raphael Holdings
  ├── Creator Division    → Focus Marketing   (Attention Economy)
  ├── Career Division     → MentorMap         (Network Effects)
  ├── Commerce Division   → AI Store          (Transaction Economy)
  └── Agency Division     → Raphael Agency    (Service Economy)

Pipeline:
1. Add Venture Thesis Memory to all proposals
2. Submit Agency proposal through Venture Council
3. CEO Approval Gate
4. Create AgencyTwin with service economy metrics
5. Run 4-business portfolio allocation
6. Venture Competition Telemetry (3 ventures in exploration pool)
7. Portfolio-Level Learning
8. CEO Strategic Recommendations
9. Generate holdings_strategy.md — first CEO strategy document
"""

import sys
from pathlib import Path
sys.path.insert(0, r"C:\Users\cyber\Downloads\RalphaelOS")

from raphael_core.kernel.services.business_registry.proposals.proposal import BusinessProposal, VentureThesis
from raphael_core.kernel.services.business_registry.proposals.proposal_manager import proposal_manager
from raphael_domains.venture_council.council import venture_council
from raphael_core.kernel.services.notification_gateway.notification_service import notification_service
from raphael_core.kernel.services.business_registry.registry import business_registry
from raphael_core.kernel.services.portfolio_manager.allocation_engine import AllocationEngine
from raphael_core.kernel.services.portfolio_manager.resource_scheduler import ResourceScheduler
from raphael_core.kernel.services.portfolio_manager.portfolio_report import PortfolioReport
from raphael_core.kernel.services.portfolio_manager.portfolio_learning import PortfolioLearning

# --- Clean state ---
for f in ["fm_phase95.json", "mm_phase95.json", "as_phase95.json", "ag_phase95.json"]:
    p = Path(f)
    if p.exists():
        p.unlink()


def divider(title):
    print(f"\n{'='*65}")
    print(f"  {title}")
    print(f"{'='*65}\n")


# ============================================================
# STEP 1: Agency Business Proposal (with Venture Thesis)
# ============================================================
divider("STEP 1: AGENCY BUSINESS PROPOSAL + VENTURE THESIS")

agency_proposal = BusinessProposal(
    name="Raphael Agency",
    category="agency_services",
    type="ai_services_agency",
    problem="Small businesses need marketing automation, cybersecurity, and business process optimization but cannot afford full-time teams.",
    solution="An AI-powered services agency that delivers enterprise-grade marketing, security, and automation at a fraction of the cost using AI agents.",
    target_customer="Small-to-medium businesses, startups, solopreneurs",
    revenue_model=["Monthly retainers", "Project-based contracts", "Performance-based fees"],
    strategic_alignment={
        "service_domain": True,
        "ai_advantage": True,
        "portfolio_synergy": True,
        "automation_potential": True,
        "cash_flow_generation": True
    },
    initial_resources_requested={
        "gpu_hours": 25,
        "agent_hours": 60,
        "budget": 400
    },
    thesis=VentureThesis(
        belief="AI automation reduces service delivery cost by 60%, enabling profitable agency operations without proportional headcount growth.",
        assumptions=[
            "AI agents can deliver marketing services at 40% of human cost",
            "Small businesses will trust AI-assisted service providers",
            "Recurring revenue model creates predictable cash flow",
            "Service margin improves as AI agents learn from delivery data",
            "Agency revenue can fund exploration in other portfolio ventures"
        ],
        risk_assumptions=[
            "Client acquisition cost may exceed first-month revenue",
            "Service quality may vary during early AI training period",
            "Client retention depends on measurable results within 30 days"
        ]
    )
)

proposal_manager.submit_proposal(agency_proposal)
print(f"Thesis Belief: {agency_proposal.thesis.belief}")
print(f"Assumptions: {len(agency_proposal.thesis.assumptions)}")
print(f"Risk Assumptions: {len(agency_proposal.thesis.risk_assumptions)}")


# ============================================================
# STEP 2: Venture Council Evaluation
# ============================================================
divider("STEP 2: VENTURE COUNCIL EVALUATION")

agency_votes = venture_council.evaluate_proposal(agency_proposal)

print(f"Venture: {agency_votes['venture']}")
print(f"VentureScore: {agency_votes['confidence']}")
print(f"Recommendation: {agency_votes['recommendation']}")
print(f"Agent Verdicts: {agency_votes['agent_verdicts']}")
print(f"Risks: {agency_votes['risks']}")
if "thesis" in agency_votes:
    print(f"Thesis Persisted: ✅")


# ============================================================
# STEP 3: CEO Approval Gate
# ============================================================
divider("STEP 3: CEO APPROVAL GATE (TELEGRAM)")

notification_service.handle_event("VENTURE.APPROVAL_REQUIRED", "Kernel", agency_votes)
print("Mocking CEO Approval: [YES]")


# ============================================================
# STEP 4: Create Agency Twin
# ============================================================
divider("STEP 4: CREATING AGENCY TWIN")

from raphael_domains.agency.agency_twin import AgencyTwin

agency_twin = AgencyTwin(storage_path=Path("ag_phase95.json"))
agency_twin.save()

business_registry.register(agency_twin, requirements={
    "opportunity_score": agency_votes["confidence"],
    "strategic_importance": 0.90
})

print(f"Twin: {agency_twin.identity['name']}")
print(f"Division: {agency_twin.venture_metadata['division']}")
print(f"Lifecycle: {agency_twin.lifecycle.get_state()}")
print(f"Strategic Role: {agency_twin.venture_metadata['strategic_role']}")
print(f"Service Lines: {len(agency_twin.strategy['service_lines'])}")
for sl in agency_twin.strategy["service_lines"]:
    print(f"  └─ {sl['name']} ({sl['status']})")
print(f"Delivery Capacity: {agency_twin.operations['delivery_capacity']} concurrent clients")


# ============================================================
# STEP 5: 4-Business Portfolio Allocation
# ============================================================
divider("STEP 5: PORTFOLIO ALLOCATION — 4 BUSINESSES")

# Focus Marketing (ACTIVE — established)
from raphael_domains.creator.business_twin.twin import BusinessTwin as FocusMarketingTwin
focus_mktg = FocusMarketingTwin(business_id="focus_mktg", storage_path=Path("fm_phase95.json"))
focus_mktg.financials["roi"] = 8.4
focus_mktg.strategy["business_model"] = "attention_economy"

# MentorMap (INCUBATING — exploring)
from raphael_domains.career.mentormap.twin import MentorMapTwin
mentormap = MentorMapTwin(storage_path=Path("mm_phase95.json"))
mentormap.strategy["business_model"] = "network_effects_marketplace"

# AI Store (INCUBATING — exploring)
from raphael_domains.commerce.ai_store.twin import AIStoreTwin
ai_store = AIStoreTwin(storage_path=Path("as_phase95.json"))

# Portfolio
portfolio = [
    {"twin": focus_mktg, "requirements": {"opportunity_score": 0.50, "strategic_importance": 0.80}},
    {"twin": mentormap, "requirements": {"opportunity_score": 0.69, "strategic_importance": 0.90}},
    {"twin": ai_store, "requirements": {"opportunity_score": 0.70, "strategic_importance": 0.85}},
    {"twin": agency_twin, "requirements": {"opportunity_score": agency_votes["confidence"], "strategic_importance": 0.90}}
]

engine = AllocationEngine()
scheduler = ResourceScheduler(engine)

allocations = scheduler.schedule_cycle(portfolio, 100, 500.0)

print("\nRAPHAEL HOLDINGS — RESOURCE ALLOCATION")
print("-" * 70)
print(f"{'Business':<22} {'Division':<12} {'Pool':<15} {'Score':<8} {'Alloc %':<8} {'GPU':<8} {'Budget':<8}")
print("-" * 70)
for b in portfolio:
    twin = b["twin"]
    bid = twin.identity["business_id"]
    alloc = allocations[bid]
    name = twin.identity["name"]
    domain = twin.identity.get("domain", "?").title()
    print(f"{name:<22} {domain:<12} {alloc['pool']:<15} {alloc['score']:<8.4f} {alloc['allocation_pct']*100:<8.1f} {alloc['gpu_hours']:<8.1f} ${alloc['budget']:<7.1f}")


# ============================================================
# STEP 6: Portfolio-Level Learning
# ============================================================
divider("STEP 6: PORTFOLIO-LEVEL LEARNING")

learning = PortfolioLearning()
learning.record_allocation_cycle(allocations, portfolio)
patterns = learning.learn_from_portfolio(portfolio)

# Record venture competition
exploring_ventures = [
    {"name": b["twin"].identity["name"],
     "score": allocations[b["twin"].identity["business_id"]]["score"],
     "allocation_pct": allocations[b["twin"].identity["business_id"]]["allocation_pct"]}
    for b in portfolio
    if b["twin"].lifecycle.get_state() in ["INCUBATING", "VALIDATING"]
]
exploring_ventures.sort(key=lambda x: x["score"], reverse=True)
learning.record_venture_comparison(exploring_ventures)

print("Business Model Patterns Discovered:")
for p in learning.intelligence["business_model_learning"]:
    print(f"  📊 {p['pattern']}")
    print(f"     Confidence: {p['confidence']}")
    print(f"     Evidence: {p['evidence']}")
    print()


# ============================================================
# STEP 7: CEO Strategic Recommendations
# ============================================================
divider("STEP 7: CEO HOLDINGS REPORT")

report = PortfolioReport()
report_text = report.generate_report(allocations, portfolio)
print(report_text)


# ============================================================
# STEP 8: Holdings Strategy Document
# ============================================================
divider("STEP 8: HOLDINGS STRATEGY — CEO DOCUMENT")

strategy_text = report.generate_holdings_strategy(allocations, portfolio)
print(strategy_text)


# ============================================================
# STEP 9: Exploration Pool Competition Detail
# ============================================================
divider("STEP 9: VENTURE COMPETITION — EXPLORATION POOL")

exp_pool_total = sum(v["allocation_pct"] for v in exploring_ventures)
print(f"Exploration Pool Total: {exp_pool_total*100:.0f}% of capital")
print(f"Competing Ventures: {len(exploring_ventures)}\n")

for i, v in enumerate(exploring_ventures):
    medal = ["🥇", "🥈", "🥉"][i] if i < 3 else "🏅"
    pct_of_pool = round(v["allocation_pct"] / exp_pool_total * 100, 1) if exp_pool_total > 0 else 0
    print(f"  {medal} {v['name']}")
    print(f"    Score: {v['score']:.4f}")
    print(f"    Total Allocation: {v['allocation_pct']*100:.1f}%")
    print(f"    Share of Exploration Pool: {pct_of_pool}%")
    print()


# ============================================================
# STEP 10: Final Portfolio State
# ============================================================
divider("STEP 10: FINAL PORTFOLIO STATE")

print("RAPHAEL HOLDINGS")
print("")
print("  ┌── Creator Division")
print(f"  │   └── Focus Marketing   [ACTIVE]        {round(allocations['focus_mktg']['allocation_pct']*100)}% (Exploitation)")
print("  │")
print("  ├── Career Division")
print(f"  │   └── MentorMap          [INCUBATING]    {round(allocations['mentormap_001']['allocation_pct']*100)}% (Exploration)")
print("  │")
print("  ├── Commerce Division")
print(f"  │   └── AI Store           [INCUBATING]    {round(allocations['ai_store_001']['allocation_pct']*100)}% (Exploration)")
print("  │")
print("  └── Agency Division")
print(f"      └── Raphael Agency     [INCUBATING]    {round(allocations['agency_001']['allocation_pct']*100)}% (Exploration)")

print("\n\nEconomic Model Diversity:")
print("  Creator   → Attention Economy")
print("  Career    → Network Effects")
print("  Commerce  → Transaction Economy")
print("  Agency    → Service Economy")

print("\n✅ Phase 9.5 Complete — Raphael is a diversified AI holding company.")
