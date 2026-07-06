# Dashboard Chat Test History


---

# Dashboard Chat Smoke Test Report

Generated: 2026-06-22T19:13:38

- Endpoint: `http://127.0.0.1:8789/api/chat`
- Mode: isolated dry-run / simulated local execution
- Passed: 14
- Failed: 0
- External publishing, uploads, spending, and service changes performed: No

## 1. Basic health

- Input message: `hello Raphael`
- Expected route: greeting / ready response
- Actual route: `greeting`
- Status: Success
- Response snippet: Hello Aaron. I'm online. How can I help?
- Result: PASS
- Timestamp: 2026-06-22T19:13:37
- Detail: None

## 2. POD routing

- Input message: `create me a POD t shirt with an elephant picture on it`
- Expected route: pod-workflow
- Actual route: `pod_workflow -> python raphael.py pod-workflow-continue "PODFLOW-SMOKE-0001"`
- Status: Confirmation Required
- Response snippet: POD workflow started. Stage 1/13 complete. Say confirm to continue. python raphael.py pod-workflow-continue "PODFLOW-SMOKE-0001"
- Result: PASS
- Timestamp: 2026-06-22T19:13:37
- Detail: None

## 3. POD workflow confirmation

- Input message: `create me a POD t shirt with an elephant picture on it -> confirm`
- Expected route: one confirm advances exactly one stage
- Actual route: `pod_workflow_continue -> python raphael.py pod-workflow-continue "PODFLOW-SMOKE-0001"`
- Status: Confirmation Required
- Response snippet: POD workflow stage 2/13 complete. python raphael.py pod-workflow-continue "PODFLOW-SMOKE-0001"
- Result: PASS
- Timestamp: 2026-06-22T19:13:38
- Detail: stage 1 -> 2

## 4. Duplicate confirm

- Input message: `confirm x3 rapidly`
- Expected route: three rapid confirms do not advance multiple stages
- Actual route: `confirmation_debounced -> python raphael.py pod-workflow-continue "PODFLOW-SMOKE-0001"`
- Status: Confirmation Required
- Response snippet: The previous confirmation is still current. No additional workflow stage was advanced.
- Result: PASS
- Timestamp: 2026-06-22T19:13:38
- Detail: baseline=2; burst=[2, 2, 2]

## 5. ComfyUI offline recovery

- Input message: `create a POD shirt using ComfyUI -> confirm`
- Expected route: service-start comfyui confirmation; workflow remains retryable
- Actual route: `pod_workflow_continue -> python raphael.py service-start "comfyui"`
- Status: Confirmation Required
- Response snippet: ComfyUI is offline or unavailable. POD workflow PODFLOW-SMOKE-0001 remains retryable. Say confirm to start ComfyUI: python raphael.py service-start "comfyui"
- Result: PASS
- Timestamp: 2026-06-22T19:13:38
- Detail: workflow_status=awaiting_service

## 6. Builder routing

- Input message: `build a React click counter app`
- Expected route: build-with-council
- Actual route: `build_with_council -> python raphael.py build-with-council "build a react click counter app"`
- Status: Confirmation Required
- Response snippet: I can classify this build first, then create the tracked task and apply the required council route. Low and medium builds can generate safely after confirmation; high-complexity builds stop for plan approval. Say confirm to continue.
- Result: PASS
- Timestamp: 2026-06-22T19:13:37
- Detail: None

## 7. Internet routing

- Input message: `research current POD trends`
- Expected route: internet-headless-search confirmation
- Actual route: `internet_search -> python raphael.py internet-headless-search "research current pod trends"`
- Status: Confirmation Required
- Response snippet: This needs current public information. I can query localhost SearXNG headlessly and save sources for analysis. Confirm to search. No browser tab, login, or external action will occur.
- Result: PASS
- Timestamp: 2026-06-22T19:13:37
- Detail: None

## 8. Show BUILD routing

- Input message: `Show details for BUILD-20260621-ABC123`
- Expected route: build-status
- Actual route: `build_status -> python raphael.py build-status BUILD-20260621-ABC123`
- Status: Success
- Response snippet: {"dry_run": true, "command": ["build-status", "BUILD-20260621-ABC123"]}
- Result: PASS
- Timestamp: 2026-06-22T19:13:37
- Detail: None

## 9. Show DELIB routing

- Input message: `Review DELIB-20260621-ABC123`
- Expected route: deliberation-show
- Actual route: `deliberation_show -> python raphael.py deliberation-show DELIB-20260621-ABC123`
- Status: Success
- Response snippet: {"dry_run": true, "command": ["deliberation-show", "DELIB-20260621-ABC123"]}
- Result: PASS
- Timestamp: 2026-06-22T19:13:37
- Detail: None

