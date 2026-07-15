"""
Executive Reasoning Engine
"""
from typing import Dict, Any

def execute_reasoning_step_2(agent_id: str, purpose: str, question: str) -> Dict[str, Any]:
    """
    Step 2: Query World Model to establish facts before reasoning.
    """
    # [MIGRATED] Native call to RRK Daemon API
    import urllib.request
    import json
    
    try:
        req = urllib.request.Request(
            "http://127.0.0.1:8788/api/world-model/query",
            data=json.dumps({
                "agent_id": agent_id,
                "purpose": purpose,
                "question": question
            }).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=5) as response:
            if response.status == 200:
                data = json.loads(response.read().decode("utf-8"))
                if "error" not in data:
                    return data
                raise RuntimeError(f"RRK Error: {data['error']}")
    except Exception as e:
        raise RuntimeError(f"Kernel offline or unavailable. Ensure RRK daemon is running. {e}")
