# FunnelScript Research

<img src="https://raw.githubusercontent.com/funnelscript/funnelscript/main/assets/brand/funnelscript-wordmark-light.svg" alt="FunnelScript language logo" width="420"/>

Research specifications, falsification protocols, and scientific manuscripts for [FunnelScript](https://github.com/funnelscript/funnelscript), an **experimental** language for expressing and executing stateful marketing-system models. The compiler, CLI, tests, bundled Marketing Standard Library, and Web Studio live in the [application repository](https://github.com/funnelscript/funnelscript).

FunnelScript language branding and logo usage rules are maintained in the [application visual identity guide](https://github.com/funnelscript/funnelscript/blob/main/docs/brand/README.md). The research repository retains the same wordmark without introducing a separate scientific-project identity.

## Current evidence boundary

| Capability or claim | Status | Evidence |
| --- | --- | --- |
| Typed World syntax, event-driven transitions, guards, and event payloads | Implemented in the reference interpreter | [World rules](spec/rule-transitions-v0.md), [events](spec/typed-event-payloads-v0.md), [evals](evals/world-rules-v0.md) |
| Seeded Bernoulli/Uniform sampling and local event scheduling | Implemented; assumption-driven only | [Stochastic specification](spec/stochastic-operators-v0.md), [evaluation](evals/stochastic-operators-v0.md) |
| Source imports and first `std:marketing/lead_response.fnl` module | Implemented, one exported entity/agent per module | [Library contract](spec/marketing-stdlib-v0.md), [evaluation](evals/marketing-stdlib-v0.md) |
| Installed CLI starter and source-tagged `v0.2.0a1` preview | Published via Git tag; CI and clean-directory Git install verified | [Preview specification](spec/developer-preview-v0.md), [attestation](evals/developer-preview-v0.md) |
| Market digital twin, fitted human behavior, causal lift prediction, PyMC/OmniTwin adapter | Research intent; **not validated or shipped as the World runtime** | [Paper and limitations](paper/README.md) |
| Live marketing actions, `fpm` registry, PyPI distribution | Not shipped | [Ecosystem proposal](docs/fpm.md), [preview limits](spec/developer-preview-v0.md) |

The source preview is reproducible for a given model, event sequence, and seed. This does **not** establish statistical calibration, economic realism, or out-of-sample predictive accuracy.

## Try the versioned interpreter

The public `v0.2.0a1` tag can be installed without cloning the research repository. Python 3.12+ and [uv](https://docs.astral.sh/uv/) are required:

```bash
uvx --from "git+https://github.com/funnelscript/funnelscript@v0.2.0a1" funnelscript --version
uvx --from "git+https://github.com/funnelscript/funnelscript@v0.2.0a1" funnelscript init-world first.fnl
uvx --from "git+https://github.com/funnelscript/funnelscript@v0.2.0a1" funnelscript check first.fnl
uvx --from "git+https://github.com/funnelscript/funnelscript@v0.2.0a1" funnelscript run-world first.fnl --event '{"name":"Prospect.Impression","time":0,"payload":{"cpc":2.0,"conversion_probability":0.7,"order_value":100.0}}' --seed 1
```

This models one assumed lead journey, not a market population. The [application tutorial](https://github.com/funnelscript/funnelscript/blob/main/docs/EXPERIMENTAL_PREVIEW.md) covers the result and local module extension. A Git tag is not a PyPI release or a standalone GitHub Release object.

## Language and evaluation contracts

- [Domain-neutral event kernel](spec/event-kernel-v0.md) and [evaluation](evals/event-kernel-v0.md)
- [World declarations](spec/world-declarations-v0.md) and [evaluation](evals/world-declarations-v0.md)
- [World rules](spec/rule-transitions-v0.md) and [evaluation](evals/world-rules-v0.md)
- [Local event emission](spec/event-emission-v0.md) and [evaluation](evals/event-emission-v0.md)
- [Typed guards](spec/world-guards-v0.md) and [evaluation](evals/world-guards-v0.md)
- [Typed event payloads](spec/typed-event-payloads-v0.md) and [evaluation](evals/typed-event-payloads-v0.md)
- [Stochastic operators](spec/stochastic-operators-v0.md) and [evaluation](evals/stochastic-operators-v0.md)
- [Marketing source library](spec/marketing-stdlib-v0.md) and [evaluation](evals/marketing-stdlib-v0.md)
- [Installed developer preview and documentation contract](spec/developer-preview-v0.md) and [evaluation](evals/developer-preview-v0.md)
- [Reference EBNF](spec/grammar.ebnf), [JSON Schema](spec/schema.json)

## Broader research and design records

- [Bundled contributor agent skills](agents/README.md), [resource integrity contract](spec/skill-bundle-v0.md) and [evaluation](evals/skill-bundle-v0.md)
- [Research manuscript](paper/README.md), [LaTeX source](paper/funnelscript.tex), and [bibliography](paper/references.bib)
- [Exploratory notebook](notebooks/executive_engineering_notebook.ipynb) and [engineering notes](notebooks/executive_engineering_notebook.md): exploratory, not evidence of calibrated market forecasting
- [Accepted decisions](DECISIONS.md), [debates](DEBATES.md), and [unproven hypotheses](OUT_OF_THE_BOX.md)
- [Marketing Systems Engineering](docs/MARKETING_SYSTEMS_ENGINEERING.md), [fpm concept](docs/fpm.md), and [ecosystem growth plan](docs/OPEN_SOURCE_GROWTH_PLAYBOOK.md): design proposals where not corroborated by the interpreter

## Contributing

Follow the [research contribution guide](CONTRIBUTING.md). This repository has a standard-library documentation-link check: `python3 -m unittest discover -s tests -v`. Runtime and frontend changes belong in the [application contribution workflow](https://github.com/funnelscript/funnelscript/blob/main/CONTRIBUTING.md).

## License

[MIT](LICENSE).
