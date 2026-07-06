# Archived n8n Workflow WFARCH-CE2D8CAD77

## Workflow ID

WFARCH-CE2D8CAD77

## Name

0816_Splitout_Code_Automation_Scheduled

## Category

Notifications

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

0816_Splitout_Code_Automation_Scheduled.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 30
- Connections: 24
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.lmChatOpenAi`
- `@n8n/n8n-nodes-langchain.textClassifier`
- `n8n-nodes-base.code`
- `n8n-nodes-base.discord`
- `n8n-nodes-base.executeWorkflow`
- `n8n-nodes-base.executeWorkflowTrigger`
- `n8n-nodes-base.filter`
- `n8n-nodes-base.if`
- `n8n-nodes-base.merge`
- `n8n-nodes-base.noOp`
- `n8n-nodes-base.removeDuplicates`
- `n8n-nodes-base.scheduleTrigger`
- `n8n-nodes-base.set`
- `n8n-nodes-base.splitInBatches`
- `n8n-nodes-base.splitOut`
- `n8n-nodes-base.stickyNote`
- `n8n-nodes-base.switch`

## API and Service Analysis

- Code
- Discord
- Execute Workflow
- Execute Workflow Trigger
- Filter
- If
- Lm Chat Open Ai
- Merge
- No Op
- Remove Duplicates
- Schedule Trigger
- Set
- Split In Batches
- Split Out
- Sticky Note
- Switch
- Text Classifier

## Required Credentials

- discordBotApi (type only; no credential value stored)
- openAiApi (type only; no credential value stored)

## Reuse Assessment

- Reusable trigger/transform pattern: Yes
- Category relationship: Notifications
- The workflow exposes a standard node list for structural analysis.
- Review node settings, platform terms, privacy, rate limits, and credential requirements before any manual use.

## Safety

- Source modified: no
- Workflow imported into n8n: no
- Workflow activated: no
- Workflow executed: no
- Credential values stored: no
- External APIs called: no
