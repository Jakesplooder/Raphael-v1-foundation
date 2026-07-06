# Archived n8n Workflow WFARCH-F94DEB7EAA

## Workflow ID

WFARCH-F94DEB7EAA

## Name

0580_Code_Editimage_Import_Webhook

## Category

Automation

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

0580_Code_Editimage_Import_Webhook.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 20
- Connections: 11
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.chainLlm`
- `@n8n/n8n-nodes-langchain.informationExtractor`
- `@n8n/n8n-nodes-langchain.lmChatGoogleGemini`
- `n8n-nodes-base.aggregate`
- `n8n-nodes-base.code`
- `n8n-nodes-base.compression`
- `n8n-nodes-base.editImage`
- `n8n-nodes-base.googleDrive`
- `n8n-nodes-base.httpRequest`
- `n8n-nodes-base.manualTrigger`
- `n8n-nodes-base.sort`
- `n8n-nodes-base.stickyNote`

## API and Service Analysis

- Aggregate
- Chain Llm
- Code
- Compression
- Edit Image
- Google Drive
- Http Request
- Information Extractor
- Lm Chat Google Gemini
- Manual Trigger
- Sort
- Sticky Note

## Required Credentials

- googleDriveOAuth2Api (type only; no credential value stored)
- googlePalmApi (type only; no credential value stored)

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
