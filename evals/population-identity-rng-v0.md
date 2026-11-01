# Population Identity and Keyed RNG Evaluation v0 — Phase 007A

Status: **BOUNDED IMPLEMENTATION VERIFIED**, 2026-11-01. No accepted new language, legacy migration, or global RNG-policy ADR. No independent external reviewer sign-off is claimed. Phase 007 is still BLOCKED on financial/reference metrics.

## Source and verification provenance

- Initial application HEAD `311569d0a3ba58eaeb5d171e5b74758176720686`; initial research HEAD `89d880e44d88a7d85346bb974e91b6ad8d1ac9bf`, both initially clean, both on `work/phase-007-population-contract`. New isolated local branches `work/phase-007a-population-identity-rng`. No resets, remote actions, dependency modifications, or untracked-file overwrites.
- Host: macOS 27.0.1 arm64, Python 3.12.13 via uv, FunnelScript 0.2.0a1. Research verification uses system `python3`; provenance output and test logs are retained locally in Git-ignored `plans/007a-benchmark-results.jsonl` and `plans/007a-verification.log` on the application checkout.
- Source fixture: application `tests/fixtures/population-reference/identity-rng.fnl`, SHA-256 `c64f1caaf28330152c4bc06c44f6a98b8041a8009f5dff7a8f76bed403b3bf46`, with **no imported source dependencies**. Golden fixture: `keyed-rng-golden.json`, SHA-256 `59a52bb95425acca459abe4bec9e978aeac42d29e21c5b603cb234c72f77214e`. Exact input instances are `agent-000` through `agent-(N-1)` zero-padded to width three; cohort `batch-1` in the bounded experiment, segment membership `north` for even index and `south` for odd index; all initial `phase="new"`, each receives one `Visitor.Tick@0`, which transitions to `phase="terminal"` with one uniform draw. Trial IDs `trial-1`, `trial-2`, world seed `1`, stream role `world-transitions`, `until=None`, `max_events=100000` per instance.
- Exact replay manifest must additionally bind the application source revision (including any uncommitted working-tree delta during measurement), transitive source dependency bytes, complete ordered per-ID input events, Python/runtime/package versions, platform/floating-point environment, `world_seed`, trial and agent IDs, cohort/segment membership, stream-role namespace, derivation version, partition field, state-label set, and time/event limits. The described benchmark is a **dirty working-tree Phase 007A measurement against baseline HEAD**, not a measurement of clean historical commit `311569d`. When reproducibility across machines is material, pin the entire environment and compare canonical output, not only elapsed time.

## H-ID1/H-RNG1/H-RNG2/H-RNG3/H-RNG4 matrix

| Hypothesis | Executable counterexample boundary | Observed result | Classification |
| --- | --- | --- | --- |
| H-ID1 | Missing/duplicated IDs, missing registered state, or nonexhaustive exclusive partitions | Explicit 10/100/1000 initialization; singleton identity storage; disjoint new/terminal/inactive partitions, including inactive ID preservation. Duplicate/missing/noncanonical IDs, bad partition, invalid final state and unknown event owners reject | PASS for bounded independent-instance adapter |
| H-RNG1 | Same canonical identity maps to changed seed/draw | Independently fixed SHA-256 full-digest values, precise first/second `random.Random` draws, version label and invalid identity/seed/role rejection; forced derived-seed collision rejects | PASS for the specified deterministic derivation; no statistical independence proof |
| H-RNG2 | Reversal/permutation/insertion/removal changes a matched independent agent's stream | Forward/reverse, reproducibly shuffled enrollment, segment membership reorder, unrelated agent inserted/removed: matched per-agent states and processed events equal | PASS under no cross-agent causal interaction |
| H-RNG3 | Executing a different trial mutates first trial replay | Trial-1/trial-2 fixed goldens differ; trial-1 repeats byte-equivalent Python records after trial-2; no retained PRNG instance | PASS under stated runtime and ordered-input version constraints |
| H-RNG4 | Policy-only comparison shifts an unrelated matched instance's local stream | Unchanged agent input role remains paired while changed agent receives an extra local Tick and legitimately consumes another draw; intervention outputs reproducible | PASS for *computational pairing*, NOT causal inference, not guaranteed alignment after changed draw schedule |

## Implementation selection, governance and limitations

**Option B selected as narrow Python adapter**: `WorldExecutor` is the accepted source semantic interpreter; `EventMachine` remains the single event scheduler. `PopulationExecutor` encloses an immutable sequence of `PopulationAgent(agent_id, cohort_id, segment_id)`, fixed `seed`, exact `trial_id`, `state_field` and declared partition labels; it executes `WorldExecutor.run` independently for each agent's ordered event sequence. Public `run(events_by_agent, *, stream_role="world-transitions", until=None, max_events=100000)` returns `PopulationResult(trial_id, stream_role, rng_version, results, partitions, segments, cohorts)`. `stream_seed(agent_id, *, stream_role=...)` exposes the deterministic seed for inspection. Only one World agent source declaration is accepted as the reusable typed template. Application's `world_executor.py` contains this adjacent adapter to avoid a new engine, parser keyword, module load cycle, or duplicate event scheduler.

