# Workflow Runner Overview

Raphael executes only enabled workflows from the local workflow registry after
confirmation. Execution is limited to local files, local services, local AI
tools, native Raphael functions, and approved localhost n8n workflows.

## Boundary

- No arbitrary shell commands
- No browser automation
- No publishing, uploads, spending, messaging, account access, or credentials
- No autonomous internet actions
- Cancellation is cooperative and checked between workflow stages
