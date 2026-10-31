# DEBATES.md: Foundational Scientific & Architecture Debates

> Record of foundational philosophical debates, trade-off analyses, and resulting architectural decisions governing the FunnelScript ecosystem and its relationship to empirical reality.

---

## Executive Synthesis: The Core Dilemma

Building a Domain-Specific Language (DSL) for marketing is a solved software engineering problem (Lexer, Parser, AST, Linter). **The true scientific challenge is building a Simulated Market World whose emergent behavior can be trusted for real-world capital allocation.**

A simulation engine that outputs believable behavior is not necessarily predictively valid. In marketing, consumer agents operate in complex adaptive systems with non-linear feedback, exogenous volatility, and bounded rationality. FunnelScript addresses this through the **Tri-Pillar Separation Architecture**:

```
 ┌──────────────────────┐      ┌──────────────────────────┐      ┌─────────────────────────────┐
 │  1. Marketing DSL    │      │  2. Synthetic World      │      │  3. Reality Calibration    │
 │  (FunnelScript Core) │ ───> │  (Discrete-Event ABM)    │ <─── │  (PyMC Marketing MCP / MMM) │
 │  Tactics, Invariants │      │  Agents, Sinks, Latency  │      │  Priors, Saturation, Gates  │
 └──────────────────────┘      └──────────────────────────┘      └─────────────────────────────┘
```

---

## Debate 1: Human-Like LLM Agents vs. Parsimonious Calibrated Hybrid Agents

### The Conflict
* **Position A (Human-Like Persona Simulation):** Instantiate agents using Large Language Models (LLMs) with rich backstories, detailed memories, and conversational reasoning to mirror human qualitative nuances.
* **Position B (Scientific Hybrid ABM — *Adopted*):** Instantiate agents using a parsimonious set of mathematically bounded, observable behavioral variables (10–15 parameters), reserving LLMs strictly for complex qualitative choice heuristics where closed-form math is unavailable.

### Literature & Evidence Anchor
* **Stanford Agent Evaluation Study (Park et al., 2024 / Aher et al., 2023):** While agents parameterized with interview transcripts can mimic qualitative survey responses in narrow settings, uncalibrated LLM persona simulations exhibit severe distributional drift, lack physical budget conservation, and cannot reliably forecast macro market elasticities.
* **Wharton Marketing ABM Literature (Rand, Rust, 2011):** High-dimensional behavioral models suffer from parameter unidentifiability. A model with 100 uncalibrated psychological parameters is non-falsifiable; a model with 12 calibrated parameters grounded in empirical data possesses predictive validity.

### Resolution & Actionable Directives
1. **The Parsimony Invariant:** Core agent state must remain lightweight, vectorized, and mathematical:
   $$\theta_i = \langle \alpha_{\text{affinity}}, \beta_{\text{price}}, \gamma_{\text{fomo}}, \kappa_{\text{fatigue}}, w_{\text{wallet}}, \lambda_{\text{inertia}} \rangle$$
2. **Computational Feasibility:** Vectorized numeric agents scale to $N = 10^5$ agents per trial in NumPy/C ($< 15\text{ms}$/day). LLM-per-agent architectures collapse at scale ($10^5 \times \text{tokens} = \text{infeasible latency and cost}$).
3. **Selective LLM Injection:** LLMs may only be invoked in offline calibration passes to translate qualitative copy (e.g. ad creative text) into numeric parameter vectors ($q_{\text{ad}} \in [0, 1]$), never in the inner simulation loop.

---

## Debate 2: Deterministic Predictive Oracle vs. Stochastic Downside Stress-Testing

### The Conflict
* **The Fallacy:** Positioning FunnelScript as an infallible crystal ball: *"If you launch this strategy, you will generate exactly \$240,000 in revenue."*
* **The Reality:** Markets are open stochastic systems subject to irreducible aleatoric uncertainty and exogenous shocks (competitor price wars, ad platform auction volatility).

