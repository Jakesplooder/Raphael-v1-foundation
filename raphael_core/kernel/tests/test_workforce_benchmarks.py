import asyncio
import logging
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from raphael_core.workforce.employees.employee import DigitalEmployee, EmployeeLineage
from raphael_core.workforce.employees.employee_state import EmployeeState
from raphael_core.workforce.employees.workforce_manager import WorkforceManager
from raphael_core.workforce.departments.department import EngineeringDept, MarketingDept, CustomerSuccessDept
from raphael_core.workforce.skills.skill_registry import SkillRegistry
from raphael_core.workforce.training.employee_training import EmployeeTraining
from raphael_core.workforce.performance.employee_metrics import EmployeeMetrics
from raphael_core.workforce.memory.employee_memory import EmployeeMemory

logger = logging.getLogger("rrk.tests.workforce_benchmarks")
logging.basicConfig(level=logging.INFO)

async def run_workforce_benchmarks():
    logger.info("Starting D18 Digital Workforce Benchmarks...")
    passed = 0
    total = 6
    
    skill_registry = SkillRegistry()
    skill_registry.register_skill("Python", "Engineering")
    skill_registry.register_skill("Penetration Testing", "Security")
    skill_registry.register_skill("SEO Optimization", "Marketing")
    skill_registry.register_skill("Sales Outreach", "Sales")
    skill_registry.register_skill("Compliance Analysis", "Legal")
    
    wf_manager = WorkforceManager(skill_registry)
    trainer = EmployeeTraining()
    metrics = EmployeeMetrics()
    memory = EmployeeMemory()
    
    # 1. CEO Hires Employees
    logger.info("\n--- Benchmark 1: CEO Hires Employees ---")
    eng_dept = EngineeringDept("CYBER-001")
    
    sec_eng = wf_manager.request_capability(
        "CYBER-001", eng_dept, "Security Engineer",
        ["Python", "Penetration Testing"], "CybersecurityCEO"
    )
    sales_spec = wf_manager.request_capability(
        "CYBER-001", eng_dept, "Sales Specialist",
        ["Sales Outreach"], "CybersecurityCEO"
    )
    compliance = wf_manager.request_capability(
        "CYBER-001", eng_dept, "Compliance Analyst",
        ["Compliance Analysis"], "CybersecurityCEO"
    )
    
    if sec_eng and sales_spec and compliance and eng_dept.head_count == 3:
        logger.info(f"  [SUCCESS] CybersecurityCEO hired 3 employees: {sec_eng.role}, {sales_spec.role}, {compliance.role}")
        passed += 1
    else:
        logger.error("  [FAILURE] CEO hiring failed.")
        
    # 2. Employee Training
    logger.info("\n--- Benchmark 2: Employee Training ---")
    sec_eng.performance_score = 35.0
    if trainer.needs_training(sec_eng):
        memory.setup_employee(sec_eng.id)
        memory.record(sec_eng.id, "mistakes", {"task": "firewall_config", "error": "missed port 443"})
        memory.record(sec_eng.id, "mistakes", {"task": "vuln_scan", "error": "false positive overload"})
        mistakes = memory.recall(sec_eng.id, "mistakes")
        new_score = trainer.train(sec_eng, mistakes)
        if new_score > 50.0 and sec_eng.state == EmployeeState.IMPROVING:
            logger.info(f"  [SUCCESS] Training improved score from 35.0 to {new_score:.1f}")
            passed += 1
        else:
            logger.error(f"  [FAILURE] Training did not improve score: {new_score}")
    else:
        logger.error("  [FAILURE] Training detection failed.")
        
    # 3. Department Formation
    logger.info("\n--- Benchmark 3: Department Formation ---")
    saas_eng = EngineeringDept("SAAS-001")
    saas_mkt = MarketingDept("SAAS-001")
    saas_cs = CustomerSuccessDept("SAAS-001")
    
    wf_manager.request_capability("SAAS-001", saas_eng, "Backend Dev", ["Python"], "SaaSCEO")
    wf_manager.request_capability("SAAS-001", saas_mkt, "SEO Specialist", ["SEO Optimization"], "SaaSCEO")
    wf_manager.request_capability("SAAS-001", saas_cs, "Support Lead", ["Sales Outreach"], "SaaSCEO")
    
    if saas_eng.head_count == 1 and saas_mkt.head_count == 1 and saas_cs.head_count == 1:
        logger.info(f"  [SUCCESS] SaaS formed 3 departments: Engineering({saas_eng.head_count}), Marketing({saas_mkt.head_count}), CS({saas_cs.head_count})")
        passed += 1
    else:
        logger.error("  [FAILURE] Department formation failed.")
        
    # 4. Resource Conflict
    logger.info("\n--- Benchmark 4: Resource Conflict ---")
    # Two CEOs need Python skill — WorkforceManager selects best performer
    sec_eng.performance_score = 92.0
    sec_eng.transition(EmployeeState.ACTIVE)
    # The SaaS backend dev has default 50.0
    best = wf_manager.select_best_for_task("Python")
    if best and best.id == sec_eng.id:
        logger.info(f"  [SUCCESS] WorkforceManager selected highest performer {best.id} (score: {best.performance_score})")
        passed += 1
    else:
        logger.error(f"  [FAILURE] Wrong employee selected: {best}")
        
    # 5. Employee Learning
    logger.info("\n--- Benchmark 5: Employee Learning ---")
    memory.record(sec_eng.id, "successful_patterns", {"pattern": "always_run_impact_analysis_first"})
    memory.record(sec_eng.id, "learned_skills", {"skill": "Impact Analysis", "source": "mistake_recovery"})
    patterns = memory.recall(sec_eng.id, "successful_patterns")
    learned = memory.recall(sec_eng.id, "learned_skills")
    if len(patterns) > 0 and len(learned) > 0:
        logger.info(f"  [SUCCESS] Employee {sec_eng.id} remembers {len(patterns)} patterns and {len(learned)} learned skills.")
        passed += 1
    else:
        logger.error("  [FAILURE] Employee learning failed.")
        
    # 6. Employee Selection Optimization (Merit-Based)
    logger.info("\n--- Benchmark 6: Employee Selection Optimization ---")
    # Create 3 employees with Python, different scores
    emp_a = DigitalEmployee(id="TEST-A", role="Dev A", department="Eng", skills=["Python"], performance_score=92.0, state=EmployeeState.ACTIVE)
    emp_b = DigitalEmployee(id="TEST-B", role="Dev B", department="Eng", skills=["Python"], performance_score=74.0, state=EmployeeState.ACTIVE)
    emp_c = DigitalEmployee(id="TEST-C", role="Dev C", department="Eng", skills=["Python"], performance_score=88.0, state=EmployeeState.ACTIVE)
    wf_manager.employee_pool.extend([emp_a, emp_b, emp_c])
    
    selected = wf_manager.select_best_for_task("Python")
    # Should select emp_a or sec_eng (both 92.0)
    if selected and selected.performance_score >= 92.0:
        score = metrics.calculate(
            task_success=92.0, decision_quality=85.0,
            resource_efficiency=90.0, learning_rate=88.0,
            customer_impact=80.0, autonomy_growth=95.0
        )
        logger.info(f"  [SUCCESS] Merit-based selection: {selected.id} (perf: {selected.performance_score}). Intelligence Score: {score}")
        passed += 1
    else:
        logger.error(f"  [FAILURE] Merit selection failed: {selected}")
    
    logger.info(f"\nDigital Workforce Benchmarks Complete! {passed}/{total} passed.")

if __name__ == "__main__":
    asyncio.run(run_workforce_benchmarks())
