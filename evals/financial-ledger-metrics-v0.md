# Phase 007B — Financial Ledger and Reference Metric Evaluation v0

Status: BOUNDED MARKETING-LIBRARY IMPLEMENTATION VERIFIED, 2026-11-01. This is not full economic simulation, accepted new architecture, calibrated forecasting, or an independent reviewer sign-off.

## Verified starting state and scientific boundary
- Application HEAD at preflight: `7d75d89e1e3cef5c6c5f59f84e591e678ef887ad`. Research HEAD: `4a28697e6076a5904bda51c1b3c4fe7ac2b40c45`. Both clean at preflight, previously on `work/phase-007a-population-identity-rng`; isolated local branches `work/phase-007b-financial-ledger-metrics`.
- Read both repositories' `AGENTS.md` (previous phase operating constitution) and applicable prior model/metrics research. Accepted DEC-009 prohibits embedding economic invariants as global compiler axioms. Accepted DEC-019/027/031 preserve World calendar, atomicity and shared RNG semantics. Existing legacy cash/ROAS/CAC/CVaR conventions differ and remain explicitly non-equivalent.
- Research spec: `spec/financial-ledger-metrics-v0.md`. Implementation: `funnelscript/stdlib/marketing/ledger.py` and `metrics.py`; new public marketing-domain symbols exported in `__init__.py`. Existing core EventMachine, WorldExecutor, legacy SimulationEngine, legacy TelemetryAggregator, parser, compiler and all dependencies unchanged.
- Separate domain-owned financial journal is a **model's explicit input**, not produced automatically by source-level events or a hidden market behavior simulator. All synthetic conversions and costs in the population integration fixture are *explicitly constructed*; they are not inferred market probabilities.

## Hypothesis matrix and independent references

| Hypothesis | Falsifier | Observed evidence | Boundary |
| --- | --- | --- | --- |
| H-LEDGER1 | Unpaid sale increases cash, double settlement, invalid cash-receivables conservation | Fixed P-LEDGER-1 exact hand arithmetic, horizon 1 versus 3 snapshots, missing reference/over-settlement/early-settlement/duplicate ID rejection, writeoff accounting, all passed | Only one trial currency and two-decimal declared basis, no external bank reconciliation |
| H-METRIC1 | Converted IDs duplicate/lost or CAC/ROAS use wrong denominator or cash-receipts numerator | 10-agent explicit 4/6 segments, 1+2 converted; conversion=3/10; CAC=20/3 SAR/customer (Decimal 28-digit result); ROAS=60/20=3; recognized profit=35 SAR | Conversion state must be explicitly designated, attribution declared rather than inferred; no per-segment cost attribution |
| H-RISK1 | Incorrect VaR ties or CVaR tail weighting; silently pooled inconsistent trials | [0,0,10,30] at .75 => VaR 10/CVaR 30; [0,0,0,100] => VaR 0/CVaR 100; [0,10,20,30] at .625 => VaR 20/CVaR=80/3; strict cash<threshold ruin | Empirical finite trials only; no independence, calibration or general prediction claim |
| H-INTEGRATION | Actual explicit population identities cannot be reconciled with receipts, or initial agent IDs missing | Two named trials at 10/100/1000; two segments 4:6 in each block; 3/10 deterministic conversion IDs; every converted agent has one named sale and delayed partial receipt; all ledger and identity equations match hand scale references | Controlled event fixture and authored transaction records, not automatically generated financial events |

Independent corpus P-LEDGER-1 (`tests/fixtures/population-reference/financial-ledger.json`) declares SAR, initial cash 100.00, ad payment 20.00 on day 0, other payment 5.00 on day 0, recognized sale 60.00 on day 1, receipt 30.00 on day 3 referencing that sale, minimum settlement delay 2, final horizon 3. At H=1, liquid cash=75, open receivables=60, settled=0; at H=3 cash=105, receivables=30, recognized revenue=60, receipts=30, paid ads=20, other paid costs=5, profit=35. This is a hand-computed fixed golden, not production-generated expected output.

Numeric implementation converts two-decimal Decimal inputs into Python integer minor units **without Decimal ambient context arithmetic**, so the money fold is exact over its declared magnitude/exponent boundary. Output amounts reconstruct Decimal from integer digits. Ratios and CVaR use explicitly local decimal precision=28; repeating 20/3 and 80/3 are finite decimal approximations, not exact mathematical rational representations. Only two-decimal currencies are supported; users must verify the three-uppercase-letter currency code externally (the API checks syntax, not an ISO registry). No implicit rounding, no production floats, no automatic credit-spend policy, and no automatic receipts.

