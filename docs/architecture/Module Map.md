# Raphael Core Module Map

`raphael.py` is the compatibility CLI entrypoint and delegates to
`raphael_core.cli`.

## Core Infrastructure

| Module | Responsibility |
|---|---|
| `raphael_core.config` | Settings, `RaphaelConfig`, validation |
| `raphael_core.paths` | Stable vault/runtime path helpers |
| `raphael_core.markdown` | Exact Markdown parsing and updates |
| `raphael_core.safety` | Approved roots, safe reads/writes, confirmations |
| `raphael_core.ids` | Stable record IDs |
| `raphael_core.logging_utils` | Local file and diagnostic helpers |
| `raphael_core.registry` | Agents, councils, modes, statuses |
| `raphael_core.cli` | CLI dispatch and test command |
| `raphael_core.daily` | Phase 65 advisory daily planning, check-ins, and reviews |
| `raphael_core.typography` | POD editable typography, Inkscape composition, SVG, and print exports |
| `raphael_core.bootstrap` | Safe local service startup, PID ownership, health, and recovery |

Domain modules provide stable import surfaces for tasks, goals, agents,
councils, command center, memory, knowledge, relationships, communications,
deliberations, goal propagation, execution plans, notifications, activity,
briefs, daily operating loop, finance, portfolio, Builder, POD Studio, n8n Studio, assets, and
maintenance.

`raphael_core.legacy` is the behavior-preserving compatibility kernel extracted
from the former monolithic entrypoint. Future work can move one tested domain
at a time without changing CLI, dashboard, Command Bus, or voice contracts.
