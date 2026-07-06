# Execution Policy

## Levels

- Level 0: Advisory only.
- Level 1: Generated artifacts.
- Level 2: Internal Raphael functions.
- Level 3: Approved workflows.
- Level 4: Approved builder apply.
- Level 5: External actions, blocked in this phase.

## Required Gates

- Execution request required.
- Approval required before execution.
- Dry run recommended before approval.
- Only allowlisted action types can execute.
