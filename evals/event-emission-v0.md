# Source Event Emission v0: Falsification and Verification

Research authority: [event-emission-v0.md](../spec/event-emission-v0.md).

## Verified behavior matrix

| Hypothesis | Probe | Regression boundary |
| --- | --- | --- |
| H-E1 | `test_emit_parses_with_forward_rule_reference`, `test_invalid_emissions_fail_at_typecheck`, `test_invalid_emit_syntax_is_rejected` | Source grammar, local handler lookup, numeric finite nonnegative delay |
| H-E2 | `test_emitted_event_runs_at_relative_time_on_same_calendar`, `test_fractional_delay_uses_world_time_units`, `test_cli_processes_emitted_events_from_real_file` | Emit at `t + delay`, then process with a typed handler |
| H-E3 | `test_emissions_preserve_source_order_for_same_time`, `test_horizon_leaves_emitted_events_pending`, `test_zero_delay_recursive_emission_is_bounded`, `test_zero_delay_emit_inherits_nonzero_event_priority` | Equal-time FIFO, deterministic replay, finite horizon and cycle limit |
| H-E4 | All previous `test_world_rules.py`, `test_event_machine.py`, and legacy marketing tests | No new scheduler, no external effect execution, backward compatibility |

## Observed TDD sequence (2026-10-31)

1. Before implementation, `uv run pytest -q tests/test_world_emissions.py` reported **10 failed, 3 passed**. The 10 failures were due to the old parser rejecting `emit`; three malformed-source rejection tests already passed and did not constitute RED evidence.
2. After parser and static checker support, the same command reported **5 failed, 8 passed**. The failures were in runtime event emission, pending calendars, recursion limits and the CLI-observed event count, providing behavioral RED.
3. After the `WorldExecutor` reducer emitted `Event` values via `Transition.events`, the focused suite reported 13 passed and the complete Python suite reported 99 passed. Review then exposed a nonzero-priority zero-delay error; a dedicated behavioral RED failed with `Cannot schedule retrograde priority`, after which inheriting the parent priority made the test GREEN. Final focused suite after a fractional-delay regression: **15 passed**; complete Python suite: **101 passed**.

To reproduce:

```bash
cd funnelscript
uv run pytest -v tests/test_world_emissions.py
uv run pytest -v
uv run main.py check examples/event_chain_world.fnl
uv run main.py run-world examples/event_chain_world.fnl --event Worker.Start@1
```

Success here does **not** validate consumer psychology, calibration, real-market trajectories, or any Live Execution permissions.

## Distribution and CLI evidence (2026-10-31)

- `uv run pytest -v`: **101 passed** on macOS with Python 3.12.13.
- `uv run main.py check examples/event_chain_world.fnl`: World Type Check Passed (one agent).
- `uv run funnelscript run-world examples/event_chain_world.fnl --event Worker.Start@1`: `processed_events=3`, `pending_events=0`, `Worker.progress=1`, `Worker.active=false`.
- `uv run main.py run-world examples/event_chain_world.fnl --event Worker.Start@1 --max-events 2`: controlled nonzero termination (`max_events reached before the calendar was exhausted`).
- `uv build`: exit code 0; produced `dist/funnelscript-0.1.0-py3-none-any.whl` and `dist/funnelscript-0.1.0.tar.gz`, including the World executor module.
- Both repositories passed `git diff --check` after documentation updates. Package artifact existence and CLI smoke do not prove clean-room installation on a new machine.
