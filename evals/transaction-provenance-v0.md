# Phase 007C — Transaction Provenance Evaluation v0

Date: 2026-11-01. Status: BOUNDED IMPLEMENTATION VERIFIED (proposed, no new accepted ADR).

## Implemented trace boundary

- `WorldExecutor.run(trace=[])` observes each actually invoked World transition, preserving the unmodified `EventMachine` calendar and original `RunResult` API; rejects previously populated trace sinks.
- `PopulationExecutor.run(trace=True)` supplies agent-local ordered trace steps in `PopulationResult.steps`, including rejected guards, state before/after and processed-event index. Index is the adapter's processed ordinal, **not** the kernel heap tie-break ordinal.
- Marketing `DeclaredSalePolicy` explicitly defines a state-field change by event name and exact source/target values, recognized amount, currency and attribution. `recognize_sales` validates complete per-agent trace linkage to processed events and final state and creates SHA-256 encoded versioned IDs. `post_provenanced_trial` compares every supplied sale to the actual reconstructed trace, merges identical retries, rejects conflicts, missing and invented provenance, and applies all posted money using the unmodified `MarketingLedger` and its existing exact minor-unit checks.
- External paid spend, other costs, settlements and writeoffs remain explicitly authored financial inputs; only policy-derived sales are claimed as World-caused. No general transaction scheduler, default economic inference, compiler, or legacy changes.

## RED/GREEN evidence (observed, not test-after claims)

1. `uv run pytest -q tests/test_transaction_provenance.py` exited nonzero: one behavioral assertion failure `No event-to-transition evidence exists in the population result` because `PopulationResult.steps` was absent. After opt-in World/Population trace, `uv run pytest -q tests/test_transaction_provenance.py tests/test_population_rng.py tests/test_world_conformance.py` passed **86** tests.
2. Second focused run `uv run pytest -q tests/test_transaction_provenance.py -x` failed at `Domain event-to-sale integration is not implemented`. After minimal domain-owned adapter, focused tests passed **17**.
3. Adversarial trace reuse test `uv run pytest -q tests/test_transaction_provenance.py -x` failed at `DID NOT RAISE ValueError` for a reused trace sink. After validation, focused suite passed **24**; expanded source/negative/same-time cases later passed **28**.

No missing import or missing dependency was accepted as RED. This is not an independent formal proof.

## Independent oracle

`tests/fixtures/population-reference/transaction-provenance.json` fixes a 10-agent, 2-segment input, trial seed 11 and three chosen World Tick events, with SHA-256 transaction IDs calculated independently from the written structured-encoding specification using standard-library JSON and SHA-256 (not the production adapter). It builds on the independently hand-calculated earlier `financial-ledger.json`.

- At horizon day 1: 3 recognized sales at SAR 20 = SAR 60 revenue; 20 paid ads + 5 other paid cost; initial cash SAR 100; **cash 75, receivables 60, settled 0**.
- At horizon day 3: three SAR 10 settlements referencing those sales, at least two days after recognition; **cash 105, receivables 30, recognized revenue 60, paid ads 20, other costs 5, profit 35**.
- Population 10 eligible / 3 unique converted; conversion 0.3; CAC = 20/3 SAR (28-digit decimal evaluation); ROAS 60/20 = 3; strict cash threshold 0 => ruin false.
- The ledger contract rejects duplicate IDs, unknown sales, early or over-settlement, unknown trial/currency, and out-of-horizon entries.

## Replay, noninterference and adversarial evidence

Focused tests include false guard (event exists, transition did not fire, no sale); duplicate Tick on already converted agent (no second sale); complete agent-local emitted-event trace with final rejected guard; baseline-vs-traced World state, processed events, pending events and stochastic values equal; deterministic transaction goldens; reversed enrollment at 10/100/1,000 and added unrelated agent; idempotent exact retries versus conflicting same-ID payload; missing, foreign, unknown, forged event/owner/ordinal/trial/currency records; invalid money and fractional event time; absent/inconsistent trace; premature, excessive, missing, or out-of-horizon settlements; same-day financial order; incomplete horizon prefix. Every checked partition is exhaustive including initialized agents without a financial posting. Cross-agent shared economic feedback is **not** present; permutation invariance is not claimed for coupled dynamics.

