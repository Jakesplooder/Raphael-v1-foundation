# Archived n8n Workflow WFARCH-591A3C830F

## Workflow ID

WFARCH-591A3C830F

## Name

Build a Phone Agent to qualify outbound leads and inbound calls with RetellAI -vide

## Category

Agency

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1362_Wait_Webhook_Create_Webhook.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 18
- Connections: 11
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.openAi`
- `n8n-nodes-base.filter`
- `n8n-nodes-base.gmail`
- `n8n-nodes-base.googleSheets`
- `n8n-nodes-base.googleSheetsTrigger`
- `n8n-nodes-base.httpRequest`
- `n8n-nodes-base.if`
- `n8n-nodes-base.respondToWebhook`
- `n8n-nodes-base.stickyNote`
- `n8n-nodes-base.twilio`
- `n8n-nodes-base.wait`
- `n8n-nodes-base.webhook`

## API and Service Analysis

- Filter
- Gmail
- Google Sheets
- Google Sheets Trigger
- Http Request
- If
- Open Ai
- Respond To Webhook
- Sticky Note
- Twilio
- Wait
- Webhook

## Required Credentials

- gmailOAuth2 (type only; no credential value stored)
- googleSheetsOAuth2Api (type only; no credential value stored)
- googleSheetsTriggerOAuth2Api (type only; no credential value stored)
- openAiApi (type only; no credential value stored)
- twilioApi (type only; no credential value stored)

## Reuse Assessment

- Reusable trigger/transform pattern: Yes
- Category relationship: Agency
- The workflow exposes a standard node list for structural analysis.
- Review node settings, platform terms, privacy, rate limits, and credential requirements before any manual use.

## Safety

- Source modified: no
- Workflow imported into n8n: no
- Workflow activated: no
- Workflow executed: no
- Credential values stored: no
- External APIs called: no
