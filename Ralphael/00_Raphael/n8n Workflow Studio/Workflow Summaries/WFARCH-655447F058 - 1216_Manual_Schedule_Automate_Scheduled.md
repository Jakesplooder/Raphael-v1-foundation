# Archived n8n Workflow WFARCH-655447F058

## Workflow ID

WFARCH-655447F058

## Name

1216_Manual_Schedule_Automate_Scheduled

## Category

Automation

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1216_Manual_Schedule_Automate_Scheduled.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 5
- Connections: 4
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `n8n-nodes-base.if`
- `n8n-nodes-base.manualTrigger`
- `n8n-nodes-base.openWeatherMap`
- `n8n-nodes-base.scheduleTrigger`
- `n8n-nodes-base.signl4`

## API and Service Analysis

- If
- Manual Trigger
- Open Weather Map
- Schedule Trigger
- Signl4

## Required Credentials

- openWeatherMapApi (type only; no credential value stored)
- signl4Api (type only; no credential value stored)

## Reuse Assessment

- Reusable trigger/transform pattern: Yes
- Category relationship: Automation
- The workflow exposes a standard node list for structural analysis.
- Review node settings, platform terms, privacy, rate limits, and credential requirements before any manual use.

## Safety

- Source modified: no
- Workflow imported into n8n: no
- Workflow activated: no
- Workflow executed: no
- Credential values stored: no
- External APIs called: no
