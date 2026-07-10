# Golden Master Known Limitations

This snapshot serves as the definitive behavioral baseline for Epic D. However, note the following limitation:

## Builder Smoke Test Non-Determinism
The `test_builder_outputs_stay_in_workspace` test (located in `tests/test_builder.py`) utilizes a deterministic mock for the `OllamaProvider.reason` method.
- **Reason:** The underlying Llama 3.1 8B LLM outputs are inherently non-deterministic and occasionally fail to conform strictly to the requested JSON schema, causing the parsing logic in `BuilderEngine` to fail unpredictably.
- **Scope:** This mock is isolated purely to the test harness. The production `OllamaProvider` remains untouched and continues to interact with the live model.
- **Classification:** This test is classified as a *behavioral smoke test*, not a strict regression parity test for the LLM's reasoning engine itself.
