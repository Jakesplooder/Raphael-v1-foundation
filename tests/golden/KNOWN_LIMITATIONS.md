# Golden Master - Known Limitations

## LLM Non-Determinism
The Builder smoke tests and Dashboard chat scenario tests (`tests/golden/chat/`) capture responses from the system. Because Large Language Model (LLM) outputs are inherently non-deterministic, these tests use a **deterministic LLM stub/mock** in the test harness instead of calling the real `OllamaProvider`. 

**Why:** This guarantees that the golden master payloads remain exactly stable and comparable across runs, ensuring parity checks don't fail due to token variation.
**Production Impact:** The production `OllamaProvider` and LLM integration remains completely untouched. The mocked response is strictly an artifact of the test harness and does not represent Raphael's actual dynamic runtime behavior.

## Infrastructure Capture
Infrastructure captures (`tests/golden/infra/docker_compose_ps.txt`) are environment-dependent. While they capture the state of containers at the time of generation, they should not be strictly compared for exact parity unless the test environments are identical.
