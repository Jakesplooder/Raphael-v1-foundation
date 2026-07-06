# Archived n8n Workflow WFARCH-FFDBD6860A

## Workflow ID

WFARCH-FFDBD6860A

## Name

0918_Code_Noop_Send_Triggered

## Category

Automation

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

0918_Code_Noop_Send_Triggered.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 19
- Connections: 13
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.agent`
- `@n8n/n8n-nodes-langchain.chatTrigger`
- `@n8n/n8n-nodes-langchain.informationExtractor`
- `@n8n/n8n-nodes-langchain.lmChatOpenAi`
- `@n8n/n8n-nodes-langchain.memoryBufferWindow`
- `@n8n/n8n-nodes-langchain.toolWorkflow`
- `n8n-nodes-base.code`
- `n8n-nodes-base.executeWorkflowTrigger`
- `n8n-nodes-base.googleSheets`
- `n8n-nodes-base.if`
- `n8n-nodes-base.noOp`
- `n8n-nodes-base.splitInBatches`
- `n8n-nodes-base.stickyNote`

## API and Service Analysis

- Agent
- Chat Trigger
- Code
- Execute Workflow Trigger
- Google Sheets
- If
- Information Extractor
- Lm Chat Open Ai
- Memory Buffer Window
- No Op
- Split In Batches
- Sticky Note
- Tool Workflow

## Required Credentials

- googleSheetsOAuth2Api (type only; no credential value stored)
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
