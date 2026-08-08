import sys
sys.path.insert(0, r"C:\Users\cyber\Downloads\RalphaelOS")

from raphael_core.kernel.services.notification_gateway.notification_service import notification_service

def test():
    print("Testing Discord & Telegram...")
    notification_service.handle_event(
        event_type="MISSION.FAILURE",
        source="TestScript",
        payload={
            "mission_id": "TEST_001",
            "problem": "Manual notification test triggered by the executive.",
            "recovery": "No action required.",
            "priority": "critical"
        }
    )
    print("Done.")

if __name__ == "__main__":
    test()
