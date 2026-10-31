# FunnelScript CLI: Canonical Reference

The CLI is implemented in [the application repository](https://github.com/funnelscript/funnelscript), not this research repository. Its maintained [CLI reference](https://github.com/funnelscript/funnelscript/blob/main/docs/CLI_REFERENCE.md) documents the current command set, event syntax, exit behavior, and examples. This page intentionally does not duplicate command flags, which had drifted behind the implemented World CLI.

At the verified `v0.2.0a1` source preview, `funnelscript --help` lists `check`, `compile`, `run-world`, `simulate`, `init`, `init-world`, and `schema`; `--version` is also supported. The `check` command dispatches World files to typed World checking and legacy campaign files to their separate strategy checks. `run-world` is an in-memory, assumption-driven interpreter, not a real marketing provider integration.

- [Installed preview contract](../spec/developer-preview-v0.md)
- [Observed preview evaluation and Git tag attestation](../evals/developer-preview-v0.md)
- [Language import/stdlib contract](../spec/marketing-stdlib-v0.md)

Neither this research repository nor the CLI ships PyPI publication, market-accuracy validation, a working `fpm` registry, or Live Execution.
