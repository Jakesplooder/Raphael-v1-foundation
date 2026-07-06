# Archived n8n Workflow WFARCH-D083215438

## Workflow ID

WFARCH-D083215438

## Name

0815_Telegram_Code_Update_Triggered

## Category

Notifications

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

0815_Telegram_Code_Update_Triggered.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 39
- Connections: 28
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.agent`
- `@n8n/n8n-nodes-langchain.informationExtractor`
- `@n8n/n8n-nodes-langchain.lmChatOpenAi`
- `@n8n/n8n-nodes-langchain.memoryManager`
- `@n8n/n8n-nodes-langchain.memoryRedisChat`
- `@n8n/n8n-nodes-langchain.toolWorkflow`
- `n8n-nodes-base.code`
- `n8n-nodes-base.executeWorkflow`
- `n8n-nodes-base.executeWorkflowTrigger`
- `n8n-nodes-base.if`
- `n8n-nodes-base.redis`
- `n8n-nodes-base.stickyNote`
- `n8n-nodes-base.switch`
- `n8n-nodes-base.telegram`
- `n8n-nodes-base.telegramTrigger`

## API and Service Analysis

- Agent
- Code
- Execute Workflow
- Execute Workflow Trigger
- If
- Information Extractor
- Lm Chat Open Ai
- Memory Manager
- Memory Redis Chat
- Redis
- Sticky Note
- Switch
- Telegram
- Telegram Trigger
- Tool Workflow

## Required Credentials

- openAiApi (type only; no credential value stored)
- redis (type only; no credential value stored)
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
