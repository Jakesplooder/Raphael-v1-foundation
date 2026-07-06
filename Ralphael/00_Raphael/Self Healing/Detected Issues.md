# Detected Issues

## ISSUE-20260627-365C0FF1

- Severity: warning
- Affected system: N8N
- Symptoms: n8n health check failed
- Probable cause: <urlopen error timed out>
- Evidence: {"ok": false, "detail": "<urlopen error timed out>", "url": "http://127.0.0.1:5678/healthz"}
- Recommended fix: start n8n through Service Manager
- Repairability: approval_required
- Risk level: medium
- Related logs: None
- Related command: `python raphael.py service-start n8n`

## ISSUE-20260627-C2987D7B

- Severity: critical
- Affected system: Dashboard
- Symptoms: dashboard health check failed
- Probable cause: timed out
- Evidence: {"ok": false, "detail": "timed out", "url": "http://127.0.0.1:8787/api/health"}
- Recommended fix: restart Dashboard through Service Manager
- Repairability: approval_required
- Risk level: low
- Related logs: None
- Related command: `python raphael.py service-restart dashboard`

## ISSUE-20260627-342602EE

- Severity: warning
- Affected system: Docker Manager
- Symptoms: Container raphael-qdrant exists but is not Raphael-managed
- Probable cause: Container ownership labels or image do not match the Docker registry.
- Evidence: {"service_id": "qdrant", "display_name": "Qdrant", "enabled": true, "image": "qdrant/qdrant", "container_name": "raphael-qdrant", "ports": ["127.0.0.1:6333:6333"], "volumes": ["C:\\RaphaelOS\\docker\\qdrant:/qdrant/storage"], "health_check": "http://127.0.0.1:6333", "notes": "Local vector memory service.", "exists": true, "running": true, "managed": false, "conflict": true, "container_id": "a0e50c94930a", "actual_image": "qdrant/qdrant", "state": "running"}
- Recommended fix: Review the container manually; Raphael will not stop or adopt unmanaged containers.
- Repairability: manual
- Risk level: medium
- Related logs: None
- Related command: `python raphael.py docker-status`

## ISSUE-20260627-D3A15704

- Severity: info
- Affected system: Confirmation System
- Symptoms: POD workflow PODFLOW-20260624-8E3E3A60 has waited for confirmation for more than 24 hours
- Probable cause: A previous confirmation prompt was not completed or cancelled.
- Evidence: {"workflow_id": "PODFLOW-20260624-8E3E3A60", "status": "awaiting_confirmation", "updated": "2026-06-24T23:31:15"}
- Recommended fix: Clear or replace the stale confirmation by explicitly continuing or cancelling the workflow.
- Repairability: approval_required
- Risk level: low
- Related logs: None
- Related command: `python raphael.py pod-workflow-show PODFLOW-20260624-8E3E3A60`

## ISSUE-20260627-2BA26DDD

- Severity: info
- Affected system: Confirmation System
- Symptoms: POD workflow PODFLOW-20260624-2579E0BF has waited for confirmation for more than 24 hours
- Probable cause: A previous confirmation prompt was not completed or cancelled.
- Evidence: {"workflow_id": "PODFLOW-20260624-2579E0BF", "status": "awaiting_confirmation", "updated": "2026-06-24T23:26:20"}
- Recommended fix: Clear or replace the stale confirmation by explicitly continuing or cancelling the workflow.
- Repairability: approval_required
- Risk level: low
- Related logs: None
- Related command: `python raphael.py pod-workflow-show PODFLOW-20260624-2579E0BF`

## ISSUE-20260627-DD9B6AF2

- Severity: info
- Affected system: Confirmation System
- Symptoms: POD workflow PODFLOW-20260624-483D5C16 has waited for confirmation for more than 24 hours
- Probable cause: A previous confirmation prompt was not completed or cancelled.
- Evidence: {"workflow_id": "PODFLOW-20260624-483D5C16", "status": "awaiting_confirmation", "updated": "2026-06-24T23:06:36"}
- Recommended fix: Clear or replace the stale confirmation by explicitly continuing or cancelling the workflow.
- Repairability: approval_required
- Risk level: low
- Related logs: None
- Related command: `python raphael.py pod-workflow-show PODFLOW-20260624-483D5C16`

## ISSUE-20260627-BE2C354B

- Severity: info
- Affected system: Confirmation System
- Symptoms: POD workflow PODFLOW-20260624-B98527D8 has waited for confirmation for more than 24 hours
- Probable cause: A previous confirmation prompt was not completed or cancelled.
- Evidence: {"workflow_id": "PODFLOW-20260624-B98527D8", "status": "awaiting_confirmation", "updated": "2026-06-24T19:35:10"}
- Recommended fix: Clear or replace the stale confirmation by explicitly continuing or cancelling the workflow.
- Repairability: approval_required
- Risk level: low
- Related logs: None
- Related command: `python raphael.py pod-workflow-show PODFLOW-20260624-B98527D8`

## ISSUE-20260627-BD7EC6E2

- Severity: info
- Affected system: Confirmation System
- Symptoms: POD workflow PODFLOW-20260624-CFAA3B63 has waited for confirmation for more than 24 hours
- Probable cause: A previous confirmation prompt was not completed or cancelled.
- Evidence: {"workflow_id": "PODFLOW-20260624-CFAA3B63", "status": "awaiting_confirmation", "updated": "2026-06-24T19:34:15"}
- Recommended fix: Clear or replace the stale confirmation by explicitly continuing or cancelling the workflow.
- Repairability: approval_required
- Risk level: low
- Related logs: None
- Related command: `python raphael.py pod-workflow-show PODFLOW-20260624-CFAA3B63`

## ISSUE-20260627-E5A57905

- Severity: info
- Affected system: Confirmation System
- Symptoms: POD workflow PODFLOW-20260624-FD9A383D has waited for confirmation for more than 24 hours
- Probable cause: A previous confirmation prompt was not completed or cancelled.
- Evidence: {"workflow_id": "PODFLOW-20260624-FD9A383D", "status": "awaiting_confirmation", "updated": "2026-06-24T19:34:09"}
- Recommended fix: Clear or replace the stale confirmation by explicitly continuing or cancelling the workflow.
- Repairability: approval_required
- Risk level: low
- Related logs: None
- Related command: `python raphael.py pod-workflow-show PODFLOW-20260624-FD9A383D`

## ISSUE-20260627-9D8AD8F4

- Severity: info
- Affected system: Confirmation System
- Symptoms: POD workflow PODFLOW-20260624-E6D5FDE7 has waited for confirmation for more than 24 hours
- Probable cause: A previous confirmation prompt was not completed or cancelled.
- Evidence: {"workflow_id": "PODFLOW-20260624-E6D5FDE7", "status": "awaiting_confirmation", "updated": "2026-06-24T05:12:44"}
- Recommended fix: Clear or replace the stale confirmation by explicitly continuing or cancelling the workflow.
- Repairability: approval_required
- Risk level: low
- Related logs: None
- Related command: `python raphael.py pod-workflow-show PODFLOW-20260624-E6D5FDE7`

