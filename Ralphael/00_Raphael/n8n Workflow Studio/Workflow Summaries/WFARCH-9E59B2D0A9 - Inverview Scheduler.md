# Archived n8n Workflow WFARCH-9E59B2D0A9

## Workflow ID

WFARCH-9E59B2D0A9

## Name

Inverview Scheduler

## Category

Automation

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1813_Code_GoogleCalendar_Automation_Triggered.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 25
- Connections: 20
- Source marked active: True (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.agent`
- `@n8n/n8n-nodes-langchain.chatTrigger`
- `@n8n/n8n-nodes-langchain.lmChatOpenAi`
- `@n8n/n8n-nodes-langchain.memoryBufferWindow`
- `@n8n/n8n-nodes-langchain.outputParserStructured`
- `@n8n/n8n-nodes-langchain.toolWorkflow`
- `n8n-nodes-base.code`
- `n8n-nodes-base.executeWorkflowTrigger`
- `n8n-nodes-base.googleCalendar`
- `n8n-nodes-base.if`
- `n8n-nodes-base.merge`
- `n8n-nodes-base.noOp`
- `n8n-nodes-base.set`
- `n8n-nodes-base.stickyNote`

## API and Service Analysis

- Agent
- Chat Trigger
- Code
- Execute Workflow Trigger
- Google Calendar
- If
- Lm Chat Open Ai
- Memory Buffer Window
- Merge
- No Op
- Output Parser Structured
- Set
- Sticky Note
- Tool Workflow

## Required Credentials

- googleCalendarOAuth2Api (type only; no credential value stored)
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
