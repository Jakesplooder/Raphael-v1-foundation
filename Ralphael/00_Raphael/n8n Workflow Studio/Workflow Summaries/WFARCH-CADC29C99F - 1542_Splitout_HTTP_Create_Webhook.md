# Archived n8n Workflow WFARCH-CADC29C99F

## Workflow ID

WFARCH-CADC29C99F

## Name

1542_Splitout_HTTP_Create_Webhook

## Category

Automation

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1542_Splitout_HTTP_Create_Webhook.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 10
- Connections: 9
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.chainLlm`
- `@n8n/n8n-nodes-langchain.lmChatGoogleGemini`
- `n8n-nodes-base.aggregate`
- `n8n-nodes-base.emailSend`
- `n8n-nodes-base.formTrigger`
- `n8n-nodes-base.hackerNews`
- `n8n-nodes-base.httpRequest`
- `n8n-nodes-base.markdown`
- `n8n-nodes-base.noOp`
- `n8n-nodes-base.splitOut`

## API and Service Analysis

- Aggregate
- Chain Llm
- Email Send
- Form Trigger
- Hacker News
- Http Request
- Lm Chat Google Gemini
- Markdown
- No Op
- Split Out

## Required Credentials

- googlePalmApi (type only; no credential value stored)
- smtp (type only; no credential value stored)

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
