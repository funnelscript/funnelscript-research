# Typed Event Payloads v0: Falsification and Verification Evidence

Contract: [Typed Event Payloads v0](../spec/typed-event-payloads-v0.md). Evaluation date: 2026-10-31.

## RED / GREEN timeline

1. **Baseline:** The existing World regression suite (rules, emissions, guards) passed **57/57** before feature implementation.
2. **Initial RED:** New `tests/test_world_payloads.py` produced **29 failed tests** against the original parser/runtime. Missing `event Credit(amount: int)` grammar, `payload.amount` access, emission arguments, runtime validation, and JSON event input were observable.
3. **Typed compile/parse milestone:** After adding source schemas and AST checks, the same suite had **17 failed / 12 passed**. Remaining failures exercised the runtime and CLI boundaries, including a wrong diagnostic precedence on extra source event arguments.
4. **Initial GREEN:** After runtime payload reads, source emissions and JSON input: **29 passed**.
5. **Adversarial RED 1:** Four added tests failed because IEEE-754 `NaN`, `+Infinity` and `-Infinity` flowed into World state and even JSON output. Explicit finite-float runtime checks made **33 passed**.
6. **Adversarial RED 2:** Two added tests failed: mixed Python dictionary key types raised an unrelated `TypeError` during sorting, and a future emitted message could enter the pending event calendar with an invalid payload. Non-string key rejection and pre-enqueue validation made **35 passed**.
7. **Privacy RED 3:** One additional test failed because an invalid legacy `--event` string was echoed verbatim into stderr. The CLI now reports a generic syntax diagnostic without disclosing user-supplied input, making **36 focused tests pass**.
8. **Ambiguous JSON RED 4:** One test failed because `json.loads` accepted duplicate `amount` keys and silently used the second value. A parser hook now rejects duplicate JSON keys at all nesting levels, making **37 focused tests pass**.
9. **Final fresh verification:** `uv run pytest -q` yielded **158 passed in 2.61s**, and `uv build` generated both sdist and wheel successfully after the final code change. `uv run python -m compileall -q src/funnelscript` and `git diff --check` also passed.

## Hypothesis-to-test matrix

| Research hypothesis | Falsification probes |
| --- | --- |
| H-P1, static source types | `test_payload_source_has_typed_ast_nodes`, `test_event_declaration_errors`, `test_static_references_and_emission_arguments`: unknown event fields, duplicate schemas/arguments, wrong value types, invalid expressions |
| H-P2, exact input record | `test_input_payload_is_read_by_rule`, `test_inbound_payload_shape_and_types`, `test_false_guard_does_not_bypass_payload_validation`, `test_invalid_python_payload_keys_fail_with_world_error`, `test_float_event_payload_must_be_finite`: missing/extra/non-string fields, strict bool/int, nonfinite floats |
| H-P3, causal local emission | `test_source_emission_payload_uses_pre_event_snapshot`, `test_delayed_payload_is_visible_as_pending_event`, `test_outbound_payload_is_checked_before_entering_pending_calendar`, `test_emission_order_and_payload_replay`: snapshot semantics, temporal behavior, calendar safety |
| H-P4, compatibility and no effects | `test_zero_field_and_legacy_events_stay_compatible`, `test_undeclared_event_rejects_untyped_payload`, `test_cli_reads_typed_event_json_without_executing_code`, `test_cli_malformed_event_does_not_echo_input_contents`, `test_cli_rejects_duplicate_json_event_fields`, full 158-test Python regression suite |

## Real source and CLI probes

```bash
cd funnelscript
uv run pytest -v tests/test_world_payloads.py
uv run pytest -v
uv build
uv run main.py check examples/payload_world.fnl
uv run main.py run-world examples/payload_world.fnl --event Wallet.Start@3
uv run main.py run-world examples/payload_world.fnl --event '{"name":"Wallet.Credit","time":0,"payload":{"amount":8}}'
```

Observed:

- External `Wallet.Credit@0` JSON record: `balance=8`, `processed_events=1`, `pending_events=0`.
- Internal `Wallet.Start@3` with `Credit(amount = quota) after 2`: `balance=10`, `quota=0`, `processed_events=2`, `pending_events=0`.
- `uv build`: `dist/funnelscript-0.1.0.tar.gz` and `dist/funnelscript-0.1.0-py3-none-any.whl` built successfully.

## Evidence and scope

The tests establish deterministic typed-message behavior under the source subset. They do **not** establish empirical realism, monetary correctness, cross-owner delivery, causal identification, Bayesian calibration, durable queues, or authorization for Live effects.
