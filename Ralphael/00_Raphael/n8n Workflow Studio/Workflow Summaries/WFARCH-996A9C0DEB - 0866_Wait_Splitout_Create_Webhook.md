# Archived n8n Workflow WFARCH-996A9C0DEB

## Workflow ID

WFARCH-996A9C0DEB

## Name

0866_Wait_Splitout_Create_Webhook

## Category

Automation

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

0866_Wait_Splitout_Create_Webhook.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 17
- Connections: 11
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.chainLlm`
- `@n8n/n8n-nodes-langchain.lmChatOpenAi`
- `n8n-nodes-base.formTrigger`
- `n8n-nodes-base.googleSheets`
- `n8n-nodes-base.httpRequest`
- `n8n-nodes-base.if`
- `n8n-nodes-base.splitOut`
- `n8n-nodes-base.stickyNote`
- `n8n-nodes-base.wait`

## API and Service Analysis

- Chain Llm
- Form Trigger
- Google Sheets
- Http Request
- If
- Lm Chat Open Ai
- Split Out
- Sticky Note
- Wait

## Required Credentials

- googleSheetsOAuth2Api (type only; no credential value stored)
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
