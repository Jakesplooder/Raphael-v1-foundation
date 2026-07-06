# Archived n8n Workflow WFARCH-6904F16EBC

## Workflow ID

WFARCH-6904F16EBC

## Name

Send daily weather updates via a push notification

## Category

Notifications

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1195_Openweathermap_Pushover_Update_Scheduled.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 3
- Connections: 2
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `n8n-nodes-base.cron`
- `n8n-nodes-base.openWeatherMap`
- `n8n-nodes-base.pushover`

## API and Service Analysis

- Cron
- Open Weather Map
- Pushover

## Required Credentials

- openWeatherMapApi (type only; no credential value stored)
- pushoverApi (type only; no credential value stored)

## Reuse Assessment

- Reusable trigger/transform pattern: Yes
- Category relationship: Notifications
- The workflow exposes a standard node list for structural analysis.
- Review node settings, platform terms, privacy, rate limits, and credential requirements before any manual use.

## Safety

- Source modified: no
- Workflow imported into n8n: no
- Workflow activated: no
- Workflow executed: no
- Credential values stored: no
- External APIs called: no
