# n8n-workflows-main

> Generated from a read-only source. The original files were not copied, modified, moved, renamed, deleted, overwritten, indexed, or uploaded.
> raphael-knowledge-summary: true

## Title

n8n-workflows-main

## Source Path Reference

`K:\n8n-workflows-main`

## Category

Programming

## Course

Not detected

## Technologies

- Python
- JavaScript
- C/C++
- SQL
- HTML/CSS
- Docker
- Git
- Excel
- PowerPoint

## Skills Demonstrated

- Implementation with Python, JavaScript, SQL/MySQL, HTML/CSS, Docker
- workflow automation
- systems integration
- testing and validation

## Summary

{} services: doc: image: workflows-doc:latest build: context: . ports: - "8000:8000" # N8N Workflows API Dependencies # Core API Framework fastapi>=0.104.0,<1.0.0 uvicorn[standard]>=0.24.0,<1.0.0 pydantic>=2.4.0,<3.0.0 { "name": "", "nodes": [ { "name": "SSE Trigger", "type": "n8n-nodes-base.sseTrigger", "position": [ 850, 420 ], "parameters": { "url": "https://n8n.io" }, "typeVersion": 1 } ], "active": false, "settings": {}, "connections": {} } { "nodes": [ { "name": "Mailjet Trigger", "type": "n8n-nodes-base.mailjetTrigger", "position": [ 530, 400 ], "parameters": { "event": "sent" }, "credentials": { "mailjetEmailApi": "mailjet creds" }, "typeVersion": 1 } ], "connections": {} } { "nodes": [ { "name": "AWS-SNS-Trigger", "type": "n8n-nodes-base.awsSnsTrigger", "position": [ 440, 300 ], "parameters": { "topic": "arn:aws:sns:ap-south-1:100558637562:n8n-rocks" }, "credentials": { "aws":...

## Files Found

