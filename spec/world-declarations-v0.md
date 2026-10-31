# World Declarations v0: Entity, Agent, and Typed State

Status: Experimental, additive language-core syntax. Date: 2026-10-31. Derived from DEC-008, DEC-009, DEC-010, and the event-kernel contract. No marketing or country-specific schema is built into these declarations.

## Research anchors

- Luca Cardelli and Peter Wegner, "On Understanding Types, Data Abstraction, and Polymorphism," ACM Computing Surveys 17(4), 1985. Bell Labs publication: https://www.nokia.com/bell-labs/publications-and-media/publications/on-understanding-types-data-abstraction-and-polymorphism/ . Subtyping distinguishes substitutability from a particular application domain.
- Benjamin C. Pierce, *Types and Programming Languages*, MIT Press, 2002. https://mitpress.mit.edu/9780262162098/types-and-programming-languages/ . Type checking is a syntactic judgment over terms and type environments, not evidence of real-world predictive validity.
- Pydantic v2 documentation, discriminated unions. https://pydantic.dev/docs/validation/latest/concepts/unions/ . Explicit `kind` discriminators preserve typed AST identity in the Python reference compiler.

This is a small first-order declaration checker, not a proof of general type soundness, an implementation of System F, or a complete language semantics.

## Source syntax

```funnelscript
world Warehouse {
  entity Shelf {
    state quantity: int = 20;
    state label: string = "A";
  }
  agent Picker {
    state active: bool = true;
    state confidence: float = 0.75;
    state offset: int = -2;
  }
}
```

Declarations live at the top level inside `world`. The words `world`, `entity`, `agent`, and `state` are contextual (soft) keywords, preserving their use as identifiers in legacy strategy metadata. An `agent` is a nominal subtype of `entity` in the AST, but autonomy/decision rules and actual runtime construction are outside this milestone. State declarations have explicit primitive type names `int`, `float`, `bool`, or `string`, treated as identifiers by the lexer so a future type registry can extend them. Literals must match their declared type exactly; `bool` is not an `int`, and `int` is not implicitly converted to `float`.

The existing `strategy` source format, campaign-specific JSON AST, linter, and simulation engine remain unchanged. A `world` is currently accepted for static checking only. Trying to simulate this new AST through the legacy marketing engine must return a clear unsupported-mode error, not run marketing assumptions or external effects.

## Falsifiable hypotheses

**H-W1 (Domain-neutral parsing):** A valid `world` with arbitrary `entity`, `agent`, and `state` names parses to a typed AST without referring to `Audience`, `Campaign`, or `Touchpoint`. Refuted by forced marketing fields or incorrect AST class identity.

**H-W2 (Primitive typing and uniqueness):** A declaration is accepted exactly when each state's initializer matches its explicit primitive type, each declared type is recognized, world-level entity/agent names are unique, and state names within a declaration are unique. Refuted by any accepted mismatch/duplicate or rejection of a valid negative number.

**H-W3 (Subtype identity):** Every parsed agent definition is an instance of the entity definition type, but a plain entity is not an agent definition. Refuted by wrong runtime AST class relationships.

**H-W4 (Compatibility and boundary):** All existing strategy tests continue to pass. A `world` file passes CLI `check`, while `simulate` rejects it without invoking the existing campaign engine. Refuted by a regression or unintended simulation attempt.

## Formal invariants

For world declaration set `D`, state fields `F_d`, initializer `v_f`, and declared type `T_f`:

1. `∀d_i,d_j∈D: i ≠ j ⇒ name(d_i) ≠ name(d_j)`.
2. `∀f_i,f_j∈F_d: i ≠ j ⇒ name(f_i) ≠ name(f_j)`.
3. `Γ ⊢ v_f : T_f ⇔ literal_type(v_f) = T_f`, with `T_f∈{int,float,bool,string}` for v0.
4. `AgentDefinition <: EntityDefinition` in the reference AST, with no claim that a state-only agent can act autonomously yet.
5. The legacy strategy AST and simulator are not coerced into or from a `WorldAST` implicitly.

## Implementation and evaluation mapping

- `funnelscript/src/funnelscript/compiler/world_ast.py`: typed declaration AST and checker.
- `funnelscript/src/funnelscript/tokens.py`: world/entity/agent/state delimiters and signed numeric literal.
- `funnelscript/src/funnelscript/parser.py`: explicit `world` parse path with end-of-input checks.
- `funnelscript/src/funnelscript/cli.py`: separate CLI check and unsupported-simulation path.
- `funnelscript/tests/test_world_language.py`: H-W1 through H-W4 positive, negative, boundary, and CLI tests.
- `funnelscript-research/evals/world-declarations-v0.md`: reproducible falsification commands.

## Deferred

User-defined types, typed methods, rules and transitions in source syntax, modules/imports, Marketing Standard Library, static effects, world execution, population modeling, PyMC calibration, and Live/Shadow handlers. This milestone must not be marketed as a full language interpreter or a validated market twin.
