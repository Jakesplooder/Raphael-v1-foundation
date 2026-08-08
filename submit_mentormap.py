import sys
from pathlib import Path
sys.path.insert(0, r"C:\Users\cyber\Downloads\RalphaelOS")

from raphael_core.kernel.services.business_registry.proposals.proposal import BusinessProposal
from raphael_core.kernel.services.business_registry.proposals.proposal_manager import proposal_manager
from raphael_domains.venture_council.council import venture_council
from raphael_core.kernel.services.notification_gateway.notification_service import notification_service
from raphael_domains.career.mentormap.twin import MentorMapTwin
from raphael_core.kernel.services.business_registry.registry import business_registry
from raphael_core.kernel.services.portfolio_manager.allocation_engine import AllocationEngine
from raphael_core.kernel.services.portfolio_manager.resource_scheduler import ResourceScheduler

def run_incubation():
    print("--- 1. Proposing MentorMap ---")
    mentormap_proposal = BusinessProposal(
        name="MentorMap",
        category="career_technology",
        type="software_platform",
        problem="Career changers struggle to find relevant mentors.",
        solution="AI-powered mentor matching platform.",
        target_customer="Professionals transitioning careers",
        revenue_model=["Premium memberships", "Mentor marketplace fees", "Enterprise partnerships"],
        strategic_alignment={"career_domain": True, "ai_advantage": True, "portfolio_synergy": True},
        initial_resources_requested={"gpu_hours": 20, "agent_hours": 50, "budget": 250}
    )
    
    proposal_manager.submit_proposal(mentormap_proposal)
    
    print("\n--- 2. Venture Council Evaluation ---")
    council_votes = venture_council.evaluate_proposal(mentormap_proposal)
    
    print("\n--- 3. CEO Approval Gate ---")
    # Trigger telegram approval alert
    notification_service.handle_event("VENTURE.APPROVAL_REQUIRED", "Kernel", council_votes)
    print("Mocking CEO Approval: [YES]")
    
    print("\n--- 4. Creating MentorMap Twin ---")
    # After approval, we spawn the Twin
    twin_path = Path("mentormap_incubating.json")
    if twin_path.exists():
        twin_path.unlink()
        
    mentormap_twin = MentorMapTwin(storage_path=twin_path)
    
    # Register business in portfolio
    business_registry.register(mentormap_twin, requirements={
        "opportunity_score": council_votes["confidence"],
        "strategic_importance": 0.90
    })
    
    print("\n--- 5. Exploration Budget Allocation ---")
    engine = AllocationEngine()
    scheduler = ResourceScheduler(engine)
    
    # Let's allocate across the portfolio with MentorMap now in the mix
    # We mock Focus Marketing to show them competing
    from raphael_domains.creator.business_twin.twin import BusinessTwin as FocusMarketingTwin
    fm_path = Path("fm_incubating.json")
    if fm_path.exists():
        fm_path.unlink()
    focus_mktg = FocusMarketingTwin(business_id="focus_mktg", storage_path=fm_path)
    focus_mktg.financials["roi"] = 8.4
    
    registry_businesses = [
        {"twin": focus_mktg, "requirements": {"opportunity_score": 0.50, "strategic_importance": 0.80}},
        {"twin": mentormap_twin, "requirements": {"opportunity_score": council_votes["confidence"], "strategic_importance": 0.90}}
    ]
    
    allocations = scheduler.schedule_cycle(registry_businesses, 100, 500.0)
    
    for bid, alloc in allocations.items():
        print(f"[{bid}] -> Score: {alloc['score']}, Allocation: {alloc['allocation_pct']*100}%")

if __name__ == "__main__":
    run_incubation()
