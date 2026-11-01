# Phase 007D — Financial Consequence Provenance Evaluation v0

Date: 2026-11-01. **Status: local implementation verification**. The global DONE status additionally requires remote CI, PR merge and verified remote HEAD in both repositories.

## Research choice and boundary

See `spec/financial-consequence-provenance-v0.md`. Selected opt-in domain adapter A + narrow external authorization envelope B. General financial event engine C rejected. `DeclaredFinancialAction(entry, actor_id, authorization_id)` is explicit *author-asserted* financial ownership. `post_authorized_trial()` canonicalizes entries by simulated day, kind priority and transaction ID, collapses identical retries, rejects conflicts and reused authorization identities for distinct postings, verifies all event sales with the existing complete World trace and passes postings through the sole `MarketingLedger`. Previous unprovenanced Phase 007C API remains compatible and is not rebranded authenticated. No compiler, World scheduling, RNG or external payments implementation added.

## Research hypothesis-to-test mapping

- H-FPROV1: event sale witness validation and non-sale explicit actor/authorization; forged source event and absent/incomplete traces rejected. Authorization is **not cryptographically authenticated**.
- H-FPROV2: reference, trial, currency, delay, outstanding balance and premature writeoff cases rejected by existing domain ledger.
- H-FPROV3: exact repeated settlement/writeoff/spend delivery has one effect; conflicting amount, identity, actor or authorization raises; ID collision with sale rejected. Idempotency is batch-scoped, not durable cross-process.
- H-FPROV4: day 1 cash 75, receivables 60, revenue 60, settled 0. Day 3 original historical no-writeoff cash 105, receivables 30, revenue 60, settled 30, profit 35. Separate partial-writeoff day 3 cash 105, receivables 25, revenue 60, settled 30, writeoff 5, profit 30. All SAR with minor-unit precision and preserved historical oracle.
- H-FPROV5: deterministic replay hashes of independently rerun actual World-to-ledger traces match for both trial seeds and each population size; enrollment reordering and fixed identity goldens remain verified. No Python hash or wall-time identity.
- H-FPROV6: only independent local World agents covered. Two agents competing for a shared SAR 10 budget exhibit order-sensitive ownership even when each order is reproducible; the current kernel has no declared shared-budget serialization semantics. **Bounded STOP** for shared financial coupling; no scheduler introduced. Not a real-world causality proof.

## Genuine RED → GREEN record

1. Initial test-first command `uv run pytest -q tests/test_financial_consequence_provenance.py -x`: **exit 1**, behavioral assertion `Financial action provenance and exactly-once adapter is missing`; no missing import or dependency.
2. Minimum domain contract implemented. First focused run had **7 passed then 1 failed** due to the authorization-reuse test itself also injecting a conflicting duplicate transaction ID. The test input was corrected to *replace*, rather than append, the original action; no passing assertion was weakened.
3. Focused suite `uv run pytest -q tests/test_financial_consequence_provenance.py -x`: **19 passed**, exit 0. Expanded adversarial checks + Phase 007C regression `uv run pytest -q tests/test_financial_consequence_provenance.py tests/test_transaction_provenance.py`: **61 passed**, exit 0.
4. Complete app `uv run pytest -q`: **491 passed, 58 subtests**, exit 0 (6.85 s); `uv run pytest -v`: **491 passed, 58 subtests**, exit 0 (7.09 s); compileall and `git diff --check` both exit 0. Research before documentation additions: `uv run pytest -q`: **52 passed, 147 subtests**, exit 0 (9.14 s); verbose **52 passed, 147 subtests**, exit 0 (9.40 s), and diff-check exit 0. Repeat verification after final documentation and code review before commit.

## Independent arithmetic oracle

10 agents, 2 segments (4/6), three distinct true World state changes, 3 x SAR 20 sales, initial cash SAR 100, day 0 SAR 20 paid ads and SAR 5 cost; day 3 3 x SAR 10 partial settlements referencing each origin sale, and independently a day-3 SAR 5 partial writeoff against one remaining SAR 10 balance. Conversion 3/10; CAC = 20/3 SAR, ROAS = 3, ruin predicate cash <= 0 false. For 100/1,000, explicit scenario arithmetic scales all but the single SAR 5 partial writeoff. Tests assert the hard-coded independently computed values, not values computed by the functions under test.

## Bounded integrated measurements

Environment: macOS-27.0.1-arm64-arm-64bit, Python 3.12.13, source fixture SHA-256 `c64f1caaf28330152c4bc06c44f6a98b8041a8009f5dff7a8f76bed403b3bf46`, seeds 11 and 29, RNG `population-rng-v1/sha256-mt19937`, provenance `world-event-sale-v1`. Each row includes only first-run measurements; a second exact-seed execution independently compared SHA-256 of executed event-to-sale origins and normalized authorized ledger postings. These are `tracemalloc` Python allocation peaks, **not resident memory**. Population timing includes runner construction and parsing. Each run used actual World events and explicit external financial operations with one SAR 5 writeoff, and verified partition count, 4:6 segments, source sale counts, journal operation uniqueness, receivable references and exact cash/profit equations.

| Agents | Seed | World setup + population (s) | Finance provenance + ledger (s) | Total (s) | Peak tracemalloc bytes | World sales | External actions | Journal operations | Cash SAR | Receivables SAR | Profit SAR | Replay |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|:---:|
| 10 | 11 | 0.003061 | 0.001454 | 0.004515 | 41,308 | 3 | 6 | 9 | 105.00 | 25.00 | 30.00 | pass |
| 10 | 29 | 0.002269 | 0.001216 | 0.003485 | 29,118 | 3 | 6 | 9 | 105.00 | 25.00 | 30.00 | pass |
| 100 | 11 | 0.009490 | 0.007689 | 0.017179 | 205,307 | 30 | 33 | 63 | 1050.00 | 295.00 | 345.00 | pass |
| 100 | 29 | 0.009303 | 0.007845 | 0.017147 | 196,387 | 30 | 33 | 63 | 1050.00 | 295.00 | 345.00 | pass |
| 1,000 | 11 | 0.082505 | 0.071718 | 0.154223 | 1,982,917 | 300 | 303 | 603 | 10500.00 | 2995.00 | 3495.00 | pass |
| 1,000 | 29 | 0.082267 | 0.065095 | 0.147362 | 1,900,525 | 300 | 303 | 603 | 10500.00 | 2995.00 | 3495.00 | pass |

The results do not establish scaling law, predictive calibration, statistical independence, cryptographic authenticity, distributed exactly-once execution, market effectiveness or treatment causality. They are two seeded observations per configuration.

## Review and scientific limitations

A2M Code Review Graph was attempted and returned `repo_root is outside the approved A2M workspace`; do **not** claim independent graph review or human approval. Review of production/test diffs, replay/adversarial executable checks and GitHub CI are distinct and do not certify causal realism. Local event occurrence IDs may change if an agent's own earlier event sequence changes. Accepted ADR status remains unchanged; Phase 007 overall remains separately gated. See `spec/financial-consequence-provenance-v0.md`.
