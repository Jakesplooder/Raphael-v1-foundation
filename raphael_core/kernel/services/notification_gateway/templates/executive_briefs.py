def format_executive_brief(payload: dict) -> str:
    business = payload.get("business", "Focus Marketing")
    missions_completed = payload.get("missions_completed", 0)
    best_strategy = payload.get("best_strategy", "Unknown")
    confidence = payload.get("confidence", 0.0)
    recommended_action = payload.get("recommended_action", "No action")
    
    return f"""Good morning Aaron.

Raphael Executive Brief:

Business:
{business}

Yesterday:
{missions_completed} missions completed

Best strategy:
{best_strategy}

Recommended action:
{recommended_action}

Confidence:
{confidence * 100:.0f}%"""
