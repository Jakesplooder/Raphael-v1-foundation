import os
import sys

# Ensure we're running from RalphaelOS directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Enable debug mode to see routing logs
os.environ["RAPHAEL_ROUTING_DEBUG"] = "true"

from raphael_core.operator.chat_controller import chat_controller

def test():
    print("Testing Phase 8.5 Executive Chat Router Hardening...\n")
    
    print("--- Test 1: Capability Query (What tools do you have?) ---")
    resp1 = chat_controller.process_message("test_session", "what tools do you have")
    print(f"Intent: {resp1.get('intent')}")
    print(f"Response Payload:\n{resp1.get('response')}\n")
    
    print("--- Test 2: Workflow Query (What workflows do you have?) ---")
    resp2 = chat_controller.process_message("test_session", "What workflows do you have")
    print(f"Intent: {resp2.get('intent')}")
    print(f"Response Payload:\n{resp2.get('response')}\n")
    
    print("--- Test 3: Video Workflow (create me a rap battle video between a cactus and a tree) ---")
    resp3 = chat_controller.process_message("test_session", "create me a rap battle video between a cactus and a tree")
    print(f"Intent: {resp3.get('intent')}")
    print(f"Matched Command: {resp3.get('command')}")
    print(f"Response Payload:\n{resp3.get('response')}\n")
    
    print("--- Test 4: Unknown Creation (create me a teleportation machine) ---")
    resp4 = chat_controller.process_message("test_session", "create me a teleportation machine")
    print(f"Intent: {resp4.get('intent')}")
    print(f"Response Payload:\n{resp4.get('response')}\n")
    
    print("--- Test 5: Normal Conversation (what time is it) ---")
    resp5 = chat_controller.process_message("test_session", "what time is it")
    print(f"Intent: {resp5.get('intent')}")
    print(f"Response Payload: {'[EMPTY - ROUTED TO LLM]' if not resp5.get('response') else resp5.get('response')}\n")
    
    print("Testing complete.")

if __name__ == "__main__":
    test()