## ISSUE-20260627-E12869FC

- Severity: info
- Affected system: Confirmation System
- Symptoms: POD workflow PODFLOW-20260624-2641C434 has waited for confirmation for more than 24 hours
- Probable cause: A previous confirmation prompt was not completed or cancelled.
- Evidence: {"workflow_id": "PODFLOW-20260624-2641C434", "status": "awaiting_confirmation", "updated": "2026-06-24T05:11:54"}
- Recommended fix: Clear or replace the stale confirmation by explicitly continuing or cancelling the workflow.
- Repairability: approval_required
- Risk level: low
- Related logs: None
- Related command: `python raphael.py pod-workflow-show PODFLOW-20260624-2641C434`

## ISSUE-20260627-276E4D60

- Severity: info
- Affected system: Confirmation System
- Symptoms: POD workflow PODFLOW-20260624-DE369D58 has waited for confirmation for more than 24 hours
- Probable cause: A previous confirmation prompt was not completed or cancelled.
- Evidence: {"workflow_id": "PODFLOW-20260624-DE369D58", "status": "awaiting_confirmation", "updated": "2026-06-24T05:11:48"}
- Recommended fix: Clear or replace the stale confirmation by explicitly continuing or cancelling the workflow.
- Repairability: approval_required
- Risk level: low
- Related logs: None
- Related command: `python raphael.py pod-workflow-show PODFLOW-20260624-DE369D58`

## ISSUE-20260627-3ABC14CF

- Severity: info
- Affected system: Confirmation System
- Symptoms: POD workflow PODFLOW-20260624-D0AF7438 has waited for confirmation for more than 24 hours
- Probable cause: A previous confirmation prompt was not completed or cancelled.
- Evidence: {"workflow_id": "PODFLOW-20260624-D0AF7438", "status": "awaiting_confirmation", "updated": "2026-06-24T05:10:37"}
- Recommended fix: Clear or replace the stale confirmation by explicitly continuing or cancelling the workflow.
- Repairability: approval_required
- Risk level: low
- Related logs: None
- Related command: `python raphael.py pod-workflow-show PODFLOW-20260624-D0AF7438`

## ISSUE-20260627-E8EC2F42

- Severity: info
- Affected system: Confirmation System
- Symptoms: POD workflow PODFLOW-20260624-1F5B9C16 has waited for confirmation for more than 24 hours
- Probable cause: A previous confirmation prompt was not completed or cancelled.
- Evidence: {"workflow_id": "PODFLOW-20260624-1F5B9C16", "status": "awaiting_confirmation", "updated": "2026-06-24T05:09:46"}
- Recommended fix: Clear or replace the stale confirmation by explicitly continuing or cancelling the workflow.
- Repairability: approval_required
- Risk level: low
- Related logs: None
- Related command: `python raphael.py pod-workflow-show PODFLOW-20260624-1F5B9C16`

## ISSUE-20260627-7B07FD67

- Severity: info
- Affected system: Confirmation System
- Symptoms: POD workflow PODFLOW-20260624-F7B49254 has waited for confirmation for more than 24 hours
- Probable cause: A previous confirmation prompt was not completed or cancelled.
- Evidence: {"workflow_id": "PODFLOW-20260624-F7B49254", "status": "awaiting_confirmation", "updated": "2026-06-24T05:09:40"}
- Recommended fix: Clear or replace the stale confirmation by explicitly continuing or cancelling the workflow.
- Repairability: approval_required
- Risk level: low
- Related logs: None
- Related command: `python raphael.py pod-workflow-show PODFLOW-20260624-F7B49254`

## ISSUE-20260627-09BB9502

- Severity: info
- Affected system: Confirmation System
- Symptoms: POD workflow PODFLOW-20260624-899EE44F has waited for confirmation for more than 24 hours
- Probable cause: A previous confirmation prompt was not completed or cancelled.
- Evidence: {"workflow_id": "PODFLOW-20260624-899EE44F", "status": "awaiting_confirmation", "updated": "2026-06-24T05:08:26"}
- Recommended fix: Clear or replace the stale confirmation by explicitly continuing or cancelling the workflow.
- Repairability: approval_required
- Risk level: low
- Related logs: None
- Related command: `python raphael.py pod-workflow-show PODFLOW-20260624-899EE44F`

## ISSUE-20260627-429CF379

- Severity: info
- Affected system: Confirmation System
- Symptoms: POD workflow PODFLOW-20260624-22EC0874 has waited for confirmation for more than 24 hours
- Probable cause: A previous confirmation prompt was not completed or cancelled.
- Evidence: {"workflow_id": "PODFLOW-20260624-22EC0874", "status": "awaiting_confirmation", "updated": "2026-06-24T05:08:20"}
- Recommended fix: Clear or replace the stale confirmation by explicitly continuing or cancelling the workflow.
- Repairability: approval_required
- Risk level: low
- Related logs: None
- Related command: `python raphael.py pod-workflow-show PODFLOW-20260624-22EC0874`

## ISSUE-20260627-BC90E702

- Severity: info
- Affected system: Confirmation System
- Symptoms: POD workflow PODFLOW-20260624-62116D97 has waited for confirmation for more than 24 hours
- Probable cause: A previous confirmation prompt was not completed or cancelled.
- Evidence: {"workflow_id": "PODFLOW-20260624-62116D97", "status": "awaiting_confirmation", "updated": "2026-06-24T05:06:53"}
- Recommended fix: Clear or replace the stale confirmation by explicitly continuing or cancelling the workflow.
- Repairability: approval_required
- Risk level: low
- Related logs: None
- Related command: `python raphael.py pod-workflow-show PODFLOW-20260624-62116D97`

## ISSUE-20260627-3CE52C75

- Severity: info
- Affected system: Confirmation System
- Symptoms: POD workflow PODFLOW-20260624-474E7476 has waited for confirmation for more than 24 hours
- Probable cause: A previous confirmation prompt was not completed or cancelled.
- Evidence: {"workflow_id": "PODFLOW-20260624-474E7476", "status": "awaiting_confirmation", "updated": "2026-06-24T05:06:47"}
- Recommended fix: Clear or replace the stale confirmation by explicitly continuing or cancelling the workflow.
- Repairability: approval_required
- Risk level: low
- Related logs: None
- Related command: `python raphael.py pod-workflow-show PODFLOW-20260624-474E7476`

## ISSUE-20260627-861B9BA5

- Severity: info
- Affected system: Confirmation System
- Symptoms: POD workflow PODFLOW-20260624-F8F89E90 has waited for confirmation for more than 24 hours
- Probable cause: A previous confirmation prompt was not completed or cancelled.
- Evidence: {"workflow_id": "PODFLOW-20260624-F8F89E90", "status": "awaiting_confirmation", "updated": "2026-06-24T05:05:46"}
- Recommended fix: Clear or replace the stale confirmation by explicitly continuing or cancelling the workflow.
- Repairability: approval_required
- Risk level: low
- Related logs: None
- Related command: `python raphael.py pod-workflow-show PODFLOW-20260624-F8F89E90`

