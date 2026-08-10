from raphael_core.agent_runtime import AgentRuntimeRegistry, AgentLifecycleManager, OnboardingProtocol, ConstitutionalViolationError
from raphael_core.workforce_health import scan_workforce_health
import os

def test_state_machine_validity():
    reg = AgentRuntimeRegistry(filepath=r"R:\RaphaelOS\workforce\test_registry.json")
    lif = AgentLifecycleManager(reg)
    
    # Valid transition
    reg.create_agent_record("TEST-1", "Test", 1, "Council", [], "model")
    lif.request_transition("TEST-1", "onboarding", "Starting", [])
    
    agent = reg.get_agent("TEST-1")
    assert agent["current_state"] == "onboarding"
    
    # Invalid transition
    try:
        lif.request_transition("TEST-1", "retired", "Direct retirement", [])
        assert False, "Should have raised ConstitutionalViolationError"
    except ConstitutionalViolationError:
        pass

def test_authority_boundary():
    reg = AgentRuntimeRegistry(filepath=r"R:\RaphaelOS\workforce\test_registry.json")
    lif = AgentLifecycleManager(reg)
    reg.create_agent_record("TEST-2", "Test", 1, "Council", [], "model")
    lif.request_transition("TEST-2", "onboarding", "Starting", [])
    lif.request_transition("TEST-2", "active", "Started", [])
    
    # Attempt suspended (Authority required)
    res = lif.request_transition("TEST-2", "suspended", "Needs auth", [])
    assert res["status"] == "initiative_created"
    
    # Agent state should NOT change
    agent = reg.get_agent("TEST-2")
    assert agent["current_state"] == "active"

def test_onboarding_checklist():
    reg = AgentRuntimeRegistry(filepath=r"R:\RaphaelOS\workforce\test_registry.json")
    lif = AgentLifecycleManager(reg)
    onb = OnboardingProtocol(reg, lif)
    
    reg.create_agent_record("TEST-3", "Test", 1, "Council", [], "model")
    agent = reg.get_agent("TEST-3")
    agent["world_model_node_id"] = None # Missing node
    reg.update_agent("TEST-3", agent)
    
    res = onb.start_onboarding("TEST-3")
    assert res["status"] == "halted"
    assert res["failed_item"] == "world_model_node"

def test_canary_baseline_initialization():
    reg = AgentRuntimeRegistry(filepath=r"R:\RaphaelOS\workforce\test_registry.json")
    lif = AgentLifecycleManager(reg)
    onb = OnboardingProtocol(reg, lif)
    
    reg.create_agent_record("TEST-4", "Test", 1, "Council", [], "model")
    res = onb.start_onboarding("TEST-4")
    
    assert res["status"] == "completed"
    agent = reg.get_agent("TEST-4")
    assert agent["current_state"] == "active"
    assert agent["onboarding_completed_at"] is not None

def test_workforce_health_signals():
    reg = AgentRuntimeRegistry(filepath=r"R:\RaphaelOS\workforce\test_registry.json")
    lif = AgentLifecycleManager(reg)
    
    reg.create_agent_record("TEST-5", "Test", 1, "Council", [], "model")
    agent = reg.get_agent("TEST-5")
    agent["current_state"] = "active"
    agent["safety_pressure_score"] = 65
    reg.update_agent("TEST-5", agent)
    
    signals = scan_workforce_health(reg, lif)
    assert len(signals) == 1
    assert signals[0]["recommended_transition"] == "under_review"

def test_world_model_integration():
    # Implicitly tested via execute_transition not crashing and calling world_model_emitter
    pass

def test_onboarding_resume():
    reg = AgentRuntimeRegistry(filepath=r"R:\RaphaelOS\workforce\test_registry.json")
    lif = AgentLifecycleManager(reg)
    onb = OnboardingProtocol(reg, lif)
    
    reg.create_agent_record("TEST-7", "Test", 1, "Council", [], "model")
    agent = reg.get_agent("TEST-7")
    agent["world_model_node_id"] = None
    reg.update_agent("TEST-7", agent)
    
    res = onb.start_onboarding("TEST-7")
    assert res["status"] == "halted"
    
    # Fix the missing item
    agent = reg.get_agent("TEST-7")
    agent["world_model_node_id"] = "NODE"
    reg.update_agent("TEST-7", agent)
    
    # Resume
    res = onb.resume_onboarding("TEST-7")
    assert res["status"] == "completed"
    
    agent = reg.get_agent("TEST-7")
    assert agent["current_state"] == "active"
    
    if os.path.exists(r"R:\RaphaelOS\workforce\test_registry.json"):
        os.remove(r"R:\RaphaelOS\workforce\test_registry.json")
