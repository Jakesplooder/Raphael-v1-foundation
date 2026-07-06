# Archived n8n Workflow WFARCH-A0D3EB3AE6

## Workflow ID

WFARCH-A0D3EB3AE6

## Name

0910_Bitly_Datetime_Update_Webhook

## Category

Creator

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

0910_Bitly_Datetime_Update_Webhook.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 113
- Connections: 2
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@muench-dev/n8n-nodes-bluesky.bluesky`
- `@n8n/n8n-nodes-langchain.agent`
- `@n8n/n8n-nodes-langchain.chainLlm`
- `@n8n/n8n-nodes-langchain.chainRetrievalQa`
- `@n8n/n8n-nodes-langchain.chainSummarization`
- `@n8n/n8n-nodes-langchain.chatTrigger`
- `@n8n/n8n-nodes-langchain.documentDefaultDataLoader`
- `@n8n/n8n-nodes-langchain.embeddingsGoogleGemini`
- `@n8n/n8n-nodes-langchain.embeddingsOpenAi`
- `@n8n/n8n-nodes-langchain.informationExtractor`
- `@n8n/n8n-nodes-langchain.lmChatAnthropic`
- `@n8n/n8n-nodes-langchain.lmChatGoogleGemini`
- `@n8n/n8n-nodes-langchain.lmChatOpenAi`
- `@n8n/n8n-nodes-langchain.mcpClientTool`
- `@n8n/n8n-nodes-langchain.memoryBufferWindow`
- `@n8n/n8n-nodes-langchain.memoryManager`
- `@n8n/n8n-nodes-langchain.memoryPostgresChat`
- `@n8n/n8n-nodes-langchain.memoryRedisChat`
- `@n8n/n8n-nodes-langchain.openAi`
- `@n8n/n8n-nodes-langchain.outputParserAutofixing`
- `@n8n/n8n-nodes-langchain.outputParserItemList`
- `@n8n/n8n-nodes-langchain.outputParserStructured`
- `@n8n/n8n-nodes-langchain.sentimentAnalysis`
- `@n8n/n8n-nodes-langchain.textClassifier`
- `@n8n/n8n-nodes-langchain.toolCalculator`
- `@n8n/n8n-nodes-langchain.toolCode`
- `@n8n/n8n-nodes-langchain.toolHttpRequest`
- `@n8n/n8n-nodes-langchain.toolSerpApi`
- `@n8n/n8n-nodes-langchain.toolVectorStore`
- `@n8n/n8n-nodes-langchain.toolWikipedia`
- `@n8n/n8n-nodes-langchain.toolWolframAlpha`
- `@n8n/n8n-nodes-langchain.toolWorkflow`
- `@n8n/n8n-nodes-langchain.vectorStoreInMemory`
- `@n8n/n8n-nodes-langchain.vectorStorePGVector`
- `@n8n/n8n-nodes-langchain.vectorStorePinecone`
- `@n8n/n8n-nodes-langchain.vectorStoreSupabase`
- `@watzon/n8n-nodes-perplexity.perplexity`
- `n8n-nodes-base.aggregate`
- `n8n-nodes-base.aiTransform`
- `n8n-nodes-base.bitly`
- `n8n-nodes-base.calendlyTrigger`
- `n8n-nodes-base.code`
- `n8n-nodes-base.convertToFile`
- `n8n-nodes-base.dateTime`
- `n8n-nodes-base.dropbox`
- `n8n-nodes-base.emailReadImap`
- `n8n-nodes-base.emailSendTool`
- `n8n-nodes-base.executeCommand`
- `n8n-nodes-base.executeWorkflow`
- `n8n-nodes-base.executeWorkflowTrigger`
- `n8n-nodes-base.executionData`
- `n8n-nodes-base.extractFromFile`
- `n8n-nodes-base.filter`
- `n8n-nodes-base.formTrigger`
- `n8n-nodes-base.ftp`
- `n8n-nodes-base.gmail`
- `n8n-nodes-base.gmailTool`
- `n8n-nodes-base.gmailTrigger`
- `n8n-nodes-base.googleCalendar`
- `n8n-nodes-base.googleCalendarTool`
- `n8n-nodes-base.googleDocs`
- `n8n-nodes-base.googleDocsTool`
- `n8n-nodes-base.googleDriveTrigger`
- `n8n-nodes-base.googleSheets`
- `n8n-nodes-base.googleSheetsTool`
- `n8n-nodes-base.googleSheetsTrigger`
- `n8n-nodes-base.gumroadTrigger`
- `n8n-nodes-base.html`
- `n8n-nodes-base.httpRequest`
- `n8n-nodes-base.if`
- `n8n-nodes-base.limit`
- `n8n-nodes-base.localFileTrigger`
- `n8n-nodes-base.manualTrigger`
- `n8n-nodes-base.markdown`
- `n8n-nodes-base.merge`
- `n8n-nodes-base.noOp`
- `n8n-nodes-base.postgresTool`
- `n8n-nodes-base.pushbullet`
- `n8n-nodes-base.reddit`
- `n8n-nodes-base.redisTool`
- `n8n-nodes-base.removeDuplicates`
- `n8n-nodes-base.renameKeys`
- `n8n-nodes-base.respondToWebhook`
- `n8n-nodes-base.rssFeedRead`
- `n8n-nodes-base.scheduleTrigger`
- `n8n-nodes-base.set`
- `n8n-nodes-base.sort`
- `n8n-nodes-base.splitInBatches`
- `n8n-nodes-base.splitOut`
- `n8n-nodes-base.stickyNote`
- `n8n-nodes-base.summarize`
- `n8n-nodes-base.twitter`
- `n8n-nodes-base.wait`
- `n8n-nodes-base.webhook`
- `n8n-nodes-base.youTube`
- `n8n-nodes-elevenlabs.elevenLabs`

## API and Service Analysis

- Agent
- Aggregate
- Ai Transform
- Bitly
- Bluesky
- Calendly Trigger
- Chain Llm
- Chain Retrieval Qa
- Chain Summarization
- Chat Trigger
- Code
- Convert To File
- Date Time
- Document Default Data Loader
- Dropbox
- Eleven Labs
- Email Read Imap
- Email Send Tool
- Embeddings Google Gemini
- Embeddings Open Ai
- Execute Command
- Execute Workflow
- Execute Workflow Trigger
- Execution Data
- Extract From File
- Filter
- Form Trigger
- Ftp
- Gmail
- Gmail Tool
- Gmail Trigger
- Google Calendar
- Google Calendar Tool
- Google Docs
- Google Docs Tool
- Google Drive Trigger
- Google Sheets
- Google Sheets Tool
- Google Sheets Trigger
- Gumroad Trigger
- Html
- Http Request
- If
- Information Extractor
- Limit
- Lm Chat Anthropic
- Lm Chat Google Gemini
- Lm Chat Open Ai
- Local File Trigger
- Manual Trigger
- Markdown
- Mcp Client Tool
- Memory Buffer Window
- Memory Manager
- Memory Postgres Chat
- Memory Redis Chat
- Merge
- No Op
- Open Ai
- Output Parser Autofixing
- Output Parser Item List
- Output Parser Structured
- Perplexity
- Postgres Tool
- Pushbullet
- Reddit
- Redis Tool
- Remove Duplicates
- Rename Keys
- Respond To Webhook
- Rss Feed Read
- Schedule Trigger
- Sentiment Analysis
- Set
- Sort
- Split In Batches
- Split Out
- Sticky Note
- Summarize
- Text Classifier
- Tool Calculator
- Tool Code
- Tool Http Request
- Tool Serp Api
- Tool Vector Store
- Tool Wikipedia
- Tool Wolfram Alpha
- Tool Workflow
- Twitter
- Vector Store In Memory
- Vector Store P G Vector
- Vector Store Pinecone
- Vector Store Supabase
- Wait
- Webhook
- You Tube

## Required Credentials

- dropboxOAuth2Api (type only; no credential value stored)
- elevenLabsApi (type only; no credential value stored)
- googleCalendarOAuth2Api (type only; no credential value stored)
- googleDriveOAuth2Api (type only; no credential value stored)
- googleSheetsOAuth2Api (type only; no credential value stored)
- openAiApi (type only; no credential value stored)
- serpApi (type only; no credential value stored)

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
