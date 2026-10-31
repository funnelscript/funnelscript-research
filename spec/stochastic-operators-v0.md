# Source-Level Stochastic Operators v0: Reproducible World Draws

Status: Pre-implementation research contract, 2026-10-31. Extends DEC-019 and DEC-027 through DEC-030. Proposed DEC-031.

## Research anchors

1. Python Software Foundation, *random — Generate pseudo-random numbers*, Python 3 documentation: https://docs.python.org/3/library/random.html#notes-on-reproducibility . A seeded `random.Random` has reproducible `random()` output under the compatible seeder; higher-level distribution algorithms may evolve between interpreter versions.
2. Python Software Foundation, *math.isfinite*, https://docs.python.org/3/library/math.html#math.isfinite . Explicitly reject NaN and infinity before consuming random state.
3. Project's `spec/event-kernel-v0.md` and `spec/rule-transitions-v0.md`. The existing event calendar already supplies one isolated RNG per run, stable event ordering, and snapshot-atomic state updates. No second scheduler is justified.
4. Jerry Banks et al., *Discrete-Event System Simulation* (5th ed., Pearson, 2010), random-variate generation and reproducible replication. This is a discrete-event engineering anchor, not validation of a behavioral probability estimate.

## Syntax and typing

The v0 expression is only valid as the right-hand side of `transition` within a World rule:

```funnelscript
world Experiment {
  agent Visitor {
    state conversion_probability: float = 0.25;
    state converted: bool = false;
    state offer_score: float = 0.0;
    event Impression(probability: float);
    rule Respond on event Impression {
      transition converted = sample bernoulli(payload.probability);
      transition offer_score = sample uniform(0.0, 1.0);
    }
  }
}
```

- `sample bernoulli(p)` returns exactly `bool` and `sample uniform(low, high)` returns exactly `float`.
- Parameters are **single-value** primitive expressions: explicit float literal, a same-owner float state field, or a declared float `payload.field`. No arithmetic, function nesting, implicit int-to-float promotion, arbitrary calls, probability defaults, or other distributions.
- Literal parameters are statically validated; dynamic parameters are validated at runtime *before* drawing. Bernoulli requires finite `0 <= p <= 1`; Uniform requires finite `low <= high` and finite representable `high - low`. Equal bounds are allowed and still consume one draw.
- No sampling in initializers, guards, event emission arguments, or delays. Emissions may follow a stochastic transition and still see the pre-event state; they do not sample.
- `sample`, `bernoulli`, `uniform` are contextual identifiers, not globally reserved tokens.

## Operational and mathematical invariants

Let `U = rng.random()` where `0 <= U < 1`. For a rule that passed its guard:

1. Bernoulli `B(p; U) = (U < p)`. For `p=0`, false; for `p=1`, true. No probabilistic assertion is needed to verify these endpoints.
2. Uniform `X(a,b;U) = a + (b-a)U`, using one draw, with `a <= b`; finite arithmetic is required. The resulting value lies within the representable closed interval `[a,b]`, allowing rounding at the upper endpoint. For `a=b`, `X=a`.
3. One `random()` draw per evaluated `sample`, including degenerate parameters. No draw occurs on a false guard, an unknown event, invalid input record, or an invalid distribution parameter. Draws run in the textual order of transition assignments, independent of scheduling and source ordering of emission statements.
4. All assignments in a handler still read `S_before` and `payload_before`. The rule computes its draws and new state in one reducer step; the previous state mapping and payload are not modified.
5. For fixed parser/compiler/runtime versions, seed, World source, initial state, and ordered event inputs, `run(seed=s)` yields equal `RunResult` on replay. Different seeds need *not* yield distinct outcomes. No cross-Python-version promise is made beyond the documented `random()` sequence compatibility.
6. A direct single-event `advance(state,event)` remains supported for deterministic rules. If the matched rule attempts to sample, its caller must supply an explicit `rng` object; there must not be an implicit OS-seeded generator.

## Falsifiable hypotheses

- **H-S1, source typing:** Both operators parse as typed AST nodes; wrong arity, unknown distribution, non-float parameter, wrong transition result type, and out-of-range static parameters are rejected. Counterexample: `sample bernoulli(2.0)` checks.
- **H-S2, exact draws:** Fixed seed, sequence, and source produce identical replay; each active sample consumes exactly one next `random()` from the event kernel, in transition order. Counterexample: sampled results differ across otherwise identical runs or switching a guard to false shifts later draws.
- **H-S3, boundary rejection:** Dynamic invalid probabilities/bounds and nonfinite values fail before advancing RNG or committing state. Counterexample: a dynamic `p=1.5` returns a boolean.
- **H-S4, behavioral separation:** No stochastic behavior enters ordinary World expressions, non-stochastic event chains, and legacy campaign paths; no empirical market prediction or Live effects are implied. Counterexample: deterministic regression or packaged CLI changes without using `sample`.

## Exclusions and next research gates

This is one seeded pseudorandom stream per World run, *not* independent per-agent streams, a calibration pipeline, counterfactual causal inference, or a validated digital twin. Changing event schedules can change downstream random draws. Distribution-fitting, common random numbers with stable identity, Gaussian/Beta distributions, and stochastic source emission require separate design, correlation semantics and tests.

## Evaluation routing

Write RED tests in `funnelscript/tests/test_world_stochastic.py`; implement only in existing `world_ast.py`, `parser.py`, and `runtime/world_executor.py`; verify against existing `EventMachine` (no new RNG). Record observed evidence in `evals/stochastic-operators-v0.md`.
