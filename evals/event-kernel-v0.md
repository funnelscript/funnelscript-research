# H-K1 to H-K4: Language-Neutral Event Kernel Falsification Plan

The tested implementation lives in the sister `funnelscript` repository. These checks test scheduler semantics, **not** market predictive accuracy.

## Execution

From `/Users/mamdouhaboammar/Documents/funnelscript`:

```bash
uv run pytest -v tests/test_event_machine.py
uv run pytest -v
```

## Test-to-hypothesis mapping

| Hypothesis | Falsifying observation | Executable tests |
| --- | --- | --- |
| H-K1 chronological and stable ordering | Wrong order for same-time priority/tie or nested event | `test_orders_events_by_time_priority_and_stable_insertion`, `test_new_same_time_event_respects_existing_queue_order` |
| H-K2 seeded replay | Identical controlled runs produce different traces or numeric draws | `test_seeded_replay_is_deterministic_for_pure_user_model` |
| H-K3 temporal and finite execution | Nonfinite/negative timestamp accepted, past event scheduled, or self-loop silently unbounded | `test_rejects_invalid_event_timestamps`, `test_rejects_scheduling_into_the_past`, `test_rejects_retrograde_priority_at_current_time`, `test_event_limit_stops_unbounded_zero_delay_recursion`, `test_run_until_horizon_preserves_pending_events` |
| H-K4 domain neutrality and inert effects | Domain-specific model required for integer counter, intent sent externally | `test_non_marketing_state_and_inert_effect_intents`, `test_rejects_non_intent_effect_outputs`, `test_kernel_api_is_exported_from_core_package` |

## Limitations

The reference test model uses a Python callback. The tests do not prove its purity, static effect typing, actual Live/Shadow mode behavior, or posterior predictive validity. Failure to execute these commands is an **incomplete verification**, never a passing scientific evaluation.
