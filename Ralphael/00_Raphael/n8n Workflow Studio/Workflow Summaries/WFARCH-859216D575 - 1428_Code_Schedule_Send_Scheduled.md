# Archived n8n Workflow WFARCH-859216D575

## Workflow ID

WFARCH-859216D575

## Name

1428_Code_Schedule_Send_Scheduled

## Category

Automation

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1428_Code_Schedule_Send_Scheduled.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 32
- Connections: 22
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.agent`
- `@n8n/n8n-nodes-langchain.lmChatGroq`
- `@n8n/n8n-nodes-langchain.memoryBufferWindow`
- `@n8n/n8n-nodes-langchain.openAi`
- `@n8n/n8n-nodes-langchain.toolWikipedia`
- `n8n-nodes-base.airtable`
- `n8n-nodes-base.code`
- `n8n-nodes-base.editImage`
- `n8n-nodes-base.executeWorkflow`
- `n8n-nodes-base.executeWorkflowTrigger`
- `n8n-nodes-base.executionData`
- `n8n-nodes-base.filter`
- `n8n-nodes-base.formTrigger`
- `n8n-nodes-base.gmail`
- `n8n-nodes-base.scheduleTrigger`
- `n8n-nodes-base.set`
- `n8n-nodes-base.stickyNote`

## API and Service Analysis

- Agent
- Airtable
- Code
- Edit Image
- Execute Workflow
- Execute Workflow Trigger
- Execution Data
- Filter
- Form Trigger
- Gmail
- Lm Chat Groq
- Memory Buffer Window
- Open Ai
- Schedule Trigger
- Set
- Sticky Note
- Tool Wikipedia

## Required Credentials

- airtableTokenApi (type only; no credential value stored)
- gmailOAuth2 (type only; no credential value stored)
- groqApi (type only; no credential value stored)
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
