# Archived n8n Workflow WFARCH-8C2DE04A15

## Workflow ID

WFARCH-8C2DE04A15

## Name

AI CV Screening Workflow

## Category

Automation

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1420_Form_Extractfromfile_Automate_Triggered.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 7
- Connections: 6
- Source marked active: True (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.chainLlm`
- `@n8n/n8n-nodes-langchain.lmChatGoogleGemini`
- `n8n-nodes-base.extractFromFile`
- `n8n-nodes-base.formTrigger`
- `n8n-nodes-base.gmail`
- `n8n-nodes-base.googleSheets`

## API and Service Analysis

- Chain Llm
- Extract From File
- Form Trigger
- Gmail
- Google Sheets
- Lm Chat Google Gemini

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
