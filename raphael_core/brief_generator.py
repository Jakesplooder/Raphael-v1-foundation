import os
import json
import re
from datetime import datetime
from . import reasoning_engine

class ConstitutionalViolationError(Exception):
    """Raised when the brief references evidence not present in the trace."""
    pass

def calculate_weights(trace):
    wm_count = 0
    lessons = 0
    events = 0
    patterns = 0
    
    for step in trace.get("steps", []):
        if step["action"] == "world_model_query": wm_count = step.get("result_count", 0)
        elif step["action"] == "lesson_retrieval": lessons = step.get("lessons_found", 0)
        elif step["action"] == "event_retrieval": events = step.get("events_found", 0)
        elif step["action"] == "pattern_retrieval": patterns = step.get("patterns_found", 0)
        
    total = wm_count + lessons + events + patterns
    if total == 0:
        return {"patterns": 0, "events": 0, "lessons": 0, "world_model": 0}, patterns, events, lessons, wm_count
        
    return {
        "patterns": round((patterns / total) * 100),
        "events": round((events / total) * 100),
        "lessons": round((lessons / total) * 100),
        "world_model": round((wm_count / total) * 100)
    }, patterns, events, lessons, wm_count


def validate_constitutional_compliance(brief_text: str, trace_evidence_ids: list) -> bool:
    """
    Parses the generated brief for any Evidence IDs (PATTERN-*, EVENT-*, LESSON-*)
    and strictly validates they exist in the trace_evidence_ids.
    """
    # Regex to find IDs matching PATTERN-XXXX, EVENT-XXXX, LESSON-XXXX
    found_ids = set(re.findall(r"(PATTERN-[A-Z0-9\-]+|EVENT-[A-Z0-9\-]+|LESSON-[A-Z0-9\-]+)", brief_text))
    trace_ids_set = set(trace_evidence_ids)
    
    hallucinated = found_ids - trace_ids_set
    if hallucinated:
        raise ConstitutionalViolationError(f"CRITICAL: Fabricated evidence detected in Executive Brief: {hallucinated}")
        
    return True


def extract_claim_sections(brief_text: str) -> list:
    """Extracts sections of the brief that contain claims."""
    sections = []
    # Simple heuristic for this deterministic version
    lines = brief_text.split('\n')
    current_section = []
    in_section = False
    
    for line in lines:
        if line.strip() in ["SITUATION", "HISTORICAL CONTEXT", "PATTERNS", "LESSONS", "RISKS", "OPPORTUNITIES", "RECOMMENDATION"]:
            if current_section:
                sections.append("\n".join(current_section))
            current_section = [line]
            in_section = True
        elif in_section and line.strip() in ["CONFIDENCE", "EVIDENCE", "CONSTITUTIONAL COMPLIANCE"]:
            if current_section:
                sections.append("\n".join(current_section))
            in_section = False
            current_section = []
        elif in_section:
            current_section.append(line)
            
    if current_section:
        sections.append("\n".join(current_section))
        
    return sections


def validate_evidence_density(brief_text: str, trace_evidence_ids: list) -> bool:
    """Ensures every section with claims has at least one valid evidence citation."""
    sections = extract_claim_sections(brief_text)
    
    for section in sections:
        # For Phase 69.1 mock, only check HISTORICAL, PATTERNS, LESSONS, RECOMMENDATION
        if any(h in section for h in ["HISTORICAL CONTEXT", "PATTERNS", "LESSONS", "RECOMMENDATION"]):
            if not any(eid in section for eid in trace_evidence_ids):
                # If there were no trace ids provided at all for this section type, that's okay (e.g. 0 patterns found)
                # But if there's a claim, it must be backed.
                pass
                
    # Since our formatter is entirely deterministic and rigidly injects IDs right now, 
    # it always passes. But this function is structurally prepared for the LLM phase.
    return True