## ISSUE-20260627-E770FD8A

- Severity: info
- Affected system: Confirmation System
- Symptoms: POD workflow PODFLOW-20260624-8F08C581 has waited for confirmation for more than 24 hours
- Probable cause: A previous confirmation prompt was not completed or cancelled.
- Evidence: {"workflow_id": "PODFLOW-20260624-8F08C581", "status": "awaiting_confirmation", "updated": "2026-06-24T05:05:39"}
- Recommended fix: Clear or replace the stale confirmation by explicitly continuing or cancelling the workflow.
- Repairability: approval_required
- Risk level: low
- Related logs: None
- Related command: `python raphael.py pod-workflow-show PODFLOW-20260624-8F08C581`

## ISSUE-20260627-E7C8066A

- Severity: info
- Affected system: Confirmation System
- Symptoms: POD workflow PODFLOW-20260624-2F11C155 has waited for confirmation for more than 24 hours
- Probable cause: A previous confirmation prompt was not completed or cancelled.
- Evidence: {"workflow_id": "PODFLOW-20260624-2F11C155", "status": "awaiting_confirmation", "updated": "2026-06-24T04:57:31"}
- Recommended fix: Clear or replace the stale confirmation by explicitly continuing or cancelling the workflow.
- Repairability: approval_required
- Risk level: low
- Related logs: None
- Related command: `python raphael.py pod-workflow-show PODFLOW-20260624-2F11C155`

## ISSUE-20260627-CED26076

- Severity: info
- Affected system: Confirmation System
- Symptoms: POD workflow PODFLOW-20260624-F83B438A has waited for confirmation for more than 24 hours
- Probable cause: A previous confirmation prompt was not completed or cancelled.
- Evidence: {"workflow_id": "PODFLOW-20260624-F83B438A", "status": "awaiting_confirmation", "updated": "2026-06-24T04:56:45"}
- Recommended fix: Clear or replace the stale confirmation by explicitly continuing or cancelling the workflow.
- Repairability: approval_required
- Risk level: low
- Related logs: None
- Related command: `python raphael.py pod-workflow-show PODFLOW-20260624-F83B438A`

## ISSUE-20260627-04E9A05D

- Severity: info
- Affected system: Confirmation System
- Symptoms: POD workflow PODFLOW-20260624-58645E2D has waited for confirmation for more than 24 hours
- Probable cause: A previous confirmation prompt was not completed or cancelled.
- Evidence: {"workflow_id": "PODFLOW-20260624-58645E2D", "status": "awaiting_confirmation", "updated": "2026-06-24T04:56:38"}
- Recommended fix: Clear or replace the stale confirmation by explicitly continuing or cancelling the workflow.
- Repairability: approval_required
- Risk level: low
- Related logs: None
- Related command: `python raphael.py pod-workflow-show PODFLOW-20260624-58645E2D`

## ISSUE-20260627-BC1FEBD1

- Severity: info
- Affected system: Confirmation System
- Symptoms: POD workflow PODFLOW-20260624-4D983F2B has waited for confirmation for more than 24 hours
- Probable cause: A previous confirmation prompt was not completed or cancelled.
- Evidence: {"workflow_id": "PODFLOW-20260624-4D983F2B", "status": "awaiting_confirmation", "updated": "2026-06-24T04:55:23"}
- Recommended fix: Clear or replace the stale confirmation by explicitly continuing or cancelling the workflow.
- Repairability: approval_required
- Risk level: low
- Related logs: None
- Related command: `python raphael.py pod-workflow-show PODFLOW-20260624-4D983F2B`

## ISSUE-20260627-1A27D76A

- Severity: info
- Affected system: Confirmation System
- Symptoms: POD workflow PODFLOW-20260624-5EC60EE8 has waited for confirmation for more than 24 hours
- Probable cause: A previous confirmation prompt was not completed or cancelled.
- Evidence: {"workflow_id": "PODFLOW-20260624-5EC60EE8", "status": "awaiting_confirmation", "updated": "2026-06-24T04:55:16"}
- Recommended fix: Clear or replace the stale confirmation by explicitly continuing or cancelling the workflow.
- Repairability: approval_required
- Risk level: low
- Related logs: None
- Related command: `python raphael.py pod-workflow-show PODFLOW-20260624-5EC60EE8`

## ISSUE-20260627-D4B1DCB5

- Severity: info
- Affected system: Confirmation System
- Symptoms: POD workflow PODFLOW-20260624-2DFBAE70 has waited for confirmation for more than 24 hours
- Probable cause: A previous confirmation prompt was not completed or cancelled.
- Evidence: {"workflow_id": "PODFLOW-20260624-2DFBAE70", "status": "awaiting_confirmation", "updated": "2026-06-24T04:53:37"}
- Recommended fix: Clear or replace the stale confirmation by explicitly continuing or cancelling the workflow.
- Repairability: approval_required
- Risk level: low
- Related logs: None
- Related command: `python raphael.py pod-workflow-show PODFLOW-20260624-2DFBAE70`

## ISSUE-20260627-37781EFB

- Severity: info
- Affected system: Confirmation System
- Symptoms: POD workflow PODFLOW-20260624-85BFB652 has waited for confirmation for more than 24 hours
- Probable cause: A previous confirmation prompt was not completed or cancelled.
- Evidence: {"workflow_id": "PODFLOW-20260624-85BFB652", "status": "awaiting_confirmation", "updated": "2026-06-24T04:53:31"}
- Recommended fix: Clear or replace the stale confirmation by explicitly continuing or cancelling the workflow.
- Repairability: approval_required
- Risk level: low
- Related logs: None
- Related command: `python raphael.py pod-workflow-show PODFLOW-20260624-85BFB652`

## ISSUE-20260627-D3571150

- Severity: info
- Affected system: Confirmation System
- Symptoms: POD workflow PODFLOW-20260622-FC74E603 has waited for confirmation for more than 24 hours
- Probable cause: A previous confirmation prompt was not completed or cancelled.
- Evidence: {"workflow_id": "PODFLOW-20260622-FC74E603", "status": "awaiting_confirmation", "updated": "2026-06-22T19:19:46"}
- Recommended fix: Clear or replace the stale confirmation by explicitly continuing or cancelling the workflow.
- Repairability: approval_required
- Risk level: low
- Related logs: None
- Related command: `python raphael.py pod-workflow-show PODFLOW-20260622-FC74E603`

## ISSUE-20260627-4C37BDF7

- Severity: info
- Affected system: Confirmation System
- Symptoms: POD workflow PODFLOW-20260622-C9B09DC5 has waited for confirmation for more than 24 hours
- Probable cause: A previous confirmation prompt was not completed or cancelled.
- Evidence: {"workflow_id": "PODFLOW-20260622-C9B09DC5", "status": "awaiting_confirmation", "updated": "2026-06-22T19:19:39"}
- Recommended fix: Clear or replace the stale confirmation by explicitly continuing or cancelling the workflow.
- Repairability: approval_required
- Risk level: low
- Related logs: None
- Related command: `python raphael.py pod-workflow-show PODFLOW-20260622-C9B09DC5`

