# Archived n8n Workflow WFARCH-016AE87857

## Workflow ID

WFARCH-016AE87857

## Name

0725_Splitout_Code_Update_Triggered

## Category

Automation

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

0725_Splitout_Code_Update_Triggered.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 18
- Connections: 15
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.chainLlm`
- `@n8n/n8n-nodes-langchain.lmChatOllama`
- `@n8n/n8n-nodes-langchain.lmOllama`
- `n8n-nodes-base.aggregate`
- `n8n-nodes-base.code`
- `n8n-nodes-base.executeWorkflowTrigger`
- `n8n-nodes-base.filter`
- `n8n-nodes-base.manualTrigger`
- `n8n-nodes-base.merge`
- `n8n-nodes-base.set`
- `n8n-nodes-base.splitOut`
- `n8n-nodes-base.stickyNote`

## API and Service Analysis

- Aggregate
- Chain Llm
- Code
- Execute Workflow Trigger
- Filter
- Lm Chat Ollama
- Lm Ollama
- Manual Trigger
- Merge
- Set
- Split Out
- Sticky Note

## Required Credentials

- ollamaApi (type only; no credential value stored)

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
