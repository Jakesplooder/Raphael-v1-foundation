# Archived n8n Workflow WFARCH-94C1BF0726

## Workflow ID

WFARCH-94C1BF0726

## Name

Translate questions about e-mails into SQL queries and run them

## Category

Automation

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1245_Postgres_Extractfromfile_Automation_Triggered.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 26
- Connections: 25
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.agent`
- `@n8n/n8n-nodes-langchain.chatTrigger`
- `@n8n/n8n-nodes-langchain.lmChatOllama`
- `n8n-nodes-base.convertToFile`
- `n8n-nodes-base.executeWorkflowTrigger`
- `n8n-nodes-base.extractFromFile`
- `n8n-nodes-base.if`
- `n8n-nodes-base.manualTrigger`
- `n8n-nodes-base.merge`
- `n8n-nodes-base.postgres`
- `n8n-nodes-base.readWriteFile`
- `n8n-nodes-base.set`
- `n8n-nodes-base.stickyNote`

## API and Service Analysis

- Agent
- Chat Trigger
- Convert To File
- Execute Workflow Trigger
- Extract From File
- If
- Lm Chat Ollama
- Manual Trigger
- Merge
- Postgres
- Read Write File
- Set
- Sticky Note

## Required Credentials

- None declared in source workflow.

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