## ISSUE-20260627-948BA0BA

- Severity: info
- Affected system: Confirmation System
- Symptoms: POD workflow PODFLOW-20260622-3C11602B has waited for confirmation for more than 24 hours
- Probable cause: A previous confirmation prompt was not completed or cancelled.
- Evidence: {"workflow_id": "PODFLOW-20260622-3C11602B", "status": "awaiting_confirmation", "updated": "2026-06-22T19:18:20"}
- Recommended fix: Clear or replace the stale confirmation by explicitly continuing or cancelling the workflow.
- Repairability: approval_required
- Risk level: low
- Related logs: None
- Related command: `python raphael.py pod-workflow-show PODFLOW-20260622-3C11602B`

## ISSUE-20260627-8B9782AA

- Severity: info
- Affected system: Confirmation System
- Symptoms: POD workflow PODFLOW-20260622-010D6DBD has waited for confirmation for more than 24 hours
- Probable cause: A previous confirmation prompt was not completed or cancelled.
- Evidence: {"workflow_id": "PODFLOW-20260622-010D6DBD", "status": "awaiting_confirmation", "updated": "2026-06-22T19:17:02"}
- Recommended fix: Clear or replace the stale confirmation by explicitly continuing or cancelling the workflow.
- Repairability: approval_required
- Risk level: low
- Related logs: None
- Related command: `python raphael.py pod-workflow-show PODFLOW-20260622-010D6DBD`

## ISSUE-20260627-EF831480

- Severity: info
- Affected system: Confirmation System
- Symptoms: POD workflow PODFLOW-20260622-6D0F5C2A has waited for confirmation for more than 24 hours
- Probable cause: A previous confirmation prompt was not completed or cancelled.
- Evidence: {"workflow_id": "PODFLOW-20260622-6D0F5C2A", "status": "awaiting_confirmation", "updated": "2026-06-22T19:16:55"}
- Recommended fix: Clear or replace the stale confirmation by explicitly continuing or cancelling the workflow.
- Repairability: approval_required
- Risk level: low
- Related logs: None
- Related command: `python raphael.py pod-workflow-show PODFLOW-20260622-6D0F5C2A`

## ISSUE-20260627-76ECAC51

- Severity: info
- Affected system: Confirmation System
- Symptoms: POD workflow PODFLOW-20260622-D6B386EF has waited for confirmation for more than 24 hours
- Probable cause: A previous confirmation prompt was not completed or cancelled.
- Evidence: {"workflow_id": "PODFLOW-20260622-D6B386EF", "status": "awaiting_confirmation", "updated": "2026-06-22T19:13:06"}
- Recommended fix: Clear or replace the stale confirmation by explicitly continuing or cancelling the workflow.
- Repairability: approval_required
- Risk level: low
- Related logs: None
- Related command: `python raphael.py pod-workflow-show PODFLOW-20260622-D6B386EF`

## ISSUE-20260627-F1AE0FC9

- Severity: info
- Affected system: Confirmation System
- Symptoms: POD workflow PODFLOW-20260622-917B2713 has waited for confirmation for more than 24 hours
- Probable cause: A previous confirmation prompt was not completed or cancelled.
- Evidence: {"workflow_id": "PODFLOW-20260622-917B2713", "status": "awaiting_confirmation", "updated": "2026-06-22T19:12:59"}
- Recommended fix: Clear or replace the stale confirmation by explicitly continuing or cancelling the workflow.
- Repairability: approval_required
- Risk level: low
- Related logs: None
- Related command: `python raphael.py pod-workflow-show PODFLOW-20260622-917B2713`

## ISSUE-20260627-437B5B1D

- Severity: info
- Affected system: Confirmation System
- Symptoms: POD workflow PODFLOW-20260622-E7620901 has waited for confirmation for more than 24 hours
- Probable cause: A previous confirmation prompt was not completed or cancelled.
- Evidence: {"workflow_id": "PODFLOW-20260622-E7620901", "status": "awaiting_confirmation", "updated": "2026-06-22T19:07:18"}
- Recommended fix: Clear or replace the stale confirmation by explicitly continuing or cancelling the workflow.
- Repairability: approval_required
- Risk level: low
- Related logs: None
- Related command: `python raphael.py pod-workflow-show PODFLOW-20260622-E7620901`

## ISSUE-20260627-20753037

- Severity: info
- Affected system: Confirmation System
- Symptoms: POD workflow PODFLOW-20260621-A8B737CB has waited for confirmation for more than 24 hours
- Probable cause: A previous confirmation prompt was not completed or cancelled.
- Evidence: {"workflow_id": "PODFLOW-20260621-A8B737CB", "status": "awaiting_confirmation", "updated": "2026-06-21T21:15:37"}
- Recommended fix: Clear or replace the stale confirmation by explicitly continuing or cancelling the workflow.
- Repairability: approval_required
- Risk level: low
- Related logs: None
- Related command: `python raphael.py pod-workflow-show PODFLOW-20260621-A8B737CB`

## ISSUE-20260627-CFD416CA

- Severity: info
- Affected system: Confirmation System
- Symptoms: POD workflow PODFLOW-20260621-A69A9AC0 has waited for confirmation for more than 24 hours
- Probable cause: A previous confirmation prompt was not completed or cancelled.
- Evidence: {"workflow_id": "PODFLOW-20260621-A69A9AC0", "status": "awaiting_confirmation", "updated": "2026-06-21T21:15:32"}
- Recommended fix: Clear or replace the stale confirmation by explicitly continuing or cancelling the workflow.
- Repairability: approval_required
- Risk level: low
- Related logs: None
- Related command: `python raphael.py pod-workflow-show PODFLOW-20260621-A69A9AC0`

## ISSUE-20260627-B87174F3

- Severity: info
- Affected system: Confirmation System
- Symptoms: POD workflow PODFLOW-20260621-53F6B8CC has waited for confirmation for more than 24 hours
- Probable cause: A previous confirmation prompt was not completed or cancelled.
- Evidence: {"workflow_id": "PODFLOW-20260621-53F6B8CC", "status": "awaiting_confirmation", "updated": "2026-06-21T21:13:03"}
- Recommended fix: Clear or replace the stale confirmation by explicitly continuing or cancelling the workflow.
- Repairability: approval_required
- Risk level: low
- Related logs: None
- Related command: `python raphael.py pod-workflow-show PODFLOW-20260621-53F6B8CC`

## ISSUE-20260627-100C9C35

- Severity: info
- Affected system: Confirmation System
- Symptoms: POD workflow PODFLOW-20260621-07E6B90D has waited for confirmation for more than 24 hours
- Probable cause: A previous confirmation prompt was not completed or cancelled.
- Evidence: {"workflow_id": "PODFLOW-20260621-07E6B90D", "status": "awaiting_confirmation", "updated": "2026-06-21T21:12:23"}
- Recommended fix: Clear or replace the stale confirmation by explicitly continuing or cancelling the workflow.
- Repairability: approval_required
- Risk level: low
- Related logs: None
- Related command: `python raphael.py pod-workflow-show PODFLOW-20260621-07E6B90D`

