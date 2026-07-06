# Archived n8n Workflow WFARCH-7B2B1A4F7D

## Workflow ID

WFARCH-7B2B1A4F7D

## Name

1587_Executecommand_Localfile_Automation_Triggered

## Category

Automation

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1587_Executecommand_Localfile_Automation_Triggered.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 16
- Connections: 9
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.chainLlm`
- `@n8n/n8n-nodes-langchain.lmChatMistralCloud`
- `@n8n/n8n-nodes-langchain.outputParserStructured`
- `n8n-nodes-base.executeCommand`
- `n8n-nodes-base.if`
- `n8n-nodes-base.localFileTrigger`
- `n8n-nodes-base.set`
- `n8n-nodes-base.splitOut`
- `n8n-nodes-base.stickyNote`

## API and Service Analysis

- Chain Llm
- Execute Command
- If
- Lm Chat Mistral Cloud
- Local File Trigger
- Output Parser Structured
- Set
- Split Out
- Sticky Note

## Required Credentials

- mistralCloudApi (type only; no credential value stored)

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
