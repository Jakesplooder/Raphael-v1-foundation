# Archived n8n Workflow WFARCH-914DBCAD94

## Workflow ID

WFARCH-914DBCAD94

## Name

AI Agent - Cv Resume - Automated Screening , Sorting , Rating and Tracker System

## Category

Automation

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1287_Googledocs_Googledrivetool_Monitor_Triggered.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 20
- Connections: 10
- Source marked active: True (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.agent`
- `@n8n/n8n-nodes-langchain.lmChatGroq`
- `n8n-nodes-base.extractFromFile`
- `n8n-nodes-base.gmailTool`
- `n8n-nodes-base.googleDocs`
- `n8n-nodes-base.googleDrive`
- `n8n-nodes-base.googleDriveTool`
- `n8n-nodes-base.googleDriveTrigger`
- `n8n-nodes-base.googleSheetsTool`
- `n8n-nodes-base.stickyNote`

## API and Service Analysis

- Agent
- Extract From File
- Gmail Tool
- Google Docs
- Google Drive
- Google Drive Tool
- Google Drive Trigger
- Google Sheets Tool
- Lm Chat Groq
- Sticky Note

## Required Credentials

- gmailOAuth2 (type only; no credential value stored)
- googleDocsOAuth2Api (type only; no credential value stored)
- googleDriveOAuth2Api (type only; no credential value stored)
- googleSheetsOAuth2Api (type only; no credential value stored)
- groqApi (type only; no credential value stored)

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
