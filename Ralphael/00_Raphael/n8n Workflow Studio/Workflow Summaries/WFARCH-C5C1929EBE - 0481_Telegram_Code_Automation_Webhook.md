# Archived n8n Workflow WFARCH-C5C1929EBE

## Workflow ID

WFARCH-C5C1929EBE

## Name

0481_Telegram_Code_Automation_Webhook

## Category

Notifications

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

0481_Telegram_Code_Automation_Webhook.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 14
- Connections: 11
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.chainSummarization`
- `@n8n/n8n-nodes-langchain.lmChatOpenAi`
- `n8n-nodes-base.aggregate`
- `n8n-nodes-base.code`
- `n8n-nodes-base.convertToFile`
- `n8n-nodes-base.gmail`
- `n8n-nodes-base.gmailTrigger`
- `n8n-nodes-base.httpRequest`
- `n8n-nodes-base.merge`
- `n8n-nodes-base.stickyNote`
- `n8n-nodes-base.telegram`

## API and Service Analysis

- Aggregate
- Chain Summarization
- Code
- Convert To File
- Gmail
- Gmail Trigger
- Http Request
- Lm Chat Open Ai
- Merge
- Sticky Note
- Telegram

## Required Credentials

- gmailOAuth2 (type only; no credential value stored)
- openAiApi (type only; no credential value stored)
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
