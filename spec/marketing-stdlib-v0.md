# Marketing Standard Library v0: World Module Imports and Single-Journey Lead Response

Status: Implemented research-first v0 contract, 2026-10-31. Accepted DEC-032; extends DEC-022 and DEC-027 through DEC-031.

## Primary research and engineering anchors

1. David MacQueen, *Modules for Standard ML*, ACM Symposium on LISP and Functional Programming, 1984. Reusable program units are language-level composition with explicit names rather than keywords privileged by domain.
2. Python Software Foundation, `importlib.resources` and `pathlib`, https://docs.python.org/3/library/importlib.resources.html and https://docs.python.org/3/library/pathlib.html. This Python reference interpreter locates distributed source resources independently of the invoking working directory, resolves local file paths before checking containment, and does not execute imported Python code.
3. MITRE CWE-22, *Improper Limitation of a Pathname to a Restricted Directory*, https://cwe.mitre.org/data/definitions/22.html . User-controlled module strings are not permission to inspect arbitrary local files.
4. FunnelScript research contracts `spec/world-declarations-v0.md`, `spec/typed-event-payloads-v0.md`, `spec/stochastic-operators-v0.md` and `spec/event-emission-v0.md`. Importing is a compile-time declaration operation; only the existing World event calendar executes behavior.

## Language and source boundary

```funnelscript
world HolidayExperiment {
  import "std:marketing/lead_response.fnl" as Prospect;
}
```

The `import` and `as` words are contextual identifiers inside `world`; `marketing`, `conversion`, and `campaign` are not core keywords.

Each imported module is a complete `.fnl` `world` source exporting **exactly one** `agent` or `entity` declaration. The importing World gives that declaration a local alias, `Prospect`. Its state, events and same-owner rules are deep-copied; the resulting compiled AST contains normal World declarations, with no new runtime or domain interpreter. A module with zero/multiple exports fails explicitly in v0; a future module/signature system may lift that restriction.

`std:marketing/lead_response.fnl` resolves to a packaged read-only source file in `funnelscript/stdlib/marketing/`. Local community modules may be included using relative paths such as `./lead.fnl` or `modules/lead.fnl`. Paths must be `.fnl`, relative, and contained under the importer file's own directory (or the package `stdlib` directory for `std:`), after symlink resolution. Absolute paths, traversals, missing modules, cyclic imports, and dependency chains deeper than 16 files fail before World execution. No network fetch, package registry, auto-install, executable plug-in or absolute machine path is permitted.

Both imported and local declarations participate in the existing WorldTypeChecker. Duplicate aliases or collisions with local owners fail; any implicit or nested import that would create more than one module export fails. Existing `world` and legacy `strategy` source files remain unchanged.

## Initial shipped Marketing library: single lead response

The library is intentionally **one journey per model run**:

```funnelscript
world LeadResponseLibrary {
  agent Lead {
    state exposed: bool = false;
    state converted: bool = false;
    state spend: float = 0.0;
    state revenue: float = 0.0;
    event Impression(cpc: float, conversion_probability: float, order_value: float);
    event Checkout(order_value: float);
    rule ShowAd on event Impression when (exposed == false) {
      transition exposed = true;
      transition converted = sample bernoulli(payload.conversion_probability);
      transition spend = payload.cpc;
      emit Checkout(order_value = payload.order_value) after 1;
    }
    rule Purchase on event Checkout when (converted == true) {
      transition revenue = revenue + payload.order_value;
    }
  }
}
```

No population templating or repeated impressions for one agent is claimed. A second Impression is a no-op because `exposed=true`; this prevents overlapping Checkout events from consuming an unrelated later decision. `cpc` and `order_value` must be *assumed* finite and nonnegative by the experiment author, but v0 typed event fields alone do **not** enforce nonnegativity. The example therefore cannot be used as a validated accounting or capital-conservation model. It demonstrates a source-defined user-level marketing vocabulary and a reproducible sampled causal sequence, not real market conversion predictions.

## Mathematical invariants

For one accepted Impression at `t`, probability `p in [0,1]`, unit cost `c` and order value `v`, with one `U=random.Random(seed).random()`:

1. `exposed=1` after the first Impression; future Impression handlers skip before drawing or scheduling.
2. `converted = 1[U < p]`; `spend=c`. The pre-event state is not modified in place.
3. One same-owner Checkout is scheduled at `t+1` carrying the original `v` as a typed payload. After it processes, `revenue = v` if converted, or zero otherwise.
4. Exactly one sampled RNG draw and at most one internally emitted Checkout occur per journey; no external effects, model-estimated probabilities, interest rates or market claims.
5. Imported module declarations must retain the same rule semantics under alias renaming; check deterministically against a manually inlined equivalent.
6. Path resolution `ResolvedPath ∈ AllowedRoot` for all module reads. Static alias uniqueness and no import cycles preserve a finite module graph.

## Falsifiable hypotheses

- **H-M1, generic composition:** An imported Standard Library module executes using the same WorldExecutor as an inlined World; aliasing preserves behavior, with no domain keyword in the compiler. Counterexample: imported module fails type checking or produces different state on the same seed/events.
- **H-M2, installed artifact:** The standard `.fnl` source is bundled in the distribution and works through the CLI from an unrelated working directory. Counterexample: running a wheel-installed CLI cannot find `std:marketing/lead_response.fnl`.
- **H-M3, module security:** Duplicate aliases, missing/empty/multiple-export modules, traversal, absolute paths, symlink escapes and cycles fail explicitly before executing a World. Counterexample: `import "../private.fnl"` reads the parent file.
- **H-M4, truthful marketing demo:** One Impression yields exactly one delayed Checkout and a seeded boolean; second impressions do nothing, state and revenue remain predictable under fixed seeds, and existing event/legacy suites pass unchanged. Counterexample: two queued Checkouts or unrepeatable replay.

## Explicit exclusions

No general-purpose type parameterization, alias-qualified cross-owner dispatch, export signatures, function imports, module registries, semver resolution, editable package managers, PyMC/OmniTwin calibration, independent population agents, true marketing ROI validity, economic bounds or Live/Shadow side effects. Introduce these only after new research and tests.

## Evaluation routing

Source: `src/funnelscript/parser.py` and source-packaged `src/funnelscript/stdlib/marketing/lead_response.fnl`; distribution metadata: `pyproject.toml`; runnable case: `examples/marketing_lead_response.fnl`. RED/GREEN: `tests/test_world_modules.py` and full regressions. Record evidence in `evals/marketing-stdlib-v0.md`. No new runtime.
