# Archived n8n Workflow WFARCH-6E4681F431

## Workflow ID

WFARCH-6E4681F431

## Name

AI-Generated Summary Block for WordPress Posts - with OpenAI, WordPress, Google Sheets & Slack

## Category

Notifications

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1273_Datetime_Webhook_Create_Webhook.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 32
- Connections: 21
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.lmChatOpenAi`
- `@n8n/n8n-nodes-langchain.openAi`
- `@n8n/n8n-nodes-langchain.textClassifier`
- `n8n-nodes-base.dateTime`
- `n8n-nodes-base.googleSheets`
- `n8n-nodes-base.httpRequest`
- `n8n-nodes-base.if`
- `n8n-nodes-base.manualTrigger`
- `n8n-nodes-base.markdown`
- `n8n-nodes-base.noOp`
- `n8n-nodes-base.scheduleTrigger`
- `n8n-nodes-base.set`
- `n8n-nodes-base.slack`
- `n8n-nodes-base.splitInBatches`
- `n8n-nodes-base.stickyNote`
- `n8n-nodes-base.webhook`
- `n8n-nodes-base.wordpress`

## API and Service Analysis

- Date Time
- Google Sheets
- Http Request
- If
- Lm Chat Open Ai
- Manual Trigger
- Markdown
- No Op
- Open Ai
- Schedule Trigger
- Set
- Slack
- Split In Batches
- Sticky Note
- Text Classifier
- Webhook
- Wordpress

## Required Credentials

- googleApi (type only; no credential value stored)
- httpHeaderAuth (type only; no credential value stored)
- openAiApi (type only; no credential value stored)
- slackOAuth2Api (type only; no credential value stored)
- wordpressApi (type only; no credential value stored)

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
