# Archived n8n Workflow WFARCH-DC52E1D7A5

## Workflow ID

WFARCH-DC52E1D7A5

## Name

Daily meetings summarization with Gemini AI

## Category

Notifications

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1891_Schedule_Slack_Automation_Scheduled.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 9
- Connections: 4
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.agent`
- `@n8n/n8n-nodes-langchain.lmChatGoogleGemini`
- `n8n-nodes-base.googleCalendarTool`
- `n8n-nodes-base.scheduleTrigger`
- `n8n-nodes-base.slack`
- `n8n-nodes-base.stickyNote`

## API and Service Analysis

- Agent
- Google Calendar Tool
- Lm Chat Google Gemini
- Schedule Trigger
- Slack
- Sticky Note

## Required Credentials

- googleCalendarOAuth2Api (type only; no credential value stored)
- googlePalmApi (type only; no credential value stored)
- slackApi (type only; no credential value stored)

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