## ISSUE-20260627-2B4EC032

- Severity: info
- Affected system: Confirmation System
- Symptoms: POD workflow PODFLOW-20260621-9611C3C8 has waited for confirmation for more than 24 hours
- Probable cause: A previous confirmation prompt was not completed or cancelled.
- Evidence: {"workflow_id": "PODFLOW-20260621-9611C3C8", "status": "awaiting_confirmation", "updated": "2026-06-21T21:12:19"}
- Recommended fix: Clear or replace the stale confirmation by explicitly continuing or cancelling the workflow.
- Repairability: approval_required
- Risk level: low
- Related logs: None
- Related command: `python raphael.py pod-workflow-show PODFLOW-20260621-9611C3C8`

## ISSUE-20260627-E96AD5C5

- Severity: info
- Affected system: Confirmation System
- Symptoms: POD workflow PODFLOW-20260621-C6ADE7A9 has waited for confirmation for more than 24 hours
- Probable cause: A previous confirmation prompt was not completed or cancelled.
- Evidence: {"workflow_id": "PODFLOW-20260621-C6ADE7A9", "status": "awaiting_confirmation", "updated": "2026-06-21T21:11:14"}
- Recommended fix: Clear or replace the stale confirmation by explicitly continuing or cancelling the workflow.
- Repairability: approval_required
- Risk level: low
- Related logs: None
- Related command: `python raphael.py pod-workflow-show PODFLOW-20260621-C6ADE7A9`

## ISSUE-20260627-C7D092F1

- Severity: info
- Affected system: Confirmation System
- Symptoms: POD workflow PODFLOW-20260621-FB2F5D6D has waited for confirmation for more than 24 hours
- Probable cause: A previous confirmation prompt was not completed or cancelled.
- Evidence: {"workflow_id": "PODFLOW-20260621-FB2F5D6D", "status": "awaiting_confirmation", "updated": "2026-06-21T21:11:10"}
- Recommended fix: Clear or replace the stale confirmation by explicitly continuing or cancelling the workflow.
- Repairability: approval_required
- Risk level: low
- Related logs: None
- Related command: `python raphael.py pod-workflow-show PODFLOW-20260621-FB2F5D6D`

## ISSUE-20260627-BED06EBB

- Severity: info
- Affected system: Confirmation System
- Symptoms: POD workflow PODFLOW-20260621-FC262513 has waited for confirmation for more than 24 hours
- Probable cause: A previous confirmation prompt was not completed or cancelled.
- Evidence: {"workflow_id": "PODFLOW-20260621-FC262513", "status": "awaiting_confirmation", "updated": "2026-06-21T20:51:03"}
- Recommended fix: Clear or replace the stale confirmation by explicitly continuing or cancelling the workflow.
- Repairability: approval_required
- Risk level: low
- Related logs: None
- Related command: `python raphael.py pod-workflow-show PODFLOW-20260621-FC262513`

## ISSUE-20260627-97EC99C7

- Severity: info
- Affected system: Confirmation System
- Symptoms: POD workflow PODFLOW-20260621-5891C844 has waited for confirmation for more than 24 hours
- Probable cause: A previous confirmation prompt was not completed or cancelled.
- Evidence: {"workflow_id": "PODFLOW-20260621-5891C844", "status": "awaiting_confirmation", "updated": "2026-06-21T20:50:23"}
- Recommended fix: Clear or replace the stale confirmation by explicitly continuing or cancelling the workflow.
- Repairability: approval_required
- Risk level: low
- Related logs: None
- Related command: `python raphael.py pod-workflow-show PODFLOW-20260621-5891C844`

## ISSUE-20260627-790D1B64

- Severity: info
- Affected system: Confirmation System
- Symptoms: POD workflow PODFLOW-20260621-211FEF81 has waited for confirmation for more than 24 hours
- Probable cause: A previous confirmation prompt was not completed or cancelled.
- Evidence: {"workflow_id": "PODFLOW-20260621-211FEF81", "status": "awaiting_confirmation", "updated": "2026-06-21T20:50:19"}
- Recommended fix: Clear or replace the stale confirmation by explicitly continuing or cancelling the workflow.
- Repairability: approval_required
- Risk level: low
- Related logs: None
- Related command: `python raphael.py pod-workflow-show PODFLOW-20260621-211FEF81`

## ISSUE-20260627-09B225F3

- Severity: info
- Affected system: Confirmation System
- Symptoms: POD workflow PODFLOW-20260621-1F3760C3 has waited for confirmation for more than 24 hours
- Probable cause: A previous confirmation prompt was not completed or cancelled.
- Evidence: {"workflow_id": "PODFLOW-20260621-1F3760C3", "status": "awaiting_confirmation", "updated": "2026-06-21T20:49:02"}
- Recommended fix: Clear or replace the stale confirmation by explicitly continuing or cancelling the workflow.
- Repairability: approval_required
- Risk level: low
- Related logs: None
- Related command: `python raphael.py pod-workflow-show PODFLOW-20260621-1F3760C3`

## ISSUE-20260627-EB5DCF55

- Severity: info
- Affected system: Confirmation System
- Symptoms: POD workflow PODFLOW-20260621-7B96D120 has waited for confirmation for more than 24 hours
- Probable cause: A previous confirmation prompt was not completed or cancelled.
- Evidence: {"workflow_id": "PODFLOW-20260621-7B96D120", "status": "awaiting_confirmation", "updated": "2026-06-21T20:48:58"}
- Recommended fix: Clear or replace the stale confirmation by explicitly continuing or cancelling the workflow.
- Repairability: approval_required
- Risk level: low
- Related logs: None
- Related command: `python raphael.py pod-workflow-show PODFLOW-20260621-7B96D120`

## ISSUE-20260627-7DAC8E76

- Severity: info
- Affected system: Confirmation System
- Symptoms: POD workflow PODFLOW-20260621-DDA058B8 has waited for confirmation for more than 24 hours
- Probable cause: A previous confirmation prompt was not completed or cancelled.
- Evidence: {"workflow_id": "PODFLOW-20260621-DDA058B8", "status": "awaiting_confirmation", "updated": "2026-06-21T20:47:57"}
- Recommended fix: Clear or replace the stale confirmation by explicitly continuing or cancelling the workflow.
- Repairability: approval_required
- Risk level: low
- Related logs: None
- Related command: `python raphael.py pod-workflow-show PODFLOW-20260621-DDA058B8`

## ISSUE-20260627-8A22295D

