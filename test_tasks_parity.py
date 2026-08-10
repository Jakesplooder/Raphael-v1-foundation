import os
import sys
import json
from typing import List, Dict

# Set up paths so we can import modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from raphael_core.repositories.tasks import MarkdownTaskRepository
from raphael_core.services.tasks import TaskService
from api_gateway import legacy_adapter
from pathlib import Path

def test_tasks_parity():
    print("Testing Tasks Parity between RRK and Legacy Adapter")
    
    # Initialize RRK repository directly for testing
    import json
    settings = json.loads(Path(r"R:\RalphaelOS_Repo\config\settings.json").read_text())
    vault_path = Path(settings["vault_path"])
    print(f"DEBUG: Using vault path: {vault_path}")
    print(f"DEBUG: Vault path exists? {vault_path.exists()}")
    print(f"DEBUG: Legacy vault path: {legacy_adapter.vault_path()}")
    repo = MarkdownTaskRepository(vault_path)
    service = TaskService(repo)
    
    # 1. Test Agent Tasks
    print("\n--- Testing Agent Tasks ---")
    rrk_agent_tasks = service.get_tasks("agent")
    legacy_agent_tasks = legacy_adapter.tasks()
    
    print(f"RRK Agent Tasks Count: {len(rrk_agent_tasks)}")
    print(f"Legacy Agent Tasks Count: {len(legacy_agent_tasks)}")
    
    if len(rrk_agent_tasks) != len(legacy_agent_tasks):
        print("FAIL: Task counts do not match!")
        return False
        
    for i, (rrk, leg) in enumerate(zip(rrk_agent_tasks, legacy_agent_tasks)):
        rrk_copy = {k: v for k, v in rrk.items() if k != "path"}
        leg_copy = {k: v for k, v in leg.items() if k != "path"}
        if rrk_copy != leg_copy:
            print(f"FAIL: Mismatch at index {i}")
            print(f"RRK: {rrk_copy}")
            print(f"Legacy: {leg_copy}")
            return False
            
    print("Agent Tasks Parity: PASS (Ordering, IDs, and fields match perfectly)")
    
    # 2. Test Council Tasks
    print("\n--- Testing Council Tasks ---")
    rrk_council_tasks = service.get_tasks("council")
    legacy_council_tasks = legacy_adapter.council_task_entries()
    
    print(f"RRK Council Tasks Count: {len(rrk_council_tasks)}")
    print(f"Legacy Council Tasks Count: {len(legacy_council_tasks)}")
    
    if len(rrk_council_tasks) != len(legacy_council_tasks):
        print("FAIL: Council task counts do not match!")
        return False
        
    for i, (rrk, leg) in enumerate(zip(rrk_council_tasks, legacy_council_tasks)):
        rrk_copy = {k: v for k, v in rrk.items() if k != "path"}
        leg_copy = {k: v for k, v in leg.items() if k != "path"}
        if rrk_copy != leg_copy:
            print(f"FAIL: Council Mismatch at index {i}")
            print(f"RRK: {rrk_copy}")
            print(f"Legacy: {leg_copy}")
            return False
            
    print("Council Tasks Parity: PASS (Ordering, IDs, and fields match perfectly)")
    
    return True

if __name__ == "__main__":
    success = test_tasks_parity()
    sys.exit(0 if success else 1)
