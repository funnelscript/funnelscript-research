# Stable Population Identity and Keyed RNG Substreams v0 — Phase 007A

Status: PROPOSED opt-in Python runtime extension; source-language and default-World semantics unchanged. This is a bounded engineering contract, not acceptance of a World or legacy migration ADR. 2026-11-01.

## Research anchors and governance
Banks et al., *Discrete-Event System Simulation*, 5th ed. (2010), for finite event calendars and replications; Law, *Simulation Modeling and Analysis*, 5th ed. (2015), for verification and common random numbers; Python documentation for [random reproducibility](https://docs.python.org/3/library/random.html#notes-on-reproducibility), [hashlib](https://docs.python.org/3/library/hashlib.html) and [canonical JSON limitations](https://docs.python.org/3/library/json.html). DEC-019 fixes the event-kernel ordering and single-run RNG contract; DEC-027 fixes snapshot-atomic transitions; DEC-031 fixes default source-level stochastic draw semantics and explicitly deferred population streams. This proposal MUST NOT re-interpret those accepted contracts.

## H-ID1: Explicit fixed population and immutable ownership
A *population agent instance* is NOT a World source-level agent declaration. Exactly one type-checked World agent declaration is used as a reusable event/state template; many stable instance IDs are enrolled through a Python opt-in adapter. Each entry has nonempty unique `agent_id`, nonempty `cohort_id`, and nonempty `segment_id`. `trial_id` belongs to a run configuration, never to an array index. IDs are exact case-sensitive ASCII strings matching `[A-Za-z0-9][A-Za-z0-9._:-]*`, avoiding Unicode normalization ambiguity and empty/whitespace/canonical-alias problems. Enrollment and source-typed initial state are fixed for one execution. Duplicate/missing/invalid identity, zero agents, unknown event-owning instance, invalid configured state partition, or a checkpoint with a missing instance are rejected.

The adapter owns the identity table and routes `agent_id -> ordered Event sequence`. Event names are existing source-qualified `Owner.Event` names for the one World declaration; EventMachine remains sole event scheduler. The World owns typed local fields and source-defined transition/guard/terminal policy. The adapter DOES NOT infer absorbing states or permit runtime enrollment. An `inactive` or `terminal` string value is just a declared partition label; retention, not absorbing behavior, is guaranteed by the adapter.

For initialized set `A`, state values `S`, and each complete `until`-bounded checkpoint:
`A = disjoint_union_{s in S} {a in A: state[a][state_field] == s}`, and `|A| = sum_s |A_s|`.
Set equality and pairwise disjointness must both be verified, not just counts. The adapter returns each instance's complete World `RunResult`, plus an identity-indexed partition snapshot. Checkpoints replay from initial conditions to a given `until` time; continuation or restoration of in-flight PRNG states and arbitrary per-event ordinal snapshots are NOT supplied. Failure on one agent need not roll back previously computed Python results (the adapter does not publish partial success).

Falsifier: one initialized ID vanishes, duplicates, or belongs to two exclusive partition states at a successful checkpoint.

## H-RNG1: Versioned deterministic stream identity
Use tuple `(world_seed, trial_id, agent_id, stream_role)` with explicit nonnegative exact integer `world_seed < 2**64`. Stream roles are caller-provided identity strings, default `world-transitions`. The canonical seed preimage is UTF-8 of:
`json.dumps(["population-rng-v1", world_seed, trial_id, agent_id, stream_role], ensure_ascii=True, separators=(",", ":"))`.
Hash the preimage with standard-library `hashlib.sha256`, interpret the entire 32-byte digest as an unsigned big-endian integer, and seed Python `random.Random` through the already-accepted `EventMachine.run(seed=derived_integer)`. Derivation id: `population-rng-v1/sha256-mt19937`. There is NO Python `hash()`, position offset, global RNG, platform entropy, or new dependency. Reject noncanonical identities and invalid seed types. Detect any duplicate derived seeds among concurrently enrolled IDs for a chosen role/trial rather than silently assign an aliased stream.

The adapter's one stream per agent, trial and role consumes one PRNG draw per source operator in each agent-local calendar's established chronological/priority/insertion order. It does NOT provide per-expression counter-based draws; changes to the agent's own event sequence or policy can change its subsequent draws. SHA-256 seed separation is deterministic and collision-resistant for tested finite inputs; it is NOT proof of statistical independence. Python `random()` has documented sequence-compatibility conditions; float arithmetic and other interpreter/platform behavior must be version pinned. No cross-language or cross-runtime-bitwise guarantee.

Falsifier: two identical stream identity tuples generate different first-draw bytes under pinned configuration, or an unrelated agent changes a matched agent's assigned stream.

## H-RNG2: Permutation/extension/removal invariance
For the same stable IDs, seed, trial ID, role, program/dependencies, and causally identical per-agent event sequences, matched `RunResult` projections are identical under forward/reverse/fixed permutation of agent enrollment, segment enrollment, and trial execution. Inserting or removing unrelated IDs does not shift existing streams. This is an **agent-local** invariant for independent event sequences only. Explicit interactions, shared environmental shocks, cross-agent causal effects and global tie order can alter the causal input: they are outside the current isolated-instance adapter.

Falsifier: simply reversing the adapter's enrollment order assigns a different sample to the same identity with unchanged local events.

## H-RNG3: Trial isolation and replay
An exact replay manifest must record: source+transitive dependency fingerprints, package/runtime and Python version, OS/architecture/numeric environment, `world_seed`, `trial_id`, complete stable ID+segment/cohort enrollment, `stream_role`, derivation version, ordered per-instance input events and `until`/`max_events` configuration. Equal manifests and environment produce equal normalized states, processed/pending events and effect intents. Trial identities change derivation inputs; different trials need not produce distinct stochastic outcomes. No shared mutable RNG persists between executions.

Falsifier: one execution of trial X changes the independently repeated result for trial Y.

## H-RNG4: Bounded paired common-random-number coupling
Baseline and intervention using the same agent/trial/world seed/role and **unchanged exogenous draw schedule** use the same keyed pseudorandom sequence. Policy-specific stochastic draws MUST use a different explicit `stream_role` in separate executions; randomized interventions, event-dependent sample consumption and changed event scheduling need not retain downstream alignment. The v0 adapter cannot isolate exogenous vs policy samples inside a single World handler: author separate roles/executions or accept this limitation. This is computational pairing, NOT proof of causality, unbiased effect estimation or statistically independent Monte Carlo replications.

Falsifier: a policy-only comparison on agent X silently reassigns an unchanged agent Y's local stream because of enrollment order.

## Architecture evaluation and decision gate
- **A — Opt-in population execution layer:** supports explicit identity and checkpoints but risks another event engine if it implements its own queue. Narrow its responsibility to routing/collating isolated existing `WorldExecutor.run` invocations. No agent-to-agent interaction supported.
- **B — Explicit agent execution adapter (selected for a bounded, authorized Phase 007A experiment):** one source agent template, one existing WorldExecutor/ EventMachine call per instance, explicit derived seed, no new scheduling code. Lowest compatibility risk for DEC-019/031, source neutral, simple oracle; potentially O(N) interpreter overhead, no resumable keyed RNG states, no interactions or group shared shocks. Benchmark at N=10,100,1000 before throughput claims. Only an opt-in Python API; NOT an accepted DSL migration or full population simulation architecture.
- **C — Event kernel opt-in RNG resolver:** could preserve one global calendar and support causal interactions, but invasive RNG dispatch/ownership plumbing makes default guard, priority, emission and World semantics riskier and raises an unaccepted calendar-global identity policy. Deferred.
No required ADR for changing the semantics of existing APIs: none are changed. New shared-shock/interaction semantics, generalized multi-owner population routing, checkpoint restoration, legacy unification or language changes REQUIRE a separately accepted ADR. The new adapter's optional interface and exact derivation remain documented as proposed v0 while evidence is gathered.

## Compatibility and negative controls
The existing default `EventMachine.run` and `WorldExecutor.run` continue to use exactly one run-local `random.Random(seed)`; their accepted behavior must be exercised by Phase 006 goldens and unchanged P-RNG-ORDER-1. This is not a defect in legacy execution. Legacy `SimulationEngine` uses a different array-position trial implementation with no public agent-ID mapping. Do not migrate it or claim parity. Population partition/state checks are domain neutral; financial conservation, CAC, ROAS, CVaR, receivable settlement and marketing behavior are Phase 007 dependencies, not universal compiler axioms.

**External market validity, statistical calibration, causal inference, and real-world prediction accuracy were not tested.**
