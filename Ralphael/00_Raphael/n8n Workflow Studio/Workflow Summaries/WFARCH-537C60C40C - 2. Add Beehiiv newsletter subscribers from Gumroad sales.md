# Archived n8n Workflow WFARCH-537C60C40C

## Workflow ID

WFARCH-537C60C40C

## Name

2. Add Beehiiv newsletter subscribers from Gumroad sales

## Category

Notifications

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1741_Telegram_Gumroad_Create_Webhook.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 10
- Connections: 5
- Source marked active: True (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `n8n-nodes-base.googleSheets`
- `n8n-nodes-base.gumroadTrigger`
- `n8n-nodes-base.httpRequest`
- `n8n-nodes-base.set`
- `n8n-nodes-base.stickyNote`
- `n8n-nodes-base.telegram`

## API and Service Analysis

- Google Sheets
- Gumroad Trigger
- Http Request
- Set
- Sticky Note
- Telegram

## Required Credentials

- googleSheetsOAuth2Api (type only; no credential value stored)
- gumroadApi (type only; no credential value stored)
- httpBearerAuth (type only; no credential value stored)
- httpHeaderAuth (type only; no credential value stored)
- telegramApi (type only; no credential value stored)

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
