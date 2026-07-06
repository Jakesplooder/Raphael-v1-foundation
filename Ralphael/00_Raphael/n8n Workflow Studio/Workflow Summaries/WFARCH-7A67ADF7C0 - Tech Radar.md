# Archived n8n Workflow WFARCH-7A67ADF7C0

## Workflow ID

WFARCH-7A67ADF7C0

## Name

Tech Radar

## Category

Knowledge

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1836_Code_Googledocs_Automation_Webhook.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 53
- Connections: 32
- Source marked active: True (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.agent`
- `@n8n/n8n-nodes-langchain.chainLlm`
- `@n8n/n8n-nodes-langchain.documentDefaultDataLoader`
- `@n8n/n8n-nodes-langchain.embeddingsGoogleGemini`
- `@n8n/n8n-nodes-langchain.lmChatAnthropic`
- `@n8n/n8n-nodes-langchain.lmChatGoogleGemini`
- `@n8n/n8n-nodes-langchain.lmChatGroq`
- `@n8n/n8n-nodes-langchain.memoryBufferWindow`
- `@n8n/n8n-nodes-langchain.textSplitterRecursiveCharacterTextSplitter`
- `@n8n/n8n-nodes-langchain.toolVectorStore`
- `@n8n/n8n-nodes-langchain.vectorStorePinecone`
- `n8n-nodes-base.code`
- `n8n-nodes-base.cron`
- `n8n-nodes-base.executeWorkflow`
- `n8n-nodes-base.executeWorkflowTrigger`
- `n8n-nodes-base.googleDocs`
- `n8n-nodes-base.googleDrive`
- `n8n-nodes-base.googleDriveTrigger`
- `n8n-nodes-base.googleSheets`
- `n8n-nodes-base.if`
- `n8n-nodes-base.mySql`
- `n8n-nodes-base.mySqlTool`
- `n8n-nodes-base.respondToWebhook`
- `n8n-nodes-base.stickyNote`
- `n8n-nodes-base.webhook`

## API and Service Analysis

- Agent
- Chain Llm
- Code
- Cron
- Document Default Data Loader
- Embeddings Google Gemini
- Execute Workflow
- Execute Workflow Trigger
- Google Docs
- Google Drive
- Google Drive Trigger
- Google Sheets
- If
- Lm Chat Anthropic
- Lm Chat Google Gemini
- Lm Chat Groq
- Memory Buffer Window
- My Sql
- My Sql Tool
- Respond To Webhook
- Sticky Note
- Text Splitter Recursive Character Text Splitter
- Tool Vector Store
- Vector Store Pinecone
- Webhook

## Required Credentials

- anthropicApi (type only; no credential value stored)
- googleApi (type only; no credential value stored)
- googleDriveOAuth2Api (type only; no credential value stored)
- googlePalmApi (type only; no credential value stored)
- googleSheetsOAuth2Api (type only; no credential value stored)
- groqApi (type only; no credential value stored)
- mySql (type only; no credential value stored)
- pineconeApi (type only; no credential value stored)

## Reuse Assessment

- Reusable trigger/transform pattern: Yes
- Category relationship: Knowledge
- The workflow exposes a standard node list for structural analysis.
- Review node settings, platform terms, privacy, rate limits, and credential requirements before any manual use.

## Safety

- Source modified: no
- Workflow imported into n8n: no
- Workflow activated: no
- Workflow executed: no
- Credential values stored: no
- External APIs called: no
