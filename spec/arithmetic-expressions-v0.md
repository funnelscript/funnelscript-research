# Narrow World Arithmetic and EOF Safety v0

Status: Phase 003 language contract (2026-11-01); implementation and falsification tracked in `evals/arithmetic-expressions-v0.md`.

## Research anchors and compatibility

Plotkin, *A Structural Approach to Operational Semantics* (1981), motivates explicit, inspectable expression evaluation and transition rules rather than host-language dynamic evaluation. Cardelli and Wegner, *On Understanding Types, Data Abstraction, and Polymorphism* (1985), motivates exact primitive types without implicit widening. The event-ordered, pre-event state semantics remain those of `spec/rule-transitions-v0.md` (DEC-027), and seeded sampling remains governed by DEC-031. These references motivate a design; they do not empirically validate marketing behavior.

DEC-027's original reference-plus/minus-literal restriction and the subsequently accepted typed payload references are historical v0 stages. This additive extension supersedes **only** that narrow expression syntax, not the snapshot, event, or type invariants; record it as DEC-037. No marketing-specific arithmetic axioms enter the World core.

## Falsifiable hypotheses

- **H-AR1 — Parser EOF Safety.** Parsing `[]`, exhausted token lists, empty source and truncated World expressions produces a stable `ParserError`, not `IndexError` or an unbounded parse loop. Falsifier: any empty/exhausted input causes an indexing error or silent success.
- **H-AR2 — Typed Arithmetic Correctness.** A single binary World expression passes lexer, parser, AST, checker and runtime with a result of its declared type; mismatched exact numeric types, bool/string operands, unknown references, operator chains and unsupported parentheses fail before execution. Falsifier: any accepted expression evaluates to a different primitive type or requires implicit conversion.
- **H-AR3 — Division and Comment Safety.** A zero literal divisor is a compile-time error; a zero divisor resolved from a state or payload is a controlled `WorldExecutionError` before state mutation. Source `//` retains its comment meaning. Falsifier: unchecked zero, accidental `ZeroDivisionError`, or any `//` tokenized as division.

## Syntax and typing

`StateExpression ::= StateLiteral | PayloadReference | Identifier [BinaryOperator BinaryRight] | SampleExpression` (the sampling alternative is restricted to transitions and is not a binary operand). `BinaryOperator ::= "+" | "-" | "*" | "/"` and `BinaryRight ::= StateLiteral | PayloadReference | Identifier`. A binary left operand is necessarily a **same-owner state reference**. A binary right operand is one primitive literal, a declared payload field or a same-owner state reference. Bare payload references, literals and state references retain their existing expression roles. Expressions have exactly zero or one binary operator: no chains, operator precedence, parentheses, function calls, unary plus or binary sample operands. Negative signed numeric right literals remain accepted; division `/` requires separation from the lexer's `//` comment introducer.

Given state typing context Γ, payload schema Π, and τ in {int, float}:

- Γ ⊢ left : τ and (Γ,Π) ⊢ right : τ imply `(left + right) : τ`, `(left - right) : τ`, `(left * right) : τ`.
- Γ ⊢ left : τ and (Γ,Π) ⊢ right : τ imply `(left / right) : float`, provided right is not a literal zero.
- No judgment exists for mixed int/float, bool, string or an undeclared reference. `bool` is never numeric even though Python subclasses `int`.
- Target and emitted event field assignments require the **exact** resulting primitive type. Therefore `state ratio: float = 0.0; transition ratio = count / divisor;` accepts int/int, while assignment of that result to an `int` fails checking.

Valid examples with consistent types: `transition revenue = revenue * payload.multiplier;` where both fields are float; `transition ratio = spend / clicks;` where spend and clicks are both float and ratio is float. For integer counts: `transition ratio = units / total;` with int units/total and float ratio. These examples do not silently coerce integer counts to float for marketing prices.

## Value and failure boundaries

`+`, `-` and `*` use the host's exact integer arithmetic or binary64 floating-point semantics; integers have no arbitrary numeric clamp. `/` is real division returning a Python float (including exact int/int inputs), not floor division. Float operands, float literal values and produced float results must be finite. Literal float non-finiteness is rejected at compilation; dynamic non-finite inputs and any non-finite outputs or float-conversion overflow are rejected by the runtime with `WorldExecutionError`. A representable float result of zero from underflow is allowed, whereas infinity or NaN is not. Signed integer/float `0` or `-0.0` as the **literal** right operand of `/` is a type-checking error; a dynamic zero (including negative zero) is a runtime error. If any expression fails during rule evaluation, its copy-on-write update is not committed. Initial state exact-type checking remains unchanged: an externally constructed non-finite initial float is still permitted for backward compatibility, but arithmetic consumption of it fails with `WorldExecutionError`; emission of it as a typed payload continues to fail on outbound record validation. Pre-event snapshot and seeded RNG consumption order are unchanged.

## Out of scope

Recursive expression trees, associativity, implicit casts, automatic financial unit conversions, arbitrary function evaluation, new sample arguments, cross-owner fields, nonfinite policies for unrelated legacy StrategyAST operations, and claims of observed market validity.
