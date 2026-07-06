# Archived n8n Workflow WFARCH-AE099E197E

## Workflow ID

WFARCH-AE099E197E

## Name

Email mailbox as Todoist tasks

## Category

Automation

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1749_Todoist_Schedule_Send_Scheduled.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 25
- Connections: 23
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.agent`
- `@n8n/n8n-nodes-langchain.lmChatOpenAi`
- `@n8n/n8n-nodes-langchain.outputParserStructured`
- `n8n-nodes-base.emailReadImap`
- `n8n-nodes-base.gmail`
- `n8n-nodes-base.if`
- `n8n-nodes-base.manualTrigger`
- `n8n-nodes-base.merge`
- `n8n-nodes-base.noOp`
- `n8n-nodes-base.scheduleTrigger`
- `n8n-nodes-base.stickyNote`
- `n8n-nodes-base.todoist`

## API and Service Analysis

- Agent
- Email Read Imap
- Gmail
- If
- Lm Chat Open Ai
- Manual Trigger
- Merge
- No Op
- Output Parser Structured
- Schedule Trigger
- Sticky Note
- Todoist

## Required Credentials

- gmailOAuth2 (type only; no credential value stored)
- imap (type only; no credential value stored)
- openAiApi (type only; no credential value stored)
- todoistApi (type only; no credential value stored)

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