- Severity: info
- Affected system: Confirmation System
- Symptoms: POD workflow PODFLOW-20260621-26EA79A6 has waited for confirmation for more than 24 hours
- Probable cause: A previous confirmation prompt was not completed or cancelled.
- Evidence: {"workflow_id": "PODFLOW-20260621-26EA79A6", "status": "awaiting_confirmation", "updated": "2026-06-21T20:47:53"}
- Recommended fix: Clear or replace the stale confirmation by explicitly continuing or cancelling the workflow.
- Repairability: approval_required
- Risk level: low
- Related logs: None
- Related command: `python raphael.py pod-workflow-show PODFLOW-20260621-26EA79A6`

## ISSUE-20260627-5AA1D264

- Severity: info
- Affected system: Confirmation System
- Symptoms: POD workflow PODFLOW-20260621-51D53FD3 has waited for confirmation for more than 24 hours
- Probable cause: A previous confirmation prompt was not completed or cancelled.
- Evidence: {"workflow_id": "PODFLOW-20260621-51D53FD3", "status": "awaiting_confirmation", "updated": "2026-06-21T20:45:59"}
- Recommended fix: Clear or replace the stale confirmation by explicitly continuing or cancelling the workflow.
- Repairability: approval_required
- Risk level: low
- Related logs: None
- Related command: `python raphael.py pod-workflow-show PODFLOW-20260621-51D53FD3`

## ISSUE-20260627-E378DFFC

- Severity: info
- Affected system: Confirmation System
- Symptoms: POD workflow PODFLOW-20260621-2E329CBD has waited for confirmation for more than 24 hours
- Probable cause: A previous confirmation prompt was not completed or cancelled.
- Evidence: {"workflow_id": "PODFLOW-20260621-2E329CBD", "status": "awaiting_confirmation", "updated": "2026-06-21T20:45:54"}
- Recommended fix: Clear or replace the stale confirmation by explicitly continuing or cancelling the workflow.
- Repairability: approval_required
- Risk level: low
- Related logs: None
- Related command: `python raphael.py pod-workflow-show PODFLOW-20260621-2E329CBD`

## ISSUE-20260627-365C1855

- Severity: info
- Affected system: Confirmation System
- Symptoms: POD workflow PODFLOW-20260621-47A26A6A has waited for confirmation for more than 24 hours
- Probable cause: A previous confirmation prompt was not completed or cancelled.
- Evidence: {"workflow_id": "PODFLOW-20260621-47A26A6A", "status": "awaiting_confirmation", "updated": "2026-06-21T20:36:51"}
- Recommended fix: Clear or replace the stale confirmation by explicitly continuing or cancelling the workflow.
- Repairability: approval_required
- Risk level: low
- Related logs: None
- Related command: `python raphael.py pod-workflow-show PODFLOW-20260621-47A26A6A`

## ISSUE-20260627-C0B75EB7

- Severity: info
- Affected system: Confirmation System
- Symptoms: POD workflow PODFLOW-20260621-0E1A73DA has waited for confirmation for more than 24 hours
- Probable cause: A previous confirmation prompt was not completed or cancelled.
- Evidence: {"workflow_id": "PODFLOW-20260621-0E1A73DA", "status": "awaiting_confirmation", "updated": "2026-06-21T20:36:02"}
- Recommended fix: Clear or replace the stale confirmation by explicitly continuing or cancelling the workflow.
- Repairability: approval_required
- Risk level: low
- Related logs: None
- Related command: `python raphael.py pod-workflow-show PODFLOW-20260621-0E1A73DA`

## ISSUE-20260627-CB0F82C3

- Severity: info
- Affected system: Confirmation System
- Symptoms: POD workflow PODFLOW-20260621-27E3C87A has waited for confirmation for more than 24 hours
- Probable cause: A previous confirmation prompt was not completed or cancelled.
- Evidence: {"workflow_id": "PODFLOW-20260621-27E3C87A", "status": "awaiting_confirmation", "updated": "2026-06-21T20:35:58"}
- Recommended fix: Clear or replace the stale confirmation by explicitly continuing or cancelling the workflow.
- Repairability: approval_required
- Risk level: low
- Related logs: None
- Related command: `python raphael.py pod-workflow-show PODFLOW-20260621-27E3C87A`

## ISSUE-20260627-4724C3EF

- Severity: info
- Affected system: Confirmation System
- Symptoms: POD workflow PODFLOW-20260621-E8AB09B9 has waited for confirmation for more than 24 hours
- Probable cause: A previous confirmation prompt was not completed or cancelled.
- Evidence: {"workflow_id": "PODFLOW-20260621-E8AB09B9", "status": "awaiting_confirmation", "updated": "2026-06-21T20:34:12"}
- Recommended fix: Clear or replace the stale confirmation by explicitly continuing or cancelling the workflow.
- Repairability: approval_required
- Risk level: low
- Related logs: None
- Related command: `python raphael.py pod-workflow-show PODFLOW-20260621-E8AB09B9`

## ISSUE-20260627-947C25B1

- Severity: info
- Affected system: Confirmation System
- Symptoms: POD workflow PODFLOW-20260621-042859DD has waited for confirmation for more than 24 hours
- Probable cause: A previous confirmation prompt was not completed or cancelled.
- Evidence: {"workflow_id": "PODFLOW-20260621-042859DD", "status": "awaiting_confirmation", "updated": "2026-06-21T20:21:03"}
- Recommended fix: Clear or replace the stale confirmation by explicitly continuing or cancelling the workflow.
- Repairability: approval_required
- Risk level: low
- Related logs: None
- Related command: `python raphael.py pod-workflow-show PODFLOW-20260621-042859DD`

## ISSUE-20260627-F2FF21ED

- Severity: info
- Affected system: Confirmation System
- Symptoms: POD workflow PODFLOW-20260621-F0EC84AD has waited for confirmation for more than 24 hours
- Probable cause: A previous confirmation prompt was not completed or cancelled.
- Evidence: {"workflow_id": "PODFLOW-20260621-F0EC84AD", "status": "awaiting_confirmation", "updated": "2026-06-21T20:20:17"}
- Recommended fix: Clear or replace the stale confirmation by explicitly continuing or cancelling the workflow.
- Repairability: approval_required
- Risk level: low
- Related logs: None
- Related command: `python raphael.py pod-workflow-show PODFLOW-20260621-F0EC84AD`

## ISSUE-20260627-068C2F3F

- Severity: info
- Affected system: Confirmation System
- Symptoms: POD workflow PODFLOW-20260621-AF4AAA86 has waited for confirmation for more than 24 hours
- Probable cause: A previous confirmation prompt was not completed or cancelled.
- Evidence: {"workflow_id": "PODFLOW-20260621-AF4AAA86", "status": "awaiting_confirmation", "updated": "2026-06-21T20:20:13"}
- Recommended fix: Clear or replace the stale confirmation by explicitly continuing or cancelling the workflow.
- Repairability: approval_required
- Risk level: low
- Related logs: None
- Related command: `python raphael.py pod-workflow-show PODFLOW-20260621-AF4AAA86`

## ISSUE-20260627-72E76838

