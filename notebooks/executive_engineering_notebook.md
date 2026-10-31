# 📓 FunnelScript: The Executive Engineering Notebook

> **A Declarative Programming Language & Discrete-Event Stochastic Simulation Runtime for Marketing Systems**  
> *Author:* The FunnelScript Core Architecture Group  
> *Status:* Canonical Engineering Playbook & Knowledge Graph  
> *Version:* 1.0.0 (Living Architecture)

---

## 🎯 Core Vision

> [!IMPORTANT]
> **Why test marketing hypotheses live in production with real corporate capital and accept catastrophic downside risk?**  
> Marketing strategies are complex, multi-touchpoint distributed systems. They should be written as immutable code, static-checked for topological safety, and simulated over millions of data-driven virtual humans prior to committing a single dollar of live media spend.

```
                    "Marketing Strategy as Code"
                    
     [ Declarative Intent ]  ───►  [ Static Linter & DAG ]
                                            │
                                            ▼
     [ Live Production APIs ] ◄─── [ Dual-Mode Runtime ] ───► [ Monte Carlo Sim ]
       (Meta, Google, CRM)                                       (100,000 Agents)
```

---

## 🗺️ Visual Architecture & Knowledge Graph

```
           [ 1. Humans Write Code ]
                      │
                      ▼
        ┌───────────────────────────┐
        │    FunnelScript Syntax    │  <-- Declarative Block Architecture (HCL Style)
        └─────────────┬─────────────┘
                      │ (Lexer -> Tokens -> Parser)
                      ▼
        ┌───────────────────────────┐
        │  Abstract Syntax Tree AST │  <-- Hierarchical Verification Base (JSON)
        └─────────────┬─────────────┘
                      │
         ┌────────────┴────────────┐
         ▼ (Static Check Mode)     ▼ (Execution Mode Selection)
  ┌───────────────┐         ┌──────────────────────────────┐
  │ Funnel Linter │         │  Context Configuration Layer │
  └───────┬───────┘         └──────────────┬───────────────┘
          │                                │
          ├─► [Infinite Loops]             ├─► [Simulation Mode]    ├─► [Live Mode]
          ├─► [Unreachable Nodes]          │    (Pure Vector math)  │    (Real-World APIs)
          └─► [Mass Audience Leaks]        │                        │
                                           ▼                        ▼
                                    ┌──────────────┐         ┌──────────────┐
                                    │ NumPy Tensor │         │ Production   │
                                    │ Agent Models │         │ Connectors   │
                                    └──────┬───────┘         └──────────────┘
                                           ▲
                                           │ (DNA Vector Generation)
                                    ┌──────┴───────┐
                                    │ PyMC-Marketing│ <-- Empirical Historical Data 
                                    │ Bayesian Prior│     (Closes the Prediction Gap)
                                    └──────────────┘
```

### Complete System Dataflow

```mermaid
graph TD
    A["FunnelScript Source (.fnl)"] --> B["Lexer & Parser"]
    B --> C["Abstract Syntax Tree (AST)"]
    
    subgraph Verification ["Static Verification Layer"]
        C --> D["DAG Reachability"]
        C --> E["Cycle Detection (Tarjan's SCC)"]
        C --> F["Audience Mass Conservation"]
    end
    
    subgraph Execution ["Dual-Mode Runtime Engine"]
        C --> G{"Execution Target"}
        G -->|"Simulation Mode"| H["SIMD NumPy Tensor Runtime"]
        G -->|"Live Mode"| I["Provider Effect Adapters"]
        
        J["PyMC Marketing Bayesian Priors"] -->|"Posterior Injection"| H
        H --> K["Monte Carlo Distributions (ROAS, CAC, VaR)"]
        I --> L["Meta Ads / Klaviyo / Shopify Webhooks"]
    end
```

---

## 🧠 1. The Reality Gap & The Bayesian Link

