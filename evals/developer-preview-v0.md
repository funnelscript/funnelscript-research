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

## Public Git-source preview attestation (post-publication)

**Release verdict: RELEASED through the scoped Git source tag channel.** This does not imply a PyPI publication or a standalone GitHub Release object.

- Application annotated tag [`v0.2.0a1`](https://github.com/funnelscript/funnelscript/tree/v0.2.0a1) was pushed; both the local peeled tag and remote `refs/tags/v0.2.0a1^{}` independently resolved to application commit `ba43bd4c3aba38eb8f58dadd09c16ca315bc41a0`.
- Research annotated tag [`v0.2.0a1`](https://github.com/funnelscript/funnelscript-research/tree/v0.2.0a1) was pushed; its peeled local and remote tag resolved to research commit `e1872c4c8588c4596dc6720742a1b6853d07e9cb`.
- The GitHub Actions [tag-triggered run 41218915451](https://github.com/funnelscript/funnelscript/actions/runs/41218915451) completed successfully. Both Python/wheel and Bun/frontend jobs passed on the tagged application SHA. Distribution artifact ID `13049221574` was reported with SHA-256 `5697ebeca2884d1dced7ef5fe5d83c00968044cf81305416a85156e4648c7864`.
- Independent public install smoke: from `/tmp`, `uvx --from 'git+https://github.com/funnelscript/funnelscript@v0.2.0a1' funnelscript --version` resolved and built `ba43bd4...`, installed 12 dependencies, and printed `funnelscript 0.2.0a1`. Running `init-world`, `check`, and `run-world` against the same tag created/checked a World and produced `processed_events=2`, `revenue=100.0`, `spend=2.0`, `pending_events=0`.
- Post-tag draft GTM documents may be committed to `main` separately. They do not alter the frozen preview source SHA or provide evidence of real-world market validity.

**Residual gates:** Outside contributors have not yet independently reported clean-machine installation, and the project has no PyPI publication, hosted GitHub Release object, software supply-chain attestation, full economic constraints or PyMC/OmniTwin empirical validation. None is implicitly claimed by the source tag.


## Documentation consistency evaluation: H-P5 to H-P7 (2026-10-31)

**Baseline inspection:** A standalone scan of canonical Markdown documents found three broken research links in `CONTRIBUTING.md` (root records incorrectly addressed under `docs/`) and no broken app-relative links by existence alone. The same research guide described absent application source/build paths. App failure lessons contained 18 workstation-local absolute file URLs that would not work on GitHub.

**TDD RED integrity:** The first new research `unittest` incorrectly passed with a `FutureWarning`: the matcher was overescaped, so it matched zero links. Correcting the expression caused three real missing-link subtest failures. This was a test-harness defect, not product green. The independently written application link test initially failed on a private `file:` URL. Both tests now require a minimum count of local links examined (so a zero-match regex cannot pass accidentally).

**GREEN remediation:** Research `CONTRIBUTING.md` was rewritten for its real `spec/`, `evals/`, `paper/`, `notebooks/` structure and the three links fixed. App contributor instructions were aligned with actual parser, compiler, runtime, tests and Bun paths; local file URLs in the failure lessons became repository-relative or GitHub URLs. `README.md`, preview instructions, and ecosystem proposal disclaimers now differentiate published `v0.2.0a1` Git-source capability from unshipped plans. Focused research `python3 -m unittest discover -s tests -v`: **1 passed**. Focused app `uv run pytest tests/test_documentation_links.py -q`: **1 passed** after the URL fix.

**H-P5 verdict:** PASS for canonical local file targets only. **H-P6 verdict:** manual tree/command reconciliation PASS, not a general static proof. **H-P7 verdict:** PASS for inspected entrypoint/release/proposal claims, subject to independent evidence for future releases. **Boundaries:** External links, fragment slugs, scientific correctness, empirically calibrated forecasting and outside-user usability remain unverified by these tests. No Python World interpreter or frontend behavior changed in this phase.

**Post-remediation regression gate:** Application `uv run pytest -q` completed **215 passed in 6.02s**; `uv build` built the `0.2.0a1` wheel and sdist. A source-run of the documented `examples/marketing_lead_response.fnl` with seed 1 returned `processed_events=2`, `revenue=100.0`, `spend=2.0`, `pending_events=0`. An initial `bun test` command failed only because `bun` was not on the noninteractive shell's PATH (existing FL-014); invoking the installed Bun binary directly passed **1 test** and `bun run build` completed successfully (2226 Vite modules, TypeScript build green). Both repositories' `git diff --check` checks were clean after removing Markdown trailing whitespace. These facts describe the local verification gate, not a new public tagged release or an empirical market study.