### Resolution & Actionable Directives
1. **Downside Risk & Catastrophe Detection over Point Forecasting:** FunnelScript’s primary mandate is to identify **structural vulnerabilities, failure boundaries, and capital insolvency cliffs** before spending real funds:
   * *Stable Baseline:* Does the unit economics hold under expected variance?
   * *Competitor Retaliation:* What happens if competitors cut prices by 25%?
   * *Auction Surge:* At what CPM increase does the campaign cross into negative cash flow?
   * *Cash-Flow Starvation:* Does payment gateway settlement delay ($\Delta_{\text{settle}}$) cause an ad spend freeze?
2. **Ensemble Monte Carlo Output:** All performance indicators must be delivered as probability densities (P10, P50, P90, VaR), never scalar guarantees.

---

## Debate 3: Micro-ABM vs. Macro-MMM — The `pymc-marketing-mcp` Synergy

### The Conflict & Opportunity
* **`pymc-marketing-mcp` (Macro-Level Bayesian Engine):**
  * *Input:* Real historical marketing spend, revenue time-series, lift-test outcomes.
  * *Capability:* 66 statistical methods covering Bayesian Marketing Mix Modeling (MMM), Adstock decay, Saturation curves (Hill/Michaelis-Menten), Incremental ROAS, and Statistical Decision Gates.
  * *Question Answered:* *"What did historical data prove about channel efficiency and uncertainty?"*
* **`FunnelScript` (Micro-Level Dynamic Execution Engine):**
  * *Input:* Tactical declarative strategies, touchpoint topologies, customer state machines.
  * *Capability:* Simulating discrete counterfactual scenarios, multi-step branching logic, and emergent behaviors (cannibalization, working capital freezes).
  * *Question Answered:* *"What will happen dynamically if we deploy this novel multi-step strategy tomorrow?"*

### The Integration Contract (Decoupled Statistical Bridge)
Rather than forcing an unmaintainable monolithic merge, both systems interface via an explicit **Calibration Contract**:

```
[Historical Real Data] 
         │
         ▼
[PyMC Marketing MCP]
   • Posterior Adstock Decay (λ)
   • Hill Half-Saturation (K, n)
   • Channel Marginal ROAS Prior
   • Statistical Decision Gate Status (diagnose_mmm)
         │
         │ (Calibration Export: `calibration_manifest.json`)
         ▼
[FunnelScript Simulation World]
   • Adstock & Fatigue Kernels parameterized by λ
   • Traffic Saturation Curves bounded by K
   • Volatility Sigma derived from Bayesian Posterior Uncertainty
   • Campaign Halted if Decision Gate FAILS
```

### Actionable Directives
1. **Decision Gate Inheritance:** If PyMC Marketing's diagnostic gates fail (e.g. `divergences > 0`, `r_hat > 1.05`, or `insufficient_spend_support`), FunnelScript must flag the simulation calibration as **UNVERIFIED / SYNTHETIC_ONLY**, preventing false confidence.
2. **Independent Lifecycles:** `funnelscript` and `pymc-marketing-mcp` retain separate repositories, releases, and CI suites, integrating via versioned JSON schemas (`FunnelScript Calibration Bridge v1.0`).

---

## Actionable Operational Checklist

| # | Domain | Actionable Specification | Priority | Status |
| :--- | :--- | :--- | :--- | :--- |
| **1** | **Agent Representation** | Restrict agent micro-foundations to 10–15 measurable variables; enforce strict vectorization. | P0 | **Implemented** |
| **2** | **Static Verification** | Enforce DAG reachability and cycle detection in AST linter before any simulation run. | P0 | **Implemented** |
| **3** | **Liquidity Invariant** | Model gateway settlement latency $\Delta_{\text{settle}}$ and enforce $P(\text{Insolvency})$ ad halt. | P0 | **Implemented** |
| **4** | **Calibration Contract** | Design `schema/calibration_manifest.json` to ingest Bayesian priors from `pymc-marketing-mcp`. | P1 | **Next Phase** |
| **5** | **Failure Stress-Testing** | Provide built-in simulation profiles: `baseline`, `auction_spike`, `competitor_cut`, `liquidity_squeeze`. | P1 | **Next Phase** |
| **6** | **Empirical Validation** | Backtest simulation outputs against historical incrementality lift tests to measure empirical coverage. | P2 | **Roadmap** |
