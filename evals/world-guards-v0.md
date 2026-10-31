# Typed World Guards v0: Falsification Evaluation

Contract: [world-guards-v0.md](../spec/world-guards-v0.md).

## TDD evidence (2026-10-31)

1. Initial RED with `uv run pytest -q tests/test_world_guards.py`: **16 failed, 4 passed**. The new `<` and `>` tokens and guard grammar were unrecognized; malformed-guard tests already rejected source and were not counted as implementation proof.
2. After lexical, AST and parser/type-checker support: **5 failed, 15 passed**. The remaining failures showed the runtime ignored guards, causing unbounded `emit` recursion, incorrect false-branch assignments, and a CLI failure.
3. After introducing a pure pre-event guard evaluator into `WorldExecutor`: **20 focused passed** and **121 total Python tests passed**.

## Coverage matrix

| Hypothesis | Tests and falsifier |
| --- | --- |
| H-G1 | `test_guard_is_typed_ast_node`, `test_typechecker_rejects_invalid_guard`, `test_malformed_guards_are_rejected`: incorrect or non-primitive guards are rejected |
| H-G2 | `test_false_guard_skips_transition_and_emit`, false comparison parameter cases: no state mutation and no new events on false guards |
| H-G3 | `test_guarded_reaction_chain_stops_without_exhausting_event_cap`: four events processed, final value three, empty pending calendar |
| H-G4 | `test_boolean_and_string_equality_guards`, `test_cli_executes_guarded_world_from_source`, the full existing suite: compatibility and pure interpreter behavior |

## Reproduction

```bash
cd funnelscript
uv run pytest -v tests/test_world_guards.py
uv run pytest -v
uv run main.py check examples/guarded_world.fnl
uv run main.py run-world examples/guarded_world.fnl --event Counter.Tick@0 --max-events 5
```

Expected: `processed_events = 4`, `Counter.value = 3`, and `pending_events = 0`.

This does not establish stochastic agent behavior, empirical causal identification, market forecasting accuracy, or Live platform authorization.