## RED/GREEN execution receipts

1. **Ledger API RED:** `uv run pytest tests/test_financial_ledger.py::test_delayed_settlement_does_not_increase_cash_at_sale_recognition -q` failed on a correct `AssertionError: Missing opt-in marketing ledger API`, exit 1. Module import succeeded; this was a behavioral missing-contract case, not a collection/import error.
2. **Ledger API GREEN:** identical command yielded `1 passed`, exit 0, after adding minimal `MarketingLedger`/`LedgerEntry` and checkpoint processing.
3. **Metric API RED:** `uv run pytest tests/test_financial_metrics.py::test_conversion_cac_roas_and_cash_reference_are_distinct_metrics -q` failed `AssertionError: Missing trial reference metric evaluator`, exit 1; then after adding the production trial and risk evaluators, `5 passed` across the two focused modules, exit 0 (the full module run included the originally failing test).
4. **Adversarial numeric RED:** `uv run pytest tests/test_financial_ledger.py::test_decimal_context_precision_cannot_silently_round_posted_minor_units -q` failed because `Decimal('1234567.89')` was incorrectly reported as `1234600.00` with ambient context precision 5. The original implementation used `amount.scaleb(2)`. This was a real production monetary precision defect, unlike a fixture/import issue. Fixed by exact digit/exponent-to-integer conversion and a bounded exponent range.
5. **Numeric GREEN:** identical command yielded `1 passed`, exit 0. Final full new coverage after negative tests and integration: `56 passed`, exit 0. Added edge tests mostly after the first behavioral RED; these are *not* each claimed as independent observed RED/GREEN cycles.

## Full test and packaging verification receipts

| Command | Actual outcome | Exit |
| --- | --- | ---: |
| `uv run pytest tests/test_financial_ledger.py tests/test_financial_metrics.py tests/test_population_financial_reference.py -q` | 56 passed, 0.25s | 0 |
| `uv run pytest -q` | 430 passed, 58 subtests passed, 6.82s | 0 |
| `uv run pytest tests/test_population_reference.py tests/test_population_identity.py tests/test_population_rng.py tests/test_world_conformance.py tests/test_world_stochastic.py tests/test_event_machine.py -q` | 129 passed, 0.85s | 0 |
| `python3 -m unittest discover -s tests -v` (research checkout) | 5 passed | 0 |
| `uv build --wheel --out-dir /tmp/funnelscript-phase007b-dist` | Wheel created; package archive has marketing `ledger.py`, `metrics.py`, `__init__.py`, existing `lead_response.fnl` | 0 |
| AST source inspection for all new Python functions | No new function over 80 lines | 0 |

Frontend sources/API not touched; Bun testing/build not run. Git-ignored build intermediates were not staged.

## Bounded measured integrated synthetic experiments

Measurement: Python 3.12.13, FunnelScript 0.2.0a1, macOS 27.0.1 arm64; `time.perf_counter` covers PopulationExecutor creation, deterministic World event runs, explicit per-conversion journal assembly, ledger fold, and trial-metric derivation; `tracemalloc` peak traces Python allocations **not RSS**. Historical application base revision `7d75d89e1e3cef5c6c5f59f84e591e678ef887ad`; actual implementation was dirty Phase 007B code before committing. Raw measurements retained only locally at ignored `plans/007b-benchmark-results.jsonl`.

Synthetic fixed assumptions: 10-agent block has four north and six south agents and exactly one north/two south named agents receive a model `Visitor.Tick` conversion event (preselected deterministic IDs; no random market conversion probability). Each converted agent gets a hand-authored 20.00 SAR sale on day 1 and 10.00 SAR receipt on day 3 with 2-day minimum settlement. Initial cash is 10.00 SAR per eligible agent; paid ads 2.00 and other cost 0.50 SAR per eligible agent at day 0. Horizon H=3, explicit cash ruin threshold=0 SAR, two separate trial identities, seed=1. Larger scenarios repeat the same deterministic synthetic 10-agent block, not a fitted population response model.

