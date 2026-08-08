# ADR-017: Portfolio Governance Constitution

## Status
Accepted

## Context
In Phase 9 (Multi-Business Simulation Layer), Raphael manages a portfolio of autonomous businesses (Creator, Career, Commerce, Agency). Without central portfolio governance, these businesses would act selfishly, hoarding resources (GPU, memory, execution slots) or continuing to burn capital on failed strategies, leading to sub-optimal ecosystem ROI.

## Decision
We establish the **Portfolio Governance Constitution**:

1. **The Kernel determines Resource Allocation**
   - The OS Kernel acts as the "Portfolio CEO".
   - The Kernel analyzes the `BusinessTwin` of every domain and explicitly determines their GPU budget, agent time, and execution priority.

2. **Merit-Based Capital Distribution**
   - Resource allocation is strictly meritocratic, based on:
     - Historical ROI
     - Strategy Confidence
     - Risk Profile
     - Strategic Importance
   - High-ROI businesses (e.g., Focus Marketing) will receive capital injections (e.g., 50% GPU allocation).
   - Low-performing or experimental businesses (e.g., a new SaaS MVP) will receive conservative budgets until they prove viability.

3. **Domain Sovereignty Limits**
   - Domains may request resources, but they may never self-allocate or bypass the Kernel's budget caps.

## Consequences
- Transforms Raphael from a single-track executor into an AI holding company.
- Allows Raphael to autonomously starve failing experiments and scale winning businesses, maximizing the yield of the entire ecosystem.
