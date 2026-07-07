from raphael_core.agent_runtime import AgentRuntimeRegistry
import sys

def setup_pilot():
    reg = AgentRuntimeRegistry()
    
    agents = [
        {"id": "AGENT-OPERATIONS", "name": "Operations Agent", "tier": 1},
        {"id": "AGENT-RESOURCE", "name": "Resource Manager", "tier": 1},
        {"id": "AGENT-COO", "name": "COO", "tier": 2},
        {"id": "AGENT-CHIEF-OF-STAFF", "name": "Chief of Staff", "tier": 2},
        {"id": "AGENT-PROJECT-MANAGER", "name": "Project Manager", "tier": 1},
        {"id": "AGENT-DEVELOPER", "name": "Developer Agent", "tier": 1},
        {"id": "AGENT-RESEARCH", "name": "Research Agent", "tier": 1},
        {"id": "AGENT-COMMERCE", "name": "Commerce Agent", "tier": 1},
    ]
    
    for a in agents:
        reg.create_agent_record(a["id"], a["name"], a["tier"], "Council", [], "ollama")
        print(f"Created record for {a['id']}")

if __name__ == "__main__":
    setup_pilot()
