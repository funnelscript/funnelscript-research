# Evaluation: World Module Imports and Initial Marketing Standard Library v0

Date: 2026-10-31. Implementation: `funnelscript` source parser, packaged `stdlib/marketing/lead_response.fnl`, unchanged World type checker and EventMachine. Research: `spec/marketing-stdlib-v0.md`, DEC-032.

## Falsification matrix

| Requirement | Failure oracle | Test |
|---|---|---|
| H-M1, reusable neutral modules | Import fails, changes event results, or duplicates runtime | Source import, alias creation, inlined equivalence, two distinct aliases, local import |
| H-M2, distributable package | Source module missing from wheel or dependent on source repo CWD | `uv build` artifact inspection and `uv run --no-project --with <wheel>` executed from `/tmp` |
| H-M3, finite safe module graph | Absolute/traversal/symlink/cycle/missing path or invalid export loads | Negative module cases, alias collision, invalid declaration and non-World module |
| H-M4, one-shot stochastic journey | Extra checkout, spurious random draw, changing order or unverifiable seed | Seed 1 vs seed 2, repeated exposure, typed checkout event and no external intents |

## Recorded TDD sequence

1. **Spec-first:** Wrote the v0 hypothesis and invariant contract before any source or test edits.
2. **RED:** `uv run pytest tests/test_world_modules.py -q --tb=short`: **20 failed, 1 passed**. The parser rejected `import` in the World declaration body with `Expected entity or agent declaration`. The legacy-world control passed. These are one missing-feature failure mechanism, not 20 distinct discovered defects.
3. **GREEN:** Added a bounded source loader, contextual import parsing, alias compilation, the first marketing source module, wheel package-data, and the runnable example. Focused `test_world_modules.py` reached 21 passed. Two adversarial tests were added for independent aliases and rejecting imported Strategy programs: **23 focused tests passed**.
4. **Regression:** `uv run pytest -v`: initial post-implementation **204 passed**; after two extra adversarial cases, the complete suite completed with **206 passed in 3.42s** (`uv run pytest -q`, exit code 0). Wheel and sdist built; wheel contents explicitly showed `funnelscript/stdlib/marketing/lead_response.fnl`.
5. **Real installed-artifact smoke:** From an unrelated temporary working directory, executed `uv run --no-project --with <absolute-wheel-path> python -m funnelscript.cli run-world <absolute-example-path> --event <typed-json> --seed 1`. The isolation installed 12 dependencies, then executed the shipped World module successfully. This verifies packaged source resolution separately from running the repository code.

## Concrete observed scenario

Input: one `Prospect.Impression` at t=0; `cpc=2.0`, `conversion_probability=0.7`, `order_value=100.0`. In the `Lead` one-shot World library:

- Seed 1: `converted=true`, `exposed=true`, `spend=2.0`, `revenue=100.0`; two processed events including typed Checkout at t=1.
- Seed 2: `converted=false`, `exposed=true`, `spend=2.0`, `revenue=0.0`; same two processed events. Checkout guard skips revenue.
- Two Impressions in the same run produce just one checkout because `exposed` becomes true before another Impression is handled; no extra random sample is consumed.
- No effects are executed, and no marketing-specific operator was added to the compiler.

## Scope limitations

The one-shot case is not a proof of plausible CTR/CVR, economic invariants, audience conservation, funnel unit economics, causal conversion attribution, scalable populations or predictive market validity. Payload floats are finite and typed, but negative monetary inputs are not yet prohibited: no validated financial forecast should be derived from this module. There is no full module signature/registry/lockfile system, package trust model, PyMC Marketing or OmniTwin connector. Future work needs independent empirical testing.

## Failure and lessons linkage

The expected parser RED is separately classified in the app's `failure-lessons/testing-and-verification.md` as a bounded feature gap. No incidental integration failure was observed after the minimal source patch; neither a failed isolated build nor an unrun command is reported as PASS.