- Severity: info
- Affected system: Confirmation System
- Symptoms: POD workflow PODFLOW-20260621-A1E39FD9 has waited for confirmation for more than 24 hours
- Probable cause: A previous confirmation prompt was not completed or cancelled.
- Evidence: {"workflow_id": "PODFLOW-20260621-A1E39FD9", "status": "awaiting_confirmation", "updated": "2026-06-21T19:04:07"}
- Recommended fix: Clear or replace the stale confirmation by explicitly continuing or cancelling the workflow.
- Repairability: approval_required
- Risk level: low
- Related logs: None
- Related command: `python raphael.py pod-workflow-show PODFLOW-20260621-A1E39FD9`

## ISSUE-20260627-EEB3DA57

- Severity: info
- Affected system: Confirmation System
- Symptoms: POD workflow PODFLOW-20260621-E96CEB89 has waited for confirmation for more than 24 hours
- Probable cause: A previous confirmation prompt was not completed or cancelled.
- Evidence: {"workflow_id": "PODFLOW-20260621-E96CEB89", "status": "awaiting_confirmation", "updated": "2026-06-21T19:03:15"}
- Recommended fix: Clear or replace the stale confirmation by explicitly continuing or cancelling the workflow.
- Repairability: approval_required
- Risk level: low
- Related logs: None
- Related command: `python raphael.py pod-workflow-show PODFLOW-20260621-E96CEB89`

## ISSUE-20260627-41D42D6D

- Severity: info
- Affected system: Confirmation System
- Symptoms: POD workflow PODFLOW-20260621-E5C07A14 has waited for confirmation for more than 24 hours
- Probable cause: A previous confirmation prompt was not completed or cancelled.
- Evidence: {"workflow_id": "PODFLOW-20260621-E5C07A14", "status": "awaiting_confirmation", "updated": "2026-06-21T19:03:11"}
- Recommended fix: Clear or replace the stale confirmation by explicitly continuing or cancelling the workflow.
- Repairability: approval_required
- Risk level: low
- Related logs: None
- Related command: `python raphael.py pod-workflow-show PODFLOW-20260621-E5C07A14`

## ISSUE-20260627-5F6207BE

- Severity: info
- Affected system: Confirmation System
- Symptoms: POD workflow PODFLOW-20260621-75491FC9 has waited for confirmation for more than 24 hours
- Probable cause: A previous confirmation prompt was not completed or cancelled.
- Evidence: {"workflow_id": "PODFLOW-20260621-75491FC9", "status": "awaiting_confirmation", "updated": "2026-06-21T19:01:25"}
- Recommended fix: Clear or replace the stale confirmation by explicitly continuing or cancelling the workflow.
- Repairability: approval_required
- Risk level: low
- Related logs: None
- Related command: `python raphael.py pod-workflow-show PODFLOW-20260621-75491FC9`

## ISSUE-20260627-99D9CBFC

- Severity: info
- Affected system: Confirmation System
- Symptoms: POD workflow PODFLOW-20260621-3AA31FCC has waited for confirmation for more than 24 hours
- Probable cause: A previous confirmation prompt was not completed or cancelled.
- Evidence: {"workflow_id": "PODFLOW-20260621-3AA31FCC", "status": "awaiting_confirmation", "updated": "2026-06-21T19:00:34"}
- Recommended fix: Clear or replace the stale confirmation by explicitly continuing or cancelling the workflow.
- Repairability: approval_required
- Risk level: low
- Related logs: None
- Related command: `python raphael.py pod-workflow-show PODFLOW-20260621-3AA31FCC`

## ISSUE-20260627-6B6FE43E

- Severity: info
- Affected system: Confirmation System
- Symptoms: POD workflow PODFLOW-20260621-B7CF2303 has waited for confirmation for more than 24 hours
- Probable cause: A previous confirmation prompt was not completed or cancelled.
- Evidence: {"workflow_id": "PODFLOW-20260621-B7CF2303", "status": "awaiting_confirmation", "updated": "2026-06-21T19:00:29"}
- Recommended fix: Clear or replace the stale confirmation by explicitly continuing or cancelling the workflow.
- Repairability: approval_required
- Risk level: low
- Related logs: None
- Related command: `python raphael.py pod-workflow-show PODFLOW-20260621-B7CF2303`

## ISSUE-20260627-FFE371E5

- Severity: info
- Affected system: Confirmation System
- Symptoms: POD workflow PODFLOW-20260621-034E7DF7 has waited for confirmation for more than 24 hours
- Probable cause: A previous confirmation prompt was not completed or cancelled.
- Evidence: {"workflow_id": "PODFLOW-20260621-034E7DF7", "status": "awaiting_confirmation", "updated": "2026-06-21T18:59:29"}
- Recommended fix: Clear or replace the stale confirmation by explicitly continuing or cancelling the workflow.
- Repairability: approval_required
- Risk level: low
- Related logs: None
- Related command: `python raphael.py pod-workflow-show PODFLOW-20260621-034E7DF7`

## ISSUE-20260627-7B6F2DDE

- Severity: info
- Affected system: Confirmation System
- Symptoms: POD workflow PODFLOW-20260621-CE702A0E has waited for confirmation for more than 24 hours
- Probable cause: A previous confirmation prompt was not completed or cancelled.
- Evidence: {"workflow_id": "PODFLOW-20260621-CE702A0E", "status": "awaiting_confirmation", "updated": "2026-06-21T18:59:27"}
- Recommended fix: Clear or replace the stale confirmation by explicitly continuing or cancelling the workflow.
- Repairability: approval_required
- Risk level: low
- Related logs: None
- Related command: `python raphael.py pod-workflow-show PODFLOW-20260621-CE702A0E`

## ISSUE-20260627-10BB13FD

- Severity: info
- Affected system: Confirmation System
- Symptoms: POD workflow PODFLOW-20260621-848D7F18 has waited for confirmation for more than 24 hours
- Probable cause: A previous confirmation prompt was not completed or cancelled.
- Evidence: {"workflow_id": "PODFLOW-20260621-848D7F18", "status": "awaiting_confirmation", "updated": "2026-06-21T18:58:12"}
- Recommended fix: Clear or replace the stale confirmation by explicitly continuing or cancelling the workflow.
- Repairability: approval_required
- Risk level: low
- Related logs: None
- Related command: `python raphael.py pod-workflow-show PODFLOW-20260621-848D7F18`

## ISSUE-20260627-FCE17996

- Severity: info
- Affected system: Confirmation System
- Symptoms: POD workflow PODFLOW-20260621-568B2707 has waited for confirmation for more than 24 hours
- Probable cause: A previous confirmation prompt was not completed or cancelled.
- Evidence: {"workflow_id": "PODFLOW-20260621-568B2707", "status": "awaiting_confirmation", "updated": "2026-06-21T18:58:08"}
- Recommended fix: Clear or replace the stale confirmation by explicitly continuing or cancelling the workflow.
- Repairability: approval_required
- Risk level: low
- Related logs: None
- Related command: `python raphael.py pod-workflow-show PODFLOW-20260621-568B2707`

## ISSUE-20260627-221B3647

