# Archived n8n Workflow WFARCH-45E9D6A3AD

## Workflow ID

WFARCH-45E9D6A3AD

## Name

1434_Strapi_Splitout_Automation_Webhook

## Category

Automation

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1434_Strapi_Splitout_Automation_Webhook.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 36
- Connections: 32
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.chainLlm`
- `@n8n/n8n-nodes-langchain.lmChatOpenAi`
- `n8n-nodes-base.aggregate`
- `n8n-nodes-base.executeWorkflow`
- `n8n-nodes-base.executeWorkflowTrigger`
- `n8n-nodes-base.googleDrive`
- `n8n-nodes-base.googleSheets`
- `n8n-nodes-base.httpRequest`
- `n8n-nodes-base.if`
- `n8n-nodes-base.manualTrigger`
- `n8n-nodes-base.set`
- `n8n-nodes-base.splitInBatches`
- `n8n-nodes-base.splitOut`
- `n8n-nodes-base.stickyNote`
- `n8n-nodes-base.strapi`
- `n8n-nodes-base.switch`
- `n8n-nodes-base.webflow`
- `n8n-nodes-base.wordpress`

## API and Service Analysis

- Aggregate
- Chain Llm
- Execute Workflow
- Execute Workflow Trigger
- Google Drive
- Google Sheets
- Http Request
- If
- Lm Chat Open Ai
- Manual Trigger
- Set
- Split In Batches
- Split Out
- Sticky Note
- Strapi
- Switch
- Webflow
- Wordpress

## Required Credentials

- wordpressApi (type only; no credential value stored)

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
