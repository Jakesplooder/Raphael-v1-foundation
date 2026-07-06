# Archived n8n Workflow WFARCH-0AA336936A

## Workflow ID

WFARCH-0AA336936A

## Name

SHEETS RAG

## Category

Automation

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1144_Postgres_Code_Automation_Triggered.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 23
- Connections: 18
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.agent`
- `@n8n/n8n-nodes-langchain.lmChatGoogleGemini`
- `@n8n/n8n-nodes-langchain.manualChatTrigger`
- `@n8n/n8n-nodes-langchain.toolWorkflow`
- `n8n-nodes-base.code`
- `n8n-nodes-base.executeWorkflowTrigger`
- `n8n-nodes-base.googleDriveTrigger`
- `n8n-nodes-base.googleSheets`
- `n8n-nodes-base.if`
- `n8n-nodes-base.postgres`
- `n8n-nodes-base.set`
- `n8n-nodes-base.stickyNote`

## API and Service Analysis

- Agent
- Code
- Execute Workflow Trigger
- Google Drive Trigger
- Google Sheets
- If
- Lm Chat Google Gemini
- Manual Chat Trigger
- Postgres
- Set
- Sticky Note
- Tool Workflow

## Required Credentials

- googleDriveOAuth2Api (type only; no credential value stored)
- googlePalmApi (type only; no credential value stored)
- googleSheetsOAuth2Api (type only; no credential value stored)
- postgres (type only; no credential value stored)

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
