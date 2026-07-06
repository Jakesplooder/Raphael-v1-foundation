# Archived n8n Workflow WFARCH-D21AE980C6

## Workflow ID

WFARCH-D21AE980C6

## Name

Extract text from PDF and image using Vertex AI (Gemini) into CSV

## Category

Automation

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1444_Extractfromfile_Converttofile_Automation_Webhook.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 16
- Connections: 11
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.chainLlm`
- `@n8n/n8n-nodes-langchain.lmChatGoogleGemini`
- `n8n-nodes-base.convertToFile`
- `n8n-nodes-base.extractFromFile`
- `n8n-nodes-base.googleDrive`
- `n8n-nodes-base.googleDriveTrigger`
- `n8n-nodes-base.httpRequest`
- `n8n-nodes-base.stickyNote`
- `n8n-nodes-base.switch`

## API and Service Analysis

- Chain Llm
- Convert To File
- Extract From File
- Google Drive
- Google Drive Trigger
- Http Request
- Lm Chat Google Gemini
- Sticky Note
- Switch

## Required Credentials

- googleApi (type only; no credential value stored)
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
