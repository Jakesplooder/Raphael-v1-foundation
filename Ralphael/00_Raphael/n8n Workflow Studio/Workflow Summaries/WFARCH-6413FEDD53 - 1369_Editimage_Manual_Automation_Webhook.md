# Archived n8n Workflow WFARCH-6413FEDD53

## Workflow ID

WFARCH-6413FEDD53

## Name

1369_Editimage_Manual_Automation_Webhook

## Category

Automation

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1369_Editimage_Manual_Automation_Webhook.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 13
- Connections: 7
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.chainLlm`
- `@n8n/n8n-nodes-langchain.lmChatGoogleGemini`
- `@n8n/n8n-nodes-langchain.outputParserStructured`
- `n8n-nodes-base.editImage`
- `n8n-nodes-base.googleDrive`
- `n8n-nodes-base.httpRequest`
- `n8n-nodes-base.if`
- `n8n-nodes-base.manualTrigger`
- `n8n-nodes-base.stickyNote`

## API and Service Analysis

- Chain Llm
- Edit Image
- Google Drive
- Http Request
- If
- Lm Chat Google Gemini
- Manual Trigger
- Output Parser Structured
- Sticky Note

## Required Credentials

- googleDriveOAuth2Api (type only; no credential value stored)
- googlePalmApi (type only; no credential value stored)

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
