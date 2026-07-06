# Archived n8n Workflow WFARCH-FC2C74CF35

## Workflow ID

WFARCH-FC2C74CF35

## Name

0875_Googledrivetool_Extractfromfile_Import_Triggered

## Category

Automation

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

0875_Googledrivetool_Extractfromfile_Import_Triggered.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 17
- Connections: 11
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.mcpTrigger`
- `@n8n/n8n-nodes-langchain.openAi`
- `@n8n/n8n-nodes-langchain.toolWorkflow`
- `n8n-nodes-base.executeWorkflowTrigger`
- `n8n-nodes-base.extractFromFile`
- `n8n-nodes-base.googleDrive`
- `n8n-nodes-base.googleDriveTool`
- `n8n-nodes-base.set`
- `n8n-nodes-base.stickyNote`
- `n8n-nodes-base.switch`

## API and Service Analysis

- Execute Workflow Trigger
- Extract From File
- Google Drive
- Google Drive Tool
- Mcp Trigger
- Open Ai
- Set
- Sticky Note
- Switch
- Tool Workflow

## Required Credentials

- googleDriveOAuth2Api (type only; no credential value stored)
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
