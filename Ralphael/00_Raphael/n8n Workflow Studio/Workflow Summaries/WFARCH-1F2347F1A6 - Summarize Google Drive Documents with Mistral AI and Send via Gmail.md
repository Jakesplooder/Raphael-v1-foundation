# Archived n8n Workflow WFARCH-1F2347F1A6

## Workflow ID

WFARCH-1F2347F1A6

## Name

Summarize Google Drive Documents with Mistral AI and Send via Gmail

## Category

Knowledge

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1528_Manual_Gmail_Send_Triggered.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 5
- Connections: 4
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.chainSummarization`
- `@n8n/n8n-nodes-langchain.lmChatMistralCloud`
- `n8n-nodes-base.gmail`
- `n8n-nodes-base.googleDrive`
- `n8n-nodes-base.manualTrigger`

## API and Service Analysis

- Chain Summarization
- Gmail
- Google Drive
- Lm Chat Mistral Cloud
- Manual Trigger

## Required Credentials

- gmailOAuth2 (type only; no credential value stored)
- googleDriveOAuth2Api (type only; no credential value stored)
- mistralCloudApi (type only; no credential value stored)

## Reuse Assessment

- Reusable trigger/transform pattern: Yes
- Category relationship: Knowledge
- The workflow exposes a standard node list for structural analysis.
- Review node settings, platform terms, privacy, rate limits, and credential requirements before any manual use.

## Safety

- Source modified: no
- Workflow imported into n8n: no
- Workflow activated: no
- Workflow executed: no
- Credential values stored: no
- External APIs called: no
