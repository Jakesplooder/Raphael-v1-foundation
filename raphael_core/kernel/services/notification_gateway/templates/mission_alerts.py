def format_mission_alert(payload: dict) -> str:
    mission_id = payload.get("mission_id", "Unknown")
    strategy = payload.get("strategy", "Unknown")
    status = payload.get("status", "COMPLETED")
    quality_score = payload.get("quality_score", 0.0)
    
    return f"""🤖 Raphael Mission Update

Mission:
{mission_id}

Strategy:
{strategy}

Status:
{status}

Quality Score:
{quality_score:.2f}%"""

def format_mission_failure(payload: dict) -> str:
    mission_id = payload.get("mission_id", "Unknown")
    problem = payload.get("problem", "Unknown failure")
    recovery = payload.get("recovery", "No recovery attempted")
    
    return f"""🚨 Critical Failure

Mission:
{mission_id}

Problem:
{problem}

Recovery:
{recovery}

Action Required:
None"""
