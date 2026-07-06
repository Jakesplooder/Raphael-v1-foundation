# Archived n8n Workflow WFARCH-F4EB646AC1

## Workflow ID

WFARCH-F4EB646AC1

## Name

Agent Access Control Template

## Category

Notifications

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1856_Telegram_Stickynote_Automation_Webhook.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 36
- Connections: 21
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.agent`
- `@n8n/n8n-nodes-langchain.code`
- `@n8n/n8n-nodes-langchain.lmChatOpenAi`
- `@n8n/n8n-nodes-langchain.memoryBufferWindow`
- `@n8n/n8n-nodes-langchain.toolCalculator`
- `@n8n/n8n-nodes-langchain.toolCode`
- `@n8n/n8n-nodes-langchain.toolHttpRequest`
- `@n8n/n8n-nodes-langchain.toolWikipedia`
- `@n8n/n8n-nodes-langchain.toolWorkflow`
- `n8n-nodes-base.airtable`
- `n8n-nodes-base.executeWorkflowTrigger`
- `n8n-nodes-base.if`
- `n8n-nodes-base.set`
- `n8n-nodes-base.stickyNote`
- `n8n-nodes-base.telegram`
- `n8n-nodes-base.telegramTrigger`

## API and Service Analysis

- Agent
- Airtable
- Code
- Execute Workflow Trigger
- If
- Lm Chat Open Ai
- Memory Buffer Window
- Set
- Sticky Note
- Telegram
- Telegram Trigger
- Tool Calculator
- Tool Code
- Tool Http Request
- Tool Wikipedia
- Tool Workflow

## Required Credentials

- airtableTokenApi (type only; no credential value stored)
- openAiApi (type only; no credential value stored)
- telegramApi (type only; no credential value stored)

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
