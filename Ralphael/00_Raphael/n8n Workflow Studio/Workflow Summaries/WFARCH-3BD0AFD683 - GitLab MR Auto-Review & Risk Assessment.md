# Archived n8n Workflow WFARCH-3BD0AFD683

## Workflow ID

WFARCH-3BD0AFD683

## Name

GitLab MR Auto-Review & Risk Assessment

## Category

Automation

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1895_Gitlab_Code_Automation_Webhook.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 23
- Connections: 13
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.agent`
- `@n8n/n8n-nodes-langchain.lmChatAnthropic`
- `@n8n/n8n-nodes-langchain.outputParserAutofixing`
- `@n8n/n8n-nodes-langchain.outputParserStructured`
- `n8n-nodes-base.code`
- `n8n-nodes-base.gitlabTrigger`
- `n8n-nodes-base.gmail`
- `n8n-nodes-base.httpRequest`
- `n8n-nodes-base.if`
- `n8n-nodes-base.merge`
- `n8n-nodes-base.stickyNote`

## API and Service Analysis

- Agent
- Code
- Gitlab Trigger
- Gmail
- Http Request
- If
- Lm Chat Anthropic
- Merge
- Output Parser Autofixing
- Output Parser Structured
- Sticky Note

## Required Credentials

- anthropicApi (type only; no credential value stored)
- gitlabApi (type only; no credential value stored)
- gmailOAuth2 (type only; no credential value stored)

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
