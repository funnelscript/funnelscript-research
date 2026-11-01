# Phase 007E — Durable Financial Audit and Recovery Contract (proposed)

Status: research-gated experimental opt-in domain contract, not an Accepted ADR. Anchors: discrete-event execution trace replay (Banks et al., *Discrete-Event System Simulation*), Fowler's idempotent message/transaction identity patterns (*Patterns of Enterprise Application Architecture*), NIST FIPS 180-4 SHA-256 integrity, POSIX rename and fsync semantics, and existing Phase 007B–D exact ledger conservation.

## Falsifiable contracts

- H-DPROV1: a validated trial and its complete sale/action witness produce identical domain-separated, schema-versioned canonical UTF-8 bytes regardless of input action order, hash randomization or process. Falsifier: same validated financial trial exports different bytes.
- H-DPROV2: after a strict restoration using the original World trace and declared policy, replaying any previously committed action changes neither transaction count nor any accounting balance; conflicting tx/authorization reuse fails closed. Falsifier: a replay increases settled cash.
- H-DPROV3: records must bind all source identifiers and financial details to a validated SHA-256 manifest, and optionally an independently held expected full-envelope digest. Falsifier: altered bytes are accepted without detection under the stated trusted digest assumption. SHA-256 alone is integrity, not a producer signature.
- H-DPROV4: checkpoint publication via temporary file plus file sync, atomic same-filesystem rename and directory sync leaves either the old committed checkpoint or the new one on ordinary pre-rename failure. Falsifier: interrupted uncommitted write becomes a valid posting. No claim against compromised filesystem, malicious concurrent writer, or power-loss semantics without platform tests.
- H-DPROV5: restored exact existing MarketingLedger yields cash = initial + receipts - ads - other paid cost; receivables = recognized - settled - writeoffs; profit = recognized - ads - costs - writeoffs. Falsifier: any recovery discrepancy against hand-calculated 10-agent oracle.
- H-DPROV6: canonical audit bytes and IDs must agree across independent Python processes with differing PYTHONHASHSEED. Falsifier: mismatch.
- H-DPROV7: single writer and independently replayed trial only; concurrent writers, shared budgets and global serializability are unsupported. Falsifier of any future claimed multiwriter safety: adversarial lost update.

## Architecture alternatives and decision boundary

A. Canonical export and strict trace-bound import: needed for portable exact replay, but alone cannot publish committed state.
B. Add smallest single-file atomic checkpoint writer/reader, without a database or transaction engine: selected for the bounded single-writer file checkpoint. Persistent replay must explicitly carry forward the complete previously validated journal, not trust a process-local set.
C. Message broker/transaction coordinator/distributed lock/event store: rejected absent failing concurrency requirements and operator authorization.

## Trust and crash boundaries

The caller owns the execution trace, policy and financial authorizations and must retain them for verified replay. A saved payload is not an independent proof that these authorities were legitimate. External manifest anchors are optional and must be stored outside the same writable trust domain. Without such an anchor, an attacker able to rewrite both content and checksum can forge otherwise schema-valid external financial actions. No source authentication, revocation check or real-world causal identification is asserted. Single-writer, same-filesystem atomic rename and no untrusted path are preconditions. Crash before rename retains previous committed image; after rename may yield the new committed image. The caller must explicitly handle ambiguous outcomes by rereading and replaying, never assuming exactly-once physical delivery. Recovered data is revalidated against source World events and the exact existing ledger.

## Independent oracle

10 agents (4/6), three World conversion sales of SAR 20, initial cash SAR 100, ads SAR 20, other paid costs SAR 5, three day-3 SAR 10 payments: day 1 cash 75 / receivables 60 / recognized 60 / receipts 0; day 3 cash 105 / receivables 30 / recognized 60 / receipts 30 / profit 35. Day-3 SAR 5 writeoff yields cash 105 / receivables 25 / recognized 60 / receipts 30 / profit 30. Calculated independently before implementation.

## Executed proof boundaries and results (2026-11-01)

Implemented in the domain-only `funnelscript.stdlib.marketing.audit` adapter with `export_audit`, `restore_audit`, `replay_audit`, `write_audit_checkpoint`, `read_audit_checkpoint`. Format `funnelscript-financial-audit-v1` has canonical sorted-key JSON, integer minor units, full trial metadata, event-to-sale provenance and source references, separately author-asserted external actor/authorization, ordered financial journal, SHA-256 digest with explicit domain-separation prefix `funnelscript:financial-audit:v1\0`, plus an optional independently pinned SHA-256 digest of the complete envelope. `restore_audit` requires an independently reproduced original World execution and sale policy and reproduces posting through the existing ledger. No key management or signed producer identity is implemented.

An integrity-only manifest can be rewritten along with its payload; the independent pinned envelope hash detects such a rewrite only while the external anchor is trusted. The protocol does not authenticate external authorizations or prove external financial source transactions. Reader + restore must always run before a checkpoint is treated as a financial fact. Atomic file replacement does not provide global serializability; no automatic append, background queue or shared writer arbitration exists. The authoritative single-writer application must save the *new* complete audited result before acknowledging a financial operation. Receipt ambiguity after rename is resolved by rereading, not blind retry.

**RED**: `uv run pytest -q tests/test_durable_financial_audit.py::test_phase007e_public_contract_is_available` failed (1 failed, exit 1), missing required public audit contract; not import/setup failure. **GREEN**: focused Phase 007E suite 26 passed (exit 0), after correcting test setup to provide an actual `Sequence` instead of a `reversed` iterator. This correction preserved the behavioral assertion and did not change production semantics. The Phase 007D oracle and cross-process separately seeded experiment are independently checked in `evals/durable-financial-provenance-measurements.json` and `tests/test_durable_financial_reference.py`.

Multiwriter financial operations, shared resource arbitration, producer authentication and operational authorization remain **ARCHITECTURAL STOP — APPROVAL REQUIRED**, not phase-completion claims. Deletion, swapping or substitution of persisted financial records fails under the pinned complete-envelope digest; without the pin, a fully rewritten consistent journal can pass integrity and actor-assertion validation. Python/OS measurement values are environment-specific, not scaling forecasts.

## GitHub verification remediation

GitHub PR #3 initially had **no CI checks** because this repository had no workflow. Phase 007E adds the minimal independent `Research Conformance CI` workflow, pinned to the existing application repository's verified checkout/setup-uv actions and uv version. It runs the research pytest suite with an explicitly declared Python 3.12 interpreter and ephemeral pytest dependency. It does not install a database, runtime package, signing infrastructure, or application engine. No claim of CI success until GitHub reports the new check terminal-success.
