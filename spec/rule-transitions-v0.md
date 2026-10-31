# Rule and Transition Semantics v0: Executable World State

Status: Experimental language-core behavior contract (2026-10-31). Extends DEC-012 (event-driven computation), DEC-019 (inert event kernel), and DEC-022 (typed World declarations), without invoking legacy marketing semantics. Recorded as DEC-027.

## Research anchors

1. Gordon D. Plotkin, *A Structural Approach to Operational Semantics*, University of Aarhus Technical Report, 1981. Original manuscript mirror: https://www.cs.cmu.edu/~crary/819-f09/Plotkin81.pdf . We use explicit small-step state-update rules, not Python `eval`.
2. Bernard P. Zeigler, *DEVS Representation of Dynamical Systems: Event-Based Intelligent Control*, NASA Technical Reports Server, 1989. https://ntrs.nasa.gov/citations/19890044726 . Input events drive state transitions on an ordered calendar.
3. Cardelli and Wegner, *On Understanding Types, Data Abstraction, and Polymorphism*, ACM Computing Surveys, 1985. https://www.nokia.com/bell-labs/publications-and-media/publications/on-understanding-types-data-abstraction-and-polymorphism/ . Typed state and subtype identity are independent of marketing objects.

This contract is a deliberately narrow operational subset, not a full expression language, complete DEVS implementation, distributed transaction system, or predictive market model.

## Source-level example

```funnelscript
world CounterDemo {
  entity Counter {
    state count: int = 0;
    state active: bool = true;

    rule Increment on event Pulse {
      transition count = count + 1;
      transition active = true;
    }

    rule Reset on event Clear {
      transition count = 0;
    }
  }
}
```

The lexer treats `rule`, `on`, `event`, and `transition` as contextual identifiers; it introduces only the `+` token. An entity or agent may define zero or more named rules. The v0 expression grammar accepts primitive literals, references to a state field in the same declaration, and a numeric field reference plus/minus a numeric literal. There is no dynamic code evaluation, function call, property traversal, network access, effect dispatch, or source-level event emission.

An input event is addressed as `<declaration>.<event>`, e.g. `Counter.Pulse`. The runtime requires an exactly matching handler. Unknown addresses fail explicitly. Events are externally supplied to the existing `EventMachine` with timestamps, rather than generated from a prebuilt World template.

## Execution semantics

Let `S` be the immutable-in-observation mapping `owner -> field -> value`. For event `e` addressed to owner `a`, select the unique rule `r`. For each assignment `x_i := expr_i`, compute `v_i = eval(expr_i, S[a])` against the same pre-event snapshot. Produce `S' = S[a <- S[a] union {x_i -> v_i}]` only after every assignment has passed static typing and runtime evaluation. This establishes simultaneous-assignment semantics, regardless of transition statement order. Existing previous result states must remain unchanged (copy-on-write for the addressed declaration).

Arithmetic `+` and `-` is defined only for `int` with `int` or `float` with `float`. No implicit numeric promotion; `bool` does not behave as `int`. There is no string concatenation in v0. A rule cannot assign the same target twice. Names of rules and their listened-to events are unique per declaration. No rule may mutate another declaration's state in v0.

## Falsifiable hypotheses

**H-R1 (Parse and type):** Valid source with `rule ... on event ...` yields typed rule/transition AST, while unknown targets/sources, wrong operands, duplicate handlers/targets, or invalid syntax are rejected before runtime. Counterexample: any malformed rule parses and executes.

**H-R2 (Snapshot semantics):** Given `a=1,b=2`, assignments `a=b; b=a;` produce `a=2,b=1` after one event, and the initial mapping remains unchanged. Counterexample: sequential mutation yields `a=2,b=2`, or original state is mutated.

**H-R3 (Event-machine integration):** For a supplied sequence of qualified events, the World runner uses the event kernel's chronological order and seed; a repeated run produces the same final state and trace. Unknown events cause a controlled error. Counterexample: source statement order dictates time order, replay differs, or unsupported events silently succeed.

**H-R4 (Safe CLI boundary and compatibility):** `run-world` executes the new source semantics without calling the legacy campaign simulator or external providers. All existing strategy and EventMachine tests stay green. Counterexample: direct platform I/O, a campaign regression, or accidental fallback to marketing assumptions.

## Invariants

1. Unique `(owner, rule_name)` and `(owner, event_name)` keys.
2. For every transition `x := expr`, `x in fields(owner)` and `typeof(expr) = typeof(x)`; binary operands use identical numeric types.
3. For a valid rule with assignments `A`, `S'|_{dom(A)} = eval(A, S_before)` and `S'|_{outside dom(A)} = S_before`.
4. The `EventMachine` controls time ordering, seed, maximum processed events, and retrograde-event rejection; no second scheduler is introduced.
5. No source-language construct can emit `EffectIntent` or invoke a Live provider in this milestone.

## Implementation and evaluation

- `funnelscript/src/funnelscript/compiler/world_ast.py`: typed expression, transition, and rule nodes and checking.
- `funnelscript/src/funnelscript/parser.py`: contextual rule parser and expression parser.
- `funnelscript/src/funnelscript/runtime/world_executor.py`: interpreter adapter that lowers rules to `EventMachine` reducers.
- `funnelscript/src/funnelscript/cli.py`: explicit `run-world` command with input events.
- `funnelscript/tests/test_world_rules.py`: RED/GREEN and negative tests.
- `funnelscript-research/evals/world-rules-v0.md`: falsification manifest.

## Deferred

Automatic agent decisions, event emission by source code, cross-entity effects, conditionals, stochastic primitive expressions, real-market calibration, source-level user-defined functions, and any Live/Shadow handler. This does not establish predictive validity or sandbox arbitrary Python callbacks outside the source-language interpreter.
