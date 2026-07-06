# Archived n8n Workflow WFARCH-54CAE57EF6

## Workflow ID

WFARCH-54CAE57EF6

## Name

🤖Calendar Agent

## Category

Automation

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1792_Googlecalendartool_Executeworkflow_Automation_Triggered.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 10
- Connections: 9
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.agent`
- `@n8n/n8n-nodes-langchain.lmChatOpenAi`
- `n8n-nodes-base.executeWorkflowTrigger`
- `n8n-nodes-base.googleCalendarTool`
- `n8n-nodes-base.set`

## API and Service Analysis

- Agent
- Execute Workflow Trigger
- Google Calendar Tool
- Lm Chat Open Ai
- Set

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
