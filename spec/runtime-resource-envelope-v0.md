# Runtime Resource Envelope v0: Queue Admission, Retention and Population Scale

Status: **PROPOSED, NOT ACCEPTED OR IMPLEMENTED**, 2026-11-02.
Recovery stage: R3. Authority: accepted DEC-008/009/019/027/031 and
[event-kernel-v0](event-kernel-v0.md),
[population-identity-rng-v0](population-identity-rng-v0.md).
No existing public Python or World contract is changed by this document.

## Problem and direct evidence

`EventMachine.run(..., max_events=N)` limits processed due events only. It eagerly
loads every initial event into a heap, admits every valid emitted event and returns
fully retained `processed`, `intents`, and `pending` tuples. An `until` horizon
does not exempt future events from initial queue allocation. An event cap of one
therefore does not imply constant space. Observed on CPython 3.12.13/arm64:
100,000 future events, `until=0`, `max_events=1` produced 100,000 pending
events at a 22.1 MB traced peak. A single processed event emitting 100,000
future events also returned 100,000 pending at a 22.9 MB traced peak.
See [measured baseline](../evals/runtime-resource-baseline-2026-11-02.md).

`PopulationExecutor.run` executes one isolated `WorldExecutor.run` per enrolled
agent and retains every `RunResult`, identity partition and optional trace.
The currently supported adapter has no shared causal agent interactions or
incremental aggregate-only output contract. Existing vectorized *legacy*
`SimulationEngine` throughput does not benchmark this World path.

## Contract axes and invariants

For queue Q after each admission, processed history P, inert intents I and
declared limits `Lq`, `Lp`, `Li`:

1. **Admission:** `|Q| <= Lq` throughout a successful bounded run. Apply the
   same admission rule to initial events and transition-emitted events. A
   count-exceeding input must raise a named resource-limit failure; silently
   dropping events, ignoring a horizon-future event or truncating the return
   tuple is forbidden.
2. **Processed budget:** retain accepted `max_events` semantics; a successful
   run obeys `|P| <= max_events`. Queue limits and process limits are
   independent: neither is evidence for the other.
3. **Result retention:** a full-result mode must return every processed event,
   effect intent and pending event exactly once, in its documented order.
   If configured history/intent limits are exceeded, fail explicitly; no
   hidden sampling or summary substitution. Any aggregate-only mode has a
   distinct versioned output type and cannot be mistaken for `RunResult`.
4. **Determinism:** if resource limits do not bind, `state`, `processed`,
   `intents`, `pending`, event ordering and RNG draws must exactly match the
   unlimited v0 run for identical source, inputs, seed and environment.
5. **Failure boundary:** a limit failure has a typed category, configured cap,
   observed attempted count and the event boundary. No successful partial
   `RunResult` is returned. A Python reducer may mutate external objects or
   perform I/O; the kernel cannot roll back arbitrary reducer side effects.
   Only kernel-owned queue/output publication can be atomic.
6. **Adversarial payload:** event-count caps do not cap Python object size,
   cyclic graphs or arbitrary model state. A process-level RSS/memory guarantee
   requires a separate policy/isolation mechanism. Any wall-clock deadline
   checked only between reducers cannot interrupt a blocking Python callback.

The kernel must remain domain-neutral: no wallet, budget, settlement, marketing
classification or inferred absorbing-state rule is introduced.

## Falsifiable hypotheses

- **H-RQ1:** For an iterable with `Lq+1` future events and `until=0`,
  bounded admission rejects while consuming at most `Lq+1` entries.
  Falsifier: it materializes the full unbounded iterable or returns a
  success with missing future events.
- **H-RQ2:** One transition emitting more events than the remaining queue
  capacity produces a resource failure, not a silently truncated calendar.
  Falsifier: a pending event disappears or an effect is published as success.
- **H-RT1:** With nonbinding queue/history/intent limits, complete golden
  tuples and fixed-seed stochastic traces are byte-for-byte equivalent to v0,
  including same-time insertion and priority constraints.
  Falsifier: adding limits changes the order/draws of an otherwise valid run.
- **H-RT2:** Full-result history and intent quotas reject oversized output;
  a future aggregate-only API is distinguishable by its return type and
  records exact counts without inventing missing traces.
  Falsifier: a consumer receives incomplete `RunResult` indistinguishable
  from a complete result.
- **H-RP1:** Population execution at N=1k,10k,100k identities has measured
  elapsed time and RSS for full and proposed reduced-retention modes, with
  identical final partition identities under nonbinding limits. No claim
  follows before the 100k case completes on representative hardware.
  Falsifier: missing/duplicated IDs, changed keyed RNG for matched agents,
  or an unlabeled memory/throughput claim.

## Implementation alternatives (decision pending)

**A. Additive opt-in bounded run.** Reuse the existing heap, insertion ordinal
and `max_events`; add explicit per-run queue admission and separate retention
quotas with a typed failure contract. Default v0 behavior remains unchanged
for existing call sites. Advantages: smallest compatibility surface, easy
negative controls and rollback. Limitation: full pending/result retention still
scales with admitted event count; Python payload bytes are unbounded by counts.

**B. Distinct streaming/aggregate runner.** Keep event ordering in one
authoritative scheduler while routing processed events through a declared
consumer and returning a versioned summary/checkpoint instead of full tuples.
Advantages: can avoid linear processed-history retention for long jobs.
Costs: replay/resume boundaries, output sink failures, backpressure, checkpoint
RNG state and multi-agent causal scheduling require their own accepted contracts.
Simply adding an iterator around existing full `RunResult` is not streaming.

Recommended sequence: prove A against H-RQ1/H-RQ2/H-RT1/H-RT2 as a reversible
safety slice, benchmark both designs on explicit workloads, then choose if B is
necessary. Do not publish `max_pending` or retention parameter names, defaults,
error subclasses or summary schemas as stable APIs before acceptance.

## Verification and workload matrix

| Workload | Cardinality | Required evidence |
| --- | --- | --- |
| Future-only initial calendar | 1k, 10k, 100k events | `until=0`, `max_events=1`; elapsed, traced peak, RSS, pending |
| One-event fan-out | 1k, 10k, 100k emissions | Queue boundary failure and no lost accepted work |
| Fully due calendar | 1k, 10k, 100k events | Stable order, exact processed counts, deterministic replay |
| Mixed priorities / zero-delay loop | 1k and cap+1 | Original v0 golden order, explicit resource-limit precedence |
| Identity-isolated population | 1k, 10k, 100k agents | Seed mapping, final partitions, per-agent result retention, elapsed/RSS |
| Optional trace and effect intents | bounded/unbounded variants | Independent result budget, no silent truncation |
| Blocking/side-effecting reducer | controlled only | Document inability to enforce hard per-step deadline or external rollback |

Use a fixed, documented source revision, CPython version, CPU, input generator,
event payload size and tracing settings. Run memory experiments in fresh
processes when measuring RSS, include warm/cold effects, and report exact failure
modes. Do not use fixed wall-time assertions in CI on shared runners. Stress
100k independent World agents only with an explicit resource cap/timeout and
operator approval; a synthetic local vectorized benchmark is not equivalent.

## Stop, acceptance and rollback

STOP if the design changes accepted event order, snapshot atomicity, default
World RNG, public `RunResult` completeness, arbitrary Python callback semantics
or a live-provider effect boundary without a separate reviewed ADR. No silent
default caps and no retention-dropping `RunResult` change. Final acceptance
requires reproducible RED/GREEN counterexamples, full conformance suites,
resource failure taxonomy, local and CI test evidence, owner-signed public
contract and a migration/rollback note. This proposal creates no release claim.
