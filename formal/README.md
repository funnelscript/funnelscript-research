# FunnelScript Event Kernel: Mechanized Model, Milestone 1

## Research anchor and falsifiable claims

Contract: `spec/event-kernel-v0.md`, especially H-K1 to H-K3. The event-calendar model follows discrete-event semantics (Zeigler, 1989) and stable priority queue ordering (`heapq`, Python documentation).

* **H-F1**: For all successful finite runs in the Lean model, each processed event's timestamp is no earlier than the previous event's timestamp. Counterexample: a trace violating `ChronologicalFrom`.
* **H-F2**: The same reducer, complete machine state (including seed, clock, pending events and insertion ordinal), and event limit produce equal final state and trace. Counterexample: two calls to `run` on equal inputs producing different results.

The model orders `(time, priority, insertion ordinal)`, rejects emissions into the past and same-time priority retrogression, and gives every emission an ordinal. `run` uses explicit finite fuel, not unrestricted recursion.

## Verification boundary

The formal model uses `Nat` time and a pure Lean reducer with an explicit deterministic seed threaded through transitions. Python accepts finite, non-negative `int` and `float` timestamps, and uses Python `random.Random`. This Lean artifact **does not** prove floating-point ordering equivalence, CPython PRNG bit parity, the absence of external side effects in arbitrary Python reducers, or Python runtime type soundness.

In this milestone, invalid emission and time contracts yield `none` in `advance`; the reference Python implementation throws an exception. The theorem applies to successful executions, not to error-message equivalence. `run` stops when fuel expires, while Python raises on exceeding `max_events`. This distinction requires separate verification before asserting interpreter conformance.

`timestamp_monotonicity` is about the executable `run` function, not an assumed pre-sorted trace. The theorem follows from the time-checking witness built by `advance`. `deterministic_replay` establishes extensional determinism of the pure model, conditional on identical full inputs. Neither theorem claims scientific predictive accuracy.

## Build

From the `formal/` directory:

```bash
lake build
rg -n '\b(sorry|admit)\b|^\s*axiom\b' Formal.lean Formal/
```

The source is intended to compile without `sorry`, `admit`, or custom axioms. Only a successful real `lake build` establishes verified build status.

## Deferred

Typed Worlds, progress and preservation, guard and payload soundness, exact stochastic distribution semantics, float fidelity, bounded-recursion error parity, and the differential oracle belong to subsequent milestones. The initial property-based suite in the implementation repository focuses on the existing Python kernel's observable contracts.
