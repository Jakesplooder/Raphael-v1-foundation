# Archived n8n Workflow WFARCH-124094ECA9

## Workflow ID

WFARCH-124094ECA9

## Name

AI-Powered Information Monitoring with OpenAI, Google Sheets, Jina AI and Slack

## Category

Research

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1281_Code_Schedule_Monitor_Webhook.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 31
- Connections: 17
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.chainLlm`
- `@n8n/n8n-nodes-langchain.lmChatOpenAi`
- `@n8n/n8n-nodes-langchain.textClassifier`
- `n8n-nodes-base.code`
- `n8n-nodes-base.googleSheets`
- `n8n-nodes-base.httpRequest`
- `n8n-nodes-base.if`
- `n8n-nodes-base.noOp`
- `n8n-nodes-base.rssFeedRead`
- `n8n-nodes-base.scheduleTrigger`
- `n8n-nodes-base.set`
- `n8n-nodes-base.slack`
- `n8n-nodes-base.stickyNote`

## API and Service Analysis

- Chain Llm
- Code
- Google Sheets
- Http Request
- If
- Lm Chat Open Ai
- No Op
- Rss Feed Read
- Schedule Trigger
- Set
- Slack
- Sticky Note
- Text Classifier

## Required Credentials

- googleApi (type only; no credential value stored)
- openAiApi (type only; no credential value stored)
- slackOAuth2Api (type only; no credential value stored)

## Reuse Assessment

- Reusable trigger/transform pattern: Yes
- Category relationship: Research
- The workflow exposes a standard node list for structural analysis.
- Review node settings, platform terms, privacy, rate limits, and credential requirements before any manual use.

## Safety

- Source modified: no
- Workflow imported into n8n: no
- Workflow activated: no
- Workflow executed: no
- Credential values stored: no
- External APIs called: no
