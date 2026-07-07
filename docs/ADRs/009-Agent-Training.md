# ADR 009: Agent Training Architecture (Phase 70.2)

**Date**: 2026-07-06
**Status**: Proposed

## Context
With Phase 70.1 providing continuous, data-driven performance reviews, we now have the capability to identify *when* an agent is underperforming or requires optimization. Phase 70.2 (Agent Training) answers *how* we fix it. In Raphael's context, "training" does not mean finetuning a neural network. It means governed, evidence-based optimization of the agent's operational parameters.

## Decisions

### 1. The Four Training Levers
**Decision**: Raphael will optimize agents using exactly four explicit levers.
**Rationale**: These are the only variables that materially affect LLM agent performance in this architecture:
1. **Prompt Improvement**: Refining the agent's core identity, instructions, and constraints.
2. **Retrieval Tuning**: Calibrating context window limits, embedding similarity thresholds, or search parameters.
3. **Tool Access Calibration**: Granting new tools or revoking misused tools.
4. **Model Routing Optimization**: Upgrading/downgrading the default model assigned to the agent (e.g., from `claude-3-haiku` to `claude-3-opus`).

### 2. Evidence-Based A/B Testing
**Decision**: Training modifications must be hypothesis-driven and tested.
**Rationale**: Raphael cannot simply overwrite an agent's prompt based on a whim. Training initiatives must be proposed as an A/B test or formal hypothesis (e.g., "If we add Tool X, Productivity will increase by 15%"). The system must track the baseline vs. the proposed change. 

### 3. Training Record Nodes
**Decision**: Every training initiative produces a persistent `Training Record` node in the World Model.
**Rationale**: This creates an audit trail of how an agent's behavior has been sculpted over time. It links the `Agent` node to the `Hypothesis` node and the specific performance data that triggered the training.

### 4. Constitutional Boundary: Mandatory Human Approval
**Decision**: Raphael may *propose* training modifications autonomously, but every training activation strictly requires Aaron's approval.
**Rationale**: Modifying an agent's tools or core prompt fundamentally alters its operational capability and safety profile. Raphael must never autonomously modify an agent's baseline configuration. Aaron must run an explicit `activate` command to deploy the training to production.

## Consequences
- Requires `agent_trainer.py` to structure training proposals and track A/B test hypotheses.
- Requires new `Training Record` nodes in the World Model.
- Requires CLI commands to propose, review, and activate training.
- Further operationalizes the Performance Review Engine by turning its outputs (performance gaps) into direct inputs for the Training Engine.