- `n8n-workflows-main\n8n-workflows-main\CLAUDE.md` (.md, 4483 bytes)
- `n8n-workflows-main\n8n-workflows-main\CLAUDE_ZH.md` (.md, 3765 bytes)
- `n8n-workflows-main\n8n-workflows-main\README-nodejs.md` (.md, 7307 bytes)
- `n8n-workflows-main\n8n-workflows-main\README.md` (.md, 15213 bytes)
- `n8n-workflows-main\n8n-workflows-main\README_ZH.md` (.md, 12029 bytes)
- `n8n-workflows-main\n8n-workflows-main\api_server.py` (.py, 21291 bytes)
- `n8n-workflows-main\n8n-workflows-main\create_categories.py` (.py, 5081 bytes)
- `n8n-workflows-main\n8n-workflows-main\docker-compose.yml` (.yml, 108 bytes)
- `n8n-workflows-main\n8n-workflows-main\import_workflows.py` (.py, 5415 bytes)
- `n8n-workflows-main\n8n-workflows-main\package.json` (.json, 753 bytes)
- `n8n-workflows-main\n8n-workflows-main\requirements.txt` (.txt, 133 bytes)
- `n8n-workflows-main\n8n-workflows-main\run-as-docker-container.sh` (.sh, 468 bytes)
- `n8n-workflows-main\n8n-workflows-main\run.py` (.py, 4651 bytes)
- `n8n-workflows-main\n8n-workflows-main\start-nodejs.sh` (.sh, 1353 bytes)
- `n8n-workflows-main\n8n-workflows-main\workflow_db.py` (.py, 29671 bytes)
- `n8n-workflows-main\n8n-workflows-main\.devcontainer\devcontainer.json` (.json, 1829 bytes)
- `n8n-workflows-main\n8n-workflows-main\.devcontainer\init-firewall.sh` (.sh, 3805 bytes)
- `n8n-workflows-main\n8n-workflows-main\context\def_categories.json` (.json, 17056 bytes)
- `n8n-workflows-main\n8n-workflows-main\context\search_categories.json` (.json, 218875 bytes)
- `n8n-workflows-main\n8n-workflows-main\src\database.js` (.js, 18269 bytes)
- `n8n-workflows-main\n8n-workflows-main\src\index-workflows.js` (.js, 2894 bytes)
- `n8n-workflows-main\n8n-workflows-main\src\init-db.js` (.js, 1290 bytes)
- `n8n-workflows-main\n8n-workflows-main\src\server.js` (.js, 10996 bytes)
- `n8n-workflows-main\n8n-workflows-main\static\index-nodejs.html` (.html, 45387 bytes)
- `n8n-workflows-main\n8n-workflows-main\static\index.html` (.html, 45387 bytes)
- `n8n-workflows-main\n8n-workflows-main\workflows\0001_Telegram_Schedule_Automation_Scheduled.json` (.json, 16273 bytes)
- `n8n-workflows-main\n8n-workflows-main\workflows\0002_Manual_Totp_Automation_Triggered.json` (.json, 1398 bytes)
- `n8n-workflows-main\n8n-workflows-main\workflows\0003_Bitwarden_Automate.json` (.json, 2294 bytes)
- `n8n-workflows-main\n8n-workflows-main\workflows\0004_GoogleSheets_Typeform_Automate_Triggered.json` (.json, 3579 bytes)
- `n8n-workflows-main\n8n-workflows-main\workflows\0005_Manual_Twitter_Create_Triggered.json` (.json, 6021 bytes)
- `n8n-workflows-main\n8n-workflows-main\workflows\0006_Openweathermap_Cron_Automate_Scheduled.json` (.json, 1442 bytes)
- `n8n-workflows-main\n8n-workflows-main\workflows\0007_Manual_Todoist_Create_Triggered.json` (.json, 857 bytes)
- `n8n-workflows-main\n8n-workflows-main\workflows\0008_Slack_Stripe_Create_Triggered.json` (.json, 10002 bytes)
- `n8n-workflows-main\n8n-workflows-main\workflows\0009_Process.json` (.json, 4217 bytes)
- `n8n-workflows-main\n8n-workflows-main\workflows\0010_Writebinaryfile_Create.json` (.json, 1374 bytes)
- `n8n-workflows-main\n8n-workflows-main\workflows\0011_Manual_Copper_Automate_Triggered.json` (.json, 2394 bytes)
- `n8n-workflows-main\n8n-workflows-main\workflows\0012_Manual_Copper_Automate_Triggered.json` (.json, 2394 bytes)
- `n8n-workflows-main\n8n-workflows-main\workflows\0013_Manual_Noop_Import_Triggered.json` (.json, 5057 bytes)
- `n8n-workflows-main\n8n-workflows-main\workflows\0014_Manual_Coda_Create_Triggered.json` (.json, 1684 bytes)
- `n8n-workflows-main\n8n-workflows-main\workflows\0015_HTTP_Cron_Update_Webhook.json` (.json, 2825 bytes)
- `n8n-workflows-main\n8n-workflows-main\workflows\0016_Manual_Googleslides_Automate_Triggered.json` (.json, 1715 bytes)
- `n8n-workflows-main\n8n-workflows-main\workflows\0017_Mattermost_Emelia_Automate_Triggered.json` (.json, 1231 bytes)
- `n8n-workflows-main\n8n-workflows-main\workflows\0018_Manual_Chargebee_Create_Triggered.json` (.json, 949 bytes)
- `n8n-workflows-main\n8n-workflows-main\workflows\0019_Manual_Uproc_Send_Triggered.json` (.json, 2097 bytes)
- `n8n-workflows-main\n8n-workflows-main\workflows\0020_Mattermost_Emelia_Automate_Triggered.json` (.json, 1231 bytes)
- `n8n-workflows-main\n8n-workflows-main\workflows\0021_HTTP_Awssqs_Automation_Scheduled.json` (.json, 2673 bytes)
- `n8n-workflows-main\n8n-workflows-main\workflows\0022_Manual_Webflow_Automate_Triggered.json` (.json, 3272 bytes)
- `n8n-workflows-main\n8n-workflows-main\workflows\0023_HTTP_Googlebigquery_Automation_Scheduled.json` (.json, 2841 bytes)
- `n8n-workflows-main\n8n-workflows-main\workflows\0024_Manual_Clearbit_Send_Triggered.json` (.json, 917 bytes)
- `n8n-workflows-main\n8n-workflows-main\workflows\0025_Manual_Uproc_Automation_Triggered.json` (.json, 3605 bytes)
- `n8n-workflows-main\n8n-workflows-main\workflows\0026_Mailcheck_Airtable_Monitor.json` (.json, 2454 bytes)
- `n8n-workflows-main\n8n-workflows-main\workflows\0027_Mattermost_N8N_Automate_Triggered.json` (.json, 967 bytes)
- `n8n-workflows-main\n8n-workflows-main\workflows\0028_Mattermost_Workflow_Automate_Webhook.json` (.json, 1902 bytes)
- `n8n-workflows-main\n8n-workflows-main\workflows\0029_Manual_Orbit_Create_Triggered.json` (.json, 3252 bytes)
- `n8n-workflows-main\n8n-workflows-main\workflows\0030_Manual_Clickup_Create_Triggered.json` (.json, 946 bytes)
- `n8n-workflows-main\n8n-workflows-main\workflows\0031_Functionitem_Dropbox_Automation_Webhook.json` (.json, 6300 bytes)
- `n8n-workflows-main\n8n-workflows-main\workflows\0032_Manual_Filemaker_Automate_Triggered.json` (.json, 3159 bytes)
- `n8n-workflows-main\n8n-workflows-main\workflows\0033_HTTP_Mqtt_Automation_Webhook.json` (.json, 2534 bytes)
- `n8n-workflows-main\n8n-workflows-main\workflows\0034_Code_Filter_Create_Scheduled.json` (.json, 25754 bytes)
- `n8n-workflows-main\n8n-workflows-main\workflows\0035_GoogleSheets_Webhook_Automate_Webhook.json` (.json, 954 bytes)
- `n8n-workflows-main\n8n-workflows-main\workflows\0036_Gmail_GoogleDrive_Import.json` (.json, 1953 bytes)
- `n8n-workflows-main\n8n-workflows-main\workflows\0037_Manual_Googlebooks_Create_Triggered.json` (.json, 2310 bytes)
- `n8n-workflows-main\n8n-workflows-main\workflows\0038_Manual_Ical_Send_Triggered.json` (.json, 1609 bytes)
- `n8n-workflows-main\n8n-workflows-main\workflows\0039_Calendly_Notion_Automate_Triggered.json` (.json, 2041 bytes)
- `n8n-workflows-main\n8n-workflows-main\workflows\0040_Mattermost_Noop_Automate_Triggered.json` (.json, 2170 bytes)
- `n8n-workflows-main\n8n-workflows-main\workflows\0041_Chargebee_Update_Triggered.json` (.json, 416 bytes)
- `n8n-workflows-main\n8n-workflows-main\workflows\0042_Crypto_Airtable_Update_Webhook.json` (.json, 29534 bytes)
- `n8n-workflows-main\n8n-workflows-main\workflows\0043_Humanticai_Calendly_Automate_Triggered.json` (.json, 3024 bytes)
- `n8n-workflows-main\n8n-workflows-main\workflows\0044_Trello_Googlecloudnaturallanguage_Automate_Triggered.json` (.json, 4225 bytes)
- `n8n-workflows-main\n8n-workflows-main\workflows\0045_Manual_Telegram_Import_Triggered.json` (.json, 2841 bytes)
- `n8n-workflows-main\n8n-workflows-main\workflows\0046_Manual_Storyblok_Import_Triggered.json` (.json, 1738 bytes)
- `n8n-workflows-main\n8n-workflows-main\workflows\0047_Clickup_Update_Triggered.json` (.json, 515 bytes)
- `n8n-workflows-main\n8n-workflows-main\workflows\0048_HTTP_Htmlextract_Create_Webhook.json` (.json, 4513 bytes)
- `n8n-workflows-main\n8n-workflows-main\workflows\0049_Manual_Awss3_Automate_Triggered.json` (.json, 1550 bytes)
- `n8n-workflows-main\n8n-workflows-main\workflows\0050_Uptimerobot_Automate.json` (.json, 1753 bytes)
- `n8n-workflows-main\n8n-workflows-main\workflows\0051_Manual_Microsofttodo_Automate_Triggered.json` (.json, 2445 bytes)
- `n8n-workflows-main\n8n-workflows-main\workflows\0052_Manual_Git_Automate_Triggered.json` (.json, 2260 bytes)
- `n8n-workflows-main\n8n-workflows-main\workflows\0053_Trello_GoogleCalendar_Create_Scheduled.json` (.json, 6439 bytes)
- `n8n-workflows-main\n8n-workflows-main\workflows\0054_Manual_Writebinaryfile_Automate_Triggered.json` (.json, 2587 bytes)
- `n8n-workflows-main\n8n-workflows-main\workflows\0055_Signl4_Interval_Create_Scheduled.json` (.json, 12324 bytes)
- `n8n-workflows-main\n8n-workflows-main\workflows\0056_Manual_Uproc_Import_Triggered.json` (.json, 2306 bytes)
- `n8n-workflows-main\n8n-workflows-main\workflows\0057_Activecampaign_Create_Triggered.json` (.json, 590 bytes)
- `n8n-workflows-main\n8n-workflows-main\workflows\0058_Manual_Readbinaryfile_Automate_Triggered.json` (.json, 1381 bytes)
- `n8n-workflows-main\n8n-workflows-main\workflows\0059_Manual_Twitter_Automate_Triggered.json` (.json, 1832 bytes)
- `n8n-workflows-main\n8n-workflows-main\workflows\0060_Travisci_GitHub_Automate_Triggered.json` (.json, 2240 bytes)
- `n8n-workflows-main\n8n-workflows-main\workflows\0061_Noop_GitHub_Automate_Triggered.json` (.json, 2673 bytes)
- `n8n-workflows-main\n8n-workflows-main\workflows\0062_Manual_Pipedrive_Create_Triggered.json` (.json, 871 bytes)
- `n8n-workflows-main\n8n-workflows-main\workflows\0063_Manual_Uproc_Import_Triggered.json` (.json, 1483 bytes)
- `n8n-workflows-main\n8n-workflows-main\workflows\0064_Manual_Writebinaryfile_Automate_Triggered.json` (.json, 1402 bytes)
- `n8n-workflows-main\n8n-workflows-main\workflows\0065_Openweathermap_Line_Update_Scheduled.json` (.json, 1595 bytes)
- `n8n-workflows-main\n8n-workflows-main\workflows\0066_Webhook_Cron_Automate_Scheduled.json` (.json, 25613 bytes)
- `n8n-workflows-main\n8n-workflows-main\workflows\0067_Manual_Uproc_Automation_Triggered.json` (.json, 2120 bytes)
- `n8n-workflows-main\n8n-workflows-main\workflows\0068_Functionitem_Manual_Import_Scheduled.json` (.json, 5138 bytes)
- `n8n-workflows-main\n8n-workflows-main\workflows\0069_Manual_Gmail_Automation_Triggered.json` (.json, 2168 bytes)
- `n8n-workflows-main\n8n-workflows-main\workflows\0070_Splitinbatches_Notion_Export_Scheduled.json` (.json, 6744 bytes)
- `n8n-workflows-main\n8n-workflows-main\workflows\0071_Pipedrive_Update_Triggered.json` (.json, 428 bytes)
- `n8n-workflows-main\n8n-workflows-main\workflows\0072_Openweathermap_Cron_Update_Scheduled.json` (.json, 1662 bytes)
- `n8n-workflows-main\n8n-workflows-main\workflows\0073_Manual_Rssfeedread_Automate_Triggered.json` (.json, 3155 bytes)
- `n8n-workflows-main\n8n-workflows-main\workflows\0074_Manual_HTTP_Monitor_Webhook.json` (.json, 4875 bytes)
- `n8n-workflows-main\n8n-workflows-main\workflows\0075_Manual_Noop_Update_Triggered.json` (.json, 2529 bytes)
- ...and 1979 more supported files.

