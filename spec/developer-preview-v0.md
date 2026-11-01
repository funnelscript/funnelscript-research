# Experimental Developer Preview v0: Installed World Quickstart and CI Contract

Status: Research-first contract implemented and public Git source tag independently verified, 2026-10-31. Accepted DEC-033. Python distribution version `0.2.0a1`, annotated source tag `v0.2.0a1`; see the later attestation in `evals/developer-preview-v0.md`. PyPI remains out of scope.

## Evidence anchors

1. Python Packaging Authority, *Version specifiers* (PEP 440): https://packaging.python.org/en/latest/specifications/version-specifiers/ . An explicit `a1` marker denotes a pre-release, not a production-stable version.
2. Astral, *Using uv in GitHub Actions*: https://docs.astral.sh/uv/guides/integration/github/ . Locked environments and test/build commands should execute in an independently provisioned CI environment.
3. Astral, *Using tools*: https://docs.astral.sh/uv/guides/tools/ . A CLI installed directly from a versioned Git source supports an install path without a premature PyPI publication.
4. GitHub, *Using pre-written building blocks in your workflow*: https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/find-and-customize-actions . Workflow execution and artifacts must be verified independently from YAML authorship.
5. FunnelScript's existing World module contract, `spec/marketing-stdlib-v0.md` (DEC-032), is the executable language substrate. This phase adds no simulator, predictive model, side effects, or marketing-language keywords.

## User-level behavior contract

The installed CLI supports `funnelscript init-world TARGET.fnl`:
- It writes a minimal valid World importing `std:marketing/lead_response.fnl` as `Prospect`.
- The created file is accepted by `funnelscript check` and produces two events under the typed Impression input and seed 1.
- It refuses existing targets without changing a byte, rejects non-`.fnl` targets, and returns an actionable nonzero exit code on filesystem errors.
- The starter is inert until `run-world` receives an explicit typed event; no provider actions or autonomous agent population are constructed.
- It works in a directory outside the source checkout from a wheel-installed or Git-installed distribution.
- The installed CLI also reports its own Python distribution version through `funnelscript --version` using standard package metadata.

CI uses pinned source checkout and environment setup steps, `uv sync --locked`, the complete Python test suite, `uv build`, installed-wheel smoke, and Bun lockfile install/test/production build. The preview is source-tag-installable via `uvx --from git+https://github.com/funnelscript/funnelscript@v0.2.0a1 funnelscript ...` **only after** the tag exists on GitHub. The tag is not a PyPI package release or GitHub Release object by implication.

## Falsifiable hypotheses

- **H-P1, first-run DX:** A developer in a new working directory can create, check, and run the starter with the installed CLI. Counterexample: it depends on the repository's `examples/` directory or a writable package installation.
- **H-P2, safe scaffolding:** A second `init-world` command on the same target leaves existing content intact and exits nonzero; invalid extension and missing parent fail clearly. Counterexample: bytes change or unintended parent directories are created.
- **H-P3, package reproducibility:** A wheel built from the candidate contains source modules and CLI entrypoint; the lockfile matches the candidate PEP 440 version; the workflow runs tests and a wheel smoke from outside the repository tree. Counterexample: CI depends on dev-mode import, unpinned dependencies, or misses packaged stdlib.
- **H-P4, truthful preview distribution:** Candidate version, documentation, tag and remote SHA are consistent; no release is called public without independently checking tag and CI state. Counterexample: mismatched version, a tag pointing at a different SHA, or an install path that fails independently.

## Formal invariants

Let `T` be a target path and `B(T)` its bytes before an invocation.

1. If `exists(T)`, then `exit(init-world T) != 0` and `B_after(T) = B_before(T)`.
2. If `suffix(T) != ".fnl"`, then `exit(init-world T) != 0` and `not exists(T)` for an initially absent target.
3. For an initially absent valid `T` in an existing writable directory: `exit(init-world T) = 0`, `Parser.from_file(T)` passes, and `WorldExecutor` runs a typed Impression through the original module.
4. For the seed-1 documented scenario `p=0.7, cpc=2.0, order_value=100.0`, `processed_events=2`, `spend=2.0`, `revenue=100.0`. These values prove interpreter replay only, not external market prediction.
5. The version string in `pyproject.toml`, Git source tag and actual wheel metadata must identify the same candidate. Clean-install evidence must not use the project cwd.
6. No secrets or long-lived publishing tokens are added to workflows. Publishing a prerelease never unlocks Shadow/Live effects.

## Documentation consistency extension (H-P5 to H-P7)

Research anchor: the repository's actual file tree, the installed `funnelscript --help` surface, and the public-tag/CI evidence recorded in `evals/developer-preview-v0.md`. An illustrative source snippet or roadmap proposal is not proof of shipping behavior.

- **H-P5, navigable contributor contract:** Every relative Markdown link in research entrypoints, specifications, evaluations, and canonical documentation resolves to a real file inside this repository. Counterexample: a contributor follows a decision link to nonexistent `docs/DECISIONS.md` instead of the root record.
- **H-P6, truthful repository scope:** Research contribution instructions describe paths and verification commands that actually exist here and refer implementation work to the application repository. Counterexample: they instruct a research-only contributor to run `uv run pytest` or `bun test` in an absent source tree.
- **H-P7, release accuracy:** README and preview docs distinguish the confirmed `v0.2.0a1` Git-source preview from unimplemented calibration, market validation, PyPI, and Live Execution. Counterexample: they call the verified tag unpublished or future features shipped.

Invariant: `link(document, target)` implies `resolved(document.parent / target).is_file()` for each repository-relative local Markdown target in canonical documents; external URLs and fragment-only links are outside this filesystem oracle. The research check uses standard-library `unittest`, without a new dependency. No interpreter semantics change in this documentation pass.

## Out of scope

PyPI distribution, an unconditional automatic GitHub Release, custom package manager, frontend hosting, market calibration, audience conservation or new consumer-world abstractions. These require separate acceptance gates. A public Git tag or GitHub Release must be reported based on verified external state, never assumed from local code.

## Evaluation plan

Record RED/GREEN for CLI behaviors in `funnelscript/tests/test_preview_quickstart.py`, Python/Bun regressions, build metadata and isolated-wheel smoke. Verify the pushed candidate's workflow status, tag uniqueness and remote tag SHA before making any public-preview claim. Document evidence and blockers in `evals/developer-preview-v0.md` and the app's failure lessons / readiness ledger.


---

## Phase 002: CLI failure and input-boundary extension (2026-11-01)

This source-level contract applies to the local development CLI **after** the historical v0.2.0a1 tag. It does not change World execution semantics or establish a new published release.

- **H-CLI1:** In `check`/`compile`/`simulate`, documented parser/lexer/type/JSON-validation failures map to status 1; filesystem read failures map to status 2; unexpected internal `AttributeError` faults are not converted to "Parse Error". The separate `run-world` error status 1 is unchanged. Counterexample: injected implementation error produces status 1 under a syntax label.
- **H-CLI2:** A JSON-form `--event` argument containing more than 65,536 encoded UTF-8 bytes, including leading/trailing whitespace, is rejected before `json.loads`. A boundary-sized valid JSON object is accepted. Existing event time validation stays in `Event`, including nonfinite and negative rejection.
- **H-CLI3:** Failed CSV/JSON export writes map to status 2 on stderr; no output success notice is emitted before all requested export calls have succeeded. Absolute and nested destinations chosen by the user remain supported.

These contracts bound common command-line failure modes; they do not introduce a recursive JSON parser, an atomic multi-file transaction, or general filesystem sandboxing.
