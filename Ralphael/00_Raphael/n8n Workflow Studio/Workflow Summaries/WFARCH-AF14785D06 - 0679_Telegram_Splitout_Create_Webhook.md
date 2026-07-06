# Archived n8n Workflow WFARCH-AF14785D06

## Workflow ID

WFARCH-AF14785D06

## Name

0679_Telegram_Splitout_Create_Webhook

## Category

Notifications

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

0679_Telegram_Splitout_Create_Webhook.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 13
- Connections: 13
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.chainLlm`
- `@n8n/n8n-nodes-langchain.lmChatGoogleGemini`
- `n8n-nodes-base.aggregate`
- `n8n-nodes-base.code`
- `n8n-nodes-base.html`
- `n8n-nodes-base.httpRequest`
- `n8n-nodes-base.merge`
- `n8n-nodes-base.scheduleTrigger`
- `n8n-nodes-base.set`
- `n8n-nodes-base.splitOut`
- `n8n-nodes-base.telegram`

## API and Service Analysis

- Aggregate
- Chain Llm
- Code
- Html
- Http Request
- Lm Chat Google Gemini
- Merge
- Schedule Trigger
- Set
- Split Out
- Telegram

## Required Credentials

- googlePalmApi (type only; no credential value stored)
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
