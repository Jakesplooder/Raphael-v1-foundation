# Authority Model

## Trust Tiers
- **Sandbox**: Local simulation, planning, formatting, reasoning. Fully autonomous.
- **Read-Only**: Access to World Model and pattern retrieval. Fully autonomous.
- **Execute**: Requires explicit human consent to execute bash commands, spend funds, or commit code outside of the builder environment.

## Override Protocol
Raphael may propose a deviation from standard authority logic, but the Authority Validator (a deterministic rules engine) strictly governs whether that proposal is immediately blocked or routed to a human for approval.
