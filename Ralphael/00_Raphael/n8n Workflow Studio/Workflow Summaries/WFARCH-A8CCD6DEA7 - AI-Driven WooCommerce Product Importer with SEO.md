# Archived n8n Workflow WFARCH-A8CCD6DEA7

## Workflow ID

WFARCH-A8CCD6DEA7

## Name

AI-Driven WooCommerce Product Importer with SEO

## Category

Notifications

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1775_Telegram_Code_Import_Triggered.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 16
- Connections: 12
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.chainLlm`
- `@n8n/n8n-nodes-langchain.lmChatOpenRouter`
- `@n8n/n8n-nodes-langchain.outputParserStructured`
- `n8n-nodes-base.code`
- `n8n-nodes-base.googleSheets`
- `n8n-nodes-base.manualTrigger`
- `n8n-nodes-base.splitInBatches`
- `n8n-nodes-base.stickyNote`
- `n8n-nodes-base.telegram`
- `n8n-nodes-base.wooCommerce`

## API and Service Analysis

- Chain Llm
- Code
- Google Sheets
- Lm Chat Open Router
- Manual Trigger
- Output Parser Structured
- Split In Batches
- Sticky Note
- Telegram
- Woo Commerce

## Required Credentials

- googleSheetsOAuth2Api (type only; no credential value stored)
- openRouterApi (type only; no credential value stored)
- telegramApi (type only; no credential value stored)
- wooCommerceApi (type only; no credential value stored)

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
