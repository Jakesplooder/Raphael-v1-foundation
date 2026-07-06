# Archived n8n Workflow WFARCH-10C25BFF00

## Workflow ID

WFARCH-10C25BFF00

## Name

WordPress Contact Form (CF7) Responses and Classification

## Category

Automation

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1860_GoogleSheets_Gmail_Automation_Webhook.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 24
- Connections: 18
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.chainLlm`
- `@n8n/n8n-nodes-langchain.lmChatGoogleGemini`
- `@n8n/n8n-nodes-langchain.outputParserStructured`
- `@n8n/n8n-nodes-langchain.textClassifier`
- `n8n-nodes-base.gmail`
- `n8n-nodes-base.googleSheets`
- `n8n-nodes-base.set`
- `n8n-nodes-base.stickyNote`
- `n8n-nodes-base.webhook`

## API and Service Analysis

- Chain Llm
- Gmail
- Google Sheets
- Lm Chat Google Gemini
- Output Parser Structured
- Set
- Sticky Note
- Text Classifier
- Webhook

## Required Credentials

- gmailOAuth2 (type only; no credential value stored)
- googlePalmApi (type only; no credential value stored)
- googleSheetsOAuth2Api (type only; no credential value stored)

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