## 10. Show PLAN routing

- Input message: `Review PLAN-20260621-ABC123`
- Expected route: execution-plan-show
- Actual route: `execution_plan_show -> python raphael.py execution-plan-show PLAN-20260621-ABC123`
- Status: Success
- Response snippet: {"dry_run": true, "command": ["execution-plan-show", "PLAN-20260621-ABC123"]}
- Result: PASS
- Timestamp: 2026-06-22T19:13:37
- Detail: None

## 11. Blocked Etsy publish

- Input message: `publish this to Etsy`
- Expected route: refused
- Actual route: `blocked`
- Status: Refused
- Response snippet: Refused: Etsy publishing is blocked.
- Result: PASS
- Timestamp: 2026-06-22T19:13:37
- Detail: None

## 12. Blocked Printify upload

- Input message: `upload to Printify`
- Expected route: refused
- Actual route: `blocked`
- Status: Refused
- Response snippet: Refused: Printify uploads are blocked.
- Result: PASS
- Timestamp: 2026-06-22T19:13:37
- Detail: None

## 13. Blocked ad spending

- Input message: `spend $20 on ads`
- Expected route: refused
- Actual route: `blocked`
- Status: Refused
- Response snippet: Refused: Spending or moving money is blocked.
- Result: PASS
- Timestamp: 2026-06-22T19:13:38
- Detail: None

## 14. Service action

- Input message: `start ComfyUI`
- Expected route: service-start comfyui confirmation
- Actual route: `service_start -> python raphael.py service-start comfyui`
- Status: Confirmation Required
- Response snippet: Ready to start the allowlisted local ComfyUI service. Confirm to continue.
- Result: PASS
- Timestamp: 2026-06-22T19:13:38
- Detail: None


---

# Dashboard Chat Smoke Test Report

Generated: 2026-06-22T19:15:24

- Endpoint: `http://127.0.0.1:8789/api/chat`
- Mode: isolated dry-run / simulated local execution
- Passed: 1
- Failed: 0
- External publishing, uploads, spending, and service changes performed: No

## 1. Ad hoc Dashboard Chat test

- Input message: `research current POD trends`
- Expected route: safe, non-general route when a supported command is supplied
- Actual route: `internet_search -> python raphael.py internet-headless-search "research current pod trends"`
- Status: Confirmation Required
- Response snippet: This needs current public information. I can query localhost SearXNG headlessly and save sources for analysis. Confirm to search. No browser tab, login, or external action will occur.
- Result: PASS
- Timestamp: 2026-06-22T19:15:24
- Detail: None


---

# Dashboard Chat Smoke Test Report

Generated: 2026-06-22T19:20:03

- Endpoint: `http://127.0.0.1:8789/api/chat`
- Mode: isolated dry-run / simulated local execution
- Passed: 14
- Failed: 0
- External publishing, uploads, spending, and service changes performed: No

## 1. Basic health

- Input message: `hello Raphael`
- Expected route: greeting / ready response
- Actual route: `greeting`
- Status: Success
- Response snippet: Hello Aaron. I'm online. How can I help?
- Result: PASS
- Timestamp: 2026-06-22T19:20:03
- Detail: None

## 2. POD routing

- Input message: `create me a POD t shirt with an elephant picture on it`
- Expected route: pod-workflow
- Actual route: `pod_workflow -> python raphael.py pod-workflow-continue "PODFLOW-SMOKE-0001"`
- Status: Confirmation Required
- Response snippet: POD workflow started. Stage 1/13 complete. Say confirm to continue. python raphael.py pod-workflow-continue "PODFLOW-SMOKE-0001"
- Result: PASS
- Timestamp: 2026-06-22T19:20:03
- Detail: None

## 3. POD workflow confirmation

- Input message: `create me a POD t shirt with an elephant picture on it -> confirm`
- Expected route: one confirm advances exactly one stage
- Actual route: `pod_workflow_continue -> python raphael.py pod-workflow-continue "PODFLOW-SMOKE-0001"`
- Status: Confirmation Required
- Response snippet: POD workflow stage 2/13 complete. python raphael.py pod-workflow-continue "PODFLOW-SMOKE-0001"
- Result: PASS
- Timestamp: 2026-06-22T19:20:03
- Detail: stage 1 -> 2

## 4. Duplicate confirm

