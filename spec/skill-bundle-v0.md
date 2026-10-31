# Bundled Agent Skills: Discoverability and Resource Integrity v0

Status: Conformance and repository hygiene contract, 2026-10-31. This is a developer-tooling boundary; it does not modify World semantics or claim market calibration.

## Research anchors

1. [Agent Skills format specification](https://github.com/agentskills/agentskills/blob/main/docs/specification.mdx): each skill contains `SKILL.md` with metadata, a constrained lowercase hyphenated name, and skill-local resources. The name must match the directory name for consistent skill discovery.
2. [Agent Skills progressive disclosure](https://agentskills.io/specification): a loaded `SKILL.md` has a context cost; scripts, references and assets are loaded conditionally. An archive containing a second copy of active files does not serve a second execution contract.
3. FunnelScript's [operating constitution](https://github.com/funnelscript/funnelscript/blob/main/AGENTS.md): the declared engineering and research skills must remain available without introducing unverified compiler behavior or exposing local-workstation paths.

## Falsifiable hypotheses

- **H-B1, discovery:** Every immediate `agents/skills/<slug>/SKILL.md` has a valid `name: <slug>`, and every primary skill is indexed by `agents/README.md`. Counterexample: `literature_search_arxiv/` ships `name: literature-search-arxiv`, causing name-versus-directory disagreement.
- **H-B2, dependency integrity:** Concrete relative Markdown file links from primary skill entrypoints resolve within the same checked-out skill, or an explicitly declared, shipped shared resource. Counterexample: an academic-paper entrypoint points to a missing `../shared/output_language_pair.md`.
- **H-B3, focused distribution:** Retain the current 22 primary skills and their required scripts/references. Remove only observed redundant archives or generated build outputs. Counterexample: a referenced script is deleted merely to reduce file count.
- **H-B4, product truth:** FunnelScript's internal marketing context separates the public Git-source language preview from hypothetical WebAssembly Studio, `fpm`, provider connectors and empirical market forecasting. Counterexample: future capabilities appear as currently installable components.

## Invariants and test plan

Let `S` be the set of top-level directories with a `SKILL.md` and `M` the names indexed by the repo-local skill README.

1. `|S| = 22` for this cleanup; `S = M`; for each `s` in `S`, `frontmatter.name(s) = directory_name(s)` and `name` uses lowercase letters, digits and hyphens only.
2. Every concrete local target from a primary skill's Markdown link is an existing file. Example placeholder `(url)` and external URLs are not filesystem dependencies.
3. The shipped skill directories contain no copied ZIP archives when their contents are already extracted in the same skill. Ignored Rust `target/` build outputs remain untracked, and may be cleaned locally without deleting Rust sources.
4. No language parser, simulator, or installed runtime dependencies change. This is a structural test, not an empirical claim about the behavior of an AI agent using any skill.

Evaluation: execute the focused standard-library or pytest contract against both repositories before and after remediation; inspect the retained skill scripts and Git diffs; run the full application and research regressions. Record actual outcomes in `evals/skill-bundle-v0.md`.
