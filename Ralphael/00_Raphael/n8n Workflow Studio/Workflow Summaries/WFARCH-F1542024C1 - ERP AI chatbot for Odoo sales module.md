# Archived n8n Workflow WFARCH-F1542024C1

## Workflow ID

WFARCH-F1542024C1

## Name

ERP AI chatbot for Odoo sales module

## Category

Automation

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1929_Odoo_Schedule_Automate_Scheduled.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 16
- Connections: 15
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.agent`
- `@n8n/n8n-nodes-langchain.chainSummarization`
- `@n8n/n8n-nodes-langchain.chatTrigger`
- `@n8n/n8n-nodes-langchain.lmChatOpenAi`
- `@n8n/n8n-nodes-langchain.lmOpenAi`
- `@n8n/n8n-nodes-langchain.memoryBufferWindow`
- `@n8n/n8n-nodes-langchain.toolCalculator`
- `n8n-nodes-base.aggregate`
- `n8n-nodes-base.convertToFile`
- `n8n-nodes-base.extractFromFile`
- `n8n-nodes-base.if`
- `n8n-nodes-base.odoo`
- `n8n-nodes-base.readWriteFile`
- `n8n-nodes-base.scheduleTrigger`
- `n8n-nodes-base.stickyNote`

## API and Service Analysis

- Agent
- Aggregate
- Chain Summarization
- Chat Trigger
- Convert To File
- Extract From File
- If
- Lm Chat Open Ai
- Lm Open Ai
- Memory Buffer Window
- Odoo
- Read Write File
- Schedule Trigger
- Sticky Note
- Tool Calculator

## Required Credentials

- odooApi (type only; no credential value stored)
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
