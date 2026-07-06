# Archived n8n Workflow WFARCH-6CBB4D2149

## Workflow ID

WFARCH-6CBB4D2149

## Name

0472_Aggregate_Gmail_Create_Triggered

## Category

Automation

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

0472_Aggregate_Gmail_Create_Triggered.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 19
- Connections: 11
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.chainLlm`
- `@n8n/n8n-nodes-langchain.lmChatOpenAi`
- `@n8n/n8n-nodes-langchain.outputParserStructured`
- `n8n-nodes-base.aggregate`
- `n8n-nodes-base.gmail`
- `n8n-nodes-base.gmailTrigger`
- `n8n-nodes-base.merge`
- `n8n-nodes-base.set`
- `n8n-nodes-base.splitOut`
- `n8n-nodes-base.stickyNote`

## API and Service Analysis

- Aggregate
- Chain Llm
- Gmail
- Gmail Trigger
- Lm Chat Open Ai
- Merge
- Output Parser Structured
- Set
- Split Out
- Sticky Note

## Required Credentials

- gmailOAuth2 (type only; no credential value stored)
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
