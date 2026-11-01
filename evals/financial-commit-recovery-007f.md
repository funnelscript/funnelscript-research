# Phase 007F — Verified Local Experiments and Failure Model

Research hypothesis contract: [financial-commit-recovery-007f.md](../spec/financial-commit-recovery-007f.md). Machine-readable evidence: [financial-commit-recovery-007f-measurements.json](financial-commit-recovery-007f-measurements.json). Runner: application `scripts/phase007f_commit_experiment.py`. Independent measurements validator: `tests/test_financial_commit_recovery_reference.py`.

## Experimental observations (local; not field durability proof)

Python 3.12.13, macOS 27.0.1 arm64. Each of six configurations executes World transitions with 2 segments, reconciles Phase 007D actions against an independently specified integer-minor-unit oracle, creates an initial checkpoint, injects a pre-rename failure while attempting a second financial state, recovers the unchanged initial state, commits the second state, verifies its SHA-256-bound deterministic receipt, then restores and replays all actions in a new Python process. All six experiments completed with receipt equality and replay accounting agreement. A separately covered deterministic directory fsync failure yields `CommitOutcomeUncertain` rather than success. These tests simulate failures at Python syscall boundaries; they do not simulate actual power loss or corrupted hardware.

| Agents | Seeds | Sales each | Final cash (SAR) | Commit publication (seconds, observed) | Child recovery (seconds, observed) |
| --- | --- | --- | --- | --- | --- |
| 10 | 11, 29 | 3 | 105.00 | 0.013834, 0.013396 | 0.002075, 0.002123 |
| 100 | 11, 29 | 30 | 1,050.00 | 0.084247, 0.080507 | 0.008696, 0.008669 |
| 1,000 | 11, 29 | 300 | 10,500.00 | 0.875634, 0.883010 | 0.064970, 0.066213 |

Source and commit implementation SHA-256 fingerprints, OS and interpreter versions, raw timings, parent traced peak memory, evidence hashes, transaction counts and commit identities are present in the machine-readable file. The parent process memory excludes child allocations. Single-run wall time is not a scaling estimator or performance guarantee.

## Fault injection and evidence coverage

| Fault / claim | Test evidence | Expected response |
| --- | --- | --- |
| Commit and deterministic receipt | `test_commit_receipt_public_contract` | Canonical receipt matches recovered audit and exact ledger |
| Second commit and retry | `test_second_commit_idempotent_settlement_writeoff_and_independent_oracle` | No double posting |
| Changed checkpoint without trusted previous anchor | `test_changed_state_without_trusted_previous_anchor_fails_closed` | Reject |
| Valid but older checkpoint substitution | `test_outdated_anchor_and_valid_old_checkpoint_substitution_are_detected` | Detect only with externally retained trusted receipt |
| Changed amount/kind/actor/authorization/trial/currency | `test_conflicting_candidate_never_replaces_checkpoint` | Reject |
| Authorization reuse; truncating committed transaction history | `test_reused_authorization_and_removed_old_action_fail_before_publish` | Reject |
| Corrupt checkpoint, forged receipt, wrong policy/World | `test_receipt_mutations_wrong_trial_world_policy_and_damage_fail_closed` | Reject |
| Temporary creation/file sync/rename/parent directory sync failure | `test_publication_failure_never_returns_success_ack` | Uncertain, never acknowledge success |
| Lost acknowledgement and subsequent retry | `test_ambiguous_post_rename_commit_resolved_by_restart_recovery` | Inspect persisted evidence; retry same candidate without reposting |
| Python hash seed variation and restart | `test_cross_process_receipt_determinism_and_recovery` and six process experiments | Same committed identity |
| Missing source event; forged event; over-settlement/writeoff; delay; horizon | Existing `test_durable_financial_audit.py`, `test_financial_consequence_provenance.py` | Reject invalid reference |
| Agent enrollment reordering and unrelated-agent insertion | Existing Phase 007A/007C population conformance tests | Keyed per-agent invariance within declared independence |
| Shared-budget coupling; multi-writer race | Counterexamples remain architectural STOP | No claimed serializability |
| Actual sudden power loss / untrusted storage | Not tested | No claim of physical persistence or authentication |

## Genuine TDD receipts and review findings

- RED 1: `uv run pytest -q tests/test_financial_commit_recovery.py::test_commit_receipt_public_contract` returned exit 1: `AttributeError: module 'funnelscript.stdlib.marketing' has no attribute 'commit_financial_checkpoint'` (missing public behavior).
- GREEN 1: rerunning the identical command after the minimal initial coordinator implementation returned exit 0, `1 passed`.
- RED 2 (adversarial security review): `uv run pytest -q tests/test_financial_commit_recovery.py::test_idempotent_retry_must_not_ack_when_durability_sync_fails` returned exit 1, `Failed: DID NOT RAISE CommitOutcomeUncertain`. An existing image was incorrectly acknowledged on retry without re-synchronizing.
- GREEN 2: after adding a file-and-parent-directory `fsync` gate plus post-sync revalidation, the Phase 007F suite returned exit 0, `19 passed`. A transitory code mistake (calling the policy object as a function) produced two additional failing tests and was corrected; the tests were not weakened.
- Full final local application `uv run pytest -q` and `uv run pytest -v`: `541 passed, 58 subtests`. `uv build`, `compileall`, Bun `test` and `build`, installed-wheel smoke and `git diff --check` succeeded.
- Research `uv run --no-project --with pytest pytest -q/-v`: `55 passed, 149 subtests`. These commands are semantically equivalent to `uv run pytest` for this no-project research repository.
- Manual non-Codex evidence-based review: isolated opt-in module, no new dependencies, no modifications to compiler or World execution, exact `MarketingLedger` remains sole money engine, and full audit/policy/World revalidation happens before replacing bytes. A2M Code Review Graph could not inspect the isolated worktree because it lies outside its approved workspace; no independent graph-review result is claimed.

Open boundaries: untrusted paths, compromised OS/filesystem, physical power-loss durability and multi-writer arbitration are outside verified scope; no fabricated independent security approval, signature or true rollback-proof authority is claimed.

## Security and recovery scope

The public coordinator is opt-in and single-writer. The file path and original World/policy are assumed trusted. The candidate must pass `export_audit` revalidation and the checkpoint is re-read and revalidated before success. The versioned receipt includes trial identity, complete checkpoint checksum, ledger identity set, fixed-minor-unit snapshot fingerprint and domain-separated derived identifier. Receipt equality is only checksum-bound consistency under known inputs. Directory `fsync` completion and supported filesystem semantics are prerequisites for the documented acknowledgement path; external power-fail atomicity and stable-media durability were not independently established. A process dying after `replace` but before successful directory sync produces an uncertain commit, irrespective of the candidate's present namespace visibility. An externally retained receipt can flag older valid content substitution, but a receipt stored next to the checkpoint on equally untrusted media is not an anti-rollback anchor.

The protocol is not a database, does not serialize competing processes, does not authenticate the claimed external financial actor, does not prove real-world economic causation, and does not provide network/physical exactly-once delivery. No accepted ADR was created. No keys, signing infrastructure, distributed locks or extra accounting engine were added.