| Population | Trial | Converted | Cash SAR | Receivables SAR | Profit SAR | Wall seconds | Peak traced bytes |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 10 | trial-1 | 3 | 105 | 30 | 35 | 0.005281 | 42,304 |
| 10 | trial-2 | 3 | 105 | 30 | 35 | 0.003402 | 38,218 |
| 100 | trial-1 | 30 | 1,050 | 300 | 350 | 0.011812 | 176,203 |
| 100 | trial-2 | 30 | 1,050 | 300 | 350 | 0.011694 | 174,211 |
| 1,000 | trial-1 | 300 | 10,500 | 3,000 | 3,500 | 0.094715 | 1,482,741 |
| 1,000 | trial-2 | 300 | 10,500 | 3,000 | 3,500 | 0.095776 | 1,482,701 |

All six observed outputs matched the exact closed-form cash, receivable, recognized revenue, settled receipts, paid ads, other costs, profit, two-segment agent counts and unique terminal identity sets. There are no measured scalability claims beyond these scenarios or statistical precision intervals.

## Compatibility and adversarial assessment

- No modification to `EventMachine.run`, `WorldExecutor.run`, default World `random.Random(seed)` behavior, legacy `SimulationEngine` or `TelemetryAggregator`. Historical `P-RNG-ORDER-1` and Phase 006 World conformance tests remain present and green.
- Trial/currency/ID and source transaction references rejected on mismatch. Settlement cannot overdraw or precede the caller's minimum delay. Recognized sales never increase liquid cash; writeoffs reduce open credit and recognized-profit proxy without increasing cash. A caller can explicitly authorize negative cash by supplying a ledger that produces it; risk detection is reported with a separate threshold, no global halt.
- Tied-timestamp journal ordering is the caller's ordered input sequence, with no separate scheduler and no time sort that masks invalid ordering. Unknown future events outside the requested prefix are not applied to the prefix; event metadata and duplicate IDs are still checked across the journal. Effects external to the journal and unobserved/censored transaction data are not verified.
- Metric declaration `attribution_label` is descriptive scope: this module cannot establish that the recorded revenue truly originated from the declared campaign. No per-segment monetary allocation, random market intervention or causal counterfactual accuracy is claimed. Risk is a discrete empirical trial distribution with no proven independence; using paired keyed streams is not independent Monte Carlo evidence.
- Static source audit and full suites completed. No separately authorized independent human/external reviewer signed off; self-audit is not reviewer independence. Separately accepted ADR would be needed for automatic World-to-ledger transaction emission, shared financial accounts across interacting agents, refunds/credit policies, or replacement of legacy telemetry.

## Remaining gates

Phase 007B satisfies the requested *bounded synthetic reference* accounting and metric contracts, subject to the explicitly recorded independent-review limitation. Phase 007 as a broader validated reference population/economic model is **not declared DONE**: real-source-to-transaction causal provenance, complete expense recognition and attribution semantics beyond the toy journal, domain-authorized credit, explicit shared-shock and multi-agent interactions, and independent scientific/model review are not proven. Phase 008 empirical calibration is still not authorized. Proposed next continuation is a separately bounded Phase 007C causal provenance and financial scenario integration decision/review, not an automatic new DSL behavior.

**External market validity, statistical calibration, causal inference, and real-world prediction accuracy were not tested.**


### Independent review attempt and availability limitation

An available local external review CLI was invoked against uncommitted application changes in read-only mode: `codex review --uncommitted -c 'sandbox_mode="read-only"'`. The reviewer process exited **1** before inspecting the implementation because its configured model endpoint returned repeated `401 Unauthorized` authentication failures (including the HTTPS fallback). The tool's own final status was `Review was interrupted`. This is NOT a completed independent adversarial review, NOT evidence that the code passed review, and not a code defect. The exact tool output is held locally under ignored `plans/007b-independent-review-app.txt`. Only the bounded self-audit and executable tests are supported by current evidence. An authenticated separate reviewer is still required for independent sign-off.


## Verified local application commit receipt

After final test rerun, the application working tree was staged with exactly ten Phase 007B files and no unexpected unstaged or untracked files. The local application commit is `ef3f434d96eb17d06503aa4ba3c85c31be570434` (`feat(marketing): add exact ledger and reference risk metrics`) on `work/phase-007b-financial-ledger-metrics`. The code was measured as uncommitted Phase 007B prior to this commit, not retroactively asserted to have been benchmarked from a clean pre-existing revision. Final freshly executed test commands: 56 new passed (exit 0), complete app 430 passed plus 58 subtests (exit 0), 129 selected World/Population compatibility passed (exit 0), research 5 passed (exit 0). The independent Codex reviewer attempt remained blocked at HTTP 401 and did not sign off. No remote Git operations were performed.
