# Archived n8n Workflow WFARCH-39D8A0C579

## Workflow ID

WFARCH-39D8A0C579

## Name

0731_Splitout_Limit_Create_Webhook

## Category

Automation

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

0731_Splitout_Limit_Create_Webhook.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 22
- Connections: 16
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.chainLlm`
- `@n8n/n8n-nodes-langchain.lmChatGoogleGemini`
- `@n8n/n8n-nodes-langchain.outputParserStructured`
- `@n8n/n8n-nodes-langchain.textClassifier`
- `n8n-nodes-base.aggregate`
- `n8n-nodes-base.filter`
- `n8n-nodes-base.html`
- `n8n-nodes-base.httpRequest`
- `n8n-nodes-base.if`
- `n8n-nodes-base.limit`
- `n8n-nodes-base.manualTrigger`
- `n8n-nodes-base.splitOut`
- `n8n-nodes-base.stickyNote`

## API and Service Analysis

- Aggregate
- Chain Llm
- Filter
- Html
- Http Request
- If
- Limit
- Lm Chat Google Gemini
- Manual Trigger
- Output Parser Structured
- Split Out
- Sticky Note
- Text Classifier

## Required Credentials

- googlePalmApi (type only; no credential value stored)
- huggingFaceApi (type only; no credential value stored)

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
