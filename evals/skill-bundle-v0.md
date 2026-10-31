# Evaluation: Bundled Agent Skills Integrity v0

Date: 2026-10-31. Research: [skill-bundle specification](../spec/skill-bundle-v0.md), H-B1 to H-B4. Scope: repository-bundled skills only, not an installed skills marketplace or an AI behavior benchmark.

## Baseline observations

- Both application and research checkouts contained 22 primary `SKILL.md` entrypoints; their `agents/` directories contained the same vendor skill trees except for repository-specific README text. App `.agents/product-marketing.md` was a separate GTM positioning note, not an Agent Skill entrypoint.
- On macOS, `du -sh agents` reported approximately 48 MiB per checkout, but `git ls-files agents` accounted for approximately 5.7 MiB. The difference was dominated by ignored `agents/skills/deep-digger/rust/target/` Cargo build output. No `rust/target` files were tracked.
- Four `literature_search_*` directories disagreed with their already hyphenated frontmatter `name` fields. The `academic-paper/SKILL.md` link to `../shared/output_language_pair.md` pointed at an absent shared registry. J-Space contained a 109 KiB ZIP archive of extracted sources, without observed consumers.
- The original academic-paper pipeline references many additional upstream `shared/` protocols, beyond the single entrypoint link audited here. Its full 12-agent offline pipeline is **not** verified in this checkout. Existing script sources and dependent assets were preserved.

## Test-first failure record

- Before remediation, application `uv run pytest tests/test_skill_bundle.py -q`: **6 failures** (4 mismatched skill paths, 1 absent shared registry, 1 redundant ZIP); 2 passed, 53 subtests passed. Research `python3 -m unittest discover -s tests -p test_skill_bundle.py -v`: the same six failures.
- An intermediate focused run reported application **3 passed, 58 subtests passed** and research **3 passed**, but the subsequent fresh full-suite check reproduced **one failed academic-paper entrypoint link** in each checkout. The registry had been placed in `academic-paper/references/`, while its SKILL entrypoint still pointed to the absent `../shared/output_language_pair.md`. This invalidated the intermediate completion claim.
- Final TDD reconciliation corrected the entrypoint target to `references/output_language_pair.md` and the registry's own abstract-guide link to `abstract_writing_guide.md`, without altering the conformance assertions or deleting the existing registry.
- Final application `uv run pytest tests/test_skill_bundle.py -v`: **4 passed, 58 subtests passed**; application `uv run pytest -q`: **219 passed, 58 subtests passed**. Final research `python3 -m unittest discover -s tests -v`: **5 passed**. A dedicated registry-to-guide regression test was added in both repositories. Application Web `cd apps/web && bun test`: **1 passed**; its only test concerns graph transpilation, not Python engine parity.
- Cargo clean with the exact Deep Digger Rust manifest in each checkout reported **1,344 generated files and 38.3 MiB removed per checkout**. This cleans local ignored outputs only; it does not imply a 38.3 MiB Git history or GitHub size reduction. Rust source and tests remain tracked.

## Hypothesis verdicts and limits

| Hypothesis | Verdict | Boundary |
| --- | --- | --- |
| H-B1: 22 discoverable, indexed skills | PASS | Top-level `SKILL.md` metadata and README consistency, not actual LLM invocation |
| H-B2: immediate resource references | PASS after reproduced RED | Concrete Markdown links in top-level entrypoints and the repaired registry-to-guide edge; other nested upstream shared protocols remain unaudited |
| H-B3: remove redundant distribution artifacts | PASS | Tracked ZIP removed; ignored Cargo cache cleaned; no supported skill executable intentionally removed |
| H-B4: truthful GTM status | Manual review PASS | Market prediction, WASM browser engine, `fpm` and cloud connectors remain unshipped despite positioning proposals |

The contract uses standard-library `unittest` in research and runs under pytest in the application. It does not automatically prove third-party vendor code safety, full transitive dependencies, network requirements, licensing for every asset, or actual agent behavior. Future vendor upgrades require separate provenance and dependency validation before adding more files.
