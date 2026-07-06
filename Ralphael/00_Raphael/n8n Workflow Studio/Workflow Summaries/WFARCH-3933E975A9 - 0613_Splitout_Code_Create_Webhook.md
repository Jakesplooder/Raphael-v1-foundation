# Archived n8n Workflow WFARCH-3933E975A9

## Workflow ID

WFARCH-3933E975A9

## Name

0613_Splitout_Code_Create_Webhook

## Category

Notifications

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

0613_Splitout_Code_Create_Webhook.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 33
- Connections: 14
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.openAi`
- `n8n-nodes-base.airtable`
- `n8n-nodes-base.code`
- `n8n-nodes-base.googleSheets`
- `n8n-nodes-base.html`
- `n8n-nodes-base.httpRequest`
- `n8n-nodes-base.manualTrigger`
- `n8n-nodes-base.merge`
- `n8n-nodes-base.nocoDb`
- `n8n-nodes-base.scheduleTrigger`
- `n8n-nodes-base.set`
- `n8n-nodes-base.slack`
- `n8n-nodes-base.splitOut`
- `n8n-nodes-base.stickyNote`

## API and Service Analysis

- Airtable
- Code
- Google Sheets
- Html
- Http Request
- Manual Trigger
- Merge
- Noco Db
- Open Ai
- Schedule Trigger
- Set
- Slack
- Split Out
- Sticky Note

## Required Credentials

- airtableOAuth2Api (type only; no credential value stored)
- googleSheetsOAuth2Api (type only; no credential value stored)
- nocoDbApiToken (type only; no credential value stored)
- openAiApi (type only; no credential value stored)
- slackOAuth2Api (type only; no credential value stored)

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
