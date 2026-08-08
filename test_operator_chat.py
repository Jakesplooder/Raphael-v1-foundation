import os
import sys
import time

# Ensure we're running from RalphaelOS directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Enable debug mode to see routing logs
os.environ["RAPHAEL_ROUTING_DEBUG"] = "true"

from raphael_core.operator.chat_controller import chat_controller

def test():
    print("Testing Phase 9 Unified Execution Layer...\n")
    session = "test_phase9"
    
    print("--- Test 1: Concept-Based Workflow Scoring (make me a video for a cat and a dog battle rapping) ---")
    resp1 = chat_controller.process_message(session, "make me a video for a cat and a dog battle rapping")
    print(f"Intent: {resp1.get('intent')}")
    print(f"Matched Command: {resp1.get('command')}")
    print(f"Response Payload:\n{resp1.get('response')}\n")
    
    print("--- Test 2: Status Query (Should say no active execution because it is just pending) ---")
    resp2 = chat_controller.process_message(session, "what is the status")
    print(f"Response Payload:\n{resp2.get('response')}\n")
    
    print("--- Test 3: Approval (confirm) ---")
    resp3 = chat_controller.process_message(session, "confirm")
    print(f"Response Payload:\n{resp3.get('response')}\n")
    
    print("--- Test 4: Status Query (Should show running status with EX- ID) ---")
    resp4 = chat_controller.process_message(session, "status of the video")
    print(f"Response Payload:\n{resp4.get('response')}\n")
    
    print("Testing complete.")

if __name__ == "__main__":
    test()
