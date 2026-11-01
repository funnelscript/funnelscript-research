# Phase 007F — Crash-Consistent Single-Writer Financial Commit Contract (Proposed)

Status: research hypothesis and implementation evaluation; not an accepted ADR.

## Research anchors and falsifiable hypotheses

Grounding: write-ahead/logical transaction recovery distinctions (Gray and Reuter, *Transaction Processing*, 1992); POSIX rename atomic namespace replacement and fsync boundaries; deterministic replay and content-addressed evidence. This contract does not claim stable-media correctness on every filesystem, producer identity authentication, Byzantine recovery, or concurrent-writer serializability.

- H-FCOMMIT1: a candidate must round-trip through Phase 007E World/policy/audit/ledger validation before publication. Falsifier: a rejected candidate changes the checkpoint.
- H-FCOMMIT2: receipt identity must be a deterministic digest of the audit, trial, operation identities and ledger snapshot. Falsifier: receipt verifies for different evidence.
- H-FCOMMIT3: a success receipt must follow successful publication plus re-read/validation. A failure after rename and before directory fsync is uncertain. Falsifier: an injected post-rename failure returns SUCCESS.
- H-FCOMMIT4: identical redelivery cannot change state, whereas conflicting identifiers fail. Falsifier: duplicated replay changes cash or receivables.
- H-FCOMMIT5: on restart the persisted checkpoint, not the attempted write, determines observed state. Falsifier: a nonexistent posting is recovered.
- H-FCOMMIT6: cash = initial + settlements - ad spend - other costs; receivables = sales - settlements - writeoffs; profit = sales - ad spend - other costs - writeoffs, exactly in minor units. Falsifier: restored snapshot differs from the independent reference oracle.
- H-FCOMMIT7: byte-identical inputs yield identical receipts across Python processes and hash seeds. Falsifier: a cross-process mismatch.
- H-FCOMMIT8: single trusted writer, trusted input World, externally asserted authorizations and a trusted external receipt anchor are preconditions; local digests alone cannot prove source identity, prevent valid older checkpoint substitution or arbitrate concurrent writes. Falsifier: documentation or tests claim more than this.

## Architectural alternatives

A: caller-managed lifecycle — smallest change, but cannot standardize ambiguous acknowledgements.
B: opt-in domain financial commit coordinator using the existing canonical audit, exact ledger and atomic writer. Selected for direct testability and limited production surface.
C: generic distributed transactional infrastructure — rejected: no requirement for consensus, broker, multi-writer or a second ledger.

## State machine and intended contracts

ABSENT → VALIDATED → PUBLICATION_IN_PROGRESS → (COMMITTED_VERIFIED | PUBLICATION_UNCERTAIN | NOT_PUBLISHED).
COMMITTED_VERIFIED → RECOVERED_VERIFIED → (UNCHANGED_IDEMPOTENT | VALIDATED_NEXT).
Recovered validation uses original World and policy. Caller-supplied previous receipt is an optional trusted compare-before-publish anchor for subsequent state updates; a missing anchor on an existing different checkpoint must fail closed. Same-state receipt after restart is idempotent. Retained older valid content is not detectable without externally retained trusted receipt.

An OSError during a write is not proof of rollback. On an interrupted publication, inspection of persisted evidence is mandatory; if a failed directory fsync leaves a candidate image, return no success receipt, signal uncertainty, and require a later recovery/revalidation. No interface may claim crash durability beyond filesystem and OS guarantees.

## Receipt scope

Deterministic, versioned receipt fields: trial, audit schema, SHA-256 digest of complete canonical checkpoint bytes, exact financial transaction identifiers, exact minor-unit financial-state fingerprint, and derived domain-separated commit identity. No process clock, random salt, untrusted authorization proof or secret key. A valid receipt proves equality with the revalidated local financial evidence under declared trusted inputs, not authenticated authority.

## Independent reference oracle

SAR 100 initial cash; SAR 20 ad spend; SAR 5 other cost; SAR 60 recognized sales; three SAR 10 delayed settlements. Day 1 cash 75, receivables 60, revenue 60, receipts 0. Day 3 cash 105, receivables 30, revenue 60, receipts 30, profit 35. With a SAR 5 writeoff: cash 105, receivables 25, profit 30. This oracle is expressed independently of the production ledger implementation.

## Failure boundaries

- Before namespace replacement: old valid image or no image should survive, absent a malicious or concurrently writing actor.
- After namespace replacement but before successful parent fsync: crash persistence is uncertain; surviving content must be inspected, not guessed.
- After success and lost acknowledgement: recovering and comparing receipt allows identical retry without additional posting.
- Wrong trial/currency/World/policy or corrupt/truncated image: fail closed.
- Older valid image and competing writers: require an external trusted anchor and separately enforced single-writer ownership respectively; never describe either protection as intrinsic authentication/serializability.

No accepted architecture decision or multi-writer infrastructure is authorized by this research proposal.
