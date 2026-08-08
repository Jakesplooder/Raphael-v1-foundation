def format_approval_request(payload: dict) -> str:
    mission_id = payload.get("mission_id", "Unknown")
    strategy = payload.get("strategy", "Unknown")
    confidence = payload.get("confidence", 0.0)
    quality = payload.get("quality_score", 0.0)
    
    return f"""🤖 Raphael Mission Update

Mission:
{mission_id}

Strategy:
{strategy}

Status:
REVIEW REQUIRED

Quality Score:
{quality:.2f}%

Confidence:
{confidence:.2f}

Awaiting:
Human publishing approval

[Approve]
[Reject]
[Request Changes]"""