Observed tests before documentation edits: application full `uv run pytest -q`: **454 passed, 58 subtests**, exit 0; `uv run python -m compileall -q src/funnelscript`: exit 0; `git diff --check`: exit 0; research `uv run pytest -q`: **52 passed, 147 subtests**, exit 0. Later expanded focused tests passed 28; final full verification should be recorded separately below.

## Bounded measurements, not scaling claims

Executed on macOS 27.0.1 arm64, Python 3.12.13, source fixture SHA-256 `c64f1caaf28330152c4bc06c44f6a98b8041a8009f5dff7a8f76bed403b3bf46`, world seed 11, RNG `population-rng-v1/sha256-mt19937`, provenance `world-event-sale-v1`. Traced measured timings use `time.perf_counter` and `tracemalloc`; the population timing **includes building the population runner and parsing the source**, not isolated kernel processing. Memory column is Python traced allocation **peak**, not RSS. One unreplicated measurement per size/trial, not a statistical sample. Financial phase includes sale extraction, journal validation and evaluation.

| Agents | Trial | Population setup+run (s) | Provenance+ledger (s) | Total (s) | Peak traced bytes | Sales | Cash SAR | Receivables SAR |
|---:|---|---:|---:|---:|---:|---:|---:|---:|
| 10 | trial-1 | 0.003550 | 0.001328 | 0.004878 | 31,075 | 3 | 105.00 | 30.00 |
| 10 | trial-2 | 0.002368 | 0.001124 | 0.003492 | 25,813 | 3 | 105.00 | 30.00 |
| 100 | trial-1 | 0.010920 | 0.006805 | 0.017725 | 171,267 | 30 | 1,050.00 | 300.00 |
| 100 | trial-2 | 0.009410 | 0.006872 | 0.016283 | 171,059 | 30 | 1,050.00 | 300.00 |
| 1,000 | trial-1 | 0.081519 | 0.064946 | 0.146465 | 1,733,963 | 300 | 10,500.00 | 3,000.00 |
| 1,000 | trial-2 | 0.083262 | 0.065871 | 0.149133 | 1,730,315 | 300 | 10,500.00 | 3,000.00 |

Each run had 2 declared segment labels, preserved 4:6 membership proportions, exact agent conservation, verified one-to-one source-sale identity and cash/receivable reconciliation; a second independent execution matched the entire population and sale trace. No general throughput, statistical independence, market calibration or predictive financial accuracy is inferred.

## Review/decision boundaries

A2M Code Review Graph rejected the requested repository path with `repo_root is outside the approved A2M workspace`; no graph-based independent review was performed. Read-only source inspection, adversarial executable tests and diffs are a bounded self-review, not independent human reviewer approval. Core limitations: traces are in-process, not cryptographically signed; only event-to-sale transition policies are causal, while money settlements/costs remain author-created; within-agent event history changes may shift processed occurrence ordinals; real-money inter-agent coupling, external causality and predictive validity remain unestablished. No new Accepted ADR, and Phase 008 empirical calibration remains gated.

## Final verification receipt

To be appended only after final commands and Git review.


### Final verification and review receipt (2026-11-01)

After the final adversarial additions (28 new Phase 007C tests), `cd funnelscript && uv run pytest -q && uv run python -m compileall -q src/funnelscript && git diff --check` exited 0: **458 passed, 58 subtests passed**, 6.79 seconds for pytest. `cd funnelscript-research && uv run pytest -q && git diff --check` exited 0: **52 passed, 147 subtests passed**, 9.73 seconds for pytest. Independent Code Review Graph could not be used because A2M rejected the repo path as outside its approved graph workspace; no independent reviewer is claimed. Local diff and source invariants were inspected; Python AST audit found no changed functions above 80 lines. Commits, if created, are separate local-only phase commits.
