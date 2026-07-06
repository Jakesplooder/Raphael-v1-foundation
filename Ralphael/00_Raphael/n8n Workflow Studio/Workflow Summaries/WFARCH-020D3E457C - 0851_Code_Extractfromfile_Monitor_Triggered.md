# Archived n8n Workflow WFARCH-020D3E457C

## Workflow ID

WFARCH-020D3E457C

## Name

0851_Code_Extractfromfile_Monitor_Triggered

## Category

Automation

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

0851_Code_Extractfromfile_Monitor_Triggered.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 22
- Connections: 15
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.informationExtractor`
- `@n8n/n8n-nodes-langchain.lmChatOpenAi`
- `@n8n/n8n-nodes-langchain.textClassifier`
- `n8n-nodes-base.code`
- `n8n-nodes-base.extractFromFile`
- `n8n-nodes-base.if`
- `n8n-nodes-base.microsoftOutlook`
- `n8n-nodes-base.microsoftOutlookTrigger`
- `n8n-nodes-base.noOp`
- `n8n-nodes-base.set`
- `n8n-nodes-base.stickyNote`

## API and Service Analysis

- Code
- Extract From File
- If
- Information Extractor
- Lm Chat Open Ai
- Microsoft Outlook
- Microsoft Outlook Trigger
- No Op
- Set
- Sticky Note
- Text Classifier

## Required Credentials

- microsoftOutlookOAuth2Api (type only; no credential value stored)
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
