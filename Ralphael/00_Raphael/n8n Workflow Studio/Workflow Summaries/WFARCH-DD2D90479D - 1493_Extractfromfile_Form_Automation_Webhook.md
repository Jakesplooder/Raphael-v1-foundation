# Archived n8n Workflow WFARCH-DD2D90479D

## Workflow ID

WFARCH-DD2D90479D

## Name

1493_Extractfromfile_Form_Automation_Webhook

## Category

Automation

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1493_Extractfromfile_Form_Automation_Webhook.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 23
- Connections: 15
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.chainLlm`
- `@n8n/n8n-nodes-langchain.lmChatOpenAi`
- `@n8n/n8n-nodes-langchain.outputParserStructured`
- `@n8n/n8n-nodes-langchain.textClassifier`
- `n8n-nodes-base.airtable`
- `n8n-nodes-base.extractFromFile`
- `n8n-nodes-base.form`
- `n8n-nodes-base.formTrigger`
- `n8n-nodes-base.httpRequest`
- `n8n-nodes-base.stickyNote`

## API and Service Analysis

- Airtable
- Chain Llm
- Extract From File
- Form
- Form Trigger
- Http Request
- Lm Chat Open Ai
- Output Parser Structured
- Sticky Note
- Text Classifier

## Required Credentials

- airtableTokenApi (type only; no credential value stored)
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
