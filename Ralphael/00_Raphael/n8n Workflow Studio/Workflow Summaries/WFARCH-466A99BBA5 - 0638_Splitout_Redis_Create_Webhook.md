# Archived n8n Workflow WFARCH-466A99BBA5

## Workflow ID

WFARCH-466A99BBA5

## Name

0638_Splitout_Redis_Create_Webhook

## Category

Automation

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

0638_Splitout_Redis_Create_Webhook.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 40
- Connections: 30
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.agent`
- `@n8n/n8n-nodes-langchain.lmChatGroq`
- `@n8n/n8n-nodes-langchain.memoryBufferWindow`
- `@n8n/n8n-nodes-langchain.memoryManager`
- `n8n-nodes-base.crypto`
- `n8n-nodes-base.form`
- `n8n-nodes-base.formTrigger`
- `n8n-nodes-base.googleSheets`
- `n8n-nodes-base.html`
- `n8n-nodes-base.if`
- `n8n-nodes-base.redis`
- `n8n-nodes-base.respondToWebhook`
- `n8n-nodes-base.set`
- `n8n-nodes-base.splitOut`
- `n8n-nodes-base.stickyNote`
- `n8n-nodes-base.webhook`

## API and Service Analysis

- Agent
- Crypto
- Form
- Form Trigger
- Google Sheets
- Html
- If
- Lm Chat Groq
- Memory Buffer Window
- Memory Manager
- Redis
- Respond To Webhook
- Set
- Split Out
- Sticky Note
- Webhook

## Required Credentials

- googleSheetsOAuth2Api (type only; no credential value stored)
- groqApi (type only; no credential value stored)
- redis (type only; no credential value stored)

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
