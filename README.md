# FunnelScript Research

> Formal specification, theoretical foundations, mathematical proofs, and scientific research paper for **FunnelScript** — the Declarative Domain-Specific Language (DSL) and Stochastic Agent-Based Simulation Runtime for Marketing Systems Engineering.

## Repository Structure

```
.
├── paper/
│   ├── README.md              # Full academic research paper (Markdown format)
│   ├── funnelscript.tex       # IEEE/ACM LaTeX manuscript source
│   └── references.bib         # Academic citations and foundational bibliography
├── spec/
│   └── grammar.ebnf           # Complete, closed EBNF grammar specification
└── evals/
    └── falsification_tests/   # Formal falsification scenarios (H1, H2, H3)
```

## Key Theoretical Contributions

1. **Finite State Automaton Customer Model ($M$):** Formal stochastic state transitions across `COLD`, `AWARE`, `CONSIDERING`, `CART_ABANDONED`, `CONVERTED`, and `CHURNED`.
2. **Multi-Scale Discrete-Event $\tau$-Calendar:** Eliminates temporal race conditions across micro-second ad clicks, hourly abandonment, and daily payout schedules.
3. **Working Capital Dynamics & Cash Ruin Probability $P(\text{Insolvency})$:** Mathematical proof that high-ROAS marketing strategies face catastrophic failure without accounting for settlement latency ($\Delta_{\text{settle}}$).
4. **Behavioral Cannibalization Detection:** Dynamic agent-based proof of margin erosion caused by automated cart abandonment incentives.

## Core Language Implementation

The reference compiler, parser, AST semantic validator, and Monte Carlo simulation runtime live in the sister repository:
👉 [funnelscript-core](https://github.com/funnelscript/funnelscript)

## License

MIT License. See [LICENSE](LICENSE) for details.
