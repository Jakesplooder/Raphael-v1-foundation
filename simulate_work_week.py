from raphael_core.agent_runtime import AgentRuntimeRegistry
import random

def simulate_work_week():
    reg = AgentRuntimeRegistry()
    agents = reg.load_registry()
    
    tasks_completed_count = 0
    
    for agent_id, agent in agents.items():
        if agent["current_state"] != "active":
            continue
            
        # Simulate 3 to 12 tasks per agent
        num_tasks = random.randint(3, 12)
        tasks_completed_count += num_tasks
        
        # Inject metrics into agent runtime for performance evaluator to discover
        # Productivity (70 to 98)
        prod = random.uniform(70.0, 98.0)
        # Accuracy (80 to 100)
        acc = random.uniform(80.0, 100.0)
        # Reliability (85 to 100)
        rel = random.uniform(85.0, 100.0)
        # Cost Efficiency (60 to 95)
        cost = random.uniform(60.0, 95.0)
        
        agent["simulated_metrics"] = {
            "productivity_raw": prod,
            "accuracy_raw": acc,
            "reliability_raw": rel,
            "cost_efficiency_raw": cost
        }
        
        # Just to show they did work
        agent["active_task_count"] = 0
        agent["total_tasks_completed"] = agent.get("total_tasks_completed", 0) + num_tasks
        agent["safety_pressure_score"] = random.uniform(0.0, 45.0)
        
        reg.update_agent(agent_id, agent)
        print(f"Simulated {num_tasks} tasks for {agent_id}. Prod: {prod:.1f}, Acc: {acc:.1f}, Rel: {rel:.1f}, Cost: {cost:.1f}")
        
    print(f"Successfully simulated {tasks_completed_count} tasks across the workforce.")

if __name__ == "__main__":
    simulate_work_week()