Option A generalized population execution layer is deferred because causal shared-state/global-calendar semantics would require an accepted new migration/interaction decision; Option C kernel-level keyed RNG injection is more invasive and threatens accepted event tie/guard/shared-RNG behavior with no present necessity. The adapter leaves default `EventMachine.run` and `WorldExecutor.run` unmodified. Accepted DEC-019/027/031 remain in force. Proposed Phase 007A research contract is **not an accepted language ADR**, and no accepted ADR is invented. A future shared-shock or global interaction contract requires explicit acceptance.

**RNG identity:** `population-rng-v1/sha256-mt19937`. UTF-8 of compact ASCII JSON array `["population-rng-v1", 1, "trial-1", "agent-000", "world-transitions"]`; hash with `hashlib.sha256`, take full 256-bit unsigned big-endian integer as the seed to existing Python Mersenne Twister. Independent reference digest for this identity: `8f4f6d5087da7bf410bb3d4387ae4b0efeef21b78730df44d42fbd90f658f8da`; first draws `0.15311003683137503`, `0.8942108333437118`. For `agent-001`, first draws `0.7905505363492208`, `0.9135983467787107`. For trial-2, the first `agent-000` and `agent-001` draws are `0.38727023169593455` and `0.12862839062877407`. These expected numbers originated from a separate Python standard-library reference computation, not production stream derivation. No numerical guarantee across Python distributions/interpreters, no measured statistical independence, and no collision-free mathematical guarantee. Within one role's event calendar, source-order draw consumption and the event kernel's ordering remain unchanged.

**State ownership:** The adapter holds a fixed identity table; each agent's typed World run starts from its own freshly generated source initial state. Its run-result mapping is an identity-indexed **readable snapshot** at the requested stopping horizon, with no implicit population creation/destruction. Identity partition sets are constructed from each completed record with every declared partition present, and are compared to the initialized ID set. The returned Python dictionaries are not tamper-proof immutable serialization; external mutation of a returned run state's nested dict is not an executed engine transition and is outside the checkpoint guarantee. Every `until` query replays from initial conditions; it does not serialize/restorably resume RNG state. Source-authored handlers decide which states are absorbing, and the adapter does not force terminal transitions.

**Causal limits:** No cross-agent event emission, inter-agent messaging, global event tie-order semantics, shared-shock stream, policy-specific random operator roles within one World handler, or independently randomized intervention framework is implemented. Common-random-number pairing holds only when matched identities, roles and consumption schedule match. Different outcomes following altered event schedules are expected. Stateless stream derivation across distinct agents does not establish statistical independence or empirical intervention identification.

## RED/GREEN and independent fixture evidence

1. **Behavioral RED (public API missing):** `uv run pytest tests/test_population_identity.py::test_ten_instances_have_exhaustive_identity_partition -q` yielded the precise assertion `AssertionError: Missing opt-in population API`, `1 failed`, exit **1**. The existing module imported successfully; this was neither a fixture/collection error nor a default-World defect.
2. **GREEN for the same test:** identical command, `1 passed`, exit **0**, after adding the minimal production adapter. The test verified exact population membership and pinned, independently computed first draws.
3. **Second behavioral RED:** `uv run pytest tests/test_population_identity.py tests/test_population_rng.py -q` yielded `31 passed, 1 failed`, exit **1**, because a generator event sequence was silently consumed as a one-shot input (`Failed: DID NOT RAISE TypeError`). A replayable-input boundary was necessary for the claimed deterministic replay.
4. **GREEN after a two-line sequence validation:** identical focused command yielded `32 passed`, exit **0**; after adding an independently checked fixed fixture plus edge tests, final focused corpus yielded `36 passed`, exit **0**. Later additions extended coverage after the initial RED/GREEN cycles; they are NOT misrepresented as individually observed RED cycles.
5. **Independent corpus ID P-KEYED-1:** explicit fixed JSON preimage, digest, first and second draws, separate trial constants and rejection cases. Expected values are pinned rather than generated through the production adapter. **P-RNG-ORDER-1 remains untouched and passes on default World**, with the exact original A/B order coupling.

## Bounded measured experiments

Method: `uv run python -` inline runner; `time.perf_counter` measures `PopulationExecutor`/World construction plus one forward population run; Python `tracemalloc` reports peak *traced Python allocations* in that interval (not total process RSS, heap-resident VMs, or platform memory footprint). Garbage collection occurs immediately before each sample; each forward result is independently compared with an unmeasured reversed-enrollment replay; input event streams are one Tick at time zero per ID. Two exact trials, seed 1. No warmup statistical confidence interval, throughput projection or scaling claim is authorized.