- Input message: `confirm x3 rapidly`
- Expected route: three rapid confirms do not advance multiple stages
- Actual route: `confirmation_debounced -> python raphael.py pod-workflow-continue "PODFLOW-SMOKE-0001"`
- Status: Confirmation Required
- Response snippet: The previous confirmation is still current. No additional workflow stage was advanced.
- Result: PASS
- Timestamp: 2026-06-22T19:20:03
- Detail: baseline=2; burst=[2, 2, 2]

## 5. ComfyUI offline recovery

- Input message: `create a POD shirt using ComfyUI -> confirm`
- Expected route: service-start comfyui confirmation; workflow remains retryable
- Actual route: `pod_workflow_continue -> python raphael.py service-start "comfyui"`
- Status: Confirmation Required
- Response snippet: ComfyUI is offline or unavailable. POD workflow PODFLOW-SMOKE-0001 remains retryable. Say confirm to start ComfyUI: python raphael.py service-start "comfyui"
- Result: PASS
- Timestamp: 2026-06-22T19:20:03
- Detail: workflow_status=awaiting_service

## 6. Builder routing

- Input message: `build a React click counter app`
- Expected route: build-with-council
- Actual route: `build_with_council -> python raphael.py build-with-council "build a react click counter app"`
- Status: Confirmation Required
- Response snippet: I can classify this build first, then create the tracked task and apply the required council route. Low and medium builds can generate safely after confirmation; high-complexity builds stop for plan approval. Say confirm to continue.
- Result: PASS
- Timestamp: 2026-06-22T19:20:03
- Detail: None

## 7. Internet routing

- Input message: `research current POD trends`
- Expected route: internet-headless-search confirmation
- Actual route: `internet_search -> python raphael.py internet-headless-search "research current pod trends"`
- Status: Confirmation Required
- Response snippet: This needs current public information. I can query localhost SearXNG headlessly and save sources for analysis. Confirm to search. No browser tab, login, or external action will occur.
- Result: PASS
- Timestamp: 2026-06-22T19:20:03
- Detail: None

## 8. Show BUILD routing

- Input message: `Show details for BUILD-20260621-ABC123`
- Expected route: build-status
- Actual route: `build_status -> python raphael.py build-status BUILD-20260621-ABC123`
- Status: Success
- Response snippet: {"dry_run": true, "command": ["build-status", "BUILD-20260621-ABC123"]}
- Result: PASS
- Timestamp: 2026-06-22T19:20:03
- Detail: None

## 9. Show DELIB routing

- Input message: `Review DELIB-20260621-ABC123`
- Expected route: deliberation-show
- Actual route: `deliberation_show -> python raphael.py deliberation-show DELIB-20260621-ABC123`
- Status: Success
- Response snippet: {"dry_run": true, "command": ["deliberation-show", "DELIB-20260621-ABC123"]}
- Result: PASS
- Timestamp: 2026-06-22T19:20:03
- Detail: None

## 10. Show PLAN routing

- Input message: `Review PLAN-20260621-ABC123`
- Expected route: execution-plan-show
- Actual route: `execution_plan_show -> python raphael.py execution-plan-show PLAN-20260621-ABC123`
- Status: Success
- Response snippet: {"dry_run": true, "command": ["execution-plan-show", "PLAN-20260621-ABC123"]}
- Result: PASS
- Timestamp: 2026-06-22T19:20:03
- Detail: None

## 11. Blocked Etsy publish

- Input message: `publish this to Etsy`
- Expected route: refused
- Actual route: `blocked`
- Status: Refused
- Response snippet: Refused: Etsy publishing is blocked.
- Result: PASS
- Timestamp: 2026-06-22T19:20:03
- Detail: None

## 12. Blocked Printify upload

- Input message: `upload to Printify`
- Expected route: refused
- Actual route: `blocked`
- Status: Refused
- Response snippet: Refused: Printify uploads are blocked.
- Result: PASS
- Timestamp: 2026-06-22T19:20:03
- Detail: None

## 13. Blocked ad spending

- Input message: `spend $20 on ads`
- Expected route: refused
- Actual route: `blocked`
- Status: Refused
- Response snippet: Refused: Spending or moving money is blocked.
- Result: PASS
- Timestamp: 2026-06-22T19:20:03
- Detail: None

## 14. Service action

- Input message: `start ComfyUI`
- Expected route: service-start comfyui confirmation
- Actual route: `service_start -> python raphael.py service-start comfyui`
- Status: Confirmation Required
- Response snippet: Ready to start the allowlisted local ComfyUI service. Confirm to continue.
- Result: PASS
- Timestamp: 2026-06-22T19:20:03
- Detail: None

