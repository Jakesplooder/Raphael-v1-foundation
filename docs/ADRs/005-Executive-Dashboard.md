# ADR 005: Executive Dashboard (Phase 69.9)

**Date**: 2026-07-06
**Status**: Proposed

## Context
Across Pillar I, Raphael has gained the ability to govern, reason, plan, predict, self-correct, detect initiatives, optimize resources, and manage a portfolio. However, each capability currently outputs its data via distinct CLI commands. Phase 69.9 introduces the Executive Dashboard: the unified, curated interface that surfaces exactly what the operator needs to know *right now*, transitioning Raphael from a collection of scripts to a cohesive Executive OS.

## Decisions

### 1. Interface Paradigm: Terminal
**Decision**: The dashboard will be a Terminal interface (leveraging libraries like `rich` or `textual`), not a Web UI.
**Rationale**: A terminal interface requires no background server, introduces no browser dependencies, works seamlessly over SSH, and is perfectly consistent with our existing CLI architecture. A Web UI is deferred until Raphael develops a mature, generic API layer.

### 2. State Strategy: Static (Pull) vs Live (Push)
**Decision**: The dashboard will be a static, pull-based interface triggered on command execution, rather than a live-updating threaded interface.
**Rationale**: Live-updating requires background threads that violate our current synchronous architectural patterns. The dashboard is a "pull" interface (`python raphael.py dashboard`) that complements the "push" interface of the Daily Briefing. 

### 3. Drill-Down Strategy: Command Referencing
**Decision**: The dashboard surfaces summaries, not raw data. Drill-downs are facilitated by referencing existing CLI commands.
**Rationale**: 
- `[Press 1 for initiative detail: python raphael.py initiative-status]`
- `[Press W for weekly summary: python raphael.py generate-weekly-summary]`
- `[Press F for forecast: python raphael.py capacity-forecast PROJECT-ID]`
This prevents the dashboard from becoming overly complex or duplicating existing detail views.

### 4. Constitutional and Operational Boundaries
**Decision**: The dashboard must strictly adhere to three boundaries:
1. **It must not produce new data**: The dashboard strictly reads from existing outputs (World Model, Initiative Queue, Learning Metrics). If the dashboard goes offline, no core functionality breaks.
2. **It must not replace the Daily Briefing**: The briefing is Raphael pushing what it decides you must see. The dashboard is Aaron pulling everything available to see.
3. **It must not require internet access**: The dashboard must render entirely from local data, upholding Raphael's local-first constitutional principle.

### 5. Degraded State Policy & Staleness Penalties
**Decision**: The dashboard must render gracefully if any underlying data source (e.g., the World Model, the Initiative Queue, or the Ledger) is missing, corrupted, or stale.
**Rationale**: Raphael's components will not always be in perfect sync. If `initiative_queue.json` is missing, the dashboard must display "Unavailable" rather than crashing. Furthermore, stale data (files that exist but haven't updated in an expected timeframe) is explicitly handled via `STALENESS_THRESHOLDS`:
- `initiative_queue.json`: 25 hours
- `llm_ledger.json`: 72 hours
- `world_model_cache.json`: 48 hours
- `learning_metrics.json`: 25 hours

If data is stale, the dashboard renders a `⚠ Data stale` warning.

**Health Score Penalty**: The system health calculator applies a penalty based on staleness before calculating the final weighted score:
- **Current**: 100% of component score
- **Stale**: 85% of component score (15% penalty)
- **Missing/Error**: 50% of component score (50% penalty)

## Structure

The dashboard layout is locked to a three-panel structure:

**Panel 1: Executive Status**
- Raphael OS Health Score, Date, OS Version
- Today's Focus (Top items from Initiative Queue)
- Alerts (Critical risks and Constitutional compliance)

**Panel 2: Operational Metrics**
- World Model stats (Nodes/Rels)
- Learning metrics (Accuracy trend)
- LLM Spend and optimization
- Agent load and Workflow blocks

**Panel 3: Portfolio View**
- Active Projects (Status and Phase)
- Critical Path Blockers (from 69.8)
