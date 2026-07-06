# Archived n8n Workflow WFARCH-86E5D6DDF0

## Workflow ID

WFARCH-86E5D6DDF0

## Name

Send daily weather updates via a message in Line

## Category

Automation

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

0065_Openweathermap_Line_Update_Scheduled.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 3
- Connections: 2
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `n8n-nodes-base.cron`
- `n8n-nodes-base.line`
- `n8n-nodes-base.openWeatherMap`

## API and Service Analysis

- Cron
- Line
- Open Weather Map

## Required Credentials

- lineNotifyOAuth2Api (type only; no credential value stored)
- openWeatherMapApi (type only; no credential value stored)

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
