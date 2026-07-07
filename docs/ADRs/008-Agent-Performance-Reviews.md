# ADR 008: Agent Performance Reviews (Phase 70.1)

**Date**: 2026-07-06
**Status**: Proposed

## Context
As agents transition into an active operational state (Phase 70.0), it is necessary to measure their performance continuously. In Raphael's architecture, performance reviews are not singular management events; they are continuous data collection processes that periodically crystallize into assessment records. Phase 70.1 builds the engine to collect, score, and surface this data without introducing perverse incentives or noise.

## Decisions

### 1. The Four Measurement Dimensions & Weights
**Decision**: Every agent is evaluated across four specific dimensions using explicit constants. 
**Rationale**: 
- **Productivity (0.35)**: Completion rate, task duration, on-time ratio. (Highest impact).
- **Accuracy (0.30)**: Validated outputs, hypothesis accuracy, recommendations acted on.
- **Reliability (0.25)**: Uptime ratio, safety pressure score trend, transition stability.
- **Cost Efficiency (0.10)**: LLM cost per task vs baseline, local model usage ratio.
*Note: While default weights apply to all agents, the schema supports agent-type overrides (e.g., Research Agents might weigh accuracy over productivity).*

### 2. The Three Cadences
**Decision**: Data is collected continuously but crystallized at three distinct rhythms:
- **Continuous**: Raw metric collection. Feeds Canary Agent and Workforce Health. Never surfaced directly.
- **Weekly**: A performance snapshot. **Suppressed from surfacing** unless the composite score drops > 15 points or rises > 20 points from the previous week.
- **Monthly**: A full performance review. Always surfaces. Produces a persistent `Performance Review Record` in the World Model. 

### 3. Trust Tier Recommendations
**Decision**: Monthly reviews drive Trust Tier modifications, replacing manual tier assignment.
**Rationale**: After a minimum of 3 months of history, if a composite score averages >= 85 and the safety pressure trend is improving, Raphael recommends a promotion. If the score drops < 60 or safety pressure degrades critically, Raphael recommends a demotion. **All trust tier modifications strictly require Aaron's explicit approval.**

### 4. Data Isolation (Constitutional Constraint)
**Decision**: Agent performance data must remain strictly isolated. 
**Rationale**: Performance data about one agent **must not** influence another agent's assignments, evaluations, or behavior. Cross-agent comparisons can inform system-level workforce health analysis, but the system must never rank agents against each other or create competitive dynamics. Each agent is evaluated independently against its own baseline and the defined metrics.

## Consequences
- Requires `performance_reviewer.py` to continuously process logs and calculate scores.
- Requires new nodes (`Performance Review Record`) to be generated in the World Model every month.
- Requires a mandatory human-in-the-loop acknowledgement step (`reviewed_by_aaron: False`) for all monthly reviews.
- Ensures the Trust Tier system (68.5B) is now data-driven rather than manually assigned.
