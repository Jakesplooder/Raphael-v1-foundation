# Archived n8n Workflow WFARCH-61A2EF5802

## Workflow ID

WFARCH-61A2EF5802

## Name

Hacker News to Video Template - AlexK1919

## Category

Creator

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1491_Linkedin_Wait_Create_Webhook.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 48
- Connections: 38
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.agent`
- `@n8n/n8n-nodes-langchain.lmChatOpenAi`
- `@n8n/n8n-nodes-langchain.openAi`
- `@n8n/n8n-nodes-langchain.outputParserStructured`
- `@n8n/n8n-nodes-langchain.toolHttpRequest`
- `n8n-nodes-base.dropbox`
- `n8n-nodes-base.googleDrive`
- `n8n-nodes-base.hackerNews`
- `n8n-nodes-base.httpRequest`
- `n8n-nodes-base.if`
- `n8n-nodes-base.limit`
- `n8n-nodes-base.linkedIn`
- `n8n-nodes-base.manualTrigger`
- `n8n-nodes-base.microsoftOneDrive`
- `n8n-nodes-base.s3`
- `n8n-nodes-base.set`
- `n8n-nodes-base.splitInBatches`
- `n8n-nodes-base.stickyNote`
- `n8n-nodes-base.twitter`
- `n8n-nodes-base.wait`
- `n8n-nodes-base.youTube`

## API and Service Analysis

- Agent
- Dropbox
- Google Drive
- Hacker News
- Http Request
- If
- Limit
- Linked In
- Lm Chat Open Ai
- Manual Trigger
- Microsoft One Drive
- Open Ai
- Output Parser Structured
- S3
- Set
- Split In Batches
- Sticky Note
- Tool Http Request
- Twitter
- Wait
- You Tube

## Required Credentials

- googleDriveOAuth2Api (type only; no credential value stored)
- httpCustomAuth (type only; no credential value stored)
- openAiApi (type only; no credential value stored)

## Reuse Assessment

- Reusable trigger/transform pattern: Yes
- Category relationship: Creator
- The workflow exposes a standard node list for structural analysis.
- Review node settings, platform terms, privacy, rate limits, and credential requirements before any manual use.

## Safety

- Source modified: no
- Workflow imported into n8n: no
- Workflow activated: no
- Workflow executed: no
- Credential values stored: no
- External APIs called: no
