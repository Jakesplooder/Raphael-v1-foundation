# Archived n8n Workflow WFARCH-1662D55CF2

## Workflow ID

WFARCH-1662D55CF2

## Name

Contact Form Text Classifier for eCommerce

## Category

Automation

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1554_Form_GoogleSheets_Automation_Triggered.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 14
- Connections: 12
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.lmChatOpenAi`
- `@n8n/n8n-nodes-langchain.textClassifier`
- `n8n-nodes-base.emailSend`
- `n8n-nodes-base.formTrigger`
- `n8n-nodes-base.googleSheets`
- `n8n-nodes-base.stickyNote`

## API and Service Analysis

- Email Send
- Form Trigger
- Google Sheets
- Lm Chat Open Ai
- Sticky Note
- Text Classifier

## Required Credentials

- googleSheetsOAuth2Api (type only; no credential value stored)
- openAiApi (type only; no credential value stored)
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
