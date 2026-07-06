# Archived n8n Workflow WFARCH-0581C89188

## Workflow ID

WFARCH-0581C89188

## Name

Send daily weather updates via a push notification using the Pushcut node

## Category

Notifications

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1156_Openweathermap_Cron_Update_Scheduled.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 3
- Connections: 2
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `n8n-nodes-base.cron`
- `n8n-nodes-base.openWeatherMap`
- `n8n-nodes-base.pushcut`

## API and Service Analysis

- Cron
- Open Weather Map
- Pushcut

## Required Credentials

- openWeatherMapApi (type only; no credential value stored)
- pushcutApi (type only; no credential value stored)

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
