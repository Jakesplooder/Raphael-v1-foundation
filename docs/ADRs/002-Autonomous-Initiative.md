# ADR 002: Autonomous Initiative & Executive Briefing (Phase 69.6)

**Date**: 2026-07-06
**Status**: Proposed

## Context
Phase 69.5 enabled Raphael to continuously learn from outcomes, decaying or reinforcing pattern confidences based on predictive accuracy. However, Raphael still waits for human prompts before acting on this compounded knowledge. To transition from a reactive assistant to a proactive Executive Operating System, Raphael requires the ability to autonomously detect opportunities and risks within the World Model, and proactively surface them. 

Crucially, **Autonomous Initiative is not autonomous action**. Raphael may observe and recommend, but it may not execute those recommendations without explicit human authorization.

## Decisions

### 1. What triggers the daily briefing?
**Decision**: Scheduled execution via explicit cron/scheduler (or a deterministic initialization hook at the start of the operator's day), supplemented by an on-demand CLI command (`python raphael.py briefing`). 
**Rationale**: Event-driven triggers risk flooding the operator with alerts, creating fatigue and violating the principle of focused executive attention. A scheduled daily briefing ensures predictability. The system computes its analysis overnight (or on command) and presents a single, coherent briefing.

### 2. How does the recommendation queue prevent approval fatigue?
**Decision**: The engine will employ strict **Throttling and Priority Ranking**. 
- **Maximum Threshold**: The briefing will surface a maximum of 3 to 5 recommendations per day. 
- **Ranking**: Items will be ranked by a composite score of `(Confidence * Impact) + Urgency`.
- **Transparency**: Every recommendation must expose its underlying evidence (Pattern IDs, Hypothesis IDs) and alternative interpretations, allowing the operator to quickly assess validity.

### 3. What is the initiative lifecycle?
**Decision**: Detected initiatives are not stateless. They must follow a strict state machine to prevent zombie alerts from polluting the daily briefing.
**Lifecycle States**:
1. `Detected`: Found during the scan, stored in the initiative queue.
2. `Briefed`: Surfaced to the operator in a Daily Briefing.
3. `Acknowledged`: Operator has seen it (can be implicit).
4. `Acted`: Operator authorized execution.
5. `Deferred`: Operator delayed action. Will resurface after a defined cooldown (e.g., 7 days).
6. `Dismissed`: Operator explicitly rejected it. Will not resurface unless underlying evidence fundamentally changes.

## Consequences
- Requires the creation of `opportunity_detector.py` and `risk_detector.py`.
- Requires an `initiative_queue.json` in the World Model to track the state of detected items.
- Requires a `daily_briefing.py` module capable of synthesizing the queue into the structured briefing format.
- Significantly increases the importance of the Constitution's "Truth & Evidence" article, as Raphael must justify why it is directing the operator's attention.
