import sys
from pathlib import Path
import datetime as dt

sys.path.insert(0, '.')
from raphael_core import legacy, world_model

def main():
    config = legacy.load_config(Path('Ralphael/config/settings.json'))
    model = world_model.load_model(config)
    
    # 1. Add Person node
    person_node = {
        "node_id": "PERSON-AARON-TEST",
        "node_type": "Employee",
        "name": "Aaron_Test_User",
        "summary": "A test user for career domains",
        "confidence": 1.0,
        "confidence_state": "active",
        "source_system": "System Generated Records",
        "source_reference": "test_script.py",
        "source_trust": "A",
        "created_at": dt.datetime.now().isoformat(),
        "updated_at": dt.datetime.now().isoformat(),
        "status": "active"
    }
    
    # 2. Add skills
    docker_node = {
        "node_id": "SKILL-DOCKER",
        "node_type": "Skill",
        "name": "Docker",
        "summary": "Docker containerization skill",
        "confidence": 1.0,
        "confidence_state": "active",
        "source_system": "System Generated Records",
        "source_reference": "test_script.py",
        "source_trust": "A",
        "created_at": dt.datetime.now().isoformat(),
        "updated_at": dt.datetime.now().isoformat(),
        "status": "active"
    }
    
    linux_node = {
        "node_id": "SKILL-LINUX",
        "node_type": "Skill",
        "name": "Linux",
        "summary": "Linux operating system skill",
        "confidence": 1.0,
        "confidence_state": "active",
        "source_system": "System Generated Records",
        "source_reference": "test_script.py",
        "source_trust": "A",
        "created_at": dt.datetime.now().isoformat(),
        "updated_at": dt.datetime.now().isoformat(),
        "status": "active"
    }
    
    # Update or add nodes
    for n in [person_node, docker_node, linux_node]:
        existing = next((x for x in model['nodes'] if x['node_id'] == n['node_id']), None)
        if existing:
            existing.update(n)
        else:
            model['nodes'].append(n)
            
    # Add relationships
    rel1 = {
        "relationship_id": "REL-TEST-1",
        "from_node": "PERSON-AARON-TEST",
        "to_node": "SKILL-DOCKER",
        "relationship_type": "RELATED_TO",
        "summary": "Aaron_Test_User HAS_SKILL Docker",
        "confidence": 0.76,
        "confidence_state": "active",
        "evidence": [{"source": "Test", "source_reference": "test", "source_trust": "A", "summary": "Tested"}],
        "source_system": "System Generated Records",
        "source_reference": "test_script.py",
        "source_trust": "A",
        "created_at": dt.datetime.now().isoformat(),
        "updated_at": dt.datetime.now().isoformat(),
        "status": "active"
    }
    
    rel2 = {
        "relationship_id": "REL-TEST-2",
        "from_node": "PERSON-AARON-TEST",
        "to_node": "SKILL-LINUX",
        "relationship_type": "RELATED_TO",
        "summary": "Aaron_Test_User HAS_SKILL Linux",
        "confidence": 0.84,
        "confidence_state": "active",
        "evidence": [{"source": "Test", "source_reference": "test", "source_trust": "A", "summary": "Tested"}],
        "source_system": "System Generated Records",
        "source_reference": "test_script.py",
        "source_trust": "A",
        "created_at": dt.datetime.now().isoformat(),
        "updated_at": dt.datetime.now().isoformat(),
        "status": "active"
    }
    
    for r in [rel1, rel2]:
        existing = next((x for x in model['relationships'] if x['relationship_id'] == r['relationship_id']), None)
        if existing:
            existing.update(r)
        else:
            model['relationships'].append(r)
            
    world_model.save_model(config, model['nodes'], model['relationships'], model['events'], model['hypotheses'], [])
    print("Added nodes and relationships successfully.")

if __name__ == "__main__":
    main()
