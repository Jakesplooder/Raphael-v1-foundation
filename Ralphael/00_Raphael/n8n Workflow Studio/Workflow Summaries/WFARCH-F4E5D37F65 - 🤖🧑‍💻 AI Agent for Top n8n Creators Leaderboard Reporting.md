# Archived n8n Workflow WFARCH-F4E5D37F65

## Workflow ID

WFARCH-F4E5D37F65

## Name

🤖🧑‍💻 AI Agent  for Top n8n Creators Leaderboard Reporting

## Category

Creator

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1113_Telegram_Splitout_Automation_Scheduled.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 49
- Connections: 30
- Source marked active: True (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.agent`
- `@n8n/n8n-nodes-langchain.chainLlm`
- `@n8n/n8n-nodes-langchain.lmChatGoogleGemini`
- `@n8n/n8n-nodes-langchain.lmChatOpenAi`
- `@n8n/n8n-nodes-langchain.toolWorkflow`
- `n8n-nodes-base.aggregate`
- `n8n-nodes-base.convertToFile`
- `n8n-nodes-base.executeWorkflowTrigger`
- `n8n-nodes-base.gmail`
- `n8n-nodes-base.googleDrive`
- `n8n-nodes-base.httpRequest`
- `n8n-nodes-base.limit`
- `n8n-nodes-base.markdown`
- `n8n-nodes-base.merge`
- `n8n-nodes-base.readWriteFile`
- `n8n-nodes-base.scheduleTrigger`
- `n8n-nodes-base.set`
- `n8n-nodes-base.sort`
- `n8n-nodes-base.splitOut`
- `n8n-nodes-base.stickyNote`
- `n8n-nodes-base.telegram`

## API and Service Analysis

- Agent
- Aggregate
- Chain Llm
- Convert To File
- Execute Workflow Trigger
- Gmail
- Google Drive
- Http Request
- Limit
- Lm Chat Google Gemini
- Lm Chat Open Ai
- Markdown
- Merge
- Read Write File
- Schedule Trigger
- Set
- Sort
- Split Out
- Sticky Note
- Telegram
- Tool Workflow

## Required Credentials

- gmailOAuth2 (type only; no credential value stored)
- googleDriveOAuth2Api (type only; no credential value stored)
- googlePalmApi (type only; no credential value stored)
- openAiApi (type only; no credential value stored)
- telegramApi (type only; no credential value stored)

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
