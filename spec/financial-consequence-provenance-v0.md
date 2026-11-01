# Phase 007D — Financial Consequence Provenance v0

Status: PROPOSED opt-in domain integration; not an Accepted ADR. Research baseline: verified Phase 007C on both GitHub default branches.

## Anchors and architectural decision boundary

Financial double-entry/conservation reasoning (the existing exact `MarketingLedger`), discrete-event simulation execution trace semantics (Banks et al., *Discrete-Event System Simulation*), idempotent message processing and stable transaction keys (Fowler, *Patterns of Enterprise Application Architecture*), and DEC-009 (economic rules belong to domain adapters, not the compiler) motivate this contract. Proof of in-model event provenance is not proof of external authorization, cryptographic authenticity, or real-world causal inference.

**Select A plus narrowly scoped B:** preserve `WorldExecutor`, `PopulationExecutor`, declared sale policy and `MarketingLedger`; introduce an opt-in, domain-owned external-operation envelope and validate it at the adapter boundary. Keep the Phase 007C direct `external_entries` API as an explicitly *legacy, unprovenanced* path; do not silently call those records authenticated. Reject C (generic execution calendar, event-sourcing platform or second financial engine): no failing test establishes need. External authorization is author-asserted, not independently authenticated. No accepted architecture decision is created.

## Falsifiable hypotheses and invariants (proposed before production edits)

- **H-FPROV1 — origin ownership:** an executed-event sale must match a complete World trace and policy; each opt-in non-sale posting carries canonical external actor, unique authorization identity and a `LedgerEntry` whose kind is `ad_spend`, `other_cost`, `settlement` or `writeoff`. External postings must not claim a World witness. Falsifier: omitted authorization or forged sale witness successfully posts.
- **H-FPROV2 — referential integrity:** settlement/writeoff source IDs resolve to an actual sale in the same trial, currency and remaining-balance scope, and settlement respects declared delay. The existing ledger is sole evaluator. Falsifier: unknown/foreign/exhausted receivable accepted.
- **H-FPROV3 — exactly-once within a supplied batch:** repeated identical external operation envelopes collapse to one journal entry; the same transaction ID with a different envelope, or the same authorization reused for a distinct posting, rejects. A transaction ID collision with a sale rejects. This is in-memory, per-evaluation idempotency, not durable delivery guarantees. Falsifier: exact replay changes a snapshot.
- **H-FPROV4 — time:** event recognition occurs on its integral event day; costs precede sales at the same day, settlement follows recognition, writeoff follows recognition; horizon prefixes exclude later cash. Cash = initial + receipts - paid advertising - paid other costs. Receivables = recognized sales - receipts - writeoffs. Profit = recognized sales - paid advertising - paid other costs - writeoffs. No implied settlements. Falsifier: uncollected sale increases cash or a future receipt leaks into earlier prefix.
- **H-FPROV5 — determinism:** equal source, agent identities, policy, seed, envelope values and order-independent independent cohorts produce byte-equivalent ordered journal semantics; external identifiers are caller-declared, validated canonical ASCII, not hash/time/randomness. Falsifier: an identical replay yields different ordered operations.
- **H-FPROV6 — declared coupling boundary:** independent-agent enrollment invariance holds only when financial actions and policies are independent of other agents. Shared mutable budgets and auctions can depend on scheduling/order and require separate kernel-level review, not a fictitious independence claim. Falsifier: changing unrelated enrollment changes a claimed independent agent's financial results with no declared coupling.

An external authorization envelope records an asserted financial actor and authorization ID. It is deliberately **not a cryptographic signature**, an immutable external audit log, proof that a person had permission, or a promise of exactly-once processing across databases/process restarts. A World-generated sale must never be relabeled as an external action. The ledger remains the sole accounting fold, including fixed two-minor-unit arithmetic.

## Reference oracle to preserve

10 agents / two segments 4:6, three executed conversions at day 1, SAR 20 per sale; initial cash SAR 100; day 0 paid ads SAR 20 and other cost SAR 5; day 3 three separately authorized SAR 10 partial settlements with matching sale references. Day 1: cash 75, receivables 60, revenue 60, settled 0. Day 3: cash 105, receivables 30, revenue 60, settled 30, profit 35. A separate partial-writeoff variant with SAR 5 writeoff from one remaining SAR 10 balance: day 3 cash 105, receivables 25, recognized 60, receipts 30, writeoffs 5, profit 30. Both variants are exact hand calculations, not outputs derived from production code.

## Causal coupling counterexample

Two actors A and B each request the only remaining SAR 10 of a shared advertising budget. If consumption follows arrival order, processing A then B authorizes A, but processing B then A authorizes B. Both runs can be individually deterministic. This is **not independent-agent enrollment invariance**, and the accepted local World executor has no cross-agent shared resource calendar or transaction arbitration contract. STOP at that decision boundary; do not install a second scheduler or assert independence.

## Unchanged constraints

No compiler/World scheduling changes; no automatic source-event fabrication, receipts or writeoffs; no new dependency; no expansion into shared financial state. Phase 008 calibration requires an independent decision gate. All IDs and asserted authorizations are valid only within the supplied trial and declared policy scope. This research specification is a falsifiable design, not a success or CI claim.
