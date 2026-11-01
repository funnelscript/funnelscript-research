# Population Reference Evaluation v0 — Phase 007

Status: **BLOCKED — H-POP2 STOP**. Evaluation date: 2026-11-01. This is a negative architectural result with a small public-API counterexample, not a completed reference population or economic simulation.

## Provenance

- Application baseline: 534449b85b3731ea81ea5d4755db0c6bb8b0e67d (work/phase-006-world-conformance).
- Research baseline: ca0c03b2c97c9b7f974add2431550f79cc4aa704 (work/phase-006-world-conformance).
- Phase 007 branches: work/phase-007-population-contract in both. Baselines were checked against HEAD, current branches and clean staged/unstaged/untracked status before branch creation. Application/research source revisions during tests still equal the stated baselines; test and research files were uncommitted during these measurements.
- Host: Darwin 27.0.0, arm64, Apple MacBook Air; Python runtime through uv 3.12.13, FunnelScript 0.2.0a1, pytest 9.2.0. Research unittest uses system python3 3.9.6.
- Research contract: spec/population-reference-v0.md. Authoritative source: current WorldExecutor, EventMachine, SimulationEngine, TelemetryAggregator, packaged lead-response model.

## Hypothesis and coverage matrix

| Hypothesis | Falsifier / test coverage | Actual evidence | Classification |
| --- | --- | --- | --- |
| H-POP1 stable distinct IDs and exhaustive partition | Distinct population IDs at every checkpoint, including terminal/inactive | No public World population initializer or agent-ID-indexed state; legacy tensor positions are not public stable IDs | NOT TESTED / essential missing capability |
| H-POP2 stable keyed streams | Same matched owner/seed/trial retains draw after merely reversing equal-time cohort event order | P-RNG-ORDER-1; seed 1, two source owners swap their uniform draw outputs on order reversal | FALSIFIED relative to requested new population contract; expected under accepted current World semantics |
| H-POP3 monetary conservation and delayed receipts | Cash equation, receivables and settlement trail | Reference hand example 100 + 30 - 20 - 5 = 105 CUR; unpaid 30 CUR separately; no runtime ledger API; not tested against executable population | SPECIFIED / NOT RUNTIME-VERIFIED |

## Minimal independent fixture and scientific boundary

Fixture ID **P-RNG-ORDER-1**:
- Application tests/fixtures/population-reference/order-coupling.fnl: two source-named World agents, each with one uniform sampled transition.
- tests/fixtures/population-reference/order-coupling.json: seed 1, same time and priority, input event names reversed.
- tests/test_population_reference.py: two tests pin exact expected first/reversed results and deterministic replay. They demonstrate *the absence of order-invariant streams*, not that a population system exists.
- Golden provenance: exact first two CPython random.Random(1) draws, independently stated in Phase 006 research conformance corpus; neither expected value is computed from WorldExecutor within the test.
- Original order A,B -> A 0.13436424411240122 / B 0.8474337369372327.
- Reversed B,A -> A 0.8474337369372327 / B 0.13436424411240122.
- Identical order replays deterministically. H-POP2 desired equality fails.

RED probe (an explicitly exploratory desired-invariant assertion, not a regression-test fix):
  cd funnelscript
  uv run python - [inline public-API probe using order-coupling.fnl, comparing A,B vs B,A, seed=1]
  Actual: AssertionError: H-POP2 RED: matched owners changed under cohort/event order perturbation
  Exit code: 1. This is a genuine missing requested behavior, not an interpreter semantic defect.

GREEN boundary regression:
  uv run pytest tests/test_population_reference.py -v
  Actual: 2 passed in 0.13s. Exit 0.
  These tests assert exact actual shared-RNG behavior, not the missing future invariant. They do not constitute RED/GREEN implementation of keyed substreams; **no production code was changed**, and no claim of a completed TDD repair is made.

## Commands and current actual verification receipts

Executed in application root unless indicated:

| Command | Outcome | Exit |
| --- | --- | --- |
| uv run pytest tests/test_population_reference.py -v | 2 passed (STOP witness), 0.13s | 0 |
| uv run pytest tests/test_world_conformance.py -v | 50 passed, 0.19s | 0 |
| uv run pytest tests/test_event_machine.py tests/test_world_stochastic.py tests/test_world_rules.py tests/test_world_guards.py tests/test_world_emissions.py tests/test_world_payloads.py tests/test_world_modules.py -q | 201 passed, 3.17s | 0 |
| uv run pytest -q | 338 passed, 58 subtests passed, 6.50s | 0 |
| cd funnelscript-research && python3 -m unittest discover -s tests -v | 5 passed, 0.043s | 0 |

The global application total includes the two new boundary cases. The research suite does not test the population model; it checks existing research repository invariants. Frontend compatibility and code were not changed; Bun tests and build were **not run**. No test was weakened or silently skipped.

## Population-size trials and resources

