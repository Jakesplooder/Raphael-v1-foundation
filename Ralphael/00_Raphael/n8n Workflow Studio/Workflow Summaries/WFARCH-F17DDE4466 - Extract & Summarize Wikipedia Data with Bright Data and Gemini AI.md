# Archived n8n Workflow WFARCH-F17DDE4466

## Workflow ID

WFARCH-F17DDE4466

## Name

Extract & Summarize Wikipedia Data with Bright Data and Gemini AI

## Category

Automation

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1979_Manual_Stickynote_Automation_Webhook.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 12
- Connections: 7
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.chainLlm`
- `@n8n/n8n-nodes-langchain.chainSummarization`
- `@n8n/n8n-nodes-langchain.lmChatGoogleGemini`
- `n8n-nodes-base.httpRequest`
- `n8n-nodes-base.manualTrigger`
- `n8n-nodes-base.set`
- `n8n-nodes-base.stickyNote`

## API and Service Analysis

- Chain Llm
- Chain Summarization
- Http Request
- Lm Chat Google Gemini
- Manual Trigger
- Set
- Sticky Note

## Required Credentials

- googlePalmApi (type only; no credential value stored)
- httpHeaderAuth (type only; no credential value stored)

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
