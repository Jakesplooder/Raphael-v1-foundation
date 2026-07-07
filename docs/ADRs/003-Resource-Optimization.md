# ADR 003: Resource Optimization (Phase 69.7)

**Date**: 2026-07-06
**Status**: Proposed

## Context
As Raphael manages a digital workforce and executes complex workflows, resources (compute, LLM API costs, agent capacity, and the operator's time) become constrained. To operate efficiently, Raphael must analyze resource utilization and surface optimization recommendations.

However, unchecked optimization creates significant constitutional risks (e.g., unauthorized reallocations overriding human intent) and instability (e.g., thrashing assignments back and forth).

## Decisions

### 1. Scope Definition
**Decision**: Phase 69.7 is strictly scoped to the following resources:
- **Agent Workload Balancing**: Identifying active, idle, or overloaded agents.
- **LLM Cost Optimization**: Recommending shifts from expensive API calls (Claude/Gemini) to local inference (Ollama) based on task accuracy data.
- **Workflow Queue Management**: Identifying bottlenecks and execution delays.

**Deferred**: Operator time optimization and hardware compute profiling are deferred (to be handled in 73.x Personal OS and dedicated monitoring infrastructure, respectively).

### 2. Constitutional Constraint: Recommendations, Not Reallocations
**Decision**: Resource optimization produces recommendations, *never* reallocations. 
**Rationale**: Reallocation of resources bypasses the Authority Autonomy boundaries (68.5A). The optimizer must strictly feed its findings into the Phase 69.6 Initiative Queue as `Detected` items. Execution requires explicit operator approval.

**Amendment: LLM Routing Constraint**
LLM routing decisions are Authority Autonomy actions.
The cost optimizer may recommend routing changes. It may not implement routing changes. Routing changes require explicit approval and flow through the Approval Policy Engine.
Exception: Aaron may pre-approve specific routing rules (e.g., "always use Ollama for summarization tasks") which become registered routing policies, not optimizer-driven changes.

### 3. How does the optimizer avoid thrashing?
**Decision**: Implement a stability threshold. 
**Rationale**: Shifting agent loads based on transient spikes causes organizational thrashing. An agent rebalancing recommendation will only trigger when the load imbalance exceeds 40% between agents for more than 3 consecutive days. Temporary spikes that resolve naturally will not surface as recommendations.

### 4. How does LLM cost data get collected without privacy risk?
**Decision**: Implement strict payload redaction for cost logging.
**Rationale**: To prevent sensitive task content from persisting unnecessarily in cost ledgers, the LLM Cost Optimizer will log only the following metadata:
- Task Type
- Provider Used
- Tokens Consumed
- Accuracy Outcome (from 69.5)
The prompt and response content will never be logged in the cost ledger.

### 5. What's the optimization cadence?
**Decision**: Bifurcate acute vs. trend recommendations.
**Rationale**: 
- **Acute problems** (e.g., an agent is critically overloaded *today*, or a workflow queue is spiked at 11 bottlenecks) are surfaced in the **Daily Briefing**.
- **Trend-based optimizations** (e.g., LLM costs trending upward over a 30-day period, or a gradual drop in Ollama performance vs Claude) are routed to a **Weekly Executive Summary**. Trend data in a daily briefing creates noise; acute data in a weekly summary creates unacceptable latency.

## Consequences
- Requires new engines: `agent_workload_balancer.py`, `llm_cost_optimizer.py`, `workflow_queue_manager.py`.
- Integrates cleanly into the Phase 69.6 `initiative_queue.py`.
- Expands the Executive Briefing architecture to support a distinct `generate-weekly-summary` command.
