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

[World Declarations v0](spec/world-declarations-v0.md) defines context-sensitive `world`, `entity`, `agent`, and `state` declarations, with an explicit primitive type checker and backward compatibility gates. It is a static AST/type-checking milestone only; agent decision rules and world execution are deferred.

## Core Language Implementation

The reference compiler, parser, AST semantic validator, and Monte Carlo simulation runtime live in the sister repository:
👉 [funnelscript-core](https://github.com/funnelscript/funnelscript)

## License

MIT License. See [LICENSE](LICENSE) for details.
