# World Semantic Conformance Oracle v0

Status: Phase 006 research contract (experimental Python reference interpreter)
Scope: interpreter semantic conformance, not empirical simulation validation.

## Research anchors and governing decisions

Discrete-event ordering and a finite calendar derive from Zeigler's discrete-event
systems framework and the accepted event-kernel contract in
`spec/event-kernel-v0.md` (DEC-019). Snapshot-atomic transitions follow
`spec/rule-transitions-v0.md` (DEC-027). Source emission, pre-event guards,
exact event records, deterministic seeded samples, and confined source imports
follow DEC-028, DEC-029, DEC-030, DEC-031, and DEC-032 respectively.
The one-operator arithmetic and EOF boundary follow DEC-037 and
`spec/arithmetic-expressions-v0.md`. Those contracts are constraints, not
subjects of reinterpretation.

The oracle exercises a single, pure, domain-neutral source interpreter and its
existing event calendar. It does not prove observational equivalence with the
legacy StrategyAST runtime, the browser simulator, or any future engine.

## H-C1: Deterministic semantic replay

**Hypothesis:** Fixed World source (including imported bytes), exact-typed input
records, insertion order, seed, Python/package interpreter version, and run
configuration produce identical canonical byte traces on repeated invocations.

**Falsifier:** Any canonical trace byte differs for identical pinned inputs and
execution environment. A changed seed is a perturbation only when a separately
verified fixture predicts a different outcome; random collisions are possible.

Canonical trace envelope (JSON object):

```json
{
  "schema": "world-conformance/v0",
  "engine": {"package": "funnelscript", "version": "0.2.0a1"},
  "seed": 1,
  "configuration": {"until": null, "max_events": 100},
  "state": {"Owner": {"field": 0}},
  "processed": [{"time": 0, "priority": 0, "name": "Owner.Event", "payload": null}],
  "pending": [],
  "intents": []
}
```

Each processed or pending event is represented as `{time, priority, name,
payload}`. The event calendar's processed order is the runtime removal order
(time ascending, priority ascending, insertion ordinal ascending); pending
events are in that same total order at termination. Insertion ordinal itself
is not exposed by `RunResult`; its effect is observable by the event order.
No wall-clock timestamps exist: `time` is an abstract, finite, nonnegative
numeric World time. Preserve integer vs floating-point JSON numeric spellings,
including `0` versus `0.0`, as received or emitted by the interpreter.
Input-event ties are resolved in supplied list order. Emissions at the current
time retain the parent's priority and enter the calendar after already queued
events of that priority.

Canonical encoding: Python `json.dumps` with `sort_keys=True`,
`separators=(',', ':')`, `ensure_ascii=True`, `allow_nan=False`,
followed by UTF-8 encoding. All mapping keys are strings and sorted
recursively. Boolean, null, string, integer and finite binary64 float remain
distinct input classes. Floats use the Python interpreter's JSON round-trip
decimal encoding; do not round, approximate, or stringify numeric state.
Non-finite floats, including nested event payloads not otherwise accepted at
the World ingress boundary, cannot be serialized and must raise rather than
be replaced by JSON NaN extensions. The test harness does not promise
cross-language, cross-Python-version or cross-platform floating-point byte
identity. Version and seed provenance are mandatory fields. Engine version
is read from installed package metadata, not a fabricated constant.

## H-C2: Snapshot atomicity and RNG discipline

**Hypothesis:** For every handled event with state `S_before` and transition
expressions `e_i`, `rhs_i = evaluate(e_i, S_before, payload, rng)` before
any `rhs_i` is committed. A false pre-event guard consumes the event but
commits neither state updates nor emissions nor random draws. Executed
`sample` operators each consume exactly one draw in transition source order,
including degenerate distributions. Pure arithmetic consumes none.

**Falsifiers:** Swapping two fields reads an intermediate assignment; an
unmatched guard emits an event or shifts a later seeded sample; an arithmetic
transition shifts the sample stream.

## H-C3: Reject invalid operations at their documented boundary

**Hypothesis:** Source parser/lexer rejects incomplete or malformed source,
type checking rejects ill-typed expressions, unknown state/payload references
and literal-zero divisors, path validation rejects illegal imports, Event
construction rejects invalid times, ingress validates payloads even when guards
are false, and runtime rejects dynamic zero division and non-finite arithmetic
before the failing event's candidate state is committed.

**Falsifiers:** An invalid input passes its boundary, or a rejected event's
transition becomes an observable committed state update.

**Scope of failure atomicity:** `WorldExecutor.advance` returns a new
state on success and does not mutate its input state on a rejection;
`WorldExecutor._step` constructs its transition before handing it to the
event machine. `EventMachine.run` does not implement a multi-event rollback
transaction or expose committed partial results on failure. Do not claim
that a failure on event N reverses previously processed events or arbitrary
user reducers' external side effects.

## Mathematical and operational invariants

- `event_time_next >= event_time_current` for newly scheduled events;
  at the same time, emitted priority cannot precede the parent's priority.
- `events_processed <= max_events` for a successful bounded run; if further
  due events exist when the bound is reached, the interpreter raises.
- `transition_rhs = evaluate(expression, pre_event_snapshot)`.
- `identical_valid_inputs + identical_seed + identical_engine_version + identical_environment => identical_canonical_trace`.
- No implicit primitive coercion (including bool-to-int or int-to-float).
- Static `x / 0` is invalid; dynamic zero division and non-finite float
  results are controlled runtime errors.
- No compiler-level financial, marketing or economic conservation constraints.

## Reusable fixture protocol

`tests/fixtures/world-conformance/cases.json` is a UTF-8 JSON document with
a `schema` identifier and a `cases` array. Each case has a stable `id`,
a relative `source` path within that directory, an ordered `events` array
using `time, name, priority, payload`, a `seed`, and optional
`until`/`max_events`. Valid cases specify `expected` with complete state,
processed, pending and intents arrays. Invalid cases specify `reject` with
`boundary` (parse/type/import/ingress/runtime/calendar), exception class
and an error substring. Where a boundary precedes event submission, `events`
may be empty. All relative source paths are confined to the fixture root.
Expected state and traces are human-authored from source-level reasoning and
independent fixed sample reference values, never obtained from the subject
interpreter during the same assertion.

## Verification and epistemic limits

The corpus may establish local semantic conformance for its finite enumerated
cases; it cannot establish a general proof for every possible program or
event sequence. External market validity, statistical calibration, causal
inference and real-world prediction accuracy were **not tested**. They cannot
be inferred from deterministic replay or passing conformance tests.
