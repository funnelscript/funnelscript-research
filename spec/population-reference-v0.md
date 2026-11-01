# Population and Reference Metric Contract v0

Status: PROPOSED, PHASE 007 BLOCKED at H-POP2, 2026-11-01. Neither a population engine nor an accepted ADR.
Evidence baseline: application 534449b85b3731ea81ea5d4755db0c6bb8b0e67d, research ca0c03b2c97c9b7f974add2431550f79cc4aa704. Work branches: work/phase-007-population-contract.

## Research anchors and established boundaries

Banks et al., Discrete-Event System Simulation, 5th ed., 2010 (event calendars and replications); Law, Simulation Modeling and Analysis, 5th ed., 2015 (verification versus empirical validation); Python Software Foundation, random module reproducibility notes (https://docs.python.org/3/library/random.html#notes-on-reproducibility); Rockafellar and Uryasev, Optimization of Conditional Value-at-Risk, Journal of Risk 2(3), 2000. Existing project contracts: DEC-003, 005, 008, 009, 010, 019, 027–032, 037; spec/event-kernel-v0.md, spec/stochastic-operators-v0.md, spec/world-conformance-v0.md, spec/marketing-stdlib-v0.md. Existing source determines current behavior; a documented future ambition is not implemented evidence.

## H-POP1: identity-preserving population partitions

Future model: an agent is an independently identifiable simulated entity, not an aggregate count, marketing exposure, trial, or source-level agent declaration. For finite initialized ID set A of size N and exclusive exhaustive states S at checkpoint t:

  disjoint_union_{s in S} A_s(t) = A
  sum_{s in S} |A_s(t)| = N.

Set equality is required in addition to a scalar count equality, to detect two miscounted IDs canceling one another. An agent_id is stable, canonical, nonempty and unique within trial; missing/duplicate IDs reject initialization, with no iteration-position-based fallback. trial_id uniquely identifies a replication, cohort_id identifies an enrollment batch, segment_id identifies a declared category; none is secretly the agent index. The initial state of each ID is an explicit valid state, with one owner responsible for atomic per-ID updates. Illustrative states are unexposed, aware, converted, inactive and churned. Terminal and inactive IDs remain counted. Absorbing-state policy is domain-authored, not universal. At every post-event-ordinal or post-time checkpoint every initialized ID belongs to exactly one declared state; pending events do not create agents. Unknown IDs, unknown transitions, mixed states, duplicate IDs and absent identity are invalid, not implicitly repaired.

Falsifier: a valid transition duplicates, loses, or assigns more than one state to an initialized ID. CURRENT GAP: WorldExecutor.initial_state() creates one state per source declaration name, not an initialized ID population. Marketing lead_response.fnl models a single journey. Legacy SimulationEngine maintains array positions without exposing stable IDs in TrialResult. H-POP1 is specified but unverified in an actual population public API.

## H-POP2: stable keyed pseudorandom streams

Future contract: for world seed w, trial ID q, agent ID a and two cohort iteration orders p1 and p2, T(a,w,q,p1)=T(a,w,q,p2) if all causally relevant conditions remain identical. A stream identity must include versioned algorithm ID and a deterministic, unambiguous, typed and length-delimited encoding of (w,q,a,stream role), then documented seed derivation. Process hash(), iteration position and unspecified seed arithmetic are forbidden. Independent stream identities are *not* a proof of statistical independence; finite seed spaces can collide and PRNG sequences have finite periods. Pin RNG version, draw algorithm, within-stream call sequence, source/module bytes, ordered events, numeric platform and input manifest. Adding/removing an unrelated agent must not shift existing local streams unless modeled interactions or shared environmental shocks causally couple them. Paired counterfactuals must match IDs, stream identities and exogenous randomness and explicitly state intervention-dependent draw changes. Separate independent trials require separately identified replication streams; distinct names are insufficient proof of statistical independence.

Confirmed limitation P-RNG-ORDER-1: EventMachine.run creates one random.Random(seed) per whole calendar, with events ordered by (time, priority, insertion ordinal). WorldExecutor.run accepts seed but no (agent_id, trial_id) stream selector. One uniform draw in each of source-named owners A and B at time 0 and seed 1 yields:
  A then B -> A=0.13436424411240122, B=0.8474337369372327.
  B then A -> A=0.8474337369372327, B=0.13436424411240122.
Identical order and seed replay exactly; owner-specific outcomes change under permutation. These numbers match the first two independent CPython Random(1) reference values from Phase 006. WorldExecutor.advance permits caller-injected RNG, but does not supply keyed derivation, population initialization or population event dispatch. Inventing those inside a test does not demonstrate an existing public API. Thus H-POP2 is not satisfied; this is not a regression in accepted shared-World RNG semantics. **STOP** pending a separately governed population-stream contract.

## H-POP3: model-owned cash and receivables

A declared trial-level ledger in one specified ISO 4217 currency CUR, time unit and horizon H must satisfy:

  cash_end = cash_initial + settled_receipts - paid_ad_spend - paid_other_declared_costs.
  receivables_end = receivables_initial + credit_sales_recognized - settlements - writeoffs + declared_adjustments.

Sales recognition does not settle funds. A receipt must reference an existing unsettled item; the same receivable may not be settled twice. Each record needs immutable trial_id, transaction_id, event type, timestamp, finite decimal amount, currency, signed adjustment semantics and reference. Reject missing IDs, repeated IDs, negative non-reversal amounts, NaN, infinity, mismatched currencies, unit mismatches, settlement without documented source, or incomplete timeline. Document currency-minor-unit precision and rounding; floating point finance is not automatically exact. Model-specific policy determines whether negative cash is permitted through explicit credit, defines insolvency threshold and specifies settlement delay. No automatic cash halt, wallet or financial invariant belongs to the generic World compiler (DEC-009).

Independent hand arithmetic: initial cash 100 CUR; 60 CUR recognized revenue; 30 CUR settled receipts and 30 CUR unpaid receivables; 20 CUR paid ads; 5 CUR other paid costs. Closing liquid cash is 100 + 30 - 20 - 5 = 105 CUR, NOT 135 CUR. Recognized trial profit is 60 - 20 - 5 = 35 CUR, NOT cash change. The sample has two segments of 4 and 6 agents, with 1 and 2 converted respectively. These are illustrative counts, not a runtime-produced population trace. Falsifier: unexplained cash changes or treating 30 CUR receivable as cash. Current Marketing library has revenue and spend fields only, no explicit cash/settlement ledger. H-POP3 contract remains unimplemented/unverified.

## Metric reporting conventions

Every metric must include the simulated-versus-observed label, scenario, trial ID set, segment/cohort, eligibility population, reporting window, currency where appropriate, exact horizon H, attribution procedure and numeric sign convention. No economic defaults are supplied. Complete zero events differ from unobserved/missing records. Missing required data produce invalid/null with reason. A zero denominator produces undefined/null, never a fabricated 0 or infinity for a comparable reference ratio. Weighting requires preregistered positive sample weights; never silently combine incompatible currencies, scopes or horizons. A pooled ratio of totals is not an arithmetic mean of per-agent, per-segment or per-trial ratios. Risk is defined on explicitly chosen losses, not an unlabeled mixture of profit and returns.

### M-CONV: conversion rate
1. Formula k/n (unique converted eligible agent IDs / unique eligible IDs).
2. Numerator k new converted IDs; denominator n baseline eligible IDs, not repeated events.
3. Unit: fraction, or percent after explicit multiplication by 100.
4. Horizon: conversions by H after declared enrollment.
5. Scope: trial, cohort or segment with disjoint eligible ID set.
6. Aggregation: sum k / sum n for pooled disjoint sets; weighted analog only if weights declared; mean of defined segment rates separately labeled.
7. Zero: n=0 -> undefined.
8. Missing: absent eligibility, identity or completion status -> invalid.
9. Sign: [0,1] for first unique conversion.
10. Example: A 1/4, B 2/6; pooled 3/10=0.30, unweighted segment mean (0.25+1/3)/2=7/24.

### M-CAC: customer acquisition cost
1. Formula paid attributable acquisition spend A / new customers k.
2. Numerator allocated cost; denominator new distinct acquired customers.
3. Unit: CUR/customer.
4. Horizon: declared attribution window H for spend and conversions.
5. Scope: per trial/segment or portfolio with attribution consistency.
6. Aggregation: total attributable spend / total acquisitions; not mean of heterogeneous per-trial ratios.
7. Zero: k=0 -> undefined, even when A=0.
8. Missing: unknown acquisition status, spend, attribution or currency -> invalid.
9. Sign: nonnegative for nonnegative paid spend.
10. Example: 20 CUR / 3 = 6.666666... CUR/customer.

### M-ROAS: return on advertising spend
1. Formula attributable *recognized* gross revenue V / paid advertising spend A.
2. Numerator V; denominator A, under same attribution contract.
3. Unit: dimensionless multiple.
4. Horizon: recognition and attribution through H, independently of cash settlement dates.
5. Scope: same trial/campaign/segment.
6. Aggregation: pooled V / pooled A, separate from arithmetic mean of trial ROAS.
7. Zero: A=0 -> undefined regardless of V.
8. Missing: unknown revenue, spend or attribution -> invalid.
9. Sign: nonnegative for nonnegative gross revenue and spend; net refund ROAS requires explicit definition.
10. Example: 60/20=3x; 30 settled is not the revenue numerator.

### M-REVENUE: recognized revenue
1. Formula V=sum of valid unique recognized gross sales by H.
2. Numerator: monetary sales; denominator: one reporting horizon, not a ratio.
3. Unit: CUR.
4. Horizon: recognition timestamps through H.
5. Scope: one trial or disjoint eligible transaction set.
6. Aggregation: additive only across disjoint valid items of same currency/window; trials analyzed as a distribution, not claimed to be simultaneous businesses.
7. Zero: complete no-sales ledger -> 0 CUR.
8. Missing: incomplete revenue records -> invalid.
9. Sign: nonnegative gross, refunds as separately recorded reversals.
10. Example: 3 sales of 20 CUR -> 60 CUR; paid receipts can be 30.

### M-SPEND: paid advertising expenditure
1. Formula A=sum of uniquely recorded ad-spend debits by H.
2. Numerator: debits; denominator: one reporting horizon.
3. Unit: CUR.
4. Horizon: actual payment dates, not merely scheduled obligations.
5. Scope: one trial or declared campaign.
6. Aggregation: add disjoint debits in same currency and time horizon.
7. Zero: complete no-spend ledger -> 0 CUR.
8. Missing: missing payment records -> invalid.
9. Sign: positive expense amount, subtracted in profit and cash equations.
10. Example: 8 + 12 = 20 CUR.

### M-PROFIT: trial profit or loss
1. Formula P=V-A-K with consistently recognized revenue V, attributable ads A and declared other cost K under a single explicit accrual basis.
2. Numerator: net monetary result; denominator: one trial.
3. Unit: CUR/trial.
4. Horizon: H consistently applied to sales and costs.
5. Scope: one simulation trial.
6. Aggregation: report mean/distribution over independent trial results, not cross-trial sum as one realized profit.
7. Zero: break-even P=0.
8. Missing: unknown revenue or declared costs -> invalid.
9. Sign: positive profit, negative loss.
10. Example: 60-20-5=+35 CUR; closing cash is 105 CUR.

### M-RUIN: probability of explicitly defined insolvency
1. Formula (1/M) sum_q 1[min_{t in [0,H]} C_q(t) < B_q(t)], with declared threshold B and checkpoint sampling policy.
2. Numerator: ruined trial count; denominator: complete valid trial count M.
3. Unit: fraction.
4. Horizon: all declared cash checkpoints through H.
5. Scope: trial distribution for one scenario.
6. Aggregation: indicator count / M, not agent fraction.
7. Zero: M=0 -> undefined.
8. Missing: undefined insolvency predicate or incomplete cash trajectory -> invalid.
9. Sign: probability in [0,1].
10. Example: one trial in four has negative cash under B=0 -> 1/4=0.25.
NOTE: legacy insolvency_triggered combines reserve and spend-target conditions; do not claim equivalence.

### M-VAR: loss value at risk
1. Formula VaR_alpha(L)=inf{x : F_L(x)>=alpha}, with signed loss L=-P or separately labeled nonnegative shortfall.
2. Numerator: alpha quantile of complete trial losses; denominator: trial distribution M.
3. Unit: CUR loss.
4. Horizon: profit/loss through H for each trial.
5. Scope: trial distribution; not one deterministic run.
6. Aggregation: empirical nearest-rank sorted loss at ceil(alpha*M); do not substitute interpolated percentiles without labeling.
7. Zero: M=0 or alpha outside (0,1) -> undefined.
8. Missing: incomplete selected trial loss -> invalid.
9. Sign: positive loss; negative gain when using L=-P.
10. Example: sorted losses [0,0,10,30] CUR, alpha=0.75 -> VaR=10 CUR.

### M-CVAR: conditional value at risk / expected shortfall
1. Formula CVaR_alpha(L)=(1/(1-alpha))*integral from alpha to 1 of inverse-CDF quantile Q_L(u) du.
2. Numerator: integrated upper-tail loss; denominator: tail mass 1-alpha.
3. Unit: CUR loss.
4. Horizon: same H and loss definition as VaR.
5. Scope: complete trial-loss distribution.
6. Aggregation: empirical sorted tail with fractional boundary weight if needed; mean(L >= VaR) is wrong for ties.
7. Zero: M=0 or alpha outside (0,1) -> undefined.
8. Missing: incomplete trial set -> invalid; report exclusions.
9. Sign: loss-positive; CVaR >= VaR under the same loss.
10. Example: [0,0,10,30] CUR, alpha=0.75 -> CVaR=30 CUR; [0,0,0,100] -> VaR=0, CVaR=100 (not naïve 25).

## Existing engine compatibility evidence

| Dimension | WorldExecutor / EventMachine | Legacy SimulationEngine / telemetry |
| --- | --- | --- |
| Execution unit | World definition, one event calendar and seeded run | StrategyAST, multiple trials, tensor of count positions per trial |
| State | Typed mapping per named owner | StateCode integer array plus psychographic arrays and campaign cash |
| Events | Timed priority/ordinal calendar, local emissions | Day iteration, StrategyAST logic_flow, array slices |
| RNG | One random.Random(seed) across all event handlers | One np.random.default_rng(seed+trial_index) per trial; vector draw order dependent |
| Population | One state per declaration name, no stable per-ID population API | agents_count sizes array; no stable named-agent trace API |
| Segments | Declaration/import alias, not a segment enrollment system | First audience only, entities.audiences[0] |
| Metrics | Typed state fields only, no automatic risk/campaign aggregation | TrialResult/TelemetryAggregator; zero-spend ROAS=0, zero-conversion CAC=inf before filtering |
| Accounting | Single-lead revenue/spend, no cash or receivable scheduling | Liquid cash and settlement buffer; reported profit excludes some fees/costs |
| Termination | until, max_events, pending events; no terminal-population tally | timeframe_days, optional day snapshots and StateCode |
| Replay | Version/source/seed/ordered event inputs | AST/count/trial seed offset/NumPy/config; no keyed per-agent substreams |

Option A (Proposed future): World-backed population runner and narrow compatibility adapter, after independently specified identity, keyed streams, event routing, cash ledger and versioned metric mapping. There is no current defensible one-to-one legacy equivalence.
Option B (defensible current boundary): keep two engines separate with explicit non-equivalence, preserving accepted World RNG semantics and legacy engine. **Recommend B for present operation; A remains Proposed, not Accepted.** This requires a reviewed future design decision; no ADR is created or declared accepted in Phase 007.

## STOP, fixtures and scientific claims

Planned bounded experimental scales are two segments at N=10,100,1000 with stable ID partitions, multiple trials and delayed cash. They were **not run as a population experiment** because H-POP2 cannot be demonstrated through present public APIs. Do not manufacture a third simulator in tests; do not claim performance, population conservation, independent Monte Carlo, or paired counterfactual reproducibility. Fixture P-RNG-ORDER-1, described above, is the smallest publicly reproducible order-dependence witness, not a true population execution. A failing desired-invariant probe is evidence of the gap and not a newly discovered regression of accepted semantics. Future implementation must have a separately approved and test-first card before unblocking Phase 007.

**External market validity, statistical calibration, causal inference, and real-world prediction accuracy were not tested.**


---

## Phase 007A verified dependency update (2026-11-01; historical Phase 007 BLOCKED status retained)

The separately proposed `spec/population-identity-rng-v0.md` contract has an opt-in independent-instance Python execution adapter with an exact identity snapshot and versioned per-agent/trial/role seed derivation. Its 10/100/1000-agent experimental results and 36 focused tests are recorded in `evals/population-identity-rng-v0.md`. This closes only the earlier **absence of a stable population identity and keyed RNG runtime capability** for causally independent instances. It does NOT revise accepted default World RNG semantics or retroactively turn the P-RNG-ORDER-1 counterexample into a regression. H-POP3 delayed cash settlement and the executable financial/metric contract remain unverified; Phase 007 is still BLOCKED. No market validity, statistical calibration, causal inference, or prediction accuracy was tested.
