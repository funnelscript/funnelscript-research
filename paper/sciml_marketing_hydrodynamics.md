# Discrete-Event Simulation, Keyed Stochastic Determinism, and Audited Financial Provenance for Marketing Systems Engineering

**Authors:** Marketing Systems Engineering Group  
**Classification:** Computer Science — Programming Languages (cs.PL); Multiagent Systems (cs.MA); Quantitative Marketing & Econometrics (econ.EM)  
**Status:** Canonical Research Monograph & Formal Architectural Paper v1.0.0 (Track A: Discrete-Event & Audited Financial Provenance)  
**Codebase Alignment:** Verified 1:1 against `funnelscript` compiler, runtime, and operations research solver (`src/funnelscript/`)

---

## Abstract

Modern quantitative marketing systems are multi-touch distributed processes involving asynchronous lead arrivals, non-linear channel saturation, and payment gateway settlement latencies. Despite committing billions of dollars in capital, enterprise growth teams continue to orchestrate campaigns through informal spreadsheets or non-executable visual flowcharts. This absence of formalization introduces catastrophic failure modes: reachability deadlocks, liquidity starvation during rapid budget scaling, and uncontrolled parameter drift.

This monograph establishes the formal foundations of **FunnelScript**, an applied domain-specific language (DSL) and deterministic execution runtime that treats marketing funnels as verifiable discrete-event state machines with double-entry financial provenance. We present four core theoretical and engineering contributions:
1. **The Discrete-Event Marketing Automaton:** We formalize the consumer journey as a guarded stochastic state machine with closed transition semantics, proving compile-time conservation of audience mass ($\sum P(\text{branch}_i) = 1$) and reachability invariants (`event_machine.py`, `linter.py`).
2. **Keyed Counter-Based Stochastic Determinism:** To eliminate ergodic simulation drift and enable bit-identical replay across parallel worker threads, we introduce a keyed counter-based pseudo-random number generation scheme that guarantees independent, uncoupled stochastic trajectories across audience cohorts (`population_rng.py`).
3. **Audited Double-Entry Financial Provenance:** We integrate double-entry accounting mechanics and SHA-256 cryptographic transaction chaining directly into the marketing runtime, modeling working-capital insolvency under payment processor settlement delays $\Delta_{\text{settle}}$ (`ledger.py`, `provenance.py`, `commit.py`).
4. **Normalized Simplex Operations Research Optimization:** We formulate multi-channel budget allocation over normalized unit simplexes ($w \in [0, 1]^m, \sum w_i = 1$) with scale-invariant gradient steps and empirical spend-support metadata classification, preventing prior-dominated extrapolation (`solver/simplex.py`, `solver/optimizer.py`).

We validate the framework through an empirical backtesting protocol on multi-channel campaign telemetry, demonstrating that FunnelScript's non-linear saturation and liquidity model accurately forecasts cash runway exhaustion where standard linear spreadsheet models fail. Every mathematical claim in this paper references an executable Python module and verified test in the FunnelScript repository.

---

## 1. Introduction: The Formalization Crisis in Marketing Systems

Enterprise marketing engineering allocates substantial financial capital through tactical media purchases across digital ad networks (Meta Ads, Google Search, TikTok), conversion landing pages, and automated retargeting sequences. Historically, this domain has operated without software engineering discipline:
* **The Spreadsheet Fallacy:** Marketing plans rely on static, linear spreadsheet projections that assume constant Customer Acquisition Cost ($\text{CAC}$) and instantaneous cash collection, ignoring non-linear saturation (diminishing returns) and cash collection latency.
* **The Closed-World Simulation Paradox:** Academic Agent-Based Models (ABM) frequently rely on uncalibrated synthetic parameters, creating self-referential toy models divorced from empirical campaign telemetry.
* **Semantic Divergence in Tooling:** Maintaining unverified visual prototypes alongside production systems introduces subtle drift where visual forecasts diverge from financial accounting reality.

