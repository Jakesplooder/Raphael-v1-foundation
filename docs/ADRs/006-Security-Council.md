# ADR 006: Security Council Charter (Phase 68.5E)

**Date**: 2026-07-06
**Status**: Proposed

## Context
As Raphael transitions from a passive analytical tool (Pillar I) to an active Digital Workforce (Pillar II), the attack surface expands significantly. Relying purely on basic constitutional validation is insufficient for an agentic system that can generate plans, route LLMs, manipulate priority queues, and sequence portfolios. Phase 68.5E retrofits the safety architecture originally envisioned in Phase 68.5, establishing a permanent, active Security Council and continuous Canary Agent monitoring before expanding capability.

## Decisions

### 1. The Security Council Membership
**Decision**: The Security Council is formalized with distinct agent roles, not a single monolithic validator.
- **Red Team Agent**: Actively executes adversarial test scenarios.
- **Safety Auditor Agent**: Retroactively reviews near-misses and logs.
- **Governance Agent**: Ensures constitutional compliance (Phase 68).
- **Compliance Agent**: Ensures policy adherence.

### 2. The Canary Agent Positioning and Median Baseline
**Decision**: The Canary Agent sits directly under Raphael Core, outside the Security Council. It uses a 30-day **median** baseline to compute behavior, actively ignoring the top and bottom 10%.
**Rationale**: A mean (average) baseline is susceptible to "poisoning" (Scenario 5)—if an agent behaves anomalously for a sustained period, the anomaly becomes the new normal. A median baseline resists outliers, requiring sustained anomaly over the majority of the period to shift, which itself triggers a behavioral warning.

### 3. Red Team Cadence and Findings
**Decision**: A full regression red team suite is executed on the completion of every major phase. The Security Council's active mission is to discover one new theoretical weakness per month.
**Rationale**: Security is adversarial. If the red team scenarios all pass, the system is secure against known vectors, but the council must actively seek unknown vectors as the system evolves. Any failed red team scenario is a hard blocker for subsequent capability expansions.

### 4. Near-Miss Logging and Safety Pressure Score
**Decision**: The system will actively track "Safety Pressure" for each agent based on near-misses and constitutional boundary approaches.
**Rationale**: Violations are rare; near-misses are common. By logging near-misses, the Canary and Safety Auditor agents can calculate a `Safety Pressure Score` for any active agent. If this score elevates, the Portfolio Optimizer (Phase 69.8) and Initiative Queue (Phase 69.6) can use it to block that agent from high-risk assignments.

## Consequences
- Requires `canary_agent.py` to maintain stateful history of agent behavioral metrics.
- Requires `red_team_agent.py` to hardcode adversarial vectors to test against the production system.
- Ensures the system is robustly tested against authority bypasses, confidence inflation, narrative fabrication, queue flooding, baseline poisoning, and escalation fatigue before Phase 70.0 activates the workforce.
