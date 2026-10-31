# Evaluation: Experimental Developer Preview v0.2.0a1

Date: 2026-10-31. Research: `spec/developer-preview-v0.md` (H-P1 to H-P4), DEC-033. Candidate: `0.2.0a1`.

## Hypothesis-to-evidence matrix

| Hypothesis | Observable oracle | Evidence |
|---|---|---|
| H-P1: first-run experience | Installed CLI scaffolds a World that checks and runs outside source checkout | `tests/test_preview_quickstart.py`; isolated wheel smoke |
| H-P2: safe creation | File bytes preserved when target exists; invalid suffix and absent parent fail | Negative tests for overwrite, suffix and directory |
| H-P3: distributable build | Locked Python/Bun dependency procedures, wheel has packaged stdlib and a working entrypoint | `uv lock`, `uv build`, `bun install --frozen-lockfile`, installed-wheel CLI smoke |
| H-P4: truthful external distribution | Version matches tag SHA and release claims match actual GitHub CI outcomes | Remote-tag and GitHub Actions verification (required for public verdict) |

## Recorded TDD and local verification

1. Research contract and mathematical file-preservation invariants were written before implementation.
2. Initial RED: `uv run pytest tests/test_preview_quickstart.py -q --tb=short` yielded **3 failed and 3 superficially passing negative tests** because the missing `init-world` command failed at argument parsing. This was a **false-green harness hazard**, not a valid negative-path success.
3. Corrected the negative-path tests to require command-specific diagnostic messages, then reran RED: **6 failed** for the intended missing public command; test collection and harness succeeded.
4. Minimal GREEN: one bounded `init_world_command` in the existing CLI using `Path.open("x")` and a three-line source starter. Focused run: **6 passed**. A seventh test asserted the installed CLI reports its version; it first failed because `--version` was unrecognized, then passed with standard-library `importlib.metadata`. Focused suite reached **7 passed** after the version test, and **8 passed** after adding the documented local community-module extension as a separate integration oracle. The full Python suite therefore has 206 previous tests plus 8 preview tests. No extra dependencies, new runtime, model or module loader were added.
5. Before the output/version CLI corrections, full `uv run pytest -v`: **212 passed**. `bun install --frozen-lockfile`, `bun test` (1 passed) and `bun run build` succeeded. `uv build` emitted `funnelscript-0.2.0a1-py3-none-any.whl` and `.tar.gz`, with `funnelscript/stdlib/marketing/lead_response.fnl` in the wheel.
6. The isolated-wheel smoke from `/tmp` installed 12 packages, created and type-checked `MarketingPreview`, then processed two events and reported `revenue=100.0` for seed 1. It exposed a double-escaped literal newline in informational stdout, which was corrected and added to the regression assertion. This did not affect source generation or state execution.

## Required final gate

**Final local gate, after the CLI output and version edits:** `uv run pytest -v` completed with **214 passed in 6.17s** (exit code 0). `uv build` regenerated `funnelscript-0.2.0a1-py3-none-any.whl` and the source distribution. An independent `uv run --no-project --python 3.12 --with <absolute-wheel-path>` invocation from `/tmp` printed `funnelscript 0.2.0a1`, created a valid `first.fnl` with a real newline in the help output, type-checked it, then processed two typed events and reported `revenue=100.0`, `spend=2.0`, no pending events. The 8 focused quickstart tests passed independently. Ruby's YAML parser accepted the CI workflow and recognized its two jobs. Bun install/test/build succeeded earlier in this mutation cycle; no Bun source changes followed.

**Remaining external gate:** Independently inspect the GitHub-hosted workflow run triggered by the pushed candidate SHA before tagging; check the remote tag SHA and actual versioned Git `uvx` installation after any tag push. Local evidence is PASS, but remote CI and source-tag publication remain unverified at this checkpoint.

## Explicit limits

Tests establish a reproducible source-language and onboarding interface, not market prediction. The demo retains user-assumed conversion probabilities and no nonnegative-money refinement. GitHub Actions configuration is not CI success; a source tag is not a PyPI release, signed provenance, or a hosted GitHub Release object.

## External GitHub Actions evidence for the first pushed candidate

The Python application commit `52a887993ac7f045605298a28ea32e8089393292` triggered [Experimental Preview CI run 41218293773](https://github.com/funnelscript/funnelscript/actions/runs/41218293773). GitHub reported the completed run as **success** and returned separately successful jobs for:

- Python tests, locked setup, wheel/sdist build, isolated-wheel CLI smoke, and upload of the distribution artifact.
- Bun lockfile installation, frontend tests and production build.

The uploaded `funnelscript-preview-distributions` artifact ID was `13049265468`, with GitHub-reported SHA-256 digest `26ed86f0edc2fe147fcfba68629487b22bb7a4d03f3a6a18dce84827e053c375` and 14-day retention through 2026-11-14. These values come from GitHub's own workflow/artifact responses, not a local forecast.

A later documentation-only commit may advance `main`; that commit requires a fresh CI check before it can become the final tagged source candidate. A Git tag, versioned Git-install smoke or standalone GitHub Release is not established by this first successful CI run.
