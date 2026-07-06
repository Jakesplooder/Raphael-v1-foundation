# Archived n8n Workflow WFARCH-9021326E98

## Workflow ID

WFARCH-9021326E98

## Name

0542_Wait_Redis_Create_Triggered

## Category

Automation

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

0542_Wait_Redis_Create_Triggered.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 18
- Connections: 12
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.agent`
- `@n8n/n8n-nodes-langchain.lmChatOpenAi`
- `@n8n/n8n-nodes-langchain.memoryBufferWindow`
- `@n8n/n8n-nodes-langchain.memoryManager`
- `n8n-nodes-base.if`
- `n8n-nodes-base.noOp`
- `n8n-nodes-base.redis`
- `n8n-nodes-base.set`
- `n8n-nodes-base.stickyNote`
- `n8n-nodes-base.twilio`
- `n8n-nodes-base.twilioTrigger`
- `n8n-nodes-base.wait`

## API and Service Analysis

- Agent
- If
- Lm Chat Open Ai
- Memory Buffer Window
- Memory Manager
- No Op
- Redis
- Set
- Sticky Note
- Twilio
- Twilio Trigger
- Wait

## Required Credentials

- openAiApi (type only; no credential value stored)
- redis (type only; no credential value stored)
- twilioApi (type only; no credential value stored)

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
