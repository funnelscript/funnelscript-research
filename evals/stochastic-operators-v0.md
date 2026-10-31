# Evaluation: Seeded Stochastic World Operators v0

Date: 2026-10-31. Implementation: `funnelscript` source interpreter; spec: `spec/stochastic-operators-v0.md`; decision: DEC-031. Scope: **interpreter conformance**, not calibrated forecasting.

## Preregistered requirements

| ID | Expected falsifier | Observable check |
|---|---|---|
| H-S1 | Unknown distribution, arity, non-float parameter, wrong output type or invalid literal succeeds | Static parser/type-check rejection matrix |
| H-S2 | Two runs with the same seed and ordered inputs yield different outcomes; guard-false shifts subsequent draws | Compare `RunResult` and source-order draws against `random.Random(seed).random()` |
| H-S3 | Invalid dynamic p/bounds draws, mutates, or silently coerces | Runtime rejection and unchanged caller RNG state |
| H-S4 | Existing campaign/World behavior breaks or source interpreter initiates an effect | Full existing regression suite, pure CLI sample, and packaged build |

## TDD trace

1. **Research gate before source edits:** Wrote `spec/stochastic-operators-v0.md` defining Bernoulli, Uniform, typed arguments, runtime bounds, precisely one draw per evaluation, false-guard zero-draw semantics and limitations.
2. **RED:** Added `tests/test_world_stochastic.py` before implementation. Initial command `uv run pytest tests/test_world_stochastic.py -q --tb=short` yielded **21 failed, 1 passed**: the original parser interpreted `sample` as a field and stopped before the distribution identifier. The deterministic legacy control passed.
3. **First integration defect:** While adding `SampleExpression`, its class was placed after the `StateExpression` union, leading to a Python `NameError` at test collection. Root cause: eager module evaluation of a referenced class. Corrected declaration order without skipping tests; reran the focused contract.
4. **GREEN:** After AST, parser, static checker and runtime changes, focused suite reached 22 passing tests; then added targeted guards for invalid-value RNG preservation, pre-event sampling/emission boundaries and end-to-end subprocess CLI replay. Final `uv run pytest tests/test_world_stochastic.py -q`: **25 passed**.
5. **Regression:** `uv run pytest -v`: **183 passed**. `uv build`: successful wheel and source archive (initial run after core implementation; no subsequent source-runtime edits). `apps/web` using an explicitly resolved installed Bun binary: **1 frontend test passed** and `tsc -b && vite build` completed. The default zsh process PATH did not include Bun; this was a tooling-discovery failure, not a code failure.

## Explicit deterministic oracle

For `seed=42`, `conversion_probability=0.25`, two source transitions and event `Shopper.Impression@0`:

- Draw #1 = `random.Random(42).random()` = approximately 0.6394267984578837; `0.6394 < 0.25` is false.
- Draw #2 = 0.025010755222666936; `sample uniform(0.0,1.0)` yields the second draw.
- Verified CLI command: `uv run main.py run-world examples/stochastic_world.fnl --event '{"name":"Shopper.Impression","time":0,"payload":{"conversion_probability":0.25}}' --seed 42`.
- Observed output: `{"pending_events":0,"processed_events":1,"state":{"Shopper":{"converted":false,"engagement_score":0.025010755222666936}},"world":"MarketTrial"}` (whitespace and key ordering may differ). A subprocess test executes this CLI twice and asserts identical outputs and expected state values.

## Limitations and residual risks

- Exact reproducibility is specified for the same source, event set/order, runtime/interpreter and seed. Event insertions can shift subsequent draws; identity-keyed common-random-number streams remain open research.
- The `random()` core sequence has a Python compatibility guarantee with compatible seeding; no cross-language equivalence is proven.
- This test suite does not prove `P(conversion)=0.25` in any real population, market causal identification, PyMC/OmniTwin integration, synthetic consumer validity, Live execution safety, or statistical power of an experiment.
- Distribution acceptance checks are v0 and intentionally reject Python int values for float parameters. Compiler grammar and runtime express this exact primitive contract.
- This is a bounded reference interpreter, not a parallel, large-scale agent simulation performance evaluation.

## Engineering lessons and traceability

The collection-time `NameError` and tooling PATH discovery are recorded in `funnelscript/failure-lessons/testing-and-verification.md`; the accepted design is mirrored in both repositories' DECISIONS/DEBATES/OUT_OF_THE_BOX ledgers.
