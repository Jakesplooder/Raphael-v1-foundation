# ADR-014: Multi-Business Resource Sovereignty

## Status
Accepted

## Context
As Raphael transitions into a Multi-Business Operator (Phase 9), it will manage a portfolio of distinct business domains (e.g., Creator, Commerce, Agency). A naive implementation would allow each business to demand resources (GPU, LLM tokens, execution slots) arbitrarily, leading to resource starvation or inefficient capital burn. 

## Decision
We establish **Multi-Business Resource Sovereignty**:
- **Businesses own goals.** (e.g., "Grow YouTube channel by 10%")
- **The Kernel owns resources.** (e.g., GPU budget, API limits, Memory priority, Execution slots).

A business may *request* resources based on its operational needs, but it cannot *demand* them. The Raphael Kernel acting as the **Portfolio Manager** will allocate resources dynamically across the portfolio based on:
- Expected ROI
- Strategic importance
- Operational risk
- Strategy Confidence
- Growth potential

## Consequences
- Every domain must pass through a central resource allocation gate before executing missions.
- The Business Twin tracks its own performance, and this intelligence is queried by the Portfolio Manager to rebalance the budget.
- We maximize the aggregate ROI of the entire Raphael portfolio by starving failing businesses and feeding winning businesses.
