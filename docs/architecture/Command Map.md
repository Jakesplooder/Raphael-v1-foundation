# Command Map

```text
python raphael.py <command>
        |
        v
raphael_core.cli.main()
        |
        v
raphael_core.legacy.main()
        |
        v
domain implementation
```

| Domain | Commands |
|---|---|
| Briefs | `executive-brief`, `morning-brief`, `weekly-brief` |
| Daily operating loop | `daily-start`, `daily-focus`, `daily-plan`, `daily-checkin`, `daily-end`, `daily-review` |
| Bootstrap | `bootstrap-*` |
| Command center | `command-center`, `prioritize` |
| Deliberations | `deliberate`, `deliberation-*` |
| Execution plans | `execution-plan*` |
| Builder | `build-*`, `builder-governance-review` |
| POD Studio | `pod-*` |
| POD Typography | `pod-typography-*`, `pod-compose-design`, `pod-svg-export`, `pod-print-export` |
| n8n Studio | `n8n-*` |
| Asset library | `asset-*`, `brand-*` |
| Knowledge | `knowledge-*` |
| Communications | `communication-*` |
| Notifications | `notification-*` |
| Activity | `activity-*` |
| Finance | `finance-*` |
| Portfolio | `portfolio-*` |
| Maintenance | `system-check`, `repair`, `backup`, route/dependency checks |

`python raphael.py test` is handled directly by `raphael_core.cli`.
