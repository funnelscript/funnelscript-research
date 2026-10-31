# Rule and Transition Semantics v0: Falsification Evaluation

Research contract: [rule-transitions-v0.md](../spec/rule-transitions-v0.md).

From the `funnelscript` working tree:

```bash
uv run pytest -v tests/test_world_rules.py
uv run pytest -v
uv run -m funnelscript.cli run-world <path.fnl> --event Owner.Event@Time
```

| Hypothesis | Failure boundary | Test probes |
| --- | --- | --- |
| **H-R1: Parse and type** | Malformed rules, invalid operators, unknown targets/sources, duplicate handlers, or type mismatches silently pass | `test_rule_source_parses_to_typed_ast`, `test_typechecker_rejects_invalid_transition`, `test_checker_rejects_ambiguous_handlers`, `test_parser_rejects_invalid_rule_syntax` |
| **H-R2: Snapshot semantics** | Sequential assignment mutation corrupts pre-event snapshot state, or original state is modified in place | `test_simultaneous_transitions_use_before_event_state`, `test_existing_other_entity_state_is_not_mutated`, `test_executor_isolates_checked_world_from_caller_mutations` |
| **H-R3: Event-machine integration** | Chronological ordering fails, seed replay diverges, or processing limits are ignored | `test_event_calendar_order_and_seeded_replay`, `test_agent_can_react_to_event`, `test_unknown_qualified_event_fails_explicitly`, `test_world_runner_respects_event_processing_limit` |
| **H-R4: Safe CLI boundary and compatibility** | `run-world` invokes legacy marketing simulator, executes external network I/O, or breaks existing campaigns | `test_cli_runs_rules_from_fnl_file`, `test_legacy_strategy_remains_unsupported_for_world_runner`, full regression suite |

Passing these tests establishes only that declarative source rules execute small-step state updates via the discrete-event calendar substrate. It does not establish autonomous agent decision-making, market prediction, or arbitrary side-effect sandboxing.

## Observed local verification (2026-10-31)

- Initial test-first RED: 18 failed, 3 passed, before adding the grammar and interpreter. After AST/parser implementation: 13 passed, 8 failed (remaining executor/CLI boundaries). After executor implementation: 20 passed, 1 failed (missing CLI). After the first implementation: 21 focused tests passed. A review-discovered mutable-AST defect then failed a new RED test (`999 != 2`); retaining a deep copy of the checked AST made it green: **22 focused tests passed**.
- Complete Python regression suite: **86 passed** via `uv run pytest -q`.
- Limit: deterministic interpreter tests do not measure market-model accuracy or performance at million-agent scale.
