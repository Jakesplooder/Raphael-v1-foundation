# Archived n8n Workflow WFARCH-FE48CB0EC7

## Workflow ID

WFARCH-FE48CB0EC7

## Name

WhatsApp business bot

## Category

Automation

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1572_Wait_Schedule_Automate_Scheduled.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 15
- Connections: 10
- Source marked active: True (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `n8n-nodes-base.filter`
- `n8n-nodes-base.googleSheets`
- `n8n-nodes-base.googleSheetsTrigger`
- `n8n-nodes-base.if`
- `n8n-nodes-base.scheduleTrigger`
- `n8n-nodes-base.splitInBatches`
- `n8n-nodes-base.stickyNote`
- `n8n-nodes-base.wait`
- `n8n-nodes-base.whatsApp`
- `n8n-nodes-base.whatsAppTrigger`

## API and Service Analysis

- Filter
- Google Sheets
- Google Sheets Trigger
- If
- Schedule Trigger
- Split In Batches
- Sticky Note
- Wait
- Whats App
- Whats App Trigger

## Required Credentials

- googleSheetsOAuth2Api (type only; no credential value stored)
- googleSheetsTriggerOAuth2Api (type only; no credential value stored)
- whatsAppApi (type only; no credential value stored)
- whatsAppTriggerApi (type only; no credential value stored)

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
