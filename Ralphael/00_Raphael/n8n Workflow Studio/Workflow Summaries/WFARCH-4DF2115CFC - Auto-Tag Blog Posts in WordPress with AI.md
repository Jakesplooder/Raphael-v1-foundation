# Archived n8n Workflow WFARCH-4DF2115CFC

## Workflow ID

WFARCH-4DF2115CFC

## Name

Auto-Tag Blog Posts in WordPress with AI

## Category

Research

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1980_Splitout_Code_Automation_Webhook.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 32
- Connections: 22
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.chainLlm`
- `@n8n/n8n-nodes-langchain.lmChatOpenAi`
- `@n8n/n8n-nodes-langchain.outputParserAutofixing`
- `@n8n/n8n-nodes-langchain.outputParserStructured`
- `n8n-nodes-base.aggregate`
- `n8n-nodes-base.code`
- `n8n-nodes-base.executeWorkflow`
- `n8n-nodes-base.executeWorkflowTrigger`
- `n8n-nodes-base.filter`
- `n8n-nodes-base.httpRequest`
- `n8n-nodes-base.if`
- `n8n-nodes-base.rssFeedReadTrigger`
- `n8n-nodes-base.set`
- `n8n-nodes-base.splitInBatches`
- `n8n-nodes-base.splitOut`
- `n8n-nodes-base.stickyNote`
- `n8n-nodes-base.wordpress`

## API and Service Analysis

- Aggregate
- Chain Llm
- Code
- Execute Workflow
- Execute Workflow Trigger
- Filter
- Http Request
- If
- Lm Chat Open Ai
- Output Parser Autofixing
- Output Parser Structured
- Rss Feed Read Trigger
- Set
- Split In Batches
- Split Out
- Sticky Note
- Wordpress

## Required Credentials

- openAiApi (type only; no credential value stored)
- wordpressApi (type only; no credential value stored)

## Reuse Assessment

- Reusable trigger/transform pattern: Yes
- Category relationship: Research
- The workflow exposes a standard node list for structural analysis.
- Review node settings, platform terms, privacy, rate limits, and credential requirements before any manual use.

## Safety

- Source modified: no
- Workflow imported into n8n: no
- Workflow activated: no
- Workflow executed: no
- Credential values stored: no
- External APIs called: no
