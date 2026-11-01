# Phase 007G — Proposed composability contracts (not an Accepted ADR)

Research anchor: Pratt/precedence-climbing expression parsing (Pratt 1973); compositional operational semantics (Plotkin 1981); deterministic discrete-event simulation (Law, Simulation Modeling and Analysis); explicit lexical symbol binding and dependency-cycle detection; RFC 8259 JSON interoperability. Implementation limits are independently falsifiable, not claims of compiler equivalence with a legacy engine.

## H-EXPR — typed composable expressions

Falsifier: parsing `a - b - c` as `a - (b - c)`, `a + b * c` as `(a + b) * c`, permitting mixed `int`/`float` without explicit conversion, or observing a partially mutated snapshot after arithmetic failure.

Versioned grammar `world-expression-v1` (bounded by 24 AST levels, 256 tokens per expression):
```ebnf
expression    = additive ;
additive      = multiplicative , { ("+" | "-") , multiplicative } ;
multiplicative= primary , { ("*" | "/") , primary } ;
primary       = number | string | boolean | state-reference
              | "payload" , "." , identifier | "(" , expression , ")"
              | stochastic-sample ;
state-reference = identifier ;
```
All state/payload references are owner-local. Binary operands must have identical exact numeric types. Division yields float and must target float; typed literal divisor zero is rejected statically, dynamic divisor zero fails without committing any transition. No implicit int-to-float coercion, no side effects or evaluation of Python code; existing sample operator semantics and RNG ownership remain unchanged. Parsing consumes expression until statement delimiters. Left-associative tiers retain deterministic source-level ordering.

## H-MODULE — named explicit exports

Falsifier: importing an unknown name, duplicated local binding, path traversal, symlink escape or transitive cycle succeeds. Versioned extension `named-import-v1`:
```ebnf
import = "import" , string , ("as" , identifier
       | "{" , selected , { "," , selected } , "}" ) , ";" ;
selected = identifier , [ "as" , identifier ] ;
```
Legacy `import "single.fnl" as Alias;` retains the exact-one-declaration rule. Named imports select declared exports by source name from a multi-declaration World module, without wildcard/implicit namespace joins; aliasing changes the owner label only. Direct and transitive module paths remain constrained to importer directory or packaged `std:` root. Duplicate aliases are rejected by the existing World type checker. No network resolution or dynamic execution.

## H-PLAYBOOK — reproducible files

Falsifier: file-input and identical inline JSON events produce different deterministic World states, malformed typed payload is admitted, duplicate key is lost, or oversized input triggers unbounded decoding. Versioned `funnelscript-event-playbook-v1` is an exact object `{"schema":"funnelscript-event-playbook-v1","events":[...]}`, containing 0–10,000 records with strict event fields `name,time,payload,priority`. File UTF-8 size at most 1 MiB. JSON duplicate keys rejected at any depth. Each record is canonicalized through existing inline event parser and World execution; no parallel event semantics. `--event` and `--events-file` are mutually exclusive in v1. No network reads or external effects.

## Compatibility and scientific boundary

World keeps snapshot-atomic event transitions, seeded keyed RNG and per-owner events. The older marketing SimulationEngine is a separate algorithm and makes no bitwise equivalence claim. Canonical financial audit/receipts are unchanged; changes are limited to parser, type AST, World evaluation and CLI ingestion. No Accepted ADR authorized. Evidence requires RED before each production change; full legacy, financial, packaging and frontend regression before GitHub delivery.
