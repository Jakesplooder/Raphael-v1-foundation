import sys
sys.path.insert(0, r"R:\RalphaelOS_Repo")

from raphael_core.kernel.services.notification_gateway.notification_service import notification_service

def test():
    print("Testing Notification Routing Policy...")
    
    print("\n--- Test 1: MISSION.COMPLETED (Normal) ---")
    notification_service.handle_event("MISSION.COMPLETED", "Test", {"mission_id": "TEST_001", "strategy": "None", "status": "DONE"})
    
    print("\n--- Test 2: MISSION.FAILURE (Warning) ---")
    notification_service.handle_event("MISSION.FAILURE", "Test", {"mission_id": "TEST_002", "priority": "warning", "problem": "Minor issue", "recovery": "Auto-retried", "action_required": "None"})

    print("\n--- Test 3: MISSION.FAILURE (Critical) ---")
    notification_service.handle_event("MISSION.FAILURE", "Test", {"mission_id": "TEST_003", "priority": "critical", "problem": "GPU Melted", "recovery": "None", "action_required": "Buy new GPU"})

    print("\n--- Test 4: APPROVAL.REQUIRED (High) ---")
    notification_service.handle_event("APPROVAL.REQUIRED", "Test", {"priority": "high", "approval_id": "app_01", "request_type": "PUBLISH", "requested_action": "Publish video", "payload": {}})

if __name__ == "__main__":
    test()