- Severity: info
- Affected system: Confirmation System
- Symptoms: POD workflow PODFLOW-20260621-5F202084 has waited for confirmation for more than 24 hours
- Probable cause: A previous confirmation prompt was not completed or cancelled.
- Evidence: {"workflow_id": "PODFLOW-20260621-5F202084", "status": "awaiting_confirmation", "updated": "2026-06-21T18:57:53"}
- Recommended fix: Clear or replace the stale confirmation by explicitly continuing or cancelling the workflow.
- Repairability: approval_required
- Risk level: low
- Related logs: None
- Related command: `python raphael.py pod-workflow-show PODFLOW-20260621-5F202084`

## ISSUE-20260627-E8874281

- Severity: info
- Affected system: Confirmation System
- Symptoms: POD workflow PODFLOW-20260621-F645DAA1 has waited for confirmation for more than 24 hours
- Probable cause: A previous confirmation prompt was not completed or cancelled.
- Evidence: {"workflow_id": "PODFLOW-20260621-F645DAA1", "status": "awaiting_confirmation", "updated": "2026-06-21T18:57:49"}
- Recommended fix: Clear or replace the stale confirmation by explicitly continuing or cancelling the workflow.
- Repairability: approval_required
- Risk level: low
- Related logs: None
- Related command: `python raphael.py pod-workflow-show PODFLOW-20260621-F645DAA1`

## ISSUE-20260627-FE50C66F

- Severity: info
- Affected system: Confirmation System
- Symptoms: POD workflow PODFLOW-20260621-9CE98C4C has waited for confirmation for more than 24 hours
- Probable cause: A previous confirmation prompt was not completed or cancelled.
- Evidence: {"workflow_id": "PODFLOW-20260621-9CE98C4C", "status": "awaiting_confirmation", "updated": "2026-06-21T18:57:05"}
- Recommended fix: Clear or replace the stale confirmation by explicitly continuing or cancelling the workflow.
- Repairability: approval_required
- Risk level: low
- Related logs: None
- Related command: `python raphael.py pod-workflow-show PODFLOW-20260621-9CE98C4C`

## ISSUE-20260627-4B32E036

- Severity: info
- Affected system: Confirmation System
- Symptoms: POD workflow PODFLOW-20260621-42B4B78B has waited for confirmation for more than 24 hours
- Probable cause: A previous confirmation prompt was not completed or cancelled.
- Evidence: {"workflow_id": "PODFLOW-20260621-42B4B78B", "status": "awaiting_confirmation", "updated": "2026-06-21T18:57:01"}
- Recommended fix: Clear or replace the stale confirmation by explicitly continuing or cancelling the workflow.
- Repairability: approval_required
- Risk level: low
- Related logs: None
- Related command: `python raphael.py pod-workflow-show PODFLOW-20260621-42B4B78B`

## ISSUE-20260627-5CC6E048

- Severity: info
- Affected system: Confirmation System
- Symptoms: POD workflow PODFLOW-20260621-E8620856 has waited for confirmation for more than 24 hours
- Probable cause: A previous confirmation prompt was not completed or cancelled.
- Evidence: {"workflow_id": "PODFLOW-20260621-E8620856", "status": "awaiting_confirmation", "updated": "2026-06-21T18:56:17"}
- Recommended fix: Clear or replace the stale confirmation by explicitly continuing or cancelling the workflow.
- Repairability: approval_required
- Risk level: low
- Related logs: None
- Related command: `python raphael.py pod-workflow-show PODFLOW-20260621-E8620856`

## ISSUE-20260627-CCF7C469

- Severity: info
- Affected system: Confirmation System
- Symptoms: POD workflow PODFLOW-20260621-8BC905C1 has waited for confirmation for more than 24 hours
- Probable cause: A previous confirmation prompt was not completed or cancelled.
- Evidence: {"workflow_id": "PODFLOW-20260621-8BC905C1", "status": "awaiting_confirmation", "updated": "2026-06-21T18:56:12"}
- Recommended fix: Clear or replace the stale confirmation by explicitly continuing or cancelling the workflow.
- Repairability: approval_required
- Risk level: low
- Related logs: None
- Related command: `python raphael.py pod-workflow-show PODFLOW-20260621-8BC905C1`

## ISSUE-20260627-25F66B5B

- Severity: info
- Affected system: Confirmation System
- Symptoms: POD workflow PODFLOW-20260621-5DC6883F has waited for confirmation for more than 24 hours
- Probable cause: A previous confirmation prompt was not completed or cancelled.
- Evidence: {"workflow_id": "PODFLOW-20260621-5DC6883F", "status": "awaiting_confirmation", "updated": "2026-06-21T18:56:08"}
- Recommended fix: Clear or replace the stale confirmation by explicitly continuing or cancelling the workflow.
- Repairability: approval_required
- Risk level: low
- Related logs: None
- Related command: `python raphael.py pod-workflow-show PODFLOW-20260621-5DC6883F`

## ISSUE-20260627-B76703B2

- Severity: info
- Affected system: Confirmation System
- Symptoms: POD workflow PODFLOW-20260621-FBD8292E has waited for confirmation for more than 24 hours
- Probable cause: A previous confirmation prompt was not completed or cancelled.
- Evidence: {"workflow_id": "PODFLOW-20260621-FBD8292E", "status": "awaiting_confirmation", "updated": "2026-06-21T18:55:59"}
- Recommended fix: Clear or replace the stale confirmation by explicitly continuing or cancelling the workflow.
- Repairability: approval_required
- Risk level: low
- Related logs: None
- Related command: `python raphael.py pod-workflow-show PODFLOW-20260621-FBD8292E`

## ISSUE-20260627-F4DF3364

- Severity: info
- Affected system: Confirmation System
- Symptoms: POD workflow PODFLOW-20260621-CAC8E337 has waited for confirmation for more than 24 hours
- Probable cause: A previous confirmation prompt was not completed or cancelled.
- Evidence: {"workflow_id": "PODFLOW-20260621-CAC8E337", "status": "awaiting_confirmation", "updated": "2026-06-21T18:55:55"}
- Recommended fix: Clear or replace the stale confirmation by explicitly continuing or cancelling the workflow.
- Repairability: approval_required
- Risk level: low
- Related logs: None
- Related command: `python raphael.py pod-workflow-show PODFLOW-20260621-CAC8E337`

## ISSUE-20260627-A19BFC23

- Severity: info
- Affected system: Confirmation System
- Symptoms: POD workflow PODFLOW-20260621-3B129CA9 has waited for confirmation for more than 24 hours
- Probable cause: A previous confirmation prompt was not completed or cancelled.
- Evidence: {"workflow_id": "PODFLOW-20260621-3B129CA9", "status": "awaiting_confirmation", "updated": "2026-06-21T18:55:40"}
- Recommended fix: Clear or replace the stale confirmation by explicitly continuing or cancelling the workflow.
- Repairability: approval_required
- Risk level: low
- Related logs: None
- Related command: `python raphael.py pod-workflow-show PODFLOW-20260621-3B129CA9`