## Portfolio Value

Medium — Curated score 66/100.

## Resume Bullet Potential

- Built or completed **n8n-workflows-main** using Python, JavaScript, C/C++, SQL, HTML/CSS, Docker, Git, Excel, PowerPoint, demonstrating technical implementation, documentation and presentation.
- Add measurable outcomes, scope, grade, users, or performance results after human review.

## Lessons Learned

- Preserve requirements, decisions, tests, and final outcomes together so the project remains explainable later.
- Review this generated summary against the original source before using it in a resume or portfolio.

## Suggested Tags

- #c-c++
- #docker
- #excel
- #git
- #html-css
- #javascript
- #powerpoint
- #programming
- #python
- #sql

## Related Raphael Projects/Goals

- Project: Sports South Integration
- Project: Secure Email Service

## Safety Record

- Source access: read-only
- Source files copied: no
- Raw source indexed: no
- Credential-bearing files/content: skipped
- External uploads: none

## Knowledge ID

KNOW-3F7C86815B

## Course Code

Not detected

## Course Name

Not detected

## Suggested Title

n8n Workflow Automation Collection

## Project Type

AI/Automation Project

## Technology Stack

- Python
- JavaScript
- SQL/MySQL
- HTML/CSS
- Docker

## Assignment/Project Status

