# ADR 004: Portfolio Management (Phase 69.8)

**Date**: 2026-07-06
**Status**: Proposed

## Context
While Resource Optimization (Phase 69.7) managed individual agents and workflows, Raphael requires a macro-level capability to evaluate projects and goals relative to each other. Portfolio Management (Phase 69.8) introduces cross-project dependency tracking, priority optimization, strategic sequencing, and capacity forecasting. 

## Decisions

### 1. Definition of a Portfolio
**Decision**: A portfolio is defined as a structured view of projects grouped by the goals they advance, not a flat list.
**Rationale**: 
```json
{
    "goal": "Goal Node",
    "projects": ["Project nodes that ADVANCE this goal"],
    "dependencies": ["cross-project DEPENDS_ON relationships"],
    "capacity": ["agents and workflows assigned"],
    "status": "derived from constituent projects"
}
```

### 2. Dependency Graph & Sequencing Over Thresholds
**Decision**: Priority optimization will use dependency graph traversal rather than simple threshold checking.
**Rationale**: Phase 69.6 spots isolated signals (e.g., "Goal Y is stalled"). Phase 69.8 spots structural sequencing (e.g., "Completing Project A before Project B reduces completion time by 3 weeks because B depends on A"). The core algorithm relies on computing the **critical path** (the longest dependency chain) through `DEPENDS_ON`, `BLOCKS`, and `ENABLES` edges.

### 3. Capacity Forecasting Format & Confidence Formula
**Decision**: Forecasts must output risk-adjusted estimates accompanied by quantitative confidence scores based on unresolved blocking dependencies. The confidence score uses a strict formula capped at 0.85 to enforce epistemic humility.
**Rationale**: A forecast without confidence is just a guess formatted as a plan. The formula is:
```python
def forecast_confidence(blocking_deps, resolved_deps, pattern_support, agent_avail, hist_accuracy):
    clarity = resolved_deps / max(1, resolved_deps + blocking_deps)
    base = (clarity * 0.40) + (pattern_support * 0.25) + (agent_avail * 0.20) + (hist_accuracy * 0.15)
    return round(max(0.15, min(0.85, base)), 2)
```
The required output format is strictly defined as:
```text
CAPACITY FORECAST
━━━━━━━━━━━━━━━━━
Project: [Name]
Current velocity: [Tasks/Week]
Remaining tasks: [Count]
Estimated completion: [Weeks]

Blocking dependencies:
  - [Dependency 1] (BLOCKS X tasks)
  - [Dependency 2] (ASSIGNED to Y other tasks)

Risk-adjusted estimate: [Range] weeks
Confidence: [Score] ([Reasoning])
```

### 4. Constitutional Constraint: Advisory Priority
**Decision**: Portfolio priority recommendations are advisory only.
**Rationale**: Raphael may identify that some projects should be deprioritized to accelerate higher-value ones. However, the operator (Aaron) may have strategic or personal context not reflected in the World Model. 
Raphael may **not**:
- Change a project's status in the World Model autonomously.
- Reassign agents away from a project autonomously.
- Mark a project as paused or cancelled autonomously.

Every priority recommendation must acknowledge that personal context may override analytical priority, mapping to an explicitly defined `ALTERNATIVE_INTERPRETATION`.

### 5. Sequencing Recommendations and the Pareto Filter
**Decision**: Portfolio sequencing recommendations will be filtered to only surface optimizations that yield meaningful time savings.
**Rationale**: To prevent overwhelming the Initiative Queue with trivial optimizations (e.g., saving 2 days), a Pareto filter evaluates sequencing changes. The threshold is set at a minimum improvement of 1.5 weeks. Only recommendations exceeding this threshold will be passed to the queue, limited to the top 3 optimizations.

## Consequences
- Requires `dependency_analyzer.py` for graph traversal.
- Requires `portfolio_optimizer.py` to feed sequencing recommendations to the Initiative Queue.
- Requires `capacity_forecaster.py` to generate the strict Capacity Forecast output.
- Defers portfolio visualization and cross-portfolio reporting to Phase 69.9 (Dashboard).
