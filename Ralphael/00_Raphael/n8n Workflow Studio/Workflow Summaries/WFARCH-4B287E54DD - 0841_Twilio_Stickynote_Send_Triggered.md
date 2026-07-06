# Archived n8n Workflow WFARCH-4B287E54DD

## Workflow ID

WFARCH-4B287E54DD

## Name

0841_Twilio_Stickynote_Send_Triggered

## Category

Automation

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

0841_Twilio_Stickynote_Send_Triggered.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 12
- Connections: 10
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.agent`
- `@n8n/n8n-nodes-langchain.lmChatOpenAi`
- `@n8n/n8n-nodes-langchain.memoryBufferWindow`
- `n8n-nodes-base.airtable`
- `n8n-nodes-base.airtableTool`
- `n8n-nodes-base.set`
- `n8n-nodes-base.stickyNote`
- `n8n-nodes-base.twilio`
- `n8n-nodes-base.twilioTrigger`

## API and Service Analysis

- Agent
- Airtable
- Airtable Tool
- Lm Chat Open Ai
- Memory Buffer Window
- Set
- Sticky Note
- Twilio
- Twilio Trigger

## Required Credentials

- airtableTokenApi (type only; no credential value stored)
- openAiApi (type only; no credential value stored)
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
