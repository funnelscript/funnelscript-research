# Typed World Event Payloads v0: Source-Level Message Contracts

Status: Research-first implementation proposal, 2026-10-31. Extends DEC-027, DEC-028 and DEC-029. Proposed decision: DEC-030.

## Primary research anchors

1. Luca Cardelli and Peter Wegner, *On Understanding Types, Data Abstraction, and Polymorphism*, ACM Computing Surveys 17(4), 1985. https://www.nokia.com/bell-labs/publications-and-media/publications/on-understanding-types-data-abstraction-and-polymorphism/ . Source-level schemas establish static field/type contracts; exact primitives in this subset deliberately do not assume an unimplemented subtype relation.
2. Gordon D. Plotkin, *A Structural Approach to Operational Semantics*, Aarhus University Technical Report, 1981. https://www.cs.cmu.edu/~crary/819-f09/Plotkin81.pdf . The handler's event record and pre-event state jointly define each transition.
3. Existing project contracts: `spec/event-kernel-v0.md`, `spec/rule-transitions-v0.md`, `spec/event-emission-v0.md` and `spec/world-guards-v0.md`. The event kernel already stores model-owned opaque payload values; World source must supply explicit typing without changing general-purpose kernel behavior.

## Deliberately small source contract

```funnelscript
world Ledger {
  entity Wallet {
    state balance: int = 0;
    event Credit(amount: int);

    rule Receive on event Credit {
      transition balance = balance + payload.amount;
    }
    rule Seed on event Start {
      emit Credit(amount = 4) after 2;
    }
  }
}
```

A World entity or agent may declare `event Name(field: PrimitiveType, ...);` with zero or more fields. Event and field names must be unique per owner, and primitive types are exactly `int`, `float`, `bool`, `string`. Event names are contextual. An event handler with no explicit declaration retains its historical no-payload contract; old source and `OWNER.EVENT@TIME` CLI input remain valid.

`payload.field` is an explicit read-only event value reference usable as a transition value or as the right operand of an existing state-reference numeric +/- expression. Payload references must be resolved against the currently handled event schema at compile time. No name capture between owner state and event fields is permitted.

`emit Name(field = Expr, ...) after Delay;` supplies all and only the fields declared for its local target event, with exactly matching expression types. The existing `emit Name after Delay;` form remains legal for zero-field events. Every emitted event still requires a same-owner handler and runs through the existing calendar.

The `run-world` CLI accepts repeatable `--event` items in their supplied order, either legacy `OWNER.EVENT@TIME` or a JSON object such as `{"name":"Wallet.Credit","time":0,"payload":{"amount":5}}`. This JSON is an input serialization, not language source. Duplicate keys in JSON event objects or nested payloads are rejected before they can silently overwrite earlier values. No `eval`, external effects, implicit coercion or Python object construction from user strings is allowed.

## Operational semantics and mathematical invariants

For an input event `e=(t,owner.name,p)`, let `Schema(owner,name)` be a finite mapping of field names to primitive types, or the empty mapping for an implicit legacy event.

1. **Exact shape:** `keys(p) = keys(Schema(owner,name))`, with string keys only and `None` as an empty record only when the schema is empty. Extra, missing or non-string fields cause an explicit WorldExecutionError; `type(p[k]) = Schema[k]` with no implicit promotion (`bool ≠ int`). Float payload values must be finite (`isfinite(p[k])`).
2. **Static field validity:** every `payload.f` in handler `r` requires `f ∈ Schema(owner,r.event)`; its static type is the declaration's type. Every source-emitted argument must resolve, have a unique field name, and match the target event's schema exactly.
3. **Read-only message semantics:** all transitions and emissions within one handler evaluate against the same `S_before` and the same input record `p`. No statement mutates incoming payload or the prior state. False guards still enforce payload shape before skipping the body.
4. **Temporal invariants:** `t_emit = t_input + d ≥ t_input` with finite, nonnegative `d`, inherited priority and existing stable FIFO tie rules; no secondary scheduler. Generated records pass the same runtime validation **before they are inserted into the pending calendar**, so a finite event horizon cannot hide an invalid future payload.
5. **Effect isolation:** World payload processing creates only in-memory `Event` data and `Transition` values, never a provider call or Live operation.

## Falsifiable hypotheses

- **H-P1, typed source:** Event declarations, payload field expressions and named emission arguments parse into typed nodes; duplicates, unknown fields and mixed primitive types are rejected before execution. Counterexample: a source with `payload.missing` checks successfully.
- **H-P2, exact inbound boundary:** A schema-matching event updates state; missing/extra/wrongly typed or unstructured input is rejected before any transitions, even when the guard is false. Counterexample: `bool` passes as `int` or a malformed record is silently ignored.
- **H-P3, causal outbound path:** Emitted payloads carry values evaluated against the source handler's pre-event state, reach the receiver at the correct scheduled time, and preserve equal-time ordering. Counterexample: a later mutation changes a prior event's payload or timing.
- **H-P4, compatibility and safety:** Existing empty-payload World scripts and legacy campaigns pass unchanged, with no dynamic execution or external API effects. Invalid CLI event strings do not echo user-supplied data to stderr, and duplicate JSON object keys are rejected rather than resolved by last-write-wins. Counterexample: previously working World dispatch changes without payload declarations, or an invalid input is printed in diagnostics.

## Exclusions and next research gates

Nested records, arrays, union types, inheritance, optional/default fields, payload-driven guards, variable-length arguments, cross-owner addressing, persistent delivery, distributed serialization, stochastic draws and Live/Shadow effects are excluded. Strict runtime checks do not prove market-model accuracy or causal identification.

## Test routing

Implement in `funnelscript/src/funnelscript/compiler/world_ast.py`, `parser.py`, `tokens.py`, `runtime/world_executor.py`, `cli.py`. Falsify with `funnelscript/tests/test_world_payloads.py` and full regression suites. Evidence to be recorded in `evals/typed-event-payloads-v0.md` after RED/GREEN execution.