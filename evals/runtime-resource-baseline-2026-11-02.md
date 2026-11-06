# Runtime Resource Baseline: Event Calendar vs. Processed Cap

Status: **OBSERVED LOCAL DIAGNOSTIC, not a performance certification**.
Date: 2026-11-02. Companion proposal:
[spec/runtime-resource-envelope-v0.md](../spec/runtime-resource-envelope-v0.md).

## Environment and procedure

Application working branch `remediation/architecture-recovery-r1-r2`, commit
`77795dc`, CPython 3.12.13, arm64 Mac. The EventMachine source was unchanged
during these measurements. Commands ran through `uv run python -c` from the
application checkout, using stdlib `time.perf_counter` and `tracemalloc`.
Each reported case was sampled once, with garbage collection before initial
queue measurements; no warmup, repeated trials, process-level RSS measurement,
or hardware power control. Figures are observations, not expected CI timing.

For the initial queue case:

```python
import time
import tracemalloc
from funnelscript.core.event_machine import Event, EventMachine, Transition

n = 100000

def noop(state, event, rng):
    return Transition(state)

tracemalloc.start()
t0 = time.perf_counter()
result = EventMachine(noop).run(
    0,
    (Event(1.0, "later") for _ in range(n)),
    seed=0, until=0, max_events=1,
)
elapsed = time.perf_counter() - t0
_, peak = tracemalloc.get_traced_memory()
```

`Event` objects were allocated by the source generator inside the traced
window. `result.pending` was measured after successful completion.

| Initial future events | Processed | Pending | Seconds | Peak traced bytes |
| ---: | ---: | ---: | ---: | ---: |
| 1,000 | 0 | 1,000 | 0.00366 | 221,044 |
| 10,000 | 0 | 10,000 | 0.03753 | 2,221,756 |
| 100,000 | 0 | 100,000 | 0.40469 | 22,126,740 |

## Emission fan-out counterexample

One due event at `time=0` reduced to `Transition(state, events=tuple(
Event(1.0, "future") for _ in range(100000)))`. The run used `until=0` and
`max_events=1`. Observed: **1 processed**, **100,000 pending**,
**0.46226 seconds**, **22,929,240 traced peak bytes**. The result was successful;
the processed cap did not constrain queue admission.

For comparison, 100,000 independent immediately due events with a no-op
reducer and `max_events=100000` yielded **100,000 processed**, **0 pending**,
**0.85765 seconds**, **20,402,348 traced peak bytes**.

## Interpretation and limitations

These measurements confirm the implementation-level gap: `max_events` is a
processed-event cap, not a queue or total-memory bound. On this controlled
100k-event input, allocated pending history grew roughly proportionally with N.
No conclusion follows about arbitrary payload sizes, nested emitted objects,
worst-case callback behavior, resident set size, representative population
speed or handling millions of concurrent users.

The next experiment must add independent queue admission and result retention
policies under a new reviewed contract, replay exact v0 ordering when limits do
not bind, and measure 1k/10k/100k events and agent identities with RSS and
adversarial fan-out. No production code, runtime semantics, public API or
accepted ADR was changed in this diagnostic.


## Reproducible fresh-process workload matrix (follow-on, 2026-11-02)

Application remediation commit `2741aaa` adds
`scripts/benchmark_event_resources.py` with four targeted tests. It measures
the **unchanged v0 EventMachine**, not an implementation of resource limits.
Each command launches a separate CPython process:

```bash
uv run python scripts/benchmark_event_resources.py --scenario initial --count 100000
uv run python scripts/benchmark_event_resources.py --scenario fanout --count 100000
uv run python scripts/benchmark_event_resources.py --scenario due --count 100000
```

Identical commands were run with `--count 1000` and `10000`. Platform:
macOS 27.0.1, arm64, CPython 3.12.13. `elapsed_seconds` measures just
`EventMachine.run`, excluding interpreter startup; RSS is the fresh process
high-water mark, not incremental queue allocation. Traced peaks include
objects allocated during the run. One sample per workload, no warmup.

| Scenario | Events | Processed | Pending | Seconds | Traced peak bytes | Process peak RSS bytes |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Future-only admission | 1,000 | 0 | 1,000 | 0.003348 | 219,964 | 30,851,072 |
| Future-only admission | 10,000 | 0 | 10,000 | 0.034992 | 2,223,468 | 36,012,032 |
| Future-only admission | 100,000 | 0 | 100,000 | 0.391962 | 22,128,956 | 89,243,648 |
| Single-event fan-out | 1,000 | 1 | 1,000 | 0.003898 | 228,160 | 30,556,160 |
| Single-event fan-out | 10,000 | 1 | 10,000 | 0.041737 | 2,303,664 | 36,323,328 |
| Single-event fan-out | 100,000 | 1 | 100,000 | 0.473330 | 22,928,928 | 88,326,144 |
| All events due | 1,000 | 1,000 | 0 | 0.006927 | 205,660 | 30,638,080 |
| All events due | 10,000 | 10,000 | 0 | 0.071033 | 2,045,980 | 36,421,632 |
| All events due | 100,000 | 100,000 | 0 | 0.885116 | 20,402,228 | 88,621,056 |

**Interpretation:** The full future calendar and full processed history both
retain memory proportional to count in these three limited workloads.
The observed process peaks near 88-89 MB at 100k events are not a hard bound:
arbitrary payload size, reducer side effects, concurrent trials and 100k
independently executed World agents are **not measured**. This cannot decide
between the proposed bounded-heap and streaming/aggregate alternatives.
A future limit must first preserve exact default replay and return typed,
explicit failure rather than incomplete successful results.