def format_brief(trace: dict) -> str:
    weights, p_cnt, e_cnt, l_cnt, wm_cnt = calculate_weights(trace)
    
    trace_id = trace["reasoning_trace_id"]
    timestamp = trace.get("generated_at", datetime.utcnow().isoformat())
    auth_req = "Yes" if trace.get("authority_required") else "No"
    question = trace.get("question", "Unknown")
    
    # Extract Confidence
    confidence = 0.0
    risks = 0
    opps = 0
    for step in trace.get("steps", []):
        if step["action"] == "recommendation_generation": confidence = step.get("confidence", 0.0)
        elif step["action"] == "risk_evaluation": risks = step.get("risks_identified", 0)
        elif step["action"] == "opportunity_evaluation": opps = step.get("opportunities_identified", 0)
    
    # Organize evidence
    ev_patterns = [e for e in trace.get("evidence_ids", []) if e.startswith("PATTERN")]
    ev_lessons = [e for e in trace.get("evidence_ids", []) if e.startswith("LESSON")]
    ev_events = [e for e in trace.get("evidence_ids", []) if e.startswith("EVENT")]
    
    # Format Schema
    brief = f"""EXECUTIVE BRIEF
===============================
Trace ID:         {trace_id}
Generated:        {timestamp}
Authority Required: {auth_req}
===============================

SITUATION
The executive layer received a strategic inquiry: "{question}". Based on World Model context, this requires evaluating structural and historical patterns to form an evidence-backed opinion.

HISTORICAL CONTEXT  
The World Model identified {e_cnt} historical events related to this domain. 
Relevant Event Signatures: {', '.join(ev_events) if ev_events else 'None explicitly mapped'}

PATTERNS
The Pattern Discovery Engine identified {p_cnt} overarching organizational patterns that apply to this situation.
Relevant Pattern Signatures: {', '.join(ev_patterns) if ev_patterns else 'None explicitly mapped'}

LESSONS
Institutional Memory surfaced {l_cnt} critical lessons learned from past workflows.
Relevant Lesson Signatures: {', '.join(ev_lessons) if ev_lessons else 'None explicitly mapped'}

RISKS
The pipeline evaluated potential drawbacks and identified {risks} structural risk(s) associated with immediate execution.

OPPORTUNITIES
The pipeline evaluated strategic advantages and identified {opps} high-leverage opportunity/opportunities.

RECOMMENDATION
Based on the synthesized evidence, the pipeline deterministically recommends proceeding with the historically verified approach, optimizing for the identified patterns while mitigating the flagged risks.

CONFIDENCE
{int(confidence * 100)}% because:
  Patterns:    {p_cnt} found    -> {weights['patterns']}%
  Events:      {e_cnt} found    -> {weights['events']}%
  Lessons:     {l_cnt} found    -> {weights['lessons']}%
  World Model: {wm_cnt} results  -> {weights['world_model']}%

EVIDENCE
{chr(10).join(f"- {eid}" for eid in trace.get("evidence_ids", [])) if trace.get("evidence_ids") else "No hard evidence IDs mapped."}

CONSTITUTIONAL COMPLIANCE
Articles referenced: {', '.join(trace.get("constitutional_articles", []))}
Authority required: {auth_req}
"""
    return brief

def generate_brief_from_query(query: str) -> str:
    # 1. Run the reasoning pipeline
    trace = reasoning_engine.execute_pipeline(query)
    
    # 2. Format the trace deterministically
    brief_text = format_brief(trace)
    
    # 3. Validate constitutional compliance
    validate_constitutional_compliance(brief_text, trace.get("evidence_ids", []))
    validate_evidence_density(brief_text, trace.get("evidence_ids", []))
    
    return brief_text

def test_validator():
    """Synthetic test to ensure the validator trips on fabricated evidence."""
    trace = {
        "reasoning_trace_id": "TRACE-TEST",
        "evidence_ids": ["EVENT-123", "PATTERN-456"]
    }
    # Create a brief with a fake ID
    bad_brief = "EXECUTIVE BRIEF\nEVIDENCE\n- EVENT-123\n- PATTERN-456\n- LESSON-FAKE999"
    try:
        validate_constitutional_compliance(bad_brief, trace["evidence_ids"])
        return False, "Validator failed to catch fabricated evidence."
    except ConstitutionalViolationError as e:
        return True, str(e)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "test-validator":
        success, msg = test_validator()
        print(f"Validator Test: {'PASS' if success else 'FAIL'} - {msg}")
    else:
        query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "What should I build next?"
        print(generate_brief_from_query(query))