| Agents | Segments | Trials | Seed | Wall-clock population duration | Peak memory | State/metric outputs |
| ---: | ---: | --- | --- | --- | --- | --- |
| 10 | planned 2 | NOT RUN | NOT APPLICABLE | NOT MEASURED | NOT MEASURED | NOT PRODUCED |
| 100 | planned 2 | NOT RUN | NOT APPLICABLE | NOT MEASURED | NOT MEASURED | NOT PRODUCED |
| 1,000 | planned 2 | NOT RUN | NOT APPLICABLE | NOT MEASURED | NOT MEASURED | NOT PRODUCED |

Methodology: no valid keyed population experiment could be executed, so no wall-clock or memory measurement was made. Pytest elapsed times are verification durations, **not** population performance benchmarks. No vectorized, parallel, independent-agent or scale capacity claim follows. Population conservation, terminal accounting, paired counterfactual reproducibility, simulated CAC/ROAS or cash reconciliation at those scales were not verified.

## Existing-engine compatibility and architecture review

Use the table in spec/population-reference-v0.md. World has named owner fields and one shared calendar RNG; legacy has a first-audience trial tensor, trial-level NumPy RNG, daily cash/receivable array and non-identical metric conventions. Its zero-spend ROAS and zero-conversion CAC conventions differ from reference undefined-ratio policy. Legacy telemetry uses an empirical interpolated percentile and mean over losses >= VaR, not necessarily the exact step-quantile expected shortfall specified here, and its cash-ruin label is not always identical to the declared cash-threshold predicate.

**Current recommendation:** Option B, preserve explicit dual-engine non-equivalence. Option A, World-backed population runner with adapter, is **Proposed** and requires accepted semantics for agent identity, stream derivation and trial/metric mapping. No ADR accepted or runtime migrated.

## Adversarial review and STOP record

Review checklist: state identity not evidenced; exclusive/exhaustive population transitions not evidenced; expected golden constants pinned independently; RNG substreams absent; reordering proven to alter matched outputs; paired counterfactual unsupported; hand cash identity internally consistent but model ledger absent; receivables must not finance spend; metric units/horizons and zero policies explicit; CVaR quantile tie handling distinguished from legacy; no model-generated numbers represented as empirical probabilities; no test-only third simulator or automatic financial compiler rule.

No production defect under accepted DEC-019/031 was found. Confirmed critical blocker: public World run does not accept stable (world_seed, agent_id, trial_id) substreams and no stable agent-based population router exists. Under Phase 007 STOP, no test scaffolding or production patch may silently implement this absent contract. This is not a failure of Phase 006 interpreter conformance.

Next executable dependent engineering action: a separately reviewed, hypothesis-first **population identity and keyed RNG contract/repair card** with an accepted ADR if architecture changes; implement via new RED tests at the public runtime seam while preserving existing default World RNG semantics, then resume Phase 007 to measure 10/100/1000 and prove metrics. Phase 008 empirical calibration remains dependent on completed population semantics and permitted observations. Independently executable Phase 005 disclosure work does not establish parity.

**External market validity, statistical calibration, causal inference, and real-world prediction accuracy were not tested.**

## Exact executable H-POP2 negative probe

Run in the application root (the assertion is intentionally expected to fail):

~~~sh
uv run python - <<'PY'
from pathlib import Path
from funnelscript.core import Event
from funnelscript.parser import Parser
from funnelscript.runtime.world_executor import WorldExecutor
p = Path('tests/fixtures/population-reference/order-coupling.fnl')
world = WorldExecutor(Parser.from_file(p))
forward = world.run([Event(0, 'A.Tick'), Event(0, 'B.Tick')], seed=1).state
reversed_order = world.run([Event(0, 'B.Tick'), Event(0, 'A.Tick')], seed=1).state
assert forward == reversed_order, 'H-POP2 RED: matched owners changed under cohort/event order perturbation'
PY
~~~

Actual exception: AssertionError with the stated H-POP2 RED message. The shell recorded PROBE_EXIT=1. The intentionally failing assertion is not included in the passing permanent regression suite because Phase 007 cannot implement this requested future behavior without out-of-scope semantics.

## Read-only review independence limitation

A separately executed read-only source/fixture audit checked accepted shared RNG ownership, legacy first-audience and trial RNG, telemetry percentile/CVaR semantics, pinned golden provenance, all nine ten-field metric definitions, domain-ledger arithmetic, no skipped or weakened tests, no third engine, staged file scope and both Git whitespace checks. The audit returned exit 0. The A2M Code Review Graph could not inspect this repository because its requested root was outside that graph tool's approved workspace. Consequently, no separate external/human reviewer verdict is claimed; independent adversarial reviewer sign-off remains unverified. This does not override the existing H-POP2 STOP result.


---

## Post-checkpoint Phase 007A evidence (historical STOP retained)

The Phase 007 STOP described above was correct at its recorded commit and execution date. An opt-in, domain-neutral, isolated-agent `PopulationExecutor` was subsequently introduced under the separate Phase 007A research contract. Its precise keyed identity and bounded verification are in `spec/population-identity-rng-v0.md` and `evals/population-identity-rng-v0.md`; the original negative P-RNG-ORDER-1 default-World fixture remains unchanged and passes. Do not conflate previously NOT RUN Phase 007 experiments with the separately measured Phase 007A 10/100/1000 independent-instance trials. Financial settlement, accounting and reference metric execution still have no verified implementation; Phase 007 remains BLOCKED.