### The Philosophical Problem
The real world is an open, non-stationary stochastic environment. Human purchasing behavior is non-linear, heteroskedastic, and subject to external macroeconomic noise. If synthetic agents are initialized with subjective, hardcoded assumptions (e.g. `price_sensitivity = 0.45` or `ctr = 0.02`), the simulation collapses into an echo chamber reflecting the developer's preconceived biases.

### The Solution: The PyMC-Marketing Empirical Bridge
Rather than guessing behavioral parameters, FunnelScript interfaces directly with Bayesian Marketing Mix Models via [`imMamdouhaboammar/pymc-marketing-mcp`](https://github.com/imMamdouhaboammar/pymc-marketing-mcp). The Bayesian engine ingests empirical historical performance data and outputs posterior probability distributions for key channel elasticities:

$$\lambda \sim \text{Beta}(a_\lambda, b_\lambda) \quad \text{(Adstock Decay Rate)}$$

$$K \sim \text{Gamma}(k_K, \theta_K) \quad \text{(Channel Half-Saturation)}$$

$$\alpha_{\text{base}} \sim \text{Normal}(\mu_\alpha, \sigma_\alpha^2) \quad \text{(Baseline Organic Conversion Drift)}$$

```
┌─────────────────────────────────┐           ┌─────────────────────────────────┐
│   PyMC Marketing MCP Engine     │           │   FunnelScript Agent Runtime    │
│  (66 Bayesian Capabilities)     │           │  (Vectorized SIMD Tensor)       │
│                                 │           │                                 │
│  • Posterior Adstock Decay (λ)  │ ────────> │  • Agent Attention Depletion    │
│  • Hill Half-Saturation (K)     │  JSON     │  • Diminishing Channel Yields   │
│  • Cross-Validation Gates       │  Schema   │  • Calibrated Cohort Vectors    │
└─────────────────────────────────┘           └─────────────────────────────────┘
```

### The Dynamic Agent DNA
Each virtual consumer $i \in \{1, \dots, N\}$ receives an orthogonal psychographic parameter vector sampled directly from calibrated empirical posteriors:

$$\mathbf{x}_i = \begin{bmatrix} \alpha_i \\ \beta_i \\ \gamma_i \\ \kappa_i \\ w_i \end{bmatrix} = \begin{bmatrix} \text{Baseline Conversion Propensity} \in [0, 1] \\ \text{Price Sensitivity Elasticity} \in [0, 1] \\ \text{FOMO \& Urgency Susceptibility} \in [0, 1] \\ \text{Ad Creative Fatigue Decay Constant} > 0 \\ \text{Liquid Disposable Category Wallet (USD)} \ge 0 \end{bmatrix}$$

---

## 🛠️ 2. Comprehensive System Architecture (The 5 Subsystems)

### I. The Frontend Compiler (Syntax & AST)
* **Declarative Grammar:** Strongly-typed domain-specific language inspired by HashiCorp Configuration Language (HCL).
* **Language Primitives:** The grammar abstracts marketing topology into declarative blocks: `audience`, `touchpoint`, `campaign`, `rule`, `transition`, and `constraint`.
* **The Compilation Pipeline:**
  $$\text{Raw Source (.fnl)} \xrightarrow{\text{Lexer}} \text{Token Stream} \xrightarrow{\text{Recursive Descent Parser}} \text{Standardized JSON AST}$$

```funnelscript
// Sample Declarative FunnelScript Block
campaign "black_friday_acceleration" {
  budget = 25000.00 USD
  horizon = 14 days
  
  touchpoint "meta_cold_traffic" {
    channel = "paid_social"
    spend = 1200.00 USD / day
    saturation_limit = 50000.00 USD
  }

  rule "cart_abandonment_trigger" {
    condition = agent.state == "cart_abandoned" && agent.idle_time >= 2 hours
    action = dispatch_email("retargeting_discount_15")
  }
}
```

---

### II. The Guardrails (Static Semantic Analyzer & Linter)
Before any simulation engine or production adapter executes, the AST must pass non-negotiable compiler-level sanity invariants:

1. **Audience Mass Conservation:**  
   The total consumer population across all discrete states $S$ must remain strictly conserved:
   $$\sum_{s \in S} N_s(t) = N_{\text{total}} \quad \forall t$$
   If an `if` branch diverts audience mass without an exhaustive fallback (`else`), the compiler rejects the strategy to prevent audience evaporation.

2. **Infinite Attribution Loop Prevention:**  
   Attribution models and user flows cannot contain circular dependencies (e.g., Touchpoint $A \to$ Landing Page $B \to$ Touchpoint $A$). The linter executes **Tarjan’s Strongly Connected Components (SCC)** algorithm to detect cycles:
   $$\mathcal{G}_{\text{attribution}} = (\mathcal{V}, \mathcal{E}) \quad \text{must be a strict DAG}$$

3. **Unreachable Node Identification:**  
   Identifies orphaned touchpoints, unreachable promotion states, and disconnected audiences prior to execution.

4. **Working Capital & Payout Delay Invariant:**  
   Models gateway settlement clearance latency $\Delta_{\text{settle}}$. If cumulative liquid reserves drop to zero:
   $$C(t) = C_0 + \sum_{\tau \le t - \Delta_{\text{settle}}} \text{Revenue}(\tau) - \sum_{\tau \le t} \text{Spend}(\tau) \le 0$$
   The engine triggers an emergency halt (`Insolvency Cliff Detected`).

---

### III. The Computational Execution Engine (Runtime)
* **Vectorized In-Memory Architecture:**  
  FunnelScript discards heavy object-oriented agent classes in favor of a **Contiguous 2D NumPy/SIMD Memory Tensor** ($\mathbb{R}^{N \times D}$).
* **Throughput Benchmark:**  
  Achieves **66,005,950 agent-days/second** on standard multi-core hardware for $N = 100,000$ agents.
* **The Clock Loop (Discrete-Event & Vectorized Step):**
  1. **Continuous Phenomenon Evaluation:** Adstock decay and message fatigue decay are evaluated across cohorts:
     $$\text{Adstock}(t) = \text{Spend}(t) + \lambda \cdot \text{Adstock}(t-1)$$
  2. **Non-Linear Channel Saturation (Hill Equation):**
     $$\text{Yield}(x) = \frac{x^n}{K^n + x^n}$$
  3. **Parallel Probabilistic Uniform Gating:** Transitions occur via vectorized broadcasting against pseudo-random uniform draws $\mathbf{U} \sim \mathcal{U}(0, 1)^N$:
     $$\mathbf{agents}_{\text{next\_state}} = \mathbf{U} < P_{\text{transition}}(\mathbf{X}, \mathbf{S}_t)$$

---

### IV. Dual-Mode Execution Blueprint (Simulation vs. Live)

```
┌────────────────────────────────────────────────────────┐
│             FunnelScript Pure Strategy Logic           │
│       Emits Pure Declarative Effect Intents Only       │
└───────────────────────────┬────────────────────────────┘
                            │
               emits EffectIntent(type, payload)
                            │
                            ▼
        ┌───────────────────────────────────────┐
        │       Pluggable Effect Handlers       │
        └───────┬───────────────┬───────────────┘
                │               │               │
  ┌─────────────▼────┐  ┌───────▼───────────┐  ┌▼──────────────────┐
  │ Simulation Mode  │  │   Shadow Mode     │  │    Live Mode      │
  │ Mutates in-memory│  │ Ingests live data,│  │ Enforces limits,  │
  │ synthetic arrays │  │ verifies rules,   │  │ signs payloads,   │
  │ Zero I/O         │  │ zero side-effects │  │ calls real APIs   │
  └──────────────────┘  └───────────────────┘  └───────────────────┘
```

1. **Simulation Mode (Pure Functional):**
   * Hermetic, in-memory evaluation with zero external side-effects.
   * Runs Monte Carlo ensemble trials ($M = 100,000$ agents) across 30–90 day campaign horizons.
   * Generates empirical probability distributions ($P_{10}, P_{50}, P_{90}$), Value-at-Risk ($\text{VaR}_{95}$), Expected Shortfall ($\text{CVaR}_{95}$), and Insolvency Ruin Probabilities ($P(\text{Insolvency})$).

2. **Shadow Execution Mode (Observational Bridge):**
   * Subscribes to real-time webhook streams from live store infrastructure (Shopify orders, Meta ad spend, Stripe chargebacks).
   * Evaluates the strategy state machine against live data without emitting outbound mutations.
   * Tracks model divergence ($\Delta_{\text{actual vs predicted}}$) to qualify a strategy before capital authorization.

3. **Live Execution Mode (Imperative with Safety Guardrails):**
   * Stateful runtime connecting to authenticated provider APIs (Meta Marketing API, Klaviyo API, Shopify Admin API).
   * **Smart-Contract Guardrails:** Enforces hard daily spend velocity ceilings ($C_{\text{daily\_cap}}$), preventing rogue loop drains.
   * **Idempotency Keys:** Every mutation carries a cryptographic hash $\text{Key} = \text{SHA256}(\text{strategy\_id} \parallel \text{event\_id} \parallel t)$ to eliminate duplicate billing on network retries.
   * **Compensating Sagas:** Declares explicit compensating actions for irreversible marketing events (e.g. canceling invalid discount codes).

---

### V. Developer Tooling & Ecosystem

* **Native CLI Suite:**  
  POSIX-compliant terminal tooling for automated CI/CD deployment pipelines:
  ```bash
  funnelscript check strategy.fnl       # Static type analysis, DAG cycle check
  funnelscript simulate strategy.fnl    # Run Monte Carlo simulation trials
  funnelscript schema                   # Export complete JSON schema specification
  funnelscript init my_strategy         # Bootstrap production scaffold
  ```
* **Visual Reactive Web Dashboard (`apps/web`):**  
  Modern browser-based visual programming canvas (React 19, TypeScript, Tailwind CSS, `@xyflow/react`):
  * **Bi-directional Transpiler:** Real-time bi-directional synchronization between graphical node flowcharts and textual FunnelScript code.
  * **Client-Side In-Browser Simulator:** WebAssembly/JS vectorized simulation engine providing real-time feedback ($< 50\text{ms}$) as users adjust sensitivity sliders.

---

## 📈 3. Cross-Industry Language Intersections

| Platform / Paradigm | Primary Inspiration | FunnelScript Translation |
| :--- | :--- | :--- |
| **Terraform (HCL)** | Declarative Infrastructure as Code (IaC), DAG dependency graphs, Provider plugins, `plan` vs `apply`. | **Marketing as Code (MaC):** Declarative touchpoint topologies, decoupled platform providers, speculative cost diffs before live execution. |
| **Julia (Agents.jl)** | High-performance numerical computing, LLVM JIT optimization, massive agent-based modeling (ABM). | **Vectorized Simulation Engine:** Contiguous SIMD psychographic tensors, Hill equation kinetics, discrete-event scheduling. |
| **Solidity / Move** | Formal verification, state machine safety, gas consumption limits, financial capital protection. | **Financial Invariant Verification:** Static analysis preventing runaway spend loops, budget burn ceilings, cryptographically idempotent actions. |
| **NetLogo & SimPy** | Behavioral consumer modeling and discrete-event simulation calendars. | **Multi-Timescale Scheduling:** Event priority queues resolving sub-second ad auctions, hourly cart emails, and multi-day settlement clearance. |
| **SQL** | Declarative query intent ("What" rather than "How"). | **Strategy Intent Declarations:** Declaring audience criteria and budget rules, letting the compiler optimize execution pathways. |

---

## 🏗️ 4. Five-Stage Implementation Roadmap

```
Stage 1: The Agent Core (Python Vector Prototypes & Behavior Formulas)
   │
   ▼
Stage 2: The Data Schema (JSON Spec Specification & Static Linter Build)
   │
   ▼
Stage 3: The Runtime Engine (Integrating PyMC Priors & Vectorized Loops)
   │
   ▼
Stage 4: Developer Tooling (CLI Architecture, Errors, & Environment Contexts)
   │
   ▼
Stage 5: The Visual Dashboard (Visual Drag & Drop Canvas to Auto-Generate Code)
```

| Phase | Milestone Name | Key Deliverables | Status |
| :---: | :--- | :--- | :---: |
| **Phase 1** | **The Agent Mind** | `PsychographicProfile` ($\alpha, \beta, \gamma, w$), choice kernels, float clamping, unit test suite. | **Verified Green** |
| **Phase 2** | **Compiler & Linter** | Recursive descent AST parser, Tarjan's SCC cycle detector, mass conservation validator. | **Verified Green** |
| **Phase 3** | **Simulation Runtime** | 66M agent-days/sec SIMD NumPy engine, Hill kinetics, clearance delay $\Delta_{\text{settle}}$, VaR/CVaR telemetry. | **Verified Green** |
| **Phase 4** | **Developer Tooling** | POSIX CLI (`check`, `simulate`, `schema`, `init`), Python packaging (`.whl`), exit codes (0/1/2). | **Verified Green** |
| **Phase 5** | **Visual Canvas** | React 19 visual flowchart builder, bi-directional transpiler, in-browser simulator ($< 50\text{ms}$). | **Verified Green** |
| **Phase 6** | **Language-Neutral Core** | Zeigler DEVS `EventKernel`, Koka-style algebraic effect intents, and formal provider abstractions. | **Active Milestone** |

---

## 🔬 5. Verified Scientific Hypotheses Ledger

* **$H_{1.1}$ (Micro-Foundation Boundedness):** Psychographic variables are strictly clamped to $[0.0, 1.0]$; purchases are mathematically prohibited if effective price exceeds liquid wallet balance ($P_{\text{eff}} > w$). *(Verified in `tests/test_agent_core.py`)*
* **$H_{2.1}$ (Topological Cycle Detection):** The AST semantic linter detects closed cyclic attribution loops and unreachable orphan nodes using Tarjan's SCC algorithm with $O(V + E)$ complexity. *(Verified in `tests/test_linter.py`)*
* **$H_{3.1}$ (Audience Mass Conservation):** Total agent population across all discrete states satisfies $\sum_{s \in S} N_s(t) = N_{\text{total}}$ with zero audience evaporation across $100,000$ agents. *(Verified in `tests/test_engine_scale.py`)*
* **$H_{3.2}$ (Liquidity Starvation Cliff):** Modeling gateway clearance latency $\Delta_{\text{settle}} \ge 5\text{ days}$ triggers an ad spend halt when working capital reaches zero, proving $P(\text{Insolvency}) > 0.80$ under cash starvation. *(Verified in `tests/test_engine_scale.py`)*
* **$H_{5.1}$ (Bi-directional Transpilation Fidelity):** Transpiling visual node canvas graphs to FunnelScript AST JSON and back preserves 100% of node identities, edges, budgets, and conditional expressions. *(Verified in `apps/web/src/lib/transpiler.test.ts`)*
* **$H_{K1}$ through $H_{K4}$ (DEVS Event Kernel Invariants):** Event processing follows strictly nondecreasing order in $(t, \pi)$; seeded replays are bit-for-bit deterministic; no event may be scheduled into the past; effect intents remain inert without provider authorization. *(Verified in `tests/test_event_machine.py`)*