Starter/Incomplete

## Portfolio Score

66/100

## Resume Value

6/10

## Outcome

Unclear — human curation needed.

## Likely Duplicates

- None detected.

## Curation Flags

- course-not-detected
- possibly-incomplete

## Cleanup Suggestions

- Identify authored workflows, use cases, integrations, and measurable automation outcomes.

## Classification Scores

- Technical depth: 9/10
- Completeness: 3/10
- Uniqueness: 5/10
- Career relevance: 8/10
- Demo potential: 7/10
- Resume value: 6/10
- Business relevance: 8/10
- Cleanup effort: 8/10

## Knowledge Relationships

- `KNOW-8EE4596287` LCIntel — same_cluster (0.89): AI / Automation Cluster, Web Development Cluster
- `KNOW-19023766AB` ajanua3_proj2 — same_cluster (0.88): Web Development Cluster
- `KNOW-21573891BF` Substitution Cipher Cryptanalysis — same_cluster (0.88): Web Development Cluster
- `KNOW-2EC4964E43` ISDS 4123 slides — same_cluster (0.88): Data / Information Systems Cluster
- `KNOW-30CFB55791` Lecture-4-Support — same_cluster (0.88): Data / Information Systems Cluster
- `KNOW-3908539F68` Tune Trails React Application — same_cluster (0.88): Web Development Cluster
- `KNOW-4F5C580EBD` csc4103-fall2024-assignment2-Jakesplooder — same_cluster (0.88): Web Development Cluster
- `KNOW-668F0A4293` Homework3 answer — same_cluster (0.88): Data / Information Systems Cluster
- `KNOW-70F2729989` Substitution Cipher Cryptanalysis — same_cluster (0.88): Web Development Cluster
- `KNOW-79704F770D` project-bolt-sb1-nkcemgrw React Application — same_cluster (0.88): Web Development Cluster
- `KNOW-BDFE213910` K Drive Knowledge Root — shared_technology (0.88): JavaScript, Python, SQL/MySQL
- `KNOW-D6BEEF0339` Substitution Cipher Cryptanalysis — same_cluster (0.88): Web Development Cluster
- `KNOW-DF38FE1F9F` Assignment 1 — same_cluster (0.88): Data / Information Systems Cluster
- `KNOW-EF35C895C3` Substitution Cipher Cryptanalysis — same_cluster (0.88): Web Development Cluster
- `KNOW-21573891BF` Substitution Cipher Cryptanalysis — shared_technology (0.87): JavaScript, Python
- `KNOW-3908539F68` Tune Trails React Application — shared_technology (0.87): HTML/CSS, JavaScript
- `KNOW-668F0A4293` Homework3 answer — shared_technology (0.87): Python, SQL/MySQL
- `KNOW-70F2729989` Substitution Cipher Cryptanalysis — shared_technology (0.87): JavaScript, Python
- `KNOW-8EE4596287` LCIntel — shared_technology (0.87): JavaScript, Python
- `KNOW-CEB9F6D3FF` React — shared_technology (0.87): HTML/CSS, JavaScript

