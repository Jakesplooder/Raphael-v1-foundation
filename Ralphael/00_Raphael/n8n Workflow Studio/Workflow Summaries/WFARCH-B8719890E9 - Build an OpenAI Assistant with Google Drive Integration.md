# Archived n8n Workflow WFARCH-B8719890E9

## Workflow ID

WFARCH-B8719890E9

## Name

Build an OpenAI Assistant with Google Drive Integration

## Category

Automation

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1360_Manual_Stickynote_Create_Triggered.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 12
- Connections: 6
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.chatTrigger`
- `@n8n/n8n-nodes-langchain.memoryBufferWindow`
- `@n8n/n8n-nodes-langchain.openAi`
- `n8n-nodes-base.googleDrive`
- `n8n-nodes-base.manualTrigger`
- `n8n-nodes-base.stickyNote`

## API and Service Analysis

- Chat Trigger
- Google Drive
- Manual Trigger
- Memory Buffer Window
- Open Ai
- Sticky Note

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
