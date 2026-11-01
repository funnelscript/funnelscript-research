# Phase 003 — Narrow Arithmetic and EOF Falsification Record

Research contract: [`spec/arithmetic-expressions-v0.md`](../spec/arithmetic-expressions-v0.md); accepted extension DEC-037.

## Test matrix

| Hypothesis | Decisive falsifier | Application probes |
| --- | --- | --- |
| H-AR1 | `Parser([])`/exhaustion leaks `IndexError`, truncated source hangs | `test_empty_parser_tokens_fail_with_deliberate_diagnostic`, `test_empty_or_truncated_source_fails_without_index_error`, `test_exhausted_non_eof_token_stream_has_deliberate_diagnostic` |
| H-AR2 | `*` or `/` missing, wrong result type, coercion, chained operators accepted, snapshot/RNG drift | `test_narrow_arithmetic_result_matches_static_type`, `test_arithmetic_accepts_typed_dynamic_right_operands`, `test_arithmetic_rejects_invalid_types_references_and_static_zero`, `test_chained_or_malformed_arithmetic_is_rejected`, `test_arithmetic_retains_pre_event_snapshot_and_seed_replay`, `test_arithmetic_expression_in_local_emitted_event_uses_pre_event_values` |
| H-AR3 | Static literal zero accepted, dynamic zero causes raw Python exception, non-finite output leaks, `//` broken | `test_dynamic_division_by_zero_is_controlled_and_atomic`, `test_division_by_negative_zero_from_payload_is_controlled`, `test_integer_division_float_conversion_overflow_is_controlled`, `test_arithmetic_rejects_runtime_nonfinite_result`, `test_rejects_nonfinite_float_literal_in_arithmetic`, `test_slash_comment_precedence_and_binary_tokenization`, `test_runtime_rejects_nonfinite_float_operand_before_arithmetic`, `test_cli_reports_dynamic_division_by_zero_as_world_error` |

## Measured local RED / GREEN (2026-11-01)

- Baselines: app `c5e4a7b`, research `0f73cc5`; original Git working trees clean on Phase 002 branches. Separate local `work/phase-003-parser-arithmetic` branches were created from these baselines. Historical `41f00f1` / `abe561f` diff checks showed only Phase 002 app tests and research documentation in scoped paths.
- Research spec and EBNF were authored before test/production edits. Focused pre-implementation `uv run pytest tests/test_world_rules.py tests/test_world_language.py -q --tb=short`: **exit 1, 44 failed, 45 passed**. Decisive failures included `IndexError: list index out of range` for `Parser([])`, `LexerError ... Unexpected character '*'`, and `LexerError ... Unexpected character '/'`. This was genuine missing behavior, not a test collection error.
- Identical focused test selection after minimal production implementation: **exit 0, 89 passed**. Expanded `-v` invocation: **exit 0, 89 passed**. `uv run pytest tests/test_world_stochastic.py -v`: **exit 0, 25 passed**.
- First application-wide `uv run pytest -q`: **exit 1, 1 failed, 282 passed, 58 subtests passed**. The new float-initializer finiteness check prematurely rejected an externally constructed `math.inf` state in `test_outbound_payload_is_checked_before_entering_pending_calendar`; its existing contract expects a controlled outbound validation error. Review removed this unintended state initializer policy change, retaining finite checks on arithmetic operands/results. Focused regression then **exit 0, 1 passed**.
- First post-fix application `uv run pytest -q`: **exit 0, 283 passed, 58 subtests passed**. An additional adversarial pass added three regression tests for non-finite runtime operands, emitted event snapshot arithmetic and CLI dynamic-zero diagnostics; `uv run pytest tests/test_world_rules.py tests/test_world_language.py -v`: **exit 0, 92 passed**; `uv run pytest tests/test_world_stochastic.py -v`: **exit 0, 25 passed**; final `uv run pytest -q`: **exit 0, 286 passed, 58 subtests passed**. Research `python3 -m unittest discover -s tests -v`: **exit 0, 5 tests passed**.
- `uv run funnelscript check examples/counter_world.fnl`: **exit 0**. Requested literal command `run-world ... --event Counter.Tick@0 --max-events 5`: **exit 1**, accurately reporting `Unknown event 'Counter.Tick'` because that file defines `Counter.Pulse` and `Counter.Halt`, not `Tick`. With `--event Counter.Pulse@0`: **exit 0**, processed 1 event and `Counter.count=1`. Example input was not silently altered.
- `cd apps/web && bun test`: **exit 0, 1 passed, 0 failed**. `bun run build`: **exit 0** (Vite built 2,226 modules).

## Interpretation

The interpreter meets the finite, exact-typed World arithmetic boundary in this test corpus. Seeded replay is deterministic with identical inputs/seed/runtime and snapshots remain pre-event. No dependency or marketing-specific numerical axiom was introduced. Unsupported chains/precedence, implicit casts, cross-runtime float bitwise reproducibility and empirically calibrated outcomes remain out of scope. The original `Counter.Tick` smoke command is an invalid fixture, not a language regression.

## Adversarial review receipt

Manual read-only scoped diff review covered comment precedence, EOF indexing, exact operator typing, static/dynamic zero and non-finite failures, snapshot semantics, emitted payload correctness, seeded replay, absence of new dependency or marketing-core coupling, and the spec/EBNF parity. The installed A2M code graph rejected the repository root as outside its approved graph workspace; no graph review is claimed. Confirmed finding: the first initializer finiteness check changed error precedence; corrected and retested. Additional adversarial integration tests passed. The literal requested `Counter.Tick@0` smoke invocation is an invalid example event; the working `Counter.Pulse@0` fixture is documented.
