# Archived n8n Workflow WFARCH-467597D7E4

## Workflow ID

WFARCH-467597D7E4

## Name

n8n Community Topic Tracker by Keyword

## Category

Notifications

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1625_Splitout_Schedule_Monitor_Webhook.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 10
- Connections: 5
- Source marked active: True (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `n8n-nodes-base.emailSend`
- `n8n-nodes-base.googleSheets`
- `n8n-nodes-base.googleSheetsTrigger`
- `n8n-nodes-base.httpRequest`
- `n8n-nodes-base.scheduleTrigger`
- `n8n-nodes-base.slack`
- `n8n-nodes-base.splitOut`
- `n8n-nodes-base.stickyNote`

## API and Service Analysis

- Email Send
- Google Sheets
- Google Sheets Trigger
- Http Request
- Schedule Trigger
- Slack
- Split Out
- Sticky Note

## Required Credentials

- googleSheetsOAuth2Api (type only; no credential value stored)
- googleSheetsTriggerOAuth2Api (type only; no credential value stored)
- smtp (type only; no credential value stored)

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
