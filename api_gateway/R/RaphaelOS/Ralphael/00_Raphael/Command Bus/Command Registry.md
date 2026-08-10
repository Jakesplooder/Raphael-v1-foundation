# Command Registry

| Command Type | Example CLI | Example Phrase | Safety Level | Confirmation Required |
|---|---|---|---|---|
| identity | `identity-status` | who are you | Level 0 | No |
| world | `world-review` | review the world model | Level 1 generated note | No |
| simulation | `simulate` | simulate Etsy store versus Agency | Level 0 advisory | No |
| opportunity | `detect-opportunities` | detect opportunities | Level 1 generated note | No |
| resource_allocation | `allocation-plan` | what should I work on this week | Level 1 generated note | No |
| blueprint | `blueprint-business` | create a blueprint for a Shopify agency | Level 1 generated note | No |
| commerce | `commerce-product-idea` | create product idea Bible verse shirt | Level 1 generated note | No |
| agency | `agency-service-offer` | create service offer Shopify Integration | Level 1 generated note | No |
| creator | `creator-content-plan` | create content plan AI automation | Level 1 generated note | No |
| kpi | `kpi-dashboard` | show KPI dashboard | Level 1 generated note | No |
| kpi | `kpi-update` | update KPI KPI-ID to 5 | Level 1 write | Yes |
| initiative | `initiative-detect` | detect initiatives | Level 1 generated note | No |
| employee | `employee-registry` | show employee registry | Level 1 generated note | No |
| execution | `execution-request` | run initiative detection | Level 2 request | Yes |
| execution_planning | `execution-plan` | create execution plan for Agency | Level 1 generated plan | No |
| execution_planning | `execution-plan-from-deliberation` | create plan from deliberation DELIB-ID | Level 1 generated plan | No |
| execution_planning | `execution-plan-history` | show execution plans | Level 0 read | No |
| execution_planning | `execution-plan-brief` | execution plan brief | Level 1 generated report | No |
| n8n_workflow_studio | `n8n-status` | show workflow studio | Level 0 read | No |
| n8n_workflow_studio | `n8n-workflow-generate` | generate workflow for POD exports | Level 1 inactive JSON draft | No |
| n8n_workflow_studio | `n8n-workflow-review` | review workflows | Level 1 generated report | No |
| n8n_workflow_studio | `n8n-workflow-graph` | show workflow graph | Level 0 read | No |
| n8n_workflow_studio | `n8n-workflow-catalog` | show workflow catalog | Level 1 generated catalog | No |
| n8n_workflow_studio | `workflow-archive-show` | what can you do with WFARCH-ID | Level 0 archived workflow details | No |
| n8n_workflow_studio | `workflow-archive-search` | search workflow archive Youtube_Automation | Level 0 archived workflow search | No |
| n8n_workflow_studio | `workflow-archive-summary` | summarize workflow archive WFARCH-ID | Level 0 archived workflow summary | No |
| pod_design_studio | `pod-status` | pod status | Level 0 read | No |
| pod_design_studio | `pod-tool-status` | pod tool status | Level 1 local tool report | Yes |
| pod_design_studio | `pod-comfyui-test` | test pod comfyui | Level 0 local diagnostic | No |
| pod_design_studio | `pod-generation-log` | show pod generation log PODGEN-ID | Level 0 local read | No |
| pod_design_studio | `pod-typography-create` | create typography LAND OF THE FREE | Level 1 local SVG | Yes |
| pod_design_studio | `pod-compose-design` | compose POD design IMAGE-PATH PODTYPE-ID | Level 2 local Inkscape composition | Yes |
| pod_design_studio | `pod-svg-export` | export SVG PODCOMP-ID | Level 2 local Inkscape export | Yes |
| pod_design_studio | `pod-print-export` | export print-ready design PODCOMP-ID | Level 2 local Inkscape export | Yes |
| pod_design_studio | `pod-workflow` | start a POD Studio workflow for a vintage camping shirt | Persistent local workflow start | No |
| pod_design_studio | `pod-workflow-status` | show POD workflows | Level 0 local read | No |
| pod_design_studio | `pod-workflow-continue` | continue PODFLOW-ID | Confirmed next local workflow stage | Yes |
| pod_design_studio | `pod-workflow-show` | show PODFLOW-ID | Level 0 local read | No |
| pod_design_studio | `pod-workflow-cancel` | cancel PODFLOW-ID | Confirmed local workflow cancellation | Yes |
| pod_design_studio | `pod-typography-review` | typography review | Level 1 generated review | No |
| pod_design_studio | `pod-typography-status` | typography status | Level 0 local read | No |
| pod_design_studio | `pod-concept` | create pod concept Christian mountain cross shirt | Level 1 generated note | Yes |
| pod_design_studio | `pod-prompt` | generate pod prompt PODCON-ID | Level 1 generated note | Yes |
| pod_design_studio | `pod-generation-request` | create pod generation request PODCON-ID sdxl | Level 1 pending request | Yes |
| pod_design_studio | `pod-generate` | generate pod design PODGEN-ID | Level 2 local tool preparation | Yes |
| pod_design_studio | `pod-review-design` | review pod design image path | Level 1 local vision review | Yes |
| pod_design_studio | `pod-review-batch` | review pod batch folder path | Level 1 local vision review | Yes |
| pod_design_studio | `pod-listing-draft` | create pod listing draft PODCON-ID | Level 1 generated draft | Yes |
| pod_design_studio | `pod-export-package` | export pod package PODCON-ID | Level 2 local export | Yes |
| pod_design_studio | `pod-pipeline` | show pod pipeline | Level 1 generated report | Yes |
| asset_brand_library | `asset-status` | show asset library | Level 0 read | No |
| asset_brand_library | `brand-create` | create brand Local Launch | Level 1 local brand metadata | Yes |
| asset_brand_library | `brand-review` | review brand | Level 1 generated review | Yes |
| asset_brand_library | `brand-brief` | show brand library | Level 1 generated brief | Yes |
| asset_brand_library | `asset-import` | import asset C:\path\design.png | Level 2 local metadata import | Yes |
| asset_brand_library | `asset-review` | review asset ASSET-ID | Level 1 local review | Yes |
| asset_brand_library | `asset-search` | search assets vintage outdoors | Level 0 local search | No |
| asset_brand_library | `asset-related` | find related assets ASSET-ID | Level 0 relationship query | No |
| asset_brand_library | `asset-tag` | tag asset ASSET-ID | Level 1 metadata write | Yes |
| asset_brand_library | `asset-export` | export asset ASSET-ID | Level 2 local export | Yes |
| asset_brand_library | `prompt-library` | show prompt library | Level 1 generated registry | Yes |
| asset_brand_library | `template-library` | show templates | Level 1 generated registry | Yes |
| asset_brand_library | `design-system-review` | review design systems | Level 1 generated registry | Yes |
| finance | `finance-summary` | show financial summary | Level 1 generated note | No |
| finance | `finance-add-revenue` | add revenue Agency 500 Shopify setup | Level 1 write | Yes |
| portfolio | `portfolio-prioritize` | which business should I focus on | Level 0 advisory | No |
| portfolio | `portfolio-delegate` | delegate PORTREC-AGENCY to Agency Council | Level 1 delegation | Yes |
| notification | `notification-list` | show notifications | Level 0 advisory | No |
| notification | `notification-detect` | detect notifications | Level 1 generated note | No |
| notification | `notification-escalate` | escalate notification NOTIF-ID | Level 1 delegation | Yes |
| brief | `morning-brief` | give me a morning brief | Level 1 generated note | No |
| brief | `executive-brief` | executive brief | Level 1 generated note | No |
| brief | `weekly-brief` | weekly brief | Level 1 generated note | No |
| brief | `monthly-review` | monthly review | Level 1 generated note | No |
| brief | `evening-review` | evening review | Level 1 generated note | No |
| daily | `daily-start` | start my day | Level 1 generated daily note | No |
| daily | `daily-focus` | what should I focus on | Level 1 generated daily note | No |
| daily | `daily-plan` | plan my day | Level 1 generated daily note | No |
| daily | `daily-checkin` | check in what changed | Level 1 generated daily note | No |
| daily | `daily-end` | end my day | Level 1 generated daily note | No |
| daily | `daily-review` | review my daily loop | Level 1 generated daily note | No |
| maintenance | `bootstrap-status` | Raphael service status | Level 0 local read | No |
| maintenance | `bootstrap-start` | start Raphael services | Allowlisted local service start | No |
| maintenance | `bootstrap-stop` | stop Raphael services | Managed service stop | Yes |
| maintenance | `bootstrap-restart` | restart Raphael services | Managed service restart | Yes |
| maintenance | `bootstrap-health` | run bootstrap health | Level 1 local diagnostic | No |
| maintenance | `bootstrap-review` | review bootstrap | Level 1 generated review | No |
| maintenance | `bootstrap-install-startup` | install Raphael startup | Windows user startup registration | Yes |
| maintenance | `bootstrap-remove-startup` | remove Raphael startup | Windows user startup removal | Yes |
| maintenance | `bootstrap-open-dashboard` | open dashboard | Local browser navigation | No |
| maintenance | `service-list` | list services | Level 0 local read | No |
| maintenance | `service-start` | start ComfyUI | Confirmed allowlisted local service start | Yes |
| maintenance | `service-start` | start creative stack | Confirmed allowlisted local stack start | Yes |
| maintenance | `service-restart-failed` | restart failed services | Managed PID recovery | Yes |
| maintenance | `self-healing-status` | check system health | Level 0 local self-health read | No |
| maintenance | `observe-system` | Raphael check yourself | Level 1 local observability notes | No |
| maintenance | `detect-issues` | detect issues | Level 1 local issue detection | No |
| maintenance | `diagnose-issue` | diagnose issue ISSUE-ID | Level 0 local diagnosis | No |
| maintenance | `repair-plan` | repair issue ISSUE-ID | Approval-gated allowlisted repair plan | Yes |
| maintenance | `repair-approve` | approve repair REPAIR-ID | Repair approval state change | Yes |
| maintenance | `repair-run` | repair approved issue REPAIR-ID | Approved allowlisted repair execution | Yes |
| maintenance | `reliability-brief` | show reliability brief | Level 1 generated reliability brief | No |
| activity | `activity-feed` | show activity | Level 1 generated note | No |
| activity | `activity-brief` | activity brief | Level 1 generated note | No |
| activity | `activity-review` | activity review | Level 1 generated note | No |
| activity | `activity-stats` | activity stats | Level 1 generated note | No |
| activity | `activity-timeline` | show timeline | Level 1 generated note | No |
| builder | `build-request` | build a Python app | Level 1 generated request | Yes |
| builder | `build-classify` | classify this build dashboard app | Level 1 governance record | Yes |
| builder | `build-with-council` | build me a SaaS app | Governance-routed build | Yes |
| builder | `build-council-plan` | create council plan for BUILD-ID | Council planning records | Yes |
| builder | `build-task-link` | link build task BUILD-ID | Level 1 task lifecycle write | Yes |
| builder | `build-task-review` | review builder tasks | Level 0 lifecycle review | No |
| builder | `build-complete` | mark build BUILD-ID ready for review | Level 1 task status write | Yes |
| builder | `builder-governance-review` | show builder governance review | Level 1 generated review | No |
| council | `list-councils` | list councils | Level 0 advisory | No |
| memory | `memory-search` | memory search portfolio review | Level 0 read | No |
| knowledge | `knowledge-scan` | scan knowledge folder K:\School | Level 0 read | No |
| knowledge | `knowledge-import` | import knowledge folder K:\School | Level 1 generated notes | Yes |
| knowledge | `knowledge-search` | search knowledge compiler project | Level 0 read | No |
| knowledge | `knowledge-classify` | classify knowledge | Level 1 generated metadata | Yes |
| knowledge | `knowledge-skills-map` | show knowledge skills map | Level 1 generated report | No |
| knowledge | `knowledge-portfolio-candidates` | show portfolio candidates | Level 1 generated report | No |
| knowledge | `knowledge-ignore` | ignore knowledge item KNOW-0123456789 | Level 1 vault-only write | Yes |
| knowledge | `knowledge-set-course` | set course for KNOW-0123456789 to CSC4103 | Level 1 vault-only write | Yes |
| knowledge | `knowledge-graph` | show knowledge graph | Level 1 generated report | No |
| knowledge | `knowledge-relationships` | show project relationships | Level 1 generated metadata | Yes |
| knowledge | `knowledge-clusters` | show related projects | Level 1 generated report | No |
| knowledge | `knowledge-career-map` | show career map | Level 1 generated report | No |
| knowledge | `knowledge-business-map` | show business map | Level 1 generated report | No |
| knowledge | `knowledge-portfolio-map` | show portfolio map | Level 1 generated report | No |
| knowledge | `knowledge-tech-map` | show technology map | Level 1 generated report | No |
| knowledge | `knowledge-skill-map` | show skills map | Level 1 generated report | No |
| knowledge | `knowledge-related` | show related projects for KNOW-0123456789 | Level 0 read | No |
| knowledge | `knowledge-path` | knowledge path KNOW-0123456789 KNOW-ABCDEF1234 | Level 0 read | No |
| communication | `communication-request` | request council review | Level 1 internal advisory record | No |
| communication | `communication-request` | request financial assessment | Level 1 internal advisory record | No |
| communication | `communication-request` | request portfolio assessment | Level 1 internal advisory record | No |
| communication | `communication-network` | show communications | Level 1 generated report | No |
| communication | `communication-brief` | show recommendations | Level 1 generated report | No |
| communication | `communication-brief` | show executive synthesis | Level 1 generated report | No |
| communication | `communication-synthesize` | synthesize recommendations | Level 1 internal advisory record | No |
| goal_propagation | `propagate-goal` | propagate goal earn first 1000 online | Level 1 generated plan | No |
| goal_propagation | `goal-cascade` | show goal cascade GOAL-ID | Level 0 read/generated plan | No |
| goal_propagation | `goal-objectives` | show goal objectives GOAL-ID | Level 0 advisory | No |
| goal_propagation | `goal-kpi-map` | show goal KPI map GOAL-ID | Level 0 advisory | No |
| goal_propagation | `goal-initiative-map` | show goal initiative map GOAL-ID | Level 0 advisory | No |
| goal_propagation | `goal-propagation-review` | review goal propagation | Level 1 generated report | No |
| goal_propagation | `goal-propagation-brief` | show goal propagation brief | Level 1 generated report | No |
| deliberation | `deliberate` | deliberate should I focus on Agency or Commerce | Level 1 generated recommendation | No |
| deliberation | `deliberation-status` | show deliberation status | Level 0 advisory | No |
| deliberation | `deliberation-history` | show deliberation history | Level 0 read | No |
| deliberation | `deliberation-show` | show latest deliberation | Level 0 read | No |
| deliberation | `deliberation-review` | review deliberations | Level 1 generated report | No |
| deliberation | `deliberation-brief` | show deliberation brief | Level 1 generated report | No |
| vision | `vision-request` | analyze this screenshot | Level 1 request | Yes |
| search | `search-request` | what happened yesterday | Level 1 request | Yes |
| search | `internet-status` | internet access status | Level 0 local read | No |
| search | `internet-request` | create internet request for Etsy trends | Local pending request | No |
| search | `internet-search` | search the web for current Etsy trends | Confirmed public browser search | Yes |
| search | `internet-review` | review internet requests | Local generated review | No |
| search | `internet-brief` | internet brief | Local evidence summary | No |
| search | `internet-source-review` | review internet source URL | Confirmed single public URL review | Yes |
| search | `internet-latest-overview` | what did it find | Latest source-backed AI Overview | No |
| search | `internet-latest-snippets` | show snippets | Latest saved source snippets | No |
| search | `internet-raw-json` | raw JSON | Explicit raw saved result view | No |
| search | `internet-save-to-knowledge` | save to knowledge | Confirmed local knowledge note | Yes |
| task | `task-status` | task status TASK-ID Done | Level 1 write | Yes |
| goal | `prioritize` | what should I prioritize today | Level 1 generated note | No |
| workflow | `workflow-request` | request portfolio review for Secure Email Service | Level 1 request | Yes |