FunnelScript addresses these challenges by unifying declarative grammar, discrete-event state machines, and audited financial provenance into a single canonical runtime.

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        FunnelScript Architectural Pipeline                             │
├───────────────────────┬───────────────────────────────┬────────────────────────────────┤
│   Declarative Layer   │       Execution Core          │      Operations Research       │
├───────────────────────┼───────────────────────────────┼────────────────────────────────┤
│ • .fnls Source Grammar │ • Event Machine (Min-Heap)    │ • Unit Simplex Bounds          │
│ • World Declarations  │ • Keyed Counter-Based RNG     │ • Scale-Invariant Gradients    │
│ • Static Type Linter  │ • Double-Entry Ledger (007f)  │ • Empirical Support Metadata   │
│ • Guard Verification  │ • Settlement Latency Δ_settle │ • Artifact Hash Verification   │
└───────────────────────┴───────────────────────────────┴────────────────────────────────┘
```

---

## 2. Discrete-Event Marketing Automata & Invariant Guards

### 2.1 The Guarded Marketing State Automaton
We formalize a marketing funnel as a finite-state automaton with guarded stochastic transitions:
$$\mathcal{M} = \langle \mathcal{S}, \Sigma, \mathcal{T}, s_0, \mathcal{F}, \mathcal{G} \rangle$$
Where:
* $\mathcal{S} = \{\text{COLD}, \text{AWARE}, \text{CONSIDERING}, \text{CART\_ABANDONED}, \text{CONVERTED}, \text{CHURNED}\}$ is the discrete state space.
* $\Sigma$ is the alphabet of marketing interventions (ad impressions, email dispatches, price discounts).
* $\mathcal{G}: \mathcal{S} \times \Sigma \to \{\text{True}, \text{False}\}$ is a set of first-order invariant guards that must evaluate to True before transition admission (`src/funnelscript/compiler/world_guards.py`).
* $\mathcal{T}: \mathcal{S} \times \Sigma \times \Theta \to \Delta(\mathcal{S})$ defines state transition probabilities parameterized by the consumer psychographic vector $\theta \in [0, 1]^k$.
* $s_0 = \text{COLD}$ is the initial entry state for unacquired leads.
* $\mathcal{F} = \{\text{CONVERTED}, \text{CHURNED}\}$ are terminal absorbing states for a bounded campaign window.

### 2.2 Conservation of Audience Mass
A fundamental invariant enforced by FunnelScript's static semantic analyzer (`src/funnelscript/compiler/linter.py`) is the Conservation of Audience Mass: no leads may be silently created or destroyed across guarded stochastic branches:
$$\sum_{j=1}^{K} P(s_t \to s_{t+1}^{(j)} \mid \theta) = 1.0, \quad \forall s_t \in \mathcal{S} \setminus \mathcal{F}$$
Any `.fnls` script where branch probabilities do not sum to unity or where terminal sinks are unreachable is rejected at compile time with exit code 1 (`tests/test_world_guards.py`).

### 2.3 The Multi-Scale Discrete-Event Calendar
Real-world marketing events span disparate timescales: impression bidding ($\sim 10^{-1}$ s), cart abandonment recovery ($\sim 10^3$ s), and payment settlement ($\sim 10^5$ s). To eliminate temporal aliasing and race conditions, FunnelScript implements an ordered discrete-event calendar driven by a priority min-heap (`src/funnelscript/core/event_machine.py`):
$$\mathcal{Q} = \{ e_k = \langle \tau_k, \text{Owner}_k, \text{EventName}_k, \text{Payload}_k \rangle \}$$
Events are dequeued and processed in non-decreasing order of absolute execution timestamp:
$$\tau_1 \le \tau_2 \le \dots \le \tau_n$$
Asynchronous actions (such as cart abandonment email nurture) are scheduled as future discrete events rather than unconstrained continuous loops.

---

## 3. Keyed Counter-Based Stochastic Determinism

### 3.1 Eliminating Inter-Trial Coupling
Standard pseudorandom generators relying on global mutable state introduce subtle correlation across parallel simulation trials. FunnelScript enforces deterministic reproducibility across distributed runs using a keyed counter-based pseudo-random number generator (`src/funnelscript/core/population_rng.py`).

For a simulation with master seed $\sigma$, agent identifier $i \in \mathbb{N}$, and event sequence step $k \in \mathbb{N}$, the unique pseudo-random value $u_{i, k}$ is generated by hashing the tuple:
$$\text{Key}_{i, k} = \text{HMAC-SHA256}(\sigma, \text{AgentID}_i \,\|\, \text{EventName} \,\|\, k)$$
$$u_{i, k} = \frac{\text{uint32}(\text{Key}_{i, k}[0:4])}{2^{32}}$$

### 3.2 Invariant Guarantees
1. **Bit-Identical Replay:** Any simulation trial re-executed with the identical master seed $\sigma$ and event stream produces identical output metrics down to the least significant bit across operating systems (`tests/test_population_rng.py`).
2. **Orthogonal Perturbation:** Modifying the psychographic attribute of agent $i$ has zero effect on the pseudo-random stream evaluated for agent $j \ne i$.

---

## 4. Audited Double-Entry Financial Provenance

### 4.1 Conservation of Capital and Dual-Entry Ledger
Unlike marketing tools that treat ad spend and revenue as unverified floating-point tallies, FunnelScript models financial flows through double-entry accounting mechanics (`src/funnelscript/stdlib/marketing/ledger.py`):
$$\sum \text{Debits} \equiv \sum \text{Credits}$$
Every financial consequence is recorded as an immutable ledger transaction with five canonical accounts:
* `Assets:Cash:Operating` (liquid working capital)
* `Assets:Receivables:Processor` (unsettled gateway revenues)
* `Expenses:Marketing:PaidMedia` (ad spend disbursed)
* `Expenses:Operations:GatewayFees` (merchant processing fees)
* `Revenues:GrossSales` (gross customer purchase value)

### 4.2 Dynamic Liquidity Constraints Under Settlement Latency
A primary cause of agency campaign failure is the *Growth Liquidity Trap*: a campaign with positive Return on Ad Spend ($\text{ROAS} > 1.0$) scales daily spend faster than payment processor settlement cycles $\Delta_{\text{settle}}$.

Available liquid working capital $C(t)$ at day $t$ obeys:
$$C(t) = C_0 - \sum_{\tau=0}^{t} \text{Spend}(\tau) + \sum_{\tau=0}^{t - \Delta_{\text{settle}}} \text{GrossRevenue}(\tau) \cdot (1 - \phi_{\text{fee}})$$
If $C(t) < C_{\text{min}}$ at any point during campaign scaling, a `LiquidityStressWarning` is emitted, and further ad spend is fenced by the runtime engine (`src/funnelscript/stdlib/marketing/metrics.py`, `tests/test_financial_ledger.py`).

### 4.3 Cryptographic Provenance Chaining (ADR 007f)
Every financial commit block in FunnelScript contains a parent hash pointer:
$$H_n = \text{SHA-256}(H_{n-1} \,\|\, \text{TxRoot}_n \,\|\, \text{Timestamp}_n \,\|\, \text{SequenceNumber}_n)$$
This guarantees tamper-evident provenance and idempotent recovery under process termination (`src/funnelscript/stdlib/marketing/provenance.py`, `tests/test_financial_commit_recovery.py`).

---

## 5. Operations Research Optimization on Normalized Simplexes

### 5.1 The Normalized Unit Simplex Formulation
In automated budget allocation, optimizing over raw monetary variables $\mathbf{x} \in \mathbb{R}^m$ introduces severe numerical instability when channels differ by orders of magnitude. FunnelScript transforms budget optimization into the normalized unit simplex (`src/funnelscript/solver/simplex.py`):
$$\Delta^{m-1} = \left\{ \mathbf{w} \in \mathbb{R}^m \;\middle|\; \sum_{i=1}^m w_i = 1, \; 0 \le w_i \le 1 \right\}$$
Where total budget $B > 0$ maps allocations via $x_i = w_i \cdot B$.

### 5.2 Scale-Invariant Finite-Difference Steps
When estimating numerical gradients over the simplex, step sizes must be invariant to the absolute budget scale $B$. FunnelScript computes directional derivatives along orthonormal tangent vectors using scale-invariant perturbations:
$$h_i = \epsilon \cdot \max(w_i, 10^{-4}), \quad \epsilon = 10^{-6}$$
Projection back onto the feasible simplex is performed via the Wang-Carreira-Perpinan projection algorithm:
$$\Pi_{\Delta}(\mathbf{v}) = \operatorname{argmin}_{\mathbf{w} \in \Delta^{m-1}} \|\mathbf{w} - \mathbf{v}\|_2^2$$

### 5.3 Canonical Response Evaluation Path
Optimization and simulation evaluate channel returns through a single canonical response function (`src/funnelscript/solver/evaluator.py`), eliminating divergence between optimizer assumptions and runtime execution:
$$R_i(x_i) = V_{\max, i} \cdot \frac{x_i^{\alpha_i}}{K_{\text{sat}, i}^{\alpha_i} + x_i^{\alpha_i}}$$
Where $V_{\max, i}$ is the asymptotic ceiling, $K_{\text{sat}, i}$ is the half-saturation spend, and $\alpha_i$ is the Hill shape parameter.

### 5.4 Empirical Spend Support Metadata
To prevent optimizers from proposing spend allocations outside observed data support, every channel model records empirical observation boundaries:
$$\operatorname{ExtrapolationRatio}(x) = \frac{\max(0, x - x_{\max}^{\text{obs}}, x_{\min}^{\text{obs}} - x)}{x_{\max}^{\text{obs}} - x_{\min}^{\text{obs}}}$$
Allocations exceeding observed support by more than 20% are classified as `EXTRAPOLATED_SPECULATIVE`, requiring explicit risk acknowledgment before plan commitment (`src/funnelscript/solver/types.py`, `tests/test_solver_engine.py`).

---

## 6. Empirical Parameter Calibration & Out-of-Sample Backtesting

### 6.1 Automated Ingestion of Campaign Telemetry
FunnelScript includes native adapters for standard advertising exports (Meta Ads, Google Search CSVs) and CRM payment logs (`src/funnelscript/stdlib/marketing/calibration.py`). The calibration engine fits Hill saturation parameters ($V_{\max}, K_{\text{sat}}, \alpha$) and adstock decay rates ($\lambda \in [0, 1]$) using bounded non-linear least squares.

### 6.2 Temporal 50/50 Backtesting Protocol
To evaluate forecast accuracy without lookahead bias, the dataset is split temporally:
* **Calibration Window (Days $1 \dots T/2$):** Used strictly for parameter inference and `.fnls` model generation.
* **Out-of-Sample Evaluation Window (Days $T/2 + 1 \dots T$):** Held out for backtesting.

Forecast accuracy is evaluated against ground truth using Mean Absolute Percentage Error ($\text{MAPE}$):
$$\text{MAPE} = \frac{1}{N} \sum_{t=1}^N \left| \frac{y_t - \hat{y}_t}{y_t} \right| \times 100\%$$
FunnelScript benchmarks its predictions directly against a standard linear spreadsheet projection, demonstrating superior accuracy during budget scaling events where linear models underestimate CAC escalation and ignore settlement lag (`tests/test_calibration_and_backtest.py`).

---

## 7. Traceability and Verification Matrix

Every mathematical construct and invariant in this paper is directly mapped to executable Python code and passing automated tests in the FunnelScript repository:

| Paper Section & Construct | Mathematical Formalism | Source Implementation | Test & Verification Suite |
| :--- | :--- | :--- | :--- |
| **§ 2.1 State Automaton** | $M = \langle S, \Sigma, \mathcal{T}, s_0, F \rangle$ | `src/funnelscript/core/event_machine.py` | `tests/test_event_machine.py` |
| **§ 2.2 Mass Conservation** | $\sum P(\text{branch}_i) = 1$ | `src/funnelscript/compiler/linter.py` | `tests/test_world_guards.py` |
| **§ 2.3 Event Calendar** | Min-Heap Priority Queue $\mathcal{Q}$ | `src/funnelscript/core/event_machine.py` | `tests/verification/test_event_kernel_properties.py` |
| **§ 3.1 Keyed Counter RNG** | $\text{HMAC-SHA256}(\sigma, \text{ID} \,\|\, k)$ | `src/funnelscript/core/population_rng.py` | `tests/test_population_rng.py` |
| **§ 4.1 Dual-Entry Ledger** | $\sum \text{Debits} = \sum \text{Credits}$ | `src/funnelscript/stdlib/marketing/ledger.py` | `tests/test_financial_ledger.py` |
| **§ 4.2 Settlement Latency** | $C(t)$ with $\Delta_{\text{settle}}$ lag | `src/funnelscript/stdlib/marketing/metrics.py` | `tests/test_durable_financial_audit.py` |
| **§ 4.3 Commit Provenance** | $H_n = \text{SHA256}(H_{n-1} \,\|\, \text{TxRoot}_n)$ | `src/funnelscript/stdlib/marketing/provenance.py` | `tests/test_financial_commit_recovery.py` |
| **§ 5.1 Unit Simplex Bounds** | $\mathbf{w} \in \Delta^{m-1}, \sum w_i = 1$ | `src/funnelscript/solver/simplex.py` | `tests/test_solver_engine.py` |
| **§ 5.2 Scale Invariance** | $h_i = \epsilon \cdot \max(w_i, 10^{-4})$ | `src/funnelscript/solver/simplex.py` | `tests/test_solver_engine.py` |
| **§ 5.3 Canonical Response** | Hill Saturation $V_{\max} \frac{x^\alpha}{K^\alpha + x^\alpha}$ | `src/funnelscript/solver/evaluator.py` | `tests/test_solver_engine.py` |
| **§ 5.4 Spend Support Gate** | $\operatorname{ExtrapolationRatio}(x) \le 0.20$ | `src/funnelscript/solver/lineage.py` | `tests/test_solver_engine.py` |
| **§ 6.1 Calibration Engine** | Parameter Inference & CodeGen | `src/funnelscript/stdlib/marketing/calibration.py` | `tests/test_calibration_and_backtest.py` |
| **§ 6.2 Backtest Protocol** | 50/50 Split & Spreadsheet Benchmark | `src/funnelscript/stdlib/marketing/backtest.py` | `tests/test_calibration_and_backtest.py` |

---

## 8. Conclusion

By grounding marketing systems engineering in discrete-event automata, keyed stochastic determinism, double-entry financial accounting, and convex operations research, FunnelScript replaces heuristic spreadsheet guesswork with verifiable, executable software engineering. The implementation eliminates semantic drift across execution surfaces and provides growth engineers with mathematically grounded decision support prior to committing capital.
