# Archived n8n Workflow WFARCH-5D321A7393

## Workflow ID

WFARCH-5D321A7393

## Name

0524_Googledocs_Webhook_Create_Webhook

## Category

Notifications

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

0524_Googledocs_Webhook_Create_Webhook.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 23
- Connections: 13
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.chainLlm`
- `@n8n/n8n-nodes-langchain.lmChatOpenAi`
- `@n8n/n8n-nodes-langchain.openAi`
- `@n8n/n8n-nodes-langchain.outputParserItemList`
- `n8n-nodes-base.extractFromFile`
- `n8n-nodes-base.gmail`
- `n8n-nodes-base.googleDocs`
- `n8n-nodes-base.set`
- `n8n-nodes-base.slack`
- `n8n-nodes-base.splitInBatches`
- `n8n-nodes-base.stickyNote`
- `n8n-nodes-base.webhook`

## API and Service Analysis

- Chain Llm
- Extract From File
- Gmail
- Google Docs
- Lm Chat Open Ai
- Open Ai
- Output Parser Item List
- Set
- Slack
- Split In Batches
- Sticky Note
- Webhook

## Required Credentials

- gmailOAuth2 (type only; no credential value stored)
- googleDocsOAuth2Api (type only; no credential value stored)
- openAiApi (type only; no credential value stored)
- slackApi (type only; no credential value stored)

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
