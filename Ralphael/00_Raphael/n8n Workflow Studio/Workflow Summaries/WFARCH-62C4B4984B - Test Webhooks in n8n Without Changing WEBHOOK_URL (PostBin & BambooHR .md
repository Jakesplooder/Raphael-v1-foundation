# Archived n8n Workflow WFARCH-62C4B4984B

## Workflow ID

WFARCH-62C4B4984B

## Name

Test Webhooks in n8n Without Changing WEBHOOK_URL (PostBin & BambooHR Example)

## Category

Notifications

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1977_Wait_Splitout_Automation_Webhook.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 58
- Connections: 31
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.chainLlm`
- `@n8n/n8n-nodes-langchain.lmChatOpenAi`
- `@n8n/n8n-nodes-langchain.outputParserAutofixing`
- `@n8n/n8n-nodes-langchain.outputParserStructured`
- `n8n-nodes-base.aggregate`
- `n8n-nodes-base.bambooHr`
- `n8n-nodes-base.debugHelper`
- `n8n-nodes-base.filter`
- `n8n-nodes-base.httpRequest`
- `n8n-nodes-base.manualTrigger`
- `n8n-nodes-base.merge`
- `n8n-nodes-base.noOp`
- `n8n-nodes-base.postBin`
- `n8n-nodes-base.renameKeys`
- `n8n-nodes-base.set`
- `n8n-nodes-base.slack`
- `n8n-nodes-base.splitOut`
- `n8n-nodes-base.stickyNote`
- `n8n-nodes-base.wait`

## API and Service Analysis

- Aggregate
- Bamboo Hr
- Chain Llm
- Debug Helper
- Filter
- Http Request
- Lm Chat Open Ai
- Manual Trigger
- Merge
- No Op
- Output Parser Autofixing
- Output Parser Structured
- Post Bin
- Rename Keys
- Set
- Slack
- Split Out
- Sticky Note
- Wait

## Required Credentials

- bambooHrApi (type only; no credential value stored)
- httpBasicAuth (type only; no credential value stored)
- openAiApi (type only; no credential value stored)
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
