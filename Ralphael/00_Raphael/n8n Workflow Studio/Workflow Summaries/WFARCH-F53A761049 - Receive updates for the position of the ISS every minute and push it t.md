# Archived n8n Workflow WFARCH-F53A761049

## Workflow ID

WFARCH-F53A761049

## Name

Receive updates for the position of the ISS every minute and push it to a database

## Category

Automation

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

0136_HTTP_Googlefirebaserealtimedatabase_Update_Webhook.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 4
- Connections: 3
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `n8n-nodes-base.cron`
- `n8n-nodes-base.googleFirebaseRealtimeDatabase`
- `n8n-nodes-base.httpRequest`
- `n8n-nodes-base.set`

## API and Service Analysis

- Cron
- Google Firebase Realtime Database
- Http Request
- Set

## Required Credentials

- googleFirebaseRealtimeDatabaseOAuth2Api (type only; no credential value stored)

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
