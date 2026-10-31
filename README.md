# FunnelScript Research

> Formal specification, theoretical foundations, mathematical proofs, and scientific research paper for **FunnelScript** — the Declarative Domain-Specific Language (DSL) and Stochastic Agent-Based Simulation Runtime for Marketing Systems Engineering.

## Repository Structure

```
.
├── paper/
│   ├── README.md              # Full academic research paper (Markdown format)
│   ├── funnelscript.tex       # IEEE/ACM LaTeX manuscript source
│   └── references.bib         # Academic citations and foundational bibliography
├── notebooks/
│   ├── executive_engineering_notebook.md   # Executive engineering playbook & visual architecture
│   └── executive_engineering_notebook.ipynb # Interactive runnable simulation & invariant verification
├── spec/
│   ├── event-kernel-v0.md     # Language-neutral DEVS event kernel specification
│   ├── grammar.ebnf           # Complete, closed EBNF grammar specification
│   └── schema.json            # AST JSON Schema specification
└── evals/
    └── event-kernel-v0.md     # Falsification plan and hypothesis mapping (H-K1 to H-K4)
```

## Key Theoretical Contributions

1. **Finite State Automaton Customer Model ($M$):** Formal stochastic state transitions across `COLD`, `AWARE`, `CONSIDERING`, `CART_ABANDONED`, `CONVERTED`, and `CHURNED`.
2. **Multi-Scale Discrete-Event $\tau$-Calendar:** Eliminates temporal race conditions across micro-second ad clicks, hourly abandonment, and daily payout schedules.
3. **Working Capital Dynamics & Cash Ruin Probability $P(\text{Insolvency})$:** Mathematical proof that high-ROAS marketing strategies face catastrophic failure without accounting for settlement latency ($\Delta_{\text{settle}}$).
4. **Behavioral Cannibalization Detection:** Dynamic agent-based proof of margin erosion caused by automated cart abandonment incentives.

## Experimental Domain-Neutral Kernel Contract

[Event Kernel v0](spec/event-kernel-v0.md) defines the bounded discrete-event scheduling, seeded replay, model-owned transitions, and inert effect-intent hypotheses (H-K1 to H-K4). It is an executable semantic foundation for the language, **not** a market prediction or authorization to invoke live platform APIs.

## Executive Engineering Playbook & Interactive Notebook

* **Playbook:** [`notebooks/executive_engineering_notebook.md`](notebooks/executive_engineering_notebook.md) — Comprehensive architecture playbook, Bayesian prior injection mechanics, 5-subsystem breakdown, and cross-industry language intersections (Terraform, Julia, Solidity).
* **Interactive Notebook:** [`notebooks/executive_engineering_notebook.ipynb`](notebooks/executive_engineering_notebook.ipynb) — Executable Jupyter notebook simulating $100,000$ agents, Hill equation saturation kinetics, and mass conservation invariants.

## Experimental Typed World Declarations

[World Declarations v0](spec/world-declarations-v0.md) defines context-sensitive `world`, `entity`, `agent`, and `state` declarations, with an explicit primitive type checker and backward compatibility gates.

## Experimental Rule and Transition Semantics

[Rule Transitions v0](spec/rule-transitions-v0.md) and [Falsification Evaluation](evals/world-rules-v0.md) define the small-step operational semantics where input events drive simultaneous state transitions across entities and agents on the discrete-event calendar substrate (`funnelscript run-world`).

## Experimental Scheduled Source Events

[Event Emission v0](spec/event-emission-v0.md) and its [falsification tests](evals/event-emission-v0.md) specify `emit Event after Delay;`, local handler resolution, deterministic discrete-event scheduling and bounded zero-delay recursion. This is a pure interpreter mechanism and is not evidence of autonomous market agents or out-of-sample predictive validity.

## Experimental Typed World Guards

[Typed Guard Semantics v0](spec/world-guards-v0.md) and [Falsification Evaluation](evals/world-guards-v0.md) define `when (field OP literal)` predicates on pre-event state with strictly typed comparisons. False guards suppress both assignments and local events; deterministic interpreter tests do not validate market predictions.

## Experimental Typed Event Payloads

[Typed Event Payloads v0](spec/typed-event-payloads-v0.md) and [Falsification Evaluation](evals/typed-event-payloads-v0.md) specify source-level event field schemas, typed input JSON records, named local emission arguments and read-only `payload.field` expressions. Both ingress and scheduled outgoing messages are validated; these mechanisms have no external effects and do not establish predictive market validity.

## Strategic Documentation & Ecosystem

* **[Contributing Guide](CONTRIBUTING.md):** Setup, testing standards, and good-first-issue taxonomy.
* **[Open-Source Growth Playbook](docs/OPEN_SOURCE_GROWTH_PLAYBOOK.md):** The 4-pillar open-source movement scaling framework.
* **[Package Manager Specification (`fpm`)](docs/fpm.md):** Modular libraries, manifests, lockfiles, and commercial incentives.
* **[Marketing Systems Engineering](docs/MARKETING_SYSTEMS_ENGINEERING.md):** Manifesto, mental models, and the MSE practitioner persona.
* **[The Shim Strategy](docs/SHIM_STRATEGY.md):** Specification-first adoption and the linter wedge.
* **[Architecture Decisions (DECISIONS.md)](DECISIONS.md):** Canonical records of accepted architectural decisions (DEC-001 through DEC-030).
* **[Engineering Debates (DEBATES.md)](DEBATES.md):** Falsifiable trade-offs and operational boundary decisions.
* **[Out of the Box Ideas (OUT_OF_THE_BOX.md)](OUT_OF_THE_BOX.md):** Frontier research tracking and speculative hypotheses (OOTB-001 through OOTB-024).

## Core Language Implementation

The reference compiler, parser, AST semantic validator, and Monte Carlo simulation runtime live in the sister repository:
👉 [funnelscript-core](https://github.com/funnelscript/funnelscript)

## License

MIT License. See [LICENSE](LICENSE) for details.
