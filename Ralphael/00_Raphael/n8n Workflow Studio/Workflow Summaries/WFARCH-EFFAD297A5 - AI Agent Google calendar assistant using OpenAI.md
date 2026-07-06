# Archived n8n Workflow WFARCH-EFFAD297A5

## Workflow ID

WFARCH-EFFAD297A5

## Name

AI Agent : Google calendar assistant using OpenAI

## Category

Automation

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1247_Googlecalendartool_Stickynote_Automation_Triggered.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 13
- Connections: 5
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.agent`
- `@n8n/n8n-nodes-langchain.chatTrigger`
- `@n8n/n8n-nodes-langchain.lmChatOpenAi`
- `@n8n/n8n-nodes-langchain.memoryBufferWindow`
- `n8n-nodes-base.googleCalendarTool`
- `n8n-nodes-base.stickyNote`

## API and Service Analysis

- Agent
- Chat Trigger
- Google Calendar Tool
- Lm Chat Open Ai
- Memory Buffer Window
- Sticky Note

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
