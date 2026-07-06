# Archived n8n Workflow WFARCH-D137343FE1

## Workflow ID

WFARCH-D137343FE1

## Name

✨🔪 Advanced AI Powered Document Parsing & Text Extraction with Llama Parse

## Category

Knowledge

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1904_Telegram_Limit_Process_Webhook.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 54
- Connections: 37
- Source marked active: True (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.chainLlm`
- `@n8n/n8n-nodes-langchain.lmChatOpenAi`
- `@n8n/n8n-nodes-langchain.textClassifier`
- `n8n-nodes-base.aggregate`
- `n8n-nodes-base.gmail`
- `n8n-nodes-base.gmailTrigger`
- `n8n-nodes-base.googleDrive`
- `n8n-nodes-base.googleSheets`
- `n8n-nodes-base.httpRequest`
- `n8n-nodes-base.if`
- `n8n-nodes-base.limit`
- `n8n-nodes-base.merge`
- `n8n-nodes-base.noOp`
- `n8n-nodes-base.set`
- `n8n-nodes-base.stickyNote`
- `n8n-nodes-base.telegram`
- `n8n-nodes-base.webhook`

## API and Service Analysis

- Aggregate
- Chain Llm
- Gmail
- Gmail Trigger
- Google Drive
- Google Sheets
- Http Request
- If
- Limit
- Lm Chat Open Ai
- Merge
- No Op
- Set
- Sticky Note
- Telegram
- Text Classifier
- Webhook

## Required Credentials

- gmailOAuth2 (type only; no credential value stored)
- googleDriveOAuth2Api (type only; no credential value stored)
- googleSheetsOAuth2Api (type only; no credential value stored)
- httpHeaderAuth (type only; no credential value stored)
- openAiApi (type only; no credential value stored)
- telegramApi (type only; no credential value stored)

## Reuse Assessment

- Reusable trigger/transform pattern: Yes
- Category relationship: Knowledge
- The workflow exposes a standard node list for structural analysis.
- Review node settings, platform terms, privacy, rate limits, and credential requirements before any manual use.

## Safety

- Source modified: no
- Workflow imported into n8n: no
- Workflow activated: no
- Workflow executed: no
- Credential values stored: no
- External APIs called: no
