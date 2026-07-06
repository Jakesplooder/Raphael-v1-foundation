# Archived n8n Workflow WFARCH-AD799CB9FD

## Workflow ID

WFARCH-AD799CB9FD

## Name

Save New Sales Opportunities

## Category

Automation

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1565_Gmail_Stickynote_Create_Triggered.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 5
- Connections: 3
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.chainSummarization`
- `@n8n/n8n-nodes-langchain.lmOpenAi`
- `n8n-nodes-base.gmailTrigger`
- `n8n-nodes-base.odoo`
- `n8n-nodes-base.stickyNote`

## API and Service Analysis

- Chain Summarization
- Gmail Trigger
- Lm Open Ai
- Odoo
- Sticky Note

## Required Credentials

- gmailOAuth2 (type only; no credential value stored)
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
