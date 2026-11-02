# Contributing to FunnelScript Research

This repository holds FunnelScript's research contracts, falsifiable hypotheses, architecture decisions, evaluations, and manuscripts. The [application repository](https://github.com/funnelscript/funnelscript) owns the compiler, interpreter, CLI, tests, packaged Standard Library, and Web Studio.

## Repository map

| Path | Purpose |
| --- | --- |
| [`spec/`](spec/developer-preview-v0.md) | Language and execution contracts, hypotheses, grammar, JSON Schema |
| [`evals/`](evals/developer-preview-v0.md) | Observations and falsification evidence against the specifications |
| [`paper/`](paper/README.md) | Academic manuscript and references; claims need independent evidence |
| [`notebooks/`](notebooks/README.md) | Research notebooks and exploratory calculations |
| [`docs/`](docs/MARKETING_SYSTEMS_ENGINEERING.md) | Strategy and ecosystem proposals, not necessarily shipped features |
| [`DECISIONS.md`](DECISIONS.md) | Accepted architecture decisions |
| [`DEBATES.md`](DEBATES.md) | Open trade-offs and counterarguments |
| [`OUT_OF_THE_BOX.md`](OUT_OF_THE_BOX.md) | Speculative ideas requiring evaluation |

## Research-first contribution workflow

1. Cite a theoretical or observed anchor. Distinguish proposed mechanisms from implemented capabilities and experimentally validated results.
2. State a falsifiable hypothesis, a counterexample, and the invariant or acceptance criterion in the relevant file under `spec/`.
3. Record the test procedure and actual outcomes under `evals/`. Link a concrete application test or GitHub Actions run when the claim depends on implementation.
4. Update the accepted decision, debate, and hypothesis records if the design boundary changes. Keep the research and [application documentation](https://github.com/funnelscript/funnelscript/tree/main/docs) aligned.
5. Run the same full research test suite as CI and verify the diff before submitting:

```bash
python3 -m pytest -q
git diff --check
```

`pytest` is required for the full research regression suite, including the documentation-link contracts and other research oracles. `python3 -m unittest discover -s tests -v` is an optional **narrower** smoke check only. These tests do not verify external URLs, scientific claims, or the behavior of the application. Research tests require `pytest`; application dependencies are not installed in this repository.

## Compiler and runtime changes

Work on parsers, World rules, CLI, Python regressions, or Bun belongs in [funnelscript/funnelscript](https://github.com/funnelscript/funnelscript). Follow its [contributor guide](https://github.com/funnelscript/funnelscript/blob/main/CONTRIBUTING.md) and local `AGENTS.md`. Reference the relevant research hypothesis and then run the application's own verification suite there. Do not run `uv run pytest` or `bun test` as if the research checkout contained the implementation.

## Evidence and language standards

- Use English for tracked research and implementation files.
- Do not label a simulation reproducible merely because it produces a fixed seed. Separate model assumptions, fitted data, uncertainty, and out-of-sample validation.
- Report failed hypotheses and reproducible failure lessons; do not alter tests or benchmarks just to obtain a passing result.
- Do not publish credentials, confidential market data, unverifiable financial returns, or predictions disguised as measurements.