| N | north | south | Trial | Forward wall seconds | Peak traced bytes | Terminal agents | Exact identity partition | Reversed per-agent match |
| ---: | ---: | ---: | --- | ---: | ---: | ---: | ---: | --- |
| 10 | 5 | 5 | trial-1 | 0.004186 | 31991 | 10 | yes | yes |
| 10 | 5 | 5 | trial-2 | 0.002631 | 28441 | 10 | yes | yes |
| 100 | 50 | 50 | trial-1 | 0.010388 | 125625 | 100 | yes | yes |
| 100 | 50 | 50 | trial-2 | 0.010096 | 125577 | 100 | yes | yes |
| 1000 | 500 | 500 | trial-1 | 0.085704 | 935697 | 1000 | yes | yes |
| 1000 | 500 | 500 | trial-2 | 0.085511 | 935649 | 1000 | yes | yes |

All benchmark records reported `inactive=0` in the full-transition scenario, `new=0`, `terminal=N`; a separate 10-agent mixed new/terminal/inactive fixture proves retained terminal/inactive identity with each unique ID counted exactly once. The repository contains no externally supplied conversion probabilities, costs or calibration parameters in this experiment. Input cohort/segment metadata has no economic meaning.

## Complete fresh verification receipts

All final commands run from application root except research unittest from its own root; each exit code is captured from actual process output:

| Command | Result | Exit |
| --- | --- | ---: |
| `uv run pytest tests/test_population_identity.py tests/test_population_rng.py -v` | 36 passed (0.22s) | 0 |
| `uv run pytest tests/test_population_reference.py -v` | 2 passed (0.12s) | 0 |
| `uv run pytest tests/test_world_conformance.py -v` | 50 passed (0.18s) | 0 |
| `uv run pytest tests/test_world_stochastic.py -v` | 25 passed (0.59s) | 0 |
| `uv run pytest tests/test_event_machine.py -v` | 16 passed (0.06s) | 0 |
| `uv run pytest tests/test_world_rules.py tests/test_world_guards.py tests/test_world_emissions.py tests/test_world_payloads.py tests/test_world_modules.py -q` | 160 passed (2.74s) | 0 |
| `uv run pytest tests/test_engine_scale.py tests/test_agent_core.py -q` | 9 passed (0.22s) | 0 |
| `uv run pytest -q` | 374 passed, 58 subtests passed (6.35s) | 0 |
| `python3 -m unittest discover -s tests -v` | 5 passed (0.036s) | 0 |

A preliminary shell loop incorrectly quoted two multi-file test targets as single paths, causing two `pytest` invocation errors (exit 4; zero tests collected) rather than behavioral failures. It was corrected; the exact separate multi-file commands above were executed and passed. No historical total was substituted for fresh runs. Frontend sources and APIs were not changed; `bun test` and build were not run.

## Review checklist and remaining risk

Bounded self-audit against the 17 requested adversarial dimensions: no diff to `EventMachine.run` or pre-existing World run code; no global RNG replacement, no `hash()`, no index-derived stream offset, no new scheduler, no new dependency, no default-world oracle modification, no test deletion/weakened assertion, no hidden cross-trial mutable RNG, duplicate and missing identities reject, final snapshots retain terminal IDs, collision check is explicit, segment/trial ID serialization is unambiguous, no overclaim of causal/statistical independence or performance beyond six observed samples. Proposed architecture preserves existing accepted semantics and documents isolated-instance/causal and mutable-return limitations. The A2M Code Review Graph declined inspection because these repositories are outside its approved graph workspace. No independent reviewer verdict was obtained; this is **self-audit evidence only**, not a separate reviewer sign-off. Additional independent review can inspect the committed local diff before any future migration.

**Remaining Phase 007 blockers:** independent financial ledger with delayed settlement, illiquid receivable ownership and cash conservation; typed, dimensioned conversion/CAC/ROAS/profit/ruin/VaR/CVaR definitions integrated with a real executable reference model; independently constructed financial counterexamples and per-trial distribution oracles; scientific and adversarial review of those contracts. No arbitrary market rates have been introduced. Phase 008 empirical calibration, external market validity, statistical calibration, causal inference and real-world prediction accuracy have NOT been tested.

**Next executable continuation:** Phase 007B, a separately reviewed domain-owned ledger and metric fixture/implementation gate using existing typed events and this optional isolated-instance population contract, without changing source-language axioms or silently assuming real-world calibration. No automatic transition executed.

**External market validity, statistical calibration, causal inference, and real-world prediction accuracy were not tested.**


## Post-verification local application commit receipt

The unchanged Phase 007A code, tests, fixture and application documentation were committed locally on `work/phase-007a-population-identity-rng` as `7d75d89e1e3cef5c6c5f59f84e591e678ef887ad` (`feat(population): add stable agent identity and keyed RNG streams`). The application Git working tree was clean immediately after this commit. Post-documentation verification before committing was repeated: full application `374 passed, 58 subtests passed` (6.38s, exit 0); research unittest `5 passed` (exit 0). The benchmark was measured before committing on the exact experimental code path and has not been re-labelled as an independently repeated post-commit benchmark. The research commit SHA and both final Git states are recorded only after research commit completion in the local ignored plan mirror.