## Relationship Concepts

- Technology Relationship: Python (0.92)
- Technology Relationship: JavaScript (0.92)
- Technology Relationship: SQL/MySQL (0.92)
- Technology Relationship: HTML/CSS (0.92)
- Technology Relationship: Docker (0.92)
- Project Family Relationship: AI/Automation Project (0.90)
- Project Family Relationship: Web Development Cluster (0.88)
- Project Family Relationship: AI / Automation Cluster (0.88)
- Project Family Relationship: Data / Information Systems Cluster (0.88)
- Skill Relationship: Implementation with Python, JavaScript, SQL/MySQL, HTML/CSS, Docker (0.84)
- Skill Relationship: workflow automation (0.84)
- Skill Relationship: systems integration (0.84)
- Skill Relationship: testing and validation (0.84)
- Career Relationship: Software Engineering (0.82)
- Career Relationship: AI / Automation (0.82)
- Career Relationship: Web Development (0.82)
- Career Relationship: Data Engineering (0.82)
- Career Relationship: Cloud / DevOps (0.82)
- Business Relationship: Agency (0.76)
- Business Relationship: AI Products (0.76)
- Business Relationship: Local SaaS (0.76)
- Business Relationship: Raphael OS (0.76)
- Portfolio Relationship: Tier 2 (0.72)
- Employee Skill Relationship: Developer Agent (0.72)
- Employee Skill Relationship: AI Researcher Agent (0.72)
- Employee Skill Relationship: Machine Learning AI Engineer Agent (0.72)
- Employee Skill Relationship: Data Analyst Agent (0.72)
- Council Relationship: Agency Council (0.68)

## Relationship Metadata

- Generated: 2026-06-18T00:20:50
- Direct relationships: 20
- Concept relationships: 28
