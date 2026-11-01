# World Conformance Evaluation v0 — Phase 006

Status: complete local experimental reference-interpreter evaluation, 2026-11-01.
Contract: `spec/world-conformance-v0.md`; governing accepted decisions:
DEC-019, DEC-027, DEC-028, DEC-029, DEC-030, DEC-031, DEC-032, DEC-037.

## Tested source and environment

- Application revision (complete test and documentation snapshot):
  `534449b85b3731ea81ea5d4755db0c6bb8b0e67d` on
  `work/phase-006-world-conformance`.
- Application production revision remains unchanged since Phase 003:
  `f95b3b32c3c7a8ae5635c99ea552d59089be2fdd`.
- Research evaluation authored against research Phase 003 baseline
  `1e9708d908db703b7028c04291439245217402c2` on
  `work/phase-006-world-conformance`; research Phase 006 commit is recorded
  in the local completion plan and Git history.
- Python/package interpreter: FunnelScript `0.2.0a1`; Python `3.12.13`;
  `pytest 9.2.0`, `pluggy 1.7.0`; uv `0.11.31`.
- Host for executed application tests: Darwin `27.0.0 arm64`.
  Independent standard-library draw values additionally checked under
  system Python `3.9.6`; this is not a cross-platform conformance claim.
- Source fixtures: `funnelscript/tests/fixtures/world-conformance/` (14
  original source files plus `overflow.fnl` for the corrected probe);
  versioned corpus: `cases.json`.
- No browser/TypeScript test or frontend build was rerun: frontend code
  and compatibility were not modified.

## H-C1 / H-C2 / H-C3 conformance matrix

| Hypothesis | Oracle coverage | Decisive observable | Local outcome |
| --- | --- | --- | --- |
| H-C1 deterministic replay | C-SNAPSHOT, C-ORDER, C-RNG-SEED-1, C-RNG-SEED-2, C-RNG-NO-SKIP, C-TYPED, C-PENDING, C-IMPORT, C-ARITH | Each full canonical state + processed/pending trace matches a fixed authored golden in three fresh parses/executions | Confirmed for enumerated fixtures |
| H-C1 input perturbation | C-ORDER with positions 1 and 3 exchanged; C-RNG-SEED-1 vs C-RNG-SEED-2 | Equal-time insertion swap changes canonical event order; pinned distinct seed samples differ | Perturbation detected, no universal different-seeds claim |
| H-C2 pre-event snapshot | C-SNAPSHOT and C-ARITH | Swapping 1/2 yields 2/1; independent assignments use initial field values | Confirmed for fixed fixtures |
| H-C2 false guard / draw order | C-RNG-SEED-1, C-RNG-NO-SKIP, C-RNG-SEED-2, R-GUARDED-PAYLOAD | Skipped guard leaves later Uniform/Bernoulli draw positions intact and emits nothing; invalid payload is rejected before guard | Confirmed for fixed fixtures |
| H-C3 compile/load boundary | R-EOF, R-REF, R-MIXED-TYPES, R-LITERAL-ZERO, R-IMPORT-PATH | Deliberate ParserError / WorldTypeError at declared boundary | Confirmed |
| H-C3 event-ingress boundary | R-PAYLOAD-MISSING, R-PAYLOAD-BOOL, R-PAYLOAD-EXTRA, R-GUARDED-PAYLOAD, R-UNKNOWN-EVENT | WorldExecutionError before candidate state mutation | Confirmed |
| H-C3 runtime / calendar | R-DYNAMIC-ZERO, R-LIMIT; separate invalid time, horizon, cap, non-finite-operand and non-finite-result tests | Controlled errors; rejected-event input state remains unchanged | Confirmed |

## Independently authored fixture expectations

Valid cases:

| ID | Fixed expectation |
| --- | --- |
| C-SNAPSHOT | Pair left/right swap: `{left:2,right:1}`; one event at 0 |
| C-ORDER | Priority -1 payload 2 first, priority 0 Trigger second, then input 1, input 3, emitted 4 last; sum 10 |
| C-RNG-SEED-1 | Skip at 0 then Tick at 1, first sample 0.13436424411240122, Bernoulli false, count 1 |
| C-RNG-SEED-2 | Same inputs, first sample 0.9560342718892494, Bernoulli false, count 1 |
| C-RNG-NO-SKIP | Tick at 1 without Skip; same state as C-RNG-SEED-1 |
| C-TYPED | Apply 3 at 0 emits Follow 3 at 1, both consumed; Sink.seen = 6 |
| C-PENDING | Same Apply processed until time 0; Follow 3 remains pending at 1, Sink.seen = 3 |
| C-IMPORT | Imported.Pulse at times 0 and 2, aliased state total = 2 |
| C-ARITH | Exact int +/-/*: 7/6/12; float division 9.0/3.0 = 3.0; other float state retained |

Rejection cases:

| ID | Boundary | Independent expected failure |
| --- | --- | --- |
| R-EOF | parse | truncated expression, `ParserError` |
| R-REF | type | unknown state reference, `WorldTypeError` |
| R-MIXED-TYPES | type | int/float mismatch, `WorldTypeError` |
| R-LITERAL-ZERO | type | static zero denominator, `WorldTypeError` |
| R-IMPORT-PATH | import | parent traversal, `ParserError` |
| R-DYNAMIC-ZERO | runtime | float-state zero divisor, `WorldExecutionError` |
| R-PAYLOAD-MISSING | ingress | missing exact-typed input field |
| R-PAYLOAD-BOOL | ingress | bool sent where int required |
| R-PAYLOAD-EXTRA | ingress | extra input field |
| R-GUARDED-PAYLOAD | ingress | malformed input rejected despite false rule guard |
| R-LIMIT | calendar | zero-delay self-emission exceeds `max_events=2` |
| R-UNKNOWN-EVENT | ingress | unknown handler rejected before state update |

The serialized goldens are manually authored in `cases.json`. No expected
values are obtained by calling the World interpreter in the same assertion.
Hand-calculated integer state, source-level event scheduling and type rules
supply the deterministic values. For stochastic provenance, independent
CPython standard-library `random.Random` draws observed under system Python
3.9.6 were seed 1: `0.13436424411240122`,
`0.8474337369372327`; seed 2: `0.9560342718892494`,
`0.9478274870593494`. The first values are Uniform(0.0, 1.0)
outputs and the second values exceed the Bernoulli 0.5 threshold.
These constants were fixed before the comparison; the test never calls
`WorldExecutor` to obtain its expected golden.

## Test-first execution record and verified commands

First execution after independent corpus authoring:

```text
cd funnelscript
uv run pytest tests/test_world_conformance.py -v
exit 1: 47 passed, 2 failed
C-ARITH: runtime float state vs golden integer JSON representation
test_non_finite_arithmetic_rejects_before_caller_state_mutation:
    DID NOT RAISE WorldExecutionError for 1e308 / 1e308
```

Both failures were fixture/test-construction mistakes, **not** confirmed
production defects. The JSON writer had erased the `.0` spelling and a
mathematically finite quotient was incorrectly used as an overflow case.
The correction preserved explicitly typed float golden literals and used
`1e308 * 1e308` in a dedicated source fixture. No interpreter source was
changed, no assertion weakened and no RED was manufactured. The corrected
focused suite passed 49 cases; an additional same-priority order
perturbation test raised the count to 50.

Latest complete commands, executed on the exact committed application tree
(the final focused and full application suites were run immediately before
the application commit, with no intervening source edits):

```text
cd funnelscript
uv run pytest tests/test_world_conformance.py -v
exit 0: 50 passed

uv run pytest tests/test_event_machine.py tests/test_world_rules.py \
  tests/test_world_language.py tests/test_world_guards.py \
  tests/test_world_payloads.py tests/test_world_stochastic.py \
  tests/test_world_modules.py -v
exit 0: 213 passed

uv run pytest -q
exit 0: 336 passed, 58 subtests passed

cd ../funnelscript-research
python3 -m unittest discover -s tests -v
exit 0: 5 passed
```

The research unittest command is rerun after writing this evaluation before
the research commit. The frontend was not tested: no frontend parity claim
is made.

## Independent adversarial read-only review

A separate post-construction diff and fixture-schema review checked all 21
stable case IDs, source-path confinement, mutually exclusive valid/rejection
outcomes, explicit `int` vs `float` values, version/seed provenance,
deterministic three-run replay, event time/priority/insertion ordering,
false-guard draw suppression, input payload validation prior to guards,
snapshot state, module aliases and traversal rejection, event cap,
non-finite numeric rejection and compatibility with six existing examples.
`git diff --check` reported no whitespace errors. The scoped application
diff contained no changes under `src/funnelscript/`, `apps/web/`,
`examples/` or `pyproject.toml`.

Corrections from that scrutiny: the two mistaken expected RED fixtures above,
plus an explicit trace-sensitivity test that perturbs equal-priority insertion
order. No production semantic defect was observed; no STOP repair card was
required. An optional A2M code graph review was unavailable because this
repository lay outside that graph tool's approved workspace; review therefore
used read-only Git diffs and an independent schema/type inspection rather
than claiming a graph review or a second-model reviewer.

## Confirmed boundaries and next dependency

Conformance is finite-case evidence, not a mechanized universal proof.
The current Python runtime does not implement multi-event rollback on a
failed run, and the fixture schema does not expose insertion ordinal as an
event field. Reproducibility is scoped to pinned source/inputs/seed/version,
host runtime and Python float serialization. No generic browser or legacy
StrategyAST engine comparison was run.

**External market validity, statistical calibration, causal inference and
real-world prediction accuracy were not tested.** Neither market economics
nor financial conservation is a compiler-level assertion of this oracle.

Phase 007 (`plans/007-population-reference-contract.md`) is the next
dependent executable research-and-test card: define a reference population,
agent-id/trial-id RNG substreams, metric units and cash/receivable accounting,
a two-segment pilot and explicit legacy non-equivalence boundaries. Phase
007 must be started separately and cannot inherit external validity claims.
