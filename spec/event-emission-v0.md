# Scheduled Source Events v0: Causal World Reactions

Status: Research-gated experimental World-language extension, 2026-10-31. Follows DEC-019 (event kernel), DEC-022 (typed Worlds), and DEC-027 (snapshot-atomic rules). Decision proposal: DEC-028.

## Research anchors

1. Bernard P. Zeigler, *DEVS Representation of Dynamical Systems: Event-Based Intelligent Control*, NASA Technical Reports Server (1989), https://ntrs.nasa.gov/citations/19890044726 . Discrete event models schedule internal transitions without continuous polling.
2. SimPy 4.0.2, *Time and Scheduling*, https://simpy.readthedocs.io/en/4.0.2/topical_guides/time_and_scheduling.html . Discrete event calendars process timestamped events and preserve first-scheduled ordering for equal-time events.
3. FunnelScript Event Kernel v0, `spec/event-kernel-v0.md`, and World Rule Semantics v0, `spec/rule-transitions-v0.md`. The existing machine already enforces temporal and event-count bounds.

## Smallest source contract

```funnelscript
world FollowUp {
  agent Worker {
    state count: int = 0;

    rule Begin on event Start {
      emit Tick after 2;
    }
    rule Advance on event Tick {
      transition count = count + 1;
    }
  }
}
```

`emit EventName after Delay;` is a contextual statement permitted inside a World `rule` block alongside `transition`. `Delay` is a primitive `int` or `float` literal, finite, non-negative, measured in the host World's abstract time units. It is **not** a dynamic expression or physical time-unit declaration. The emitted event is addressed to the same declaration (`Owner.EventName`). A matching `rule ... on event EventName` **must** exist within that declaration; forward references are valid.

The runtime schedules event `e' = (time(e) + Delay, Owner.EventName, priority(e))` through the existing `EventMachine` event queue. The generated event inherits its parent event's priority, preventing a zero-delay event from retrogressing to an earlier priority. Source emissions are pure data, not platform I/O or effect handlers. All `transition` assignments evaluate against the pre-event state; emissions neither re-enter the current rule nor change this snapshot. Multiple emissions retain source order, even if separated by transition statements. The runtime never silently lowers an event's priority.

## Falsifiable hypotheses

- **H-E1, Source and type:** Valid `emit` produces typed emission AST. Missing `after`, unknown handler, nonnumeric/negative/nonfinite delay, or unsupported syntax fails before runtime. Counterexample: malformed emission reaches execution.
- **H-E2, Causal schedule:** A `Start@3` that emits `Tick after 2` invokes the Tick handler at time 5, including when the Tick rule appears later in the source. Counterexample: immediate execution or incorrect timestamp.
- **H-E3, Bounded and deterministic:** Emitted events inherit the parent event priority, preserve chronological ordering and equal-time FIFO order; recursive zero-delay emission is stopped by `max_events`, and a horizon leaves future events pending. Counterexample: implicit busy-loop, unordered events, or hang.
- **H-E4, Non-regression and safety:** The legacy marketing simulator, source-only World rules, explicit input CLI, and inert effect boundary remain unchanged. Counterexample: unwanted provider call, new scheduler, or broken existing suite.

## Mathematical and architectural invariants

For each input event `e` at `t >= 0`, for each emitted delay `d`:

1. `d ∈ {finite real numbers | d >= 0}` (lexically int or float); `t_emit = t + d >= t`; `priority_emit = priority_parent`. Event construction also checks finite resulting times.
2. `(owner(e), emitted_name)` must resolve to exactly one statically defined local handler.
3. `S_after = transition(S_before, e)` before the next queued event starts, while all assignments of one handler read the same `S_before`.
4. Every scheduled event is inserted through the existing event calendar. Total processed events do not exceed the configured `max_events`; violating the limit raises an explicit failure.
5. No `EffectIntent` is created or dispatched; no external platform is contacted by source emission.

## Known boundaries

- One initial event is still externally supplied; no automatic World startup event exists yet.
- At this v0 milestone there was no cross-entity emission, probabilistic delay, payload, conditions, persistent scheduler, cancellation, concurrency, or Live/Shadow effects. Subsequent independently tested additions specify conditional guards (`spec/world-guards-v0.md`) and typed local payload records (`spec/typed-event-payloads-v0.md`); the remaining boundaries still apply.
- This extends a small operational interpreter, not a validated model of human behavior or market forecasts.

## Evaluation routing

Tests: `funnelscript/tests/test_world_emissions.py` (new) and existing World, EventMachine, and campaign suites. Evidence: `evals/event-emission-v0.md`.
