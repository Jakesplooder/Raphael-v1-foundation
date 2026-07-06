# Archived n8n Workflow WFARCH-9932E126B6

## Workflow ID

WFARCH-9932E126B6

## Name

OpenAI Assistant with custom n8n tools

## Category

Automation

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1582_Summarize_Stickynote_Automation_Triggered.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 14
- Connections: 10
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.manualChatTrigger`
- `@n8n/n8n-nodes-langchain.openAiAssistant`
- `@n8n/n8n-nodes-langchain.toolCode`
- `@n8n/n8n-nodes-langchain.toolWorkflow`
- `n8n-nodes-base.code`
- `n8n-nodes-base.executeWorkflowTrigger`
- `n8n-nodes-base.if`
- `n8n-nodes-base.merge`
- `n8n-nodes-base.set`
- `n8n-nodes-base.stickyNote`
- `n8n-nodes-base.summarize`

## API and Service Analysis

- Code
- Execute Workflow Trigger
- If
- Manual Chat Trigger
- Merge
- Open Ai Assistant
- Set
- Sticky Note
- Summarize
- Tool Code
- Tool Workflow

## Required Credentials

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
