# Archived n8n Workflow WFARCH-ACA927321E

## Workflow ID

WFARCH-ACA927321E

## Name

Intelligent Web Query and Semantic Re-Ranking Flow

## Category

Automation

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

2003_Datetime_Code_Automation_Webhook.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 20
- Connections: 14
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.chainLlm`
- `@n8n/n8n-nodes-langchain.lmChatAnthropic`
- `@n8n/n8n-nodes-langchain.lmChatGoogleGemini`
- `@n8n/n8n-nodes-langchain.lmChatOpenAi`
- `@n8n/n8n-nodes-langchain.outputParserAutofixing`
- `@n8n/n8n-nodes-langchain.outputParserStructured`
- `n8n-nodes-base.code`
- `n8n-nodes-base.dateTime`
- `n8n-nodes-base.httpRequest`
- `n8n-nodes-base.respondToWebhook`
- `n8n-nodes-base.stickyNote`
- `n8n-nodes-base.webhook`

## API and Service Analysis

- Chain Llm
- Code
- Date Time
- Http Request
- Lm Chat Anthropic
- Lm Chat Google Gemini
- Lm Chat Open Ai
- Output Parser Autofixing
- Output Parser Structured
- Respond To Webhook
- Sticky Note
- Webhook

## Required Credentials

- anthropicApi (type only; no credential value stored)
- googlePalmApi (type only; no credential value stored)
- openAiApi (type only; no credential value stored)

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
