import sys
sys.path.insert(0, r'C:\Users\cyber\Downloads\RalphaelOS')
import tests.test_initiative as t
import tests.test_optimization as topt
import tests.test_portfolio as tport
import tests.test_dashboard as tdash
import tests.test_security_council as tsec
import tests.test_agent_runtime as trun
import tests.test_performance_reviewer as tperf

def run():
    tests = [
        t.test_detection_and_correlation,
        t.test_throttling,
        t.test_lifecycle_dismiss,
        t.test_lifecycle_deferred_priority_update,
        t.test_briefing_transparency,
        topt.test_cost_privacy,
        topt.test_thrashing_case_1_ignored,
        topt.test_thrashing_case_2_triggers,
        topt.test_thrashing_case_3_reset_behavior,
        topt.test_cost_optimizer,
        tport.test_cycle_detection_guard,
        tport.test_critical_path_no_cycle,
        tport.test_forecast_confidence_bounds,
        tport.test_pareto_filter,
        tdash.test_health_score_calculation,
        tdash.test_dashboard_aggregator_missing_files,
        tdash.test_dashboard_staleness,
        tsec.test_red_team_all_scenarios_pass,
        tsec.test_canary_baseline_poison_resistance,
        tsec.test_near_miss_logging_and_pressure,
        trun.test_state_machine_validity,
        trun.test_authority_boundary,
        trun.test_onboarding_checklist,
        trun.test_canary_baseline_initialization,
        trun.test_workforce_health_signals,
        trun.test_world_model_integration,
        trun.test_onboarding_resume,
        tperf.test_score_calculation,
        tperf.test_weekly_snapshot_suppression,
        tperf.test_monthly_review_generation,
        tperf.test_trust_tier_recommendation,
        tperf.test_data_isolation,
        tperf.test_performance_acknowledge
    ]
    for test in tests:
        gen = t.clean_queue()
        next(gen)
        try:
            test()
        finally:
            try:
                next(gen)
            except StopIteration:
                pass
        print(f"{test.__name__} passed.")
    print("ALL TESTS PASSED")

if __name__ == '__main__':
    run()
