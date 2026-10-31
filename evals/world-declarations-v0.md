# World Declaration Core v0: Falsification Evaluation

Research contract: [world-declarations-v0.md](../spec/world-declarations-v0.md).

From the `funnelscript` working tree:

```bash
uv run pytest -v tests/test_world_language.py
uv run pytest -v
uv run main.py check examples/warehouse_world.fnl
```

| Hypothesis | Failure boundary | Test probes |
| --- | --- | --- |
| H-W1: Domain-neutral parsing | A world requires marketing-specific nodes or returns legacy strategy AST | `test_parses_general_world_with_typed_entities_and_agents`, `test_empty_world_is_valid` |
| H-W2: Literal typing and uniqueness | Invalid state type, duplicate names, or malformed source silently passes | `test_rejects_duplicate_entity_and_agent_names`, `test_rejects_duplicate_state_field_names`, `test_rejects_unknown_types`, `test_rejects_mismatched_literal_types`, `test_rejects_malformed_or_unknown_world_syntax` |
| H-W3: Agent subtype | Agent AST is not a subtype of entity AST | `test_parses_general_world_with_typed_entities_and_agents`, `test_world_types_are_available_from_compiler_api` |
| H-W4: Backward compatibility and execution boundary | Old strategy parsing breaks, CLI routes worlds into legacy marketing simulator | `test_existing_strategy_parser_remains_compatible`, `test_soft_keywords_remain_valid_in_strategy_metadata`, `test_world_cli_check_accepts_valid_and_rejects_bad`, `test_legacy_simulator_rejects_world_instead_of_using_campaign_engine` |

Passing these tests establishes only the exercised syntax and typing behavior. It does not establish operational semantics for agent decisions, market realism, causal impact, effect sandboxing, or external live execution.
