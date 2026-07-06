# Archived n8n Workflow WFARCH-55737AFBB8

## Workflow ID

WFARCH-55737AFBB8

## Name

Auto-create and publish AI social videos with Telegram, GPT-4 and Blotato

## Category

Creator

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1878_Telegram_Wait_Create_Webhook.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 42
- Connections: 37
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.openAi`
- `n8n-nodes-base.code`
- `n8n-nodes-base.googleSheets`
- `n8n-nodes-base.httpRequest`
- `n8n-nodes-base.if`
- `n8n-nodes-base.set`
- `n8n-nodes-base.stickyNote`
- `n8n-nodes-base.telegram`
- `n8n-nodes-base.telegramTrigger`
- `n8n-nodes-base.wait`

## API and Service Analysis

- Code
- Google Sheets
- Http Request
- If
- Open Ai
- Set
- Sticky Note
- Telegram
- Telegram Trigger
- Wait

## Required Credentials

- googleSheetsOAuth2Api (type only; no credential value stored)
- httpBasicAuth (type only; no credential value stored)
- httpCustomAuth (type only; no credential value stored)
- httpHeaderAuth (type only; no credential value stored)
- openAiApi (type only; no credential value stored)
- telegramApi (type only; no credential value stored)

## Reuse Assessment

- Reusable trigger/transform pattern: Yes
- Category relationship: Creator
- The workflow exposes a standard node list for structural analysis.
- Review node settings, platform terms, privacy, rate limits, and credential requirements before any manual use.

## Safety

- Source modified: no
- Workflow imported into n8n: no
- Workflow activated: no
- Workflow executed: no
- Credential values stored: no
- External APIs called: no
