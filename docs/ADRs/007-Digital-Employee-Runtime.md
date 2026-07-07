# ADR 007: Digital Employee Runtime (Phase 70.0)

**Date**: 2026-07-06
**Status**: Proposed

## Context
With Pillar I complete, Raphael possesses the cognitive engines required for executive orchestration (planning, optimization, governance). Pillar II shifts focus to the execution layer: the Digital Workforce. Phase 70.0 introduces the core infrastructure—the Agent Lifecycle State Machine—that elevates agents from static configuration entries in the World Model into dynamic, governed operational entities with state, history, and health.

## Decisions

### 1. Operational Identity vs Semantic Identity
**Decision**: An agent's operational identity (state, load, pressure) will be separated from its semantic identity (description, role, connections).
**Rationale**: The World Model defines *what* an agent is (its entity node). The Runtime Registry (`agent_runtime.json`) defines *how* an agent is operating right now. Tying fast-moving operational state directly into the World Model graph causes unnecessary churn; separating them allows the runtime registry to act as a high-speed, authoritative state layer that periodically synchronizes major lifecycle events back to the World Model.

### 2. The Agent Lifecycle State Machine
**Decision**: Agent state transitions are strictly governed by a defined state machine. 
**Rationale**: Ad-hoc state changes lead to unstable orchestration. The valid transitions are locked as follows:
- `created` → `onboarding`
- `onboarding` → `active`, `suspended`
- `active` → `overloaded`, `under_review`, `suspended`
- `overloaded` → `active`, `recovering`, `under_review`
- `recovering` → `active`, `under_review`
- `under_review` → `active`, `suspended`, `retired`
- `suspended` → `under_review`, `retired`
- `retired` → [Terminal]

### 3. Operational Autonomy vs Authority Autonomy (Constitutional Boundaries)
**Decision**: State transitions are bifurcated into operational (autonomous) and authority-required (advisory).
**Rationale**: In alignment with Article IX (Workforce Governance), Raphael may autonomously execute operational transitions (`onboarding`, `active`, `overloaded`, `recovering`) and flag agents `under_review`. However, Raphael may **only recommend** (via the Initiative Queue) transitions that require human authority: `suspended`, `retired`, trust tier changes, and new agent creation.

### 4. The Onboarding Protocol
**Decision**: New agents cannot enter `active` state without completing a structured onboarding checklist.
**Rationale**: An agent cannot be safely trusted without verified capabilities, assigned limits, and a baseline. Onboarding guarantees that the World Model node exists, a trust tier is assigned, rate limits are configured, and crucially, that the **Canary Agent observation period** (7 days) initializes the agent's behavioral baseline before active deployment.

### 5. Cross-System Integration
**Decision**: The runtime will not create new isolated dashboards or output mechanisms. It will consume and produce via the established Pillar I engines.
**Rationale**: 
- The Workforce Health Monitor scans runtime state and feeds the **Initiative Queue (Phase 69.6)**.
- Authority-required transitions (`suspended`, `retired`) are generated as `workforce_lifecycle` queue items with explicit `alternative_interpretations`.
- The runtime consumes signals from the **Agent Workload Balancer (Phase 69.7)** to trigger `overloaded` states.
- It consumes data from the **Canary Agent (Phase 68.5E)** to inform `under_review` flags.
- Lifecycle transitions emit Event nodes to the **World Model (Phase 75.x)**.

## Consequences
- Requires the creation of `agent_runtime.json` as a standalone operational registry.
- Requires building `agent_runtime.py` (Registry, Lifecycle Manager, Onboarding Protocol).
- Requires building `workforce_health.py` (Workforce Health Monitor).
- As an initial validation of the infrastructure, 8 core Tier 1 agents (COO, Chief of Staff, Project Manager, Operations Agent, Resource Manager, Commerce Agent, Developer Agent, Research Agent) will be actively transitioned through Onboarding into the Active state during this phase.
