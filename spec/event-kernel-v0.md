# Language-neutral Event Kernel v0: A Falsifiable Runtime Contract

Status: Experimental implementation contract, 2026-10-31. Derived from DEC-008, DEC-009, DEC-012, and DEC-013. This specification is not a claim of real-market predictive validity.

## Research anchors

1. B. P. Zeigler, "DEVS representation of dynamical systems: Event-based intelligent control," NASA Technical Reports Server, 1989. https://ntrs.nasa.gov/citations/19890044726 . Discrete-event system specifications separate state transitions from the advance of simulated time.
2. D. Leijen, "Type Directed Compilation of Row-Typed Algebraic Effects," Microsoft Research, 2017. https://www.microsoft.com/en-us/research/publication/type-directed-compilation-row-typed-algebraic-effects/ . Effect interfaces can be separated from their runtime handlers.
3. Python Software Foundation, "heapq: Priority Queue Implementation Notes," https://docs.python.org/3/library/heapq.html . Insertion counters break ties stably for equal-priority events.

The Python reference kernel is an operational subset inspired by these sources, not a complete DEVS implementation, not a static effect system, and not a validated stochastic market model.

## Mechanism

A user-supplied model defines an opaque state `S` and transition function:

`step : (S, Event, PRNG) -> Transition[S]`

The transition returns the next state, zero or more scheduled events, and zero or more inert `EffectIntent` values. The kernel owns only the event calendar and PRNG. It does not own consumer personas, channel economics, campaign meanings, network connections, or data calibration.

An event is `(time, priority, name, payload)`. At runtime, the queue compares `(time, priority, insertion_index)`; insertion index increases strictly from 0. For equal time and priority, earlier scheduling wins. `time` must be finite and non-negative. Events scheduled by a transition cannot precede the currently processed event; at equal timestamps, a newly scheduled event cannot use a priority numerically smaller than the active event's priority. Zero-delay events are allowed, and a finite `max_events` rejects endless zero-delay chains.

`EffectIntent` is data, not an executed instruction. The kernel intentionally has no outbound handler. A future Simulation, Shadow, or Live adapter may consume the same intents, but the current kernel cannot authorize network effects. A Python callback can itself perform I/O; purity is a programming contract in v0, not an enforced sandbox. Calling a callback "pure" does not make arbitrary Python source safe to run.

## Falsifiable hypotheses

**H-K1 (Calendar order):** For any finite event sequence with valid timestamps and priorities, processing order is nondecreasing in `(time, priority)`; ties are stable in insertion order, including new events scheduled for the current timestamp. Counterexample: a later timestamp is processed first, or equal-time/equal-priority events reorder without an earlier insertion.

**H-K2 (Seeded replay):** For a deterministic transition that uses only its inputs and the supplied PRNG, identical initial states, seeds, and event streams produce identical final states, processed traces, and intents. Counterexample: two controlled runs differ. This says nothing about real-world forecasting accuracy.

**H-K3 (Temporal boundary):** Every processed event has finite `time >= 0`, no transition may schedule into the past, and processing stops at a finite event cap. Counterexample: the kernel accepts NaN/Infinity/negative timestamps, executes a retroactive event, or loops indefinitely on immediate self-scheduling.

**H-K4 (Domain and effect separation):** The kernel can execute a non-marketing state transition without importing marketing schemas, and records effect intents without performing provider I/O. Counterexample: an inventory or counter state requires `Audience`/`Campaign`, or the kernel dispatches external actions.

## Mathematical invariants

Let `Q` be the priority queue, `e_k` the k-th processed event, and `i(e)` its insertion ordinal:

1. `(time(e_k), priority(e_k), i(e_k)) <= (time(e_{k+1}), priority(e_{k+1}), i(e_{k+1}))` for any consecutive events processed in a complete run.
2. `time(e_new) >= time(e_current) >= 0` for any event emitted by the active transition.
3. `0 <= number_of_processed_events <= max_events` for a successful bounded run.
4. `Kernel(S, Events, seed) = Kernel(S, Events, seed)` for independent calls under the deterministic-transition premise.

Economic laws such as population conservation, wallet constraints, saturation, and settlement lag belong in a user model or a marketing standard library, never as unconditional kernel rules.

## Verification mapping

Implementation target: `funnelscript/src/funnelscript/core/event_machine.py`.
Regression suite: `funnelscript/tests/test_event_machine.py`.
Test cases: stable event order; same-time event insertion; two seeded replays; malformed timestamps and retrograde scheduling; event limit; horizon deferral; marketing-free counter state; unexecuted effect intent; rejection of malformed effect output values.

## Deferred, explicit non-goals

- The existing campaign AST, linter, and vectorized marketing simulator are unchanged.
- No generic `entity` or `agent` parser syntax yet.
- No actual Live or Shadow adapter, HTTP access, credential handling, or policy enforcement.
- No claims of causality, calibration, prediction, performance scaling, or sandboxing from unit-test success.
