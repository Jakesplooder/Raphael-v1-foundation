# ADR 010: Epic B Foundation (Workforce Runtime)

**Date**: 2026-07-06  
**Status**: Accepted  
**Context**: Raphael is transitioning from a modular CLI execution model to a continuously running daemon managed by the Raphael Runtime Kernel (RRK). Epic B introduces the Digital Workforce (Agents). We need a unified pattern for defining, managing, and orchestrating these agents so they integrate seamlessly with the RRK's observability, state management, and eventing systems.

## Decisions

1. **Every Agent Implements `ServiceModule`**
   Agents are not separate loops or standalone processes; they are first-class RRK services that inherit from a `BaseAgent` class implementing the `ServiceModule` contract. The Kernel manages their initialization, lifecycle, and health.

2. **Agent Jobs Carry Kernel Trace IDs**
   All work executed by agents is triggered via the `JobSystem` or `EventBus`. The originating trigger provides a `trace_id` which the agent propagates down through all operations (World Model queries, LLM calls, tool usage).

3. **Agent Health Feeds the Kernel Dashboard**
   The `health()` and `status()` methods on the agent service must return meaningful metrics (pressure score, performance score, queue depth, trust tier). This data will be aggregated and displayed natively on the Kernel Dashboard.

4. **Agent-to-Agent Communication Uses the EventBus Only**
   No direct method calls (`agent_a.send_message(agent_b)`) are permitted. All inter-agent coordination occurs via the `EventBus` (e.g., `MESSAGE_RECEIVED` events). This ensures durability, decoupling, and complete observability.

5. **Agent State is Authoritative in the World Model**
   While agents maintain ephemeral volatile state in memory and emit snapshots to `agent_runtime.json`, the ultimate source of truth for their capabilities, assignments, and structural existence is the Phase 75 World Model graph.

6. **Migration Budget (Specification Debt Paydown)**
   The legacy codebase contains callers that bypass the RRK. To prevent this debt from growing, **one legacy caller must be migrated to the RRK bridge per Epic B phase**.
   - *Phase 70.0*: Migrate `executive_reasoning.py`
   - *Phase 70.1*: Migrate `daily_briefing.py`
   - *Phase 70.2*: Migrate `dashboard_aggregator.py`
   - *Phase 70.3*: Migrate `portfolio_optimizer.py`
   - *Phase 70.4*: Migrate `workforce_health.py`

## Consequences

- **Positive**: Complete observability across all agent actions. The RRK becomes the true heart of Raphael. The legacy CLI architecture is deprecated organically as the migration budget is paid.
- **Negative**: Adds boilerplate when creating new agents, as they must comply with the `ServiceModule` contract. Inter-agent communication is strictly asynchronous, which requires careful event-driven design.
