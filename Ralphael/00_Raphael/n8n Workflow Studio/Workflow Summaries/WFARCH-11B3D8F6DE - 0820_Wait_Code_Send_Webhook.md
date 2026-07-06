# Archived n8n Workflow WFARCH-11B3D8F6DE

## Workflow ID

WFARCH-11B3D8F6DE

## Name

0820_Wait_Code_Send_Webhook

## Category

Automation

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

0820_Wait_Code_Send_Webhook.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 24
- Connections: 20
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.lmChatGoogleGemini`
- `@n8n/n8n-nodes-langchain.textClassifier`
- `n8n-nodes-base.code`
- `n8n-nodes-base.extractFromFile`
- `n8n-nodes-base.filter`
- `n8n-nodes-base.httpRequest`
- `n8n-nodes-base.if`
- `n8n-nodes-base.markdown`
- `n8n-nodes-base.microsoftExcel`
- `n8n-nodes-base.microsoftOutlook`
- `n8n-nodes-base.noOp`
- `n8n-nodes-base.scheduleTrigger`
- `n8n-nodes-base.set`
- `n8n-nodes-base.splitInBatches`
- `n8n-nodes-base.stickyNote`
- `n8n-nodes-base.wait`

## API and Service Analysis

- Code
- Extract From File
- Filter
- Http Request
- If
- Lm Chat Google Gemini
- Markdown
- Microsoft Excel
- Microsoft Outlook
- No Op
- Schedule Trigger
- Set
- Split In Batches
- Sticky Note
- Text Classifier
- Wait

## Required Credentials

- googlePalmApi (type only; no credential value stored)
- microsoftExcelOAuth2Api (type only; no credential value stored)
- microsoftOutlookOAuth2Api (type only; no credential value stored)

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
