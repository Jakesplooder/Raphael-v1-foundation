# Execution Allowlist

| Action Type | Level | Related System | Risk | Expected Writes |
|---|---:|---|---|---|
| refresh_command_center | 2 | Command Center | Low | 00_Raphael/Daily Command Center.md |
| refresh_priority_brief | 2 | Priorities | Low | 00_Raphael/Priority Brief.md |
| refresh_kpi_dashboard | 2 | KPI System | Low | 00_Raphael/KPIs/ |
| refresh_initiative_review | 2 | Executive Initiatives | Low | 00_Raphael/Executive Initiatives/ |
| detect_initiatives | 2 | Executive Initiatives | Low | 00_Raphael/Executive Initiatives/ |
| refresh_employee_registry | 2 | Digital Employees | Low | 03_Agents/Digital Employees/ |
| refresh_council_review | 2 | Council System | Low | 03_Agents/Councils/ |
| refresh_commerce_review | 2 | Commerce Council | Low | 05_Business/Commerce/ |
| refresh_agency_review | 2 | Agency Council | Low | 05_Business/Agency/ |
| refresh_creator_review | 2 | Creator Council | Low | 05_Business/Creator/ |
| run_memory_search | 2 | Qdrant Memory | Low | runtime output only |
| run_vision_analysis | 2 | Vision | Medium | 04_Research/Vision Analysis/ |
| run_simulation | 2 | Simulation Engine | Low | 00_Raphael/Simulations/ |
| detect_opportunities | 2 | Opportunities | Low | 00_Raphael/Opportunities/ |
| generate_builder_files | 1 | Builder Mode | Low | C:/RaphaelOS/builder/workspace |
| apply_builder_output | 4 | Builder Mode | High | approved builder target only |
| run_approved_workflow | 3 | Workflows | Medium | workflow-defined vault notes |
| run_weekly_operations_review | 3 | Workflows | Low | weekly operations generated notes |
| blocked | 5 | Blocked | Blocked | None |

## Blocked Examples

- delete files
- install packages
- run arbitrary shell commands
- send email
- upload products
- create listings
- spend money
- access credentials
- external business platform actions
