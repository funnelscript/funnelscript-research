# Typed World Guards v0: Conditional Rule Execution

Status: Experimental research gate and implementation contract, 2026-10-31. Extends DEC-027 (snapshot-atomic World rules) and DEC-028 (local scheduled source events). Intended ADR: DEC-029.

## Research anchors

1. C. A. R. Hoare, *An Axiomatic Basis for Computer Programming*, Communications of the ACM 12(10), 1969, https://doi.org/10.1145/363235.363259 . Guarded state transformations can be reasoned about using preconditions and postconditions.
2. Gordon D. Plotkin, *A Structural Approach to Operational Semantics*, Technical Report, 1981, https://www.cs.cmu.edu/~crary/819-f09/Plotkin81.pdf . Rule selection and execution are defined through explicit small-step semantics.
3. Existing project contracts: `spec/rule-transitions-v0.md` and `spec/event-emission-v0.md`. Guard checks must read the same pre-event state and must not install a second scheduler.

## Proposed language subset

```funnelscript
world BoundedFlow {
  agent Counter {
    state value: int = 0;
    rule Advance on event Tick when (value < 3) {
      transition value = value + 1;
      emit Tick after 1;
    }
  }
}
```

A World rule may optionally add `when (state OP literal)` between its event name and opening brace. The primitive comparison operators are `==`, `!=`, `<`, `<=`, `>`, `>=`. Only a state field of the same entity/agent may be referenced. The literal must have exactly the same declared primitive type (`int`, `float`, `bool`, or `string`); no coercion. Ordering operators are legal only for `int` and `float`, while equality and inequality also support booleans and strings.

There is only one comparison per rule. Boolean connectives, function calls, state-to-state comparisons, stochastic operators, string ordering, property traversal, and cross-owner reads are deferred. `when` remains a keyword already used by the legacy strategy grammar; no new hard marketing concepts are added.

## Semantics and invariants

Let `S_before` be the owner state immediately before processing event `e`; let `g(S_before)` be the compiled guard evaluated without executing source text as Python code.

- When no guard exists, `g(S_before) = true` for compatibility.
- If `g(S_before) = false`, the event is consumed by the calendar, but `S_after = S_before`, no transition RHS runs, and `emitted(e) = ∅`.
- If `g(S_before) = true`, all transition RHS values are evaluated against `S_before`, updates apply simultaneously, and local emitted events are scheduled using the existing event kernel.
- Guard evaluation never performs effects. It does not change event priority or calendar ordering.

For every compiled guard `(field op literal)`:

1. `field ∈ owner.states`.
2. `type(field) = type(literal)`, exact primitive identity, including `bool ≠ int`.
3. If `op ∈ {<, <=, >, >=}`, then `type(field) ∈ {int,float}`.
4. A false guard never modifies state and never produces `Transition.events`, even if the rule body contains `transition` and `emit`.

## Falsifiable hypotheses

**H-G1 (type safety):** A valid guard parses into the typed AST; unknown state fields, mismatched literal types, invalid operators or unsupported expressions fail before runtime. Counterexample: invalid source executes.

**H-G2 (false branch):** When `value=3`, `when (value < 3)` consumes the event without modifying state or scheduling further events. Counterexample: any transition or emitted event occurs.

**H-G3 (true branch and bounded chain):** Starting from `value=0`, one `Tick@0` produces transitions to 1, 2, and 3 and then halts after the fourth `Tick` fails the guard. Counterexample: infinite loop, wrong state, or source-order mutation of the guard snapshot.

**H-G4 (compatibility and purity):** Unguarded rules, legacy strategies and the event-kernel tests continue to pass; no source guard calls Python `eval` or a Live provider. Counterexample: a regression or external effect.

## Non-goals

Probabilistic branch sampling, composite predicates, time-dependent expressions, business-specific guards, monetary invariants, and empirical validation of marketing outcomes. This gate is a typed interpreter milestone, not a predictive market result.

## Evaluation

Implementation: `funnelscript/src/funnelscript/compiler/world_ast.py`, `parser.py`, `tokens.py`, `runtime/world_executor.py`. TDD: `funnelscript/tests/test_world_guards.py`. Evidence: `evals/world-guards-v0.md`.
