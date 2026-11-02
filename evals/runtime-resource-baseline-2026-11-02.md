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
