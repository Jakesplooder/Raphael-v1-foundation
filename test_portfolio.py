import sys
from pathlib import Path
sys.path.insert(0, r"C:\Users\cyber\Downloads\RalphaelOS")

from raphael_core.kernel.services.business_registry.base_twin import BaseTwin
from raphael_core.kernel.services.business_registry.lifecycle import LifecycleState
from raphael_core.kernel.services.portfolio_manager.allocation_engine import AllocationEngine
from raphael_core.kernel.services.portfolio_manager.resource_scheduler import ResourceScheduler
from raphael_core.kernel.services.portfolio_manager.portfolio_report import PortfolioReport

def run_test():
    # 1. Setup Businesses
    focus_marketing = BaseTwin(
        business_id="focus_mktg",
        name="Focus Marketing",
        category="Marketing Education",
        domain="creator",
        storage_path=Path("fm_test.json")
    )
    focus_marketing.financials["roi"] = 8.4
    focus_marketing.confidence = 0.97
    focus_marketing.risk["operational_risk"] = 0.05

    mentor_map = BaseTwin(
        business_id="mentor_map",
        name="MentorMap",
        category="Career Transition",
        domain="career",
        storage_path=Path("mm_test.json")
    )
    mentor_map.financials["roi"] = 0.0
    mentor_map.confidence = 0.40
    mentor_map.risk["operational_risk"] = 0.15

    ai_store = BaseTwin(
        business_id="ai_store",
        name="AI Store",
        category="E-commerce",
        domain="commerce",
        storage_path=Path("ai_test.json")
    )
    ai_store.financials["roi"] = 0.0
    ai_store.confidence = 0.20
    ai_store.risk["operational_risk"] = 0.20

    businesses_registry = [
        {"twin": focus_marketing, "requirements": {"opportunity_score": 0.50, "strategic_importance": 0.80}},
        {"twin": mentor_map, "requirements": {"opportunity_score": 0.90, "strategic_importance": 0.60}},
        {"twin": ai_store, "requirements": {"opportunity_score": 0.85, "strategic_importance": 0.70}}
    ]

    # 2. Run Allocation
    engine = AllocationEngine()
    scheduler = ResourceScheduler(engine)
    
    total_gpu = 100
    total_budget = 500.0
    
    print("--- Running Allocation Engine ---")
    allocations = scheduler.schedule_cycle(businesses_registry, total_gpu, total_budget)
    
    for bid, alloc in allocations.items():
        print(f"Business: {bid}")
        print(f"  Score: {alloc['score']}")
        print(f"  Allocation: {alloc['allocation_pct']*100}% (GPU: {alloc['gpu_hours']})")
        
    # 3. Generate Report
    report = PortfolioReport().generate_report(allocations, businesses_registry)
    print("\n--- Generated Report ---")
    print(report)

if __name__ == "__main__":
    run_test()
