# Retry and Backoff: OpsDeploy Guardrails

<details>
  <summary><strong>🧭 Quick Return to Map</strong></summary>

<br>

  > You are in a sub-page of **OpsDeploy**.  
  > To reorient, go back here:  
  >
  > - [**OpsDeploy** — operations automation and deployment pipelines](./README.md)  
  > - [**WFGY Global Fix Map** — main Emergency Room, 300+ structured fixes](../README.md)  
  > - [**WFGY Problem Map 1.0** — 16 reproducible failure modes](../../README.md)  
  >
  > Think of this page as a desk within a ward.  
  > If you need the full triage and all prescriptions, return to the Emergency Room lobby.
</details>


Make retries safe and predictable. Use structured backoff, deadlines, and idempotent fences so a bad minute does not become a bad day.

---

## Open these first
- Readiness gate: [rollout_readiness_gate.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/rollout_readiness_gate.md)
- Rate limits and pressure control: [rate_limit_backpressure.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/rate_limit_backpressure.md)
- Idempotent fences: [idempotency_dedupe.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/idempotency_dedupe.md)
- Cache discipline: [cache_warmup_invalidation.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/cache_warmup_invalidation.md)
- Canary and cutover: [staged_rollout_canary.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/staged_rollout_canary.md), [blue_green_switchovers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/blue_green_switchovers.md)
- Boot and first run traps: [bootstrap-ordering.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md), [deployment-deadlock.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/deployment-deadlock.md), [predeploy-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md)
- Live ops and rollbacks: [live_monitoring_rag.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/live_monitoring_rag.md), [debug_playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/debug_playbook.md)

---

## When to use
- Provider returns 429 or 5xx or timeouts rise.  
- You integrate a new model provider or gateway.  
- Queue consumers replay after crash or failover.  
- You see retry storms that multiply side effects.

---

## Acceptance targets
- 429 rate ≤ 0.5 percent at steady state, p95 ≤ 2 percent during bursts.  
- Success after retry ≥ 90 percent for transient classes.  
- Queue wait p95 ≤ 200 ms for read paths, writes use deadlines ≤ 1× p95 service time.  
- ΔS(question, retrieved) and coverage stay inside ship targets while retries occur. λ remains convergent across 2 seeds.

---

## 60 second blueprint
1) **Classify errors**  
   408 429 500 502 503 504 are retriable. 400 401 403 404 are not. 409 is a conflict. Treat as success if idempotency proves the effect already exists.
2) **Set a hard deadline**  
   Each request carries a client side deadline. Do not exceed it while retrying.
3) **Use full jitter backoff**  
   Randomized exponential backoff with a cap. Honor Retry After when present.
4) **Coalesce with single flight**  
   Collapse duplicate work under one in flight key to prevent stampede.
5) **Fence side effects**  
   Idempotency key on every write and webhook. Exactly once for the effect.

---

## Retry policy matrix
| Class | Examples | Retry? | Notes |
|---|---|---|---|
| 408 Timeout | network idle, upstream slow | Yes | Backoff with jitter until deadline. |
| 429 Rate limit | burst guard | Yes | Respect Retry After and global token budget. |
| 5xx Transient | 500 502 503 504 | Yes | Retry with jitter. Stop on deadline. |
| 4xx Permanent | 400 401 403 404 | No | Fix request or auth. Do not retry. |
| 409 Conflict | idempotency collision | No | Fetch prior receipt and return. |

---

## Backoff recipes

### Full jitter exponential
```python
import random, time

def sleep_time(attempt, base=0.25, cap=10.0):
    return random.random() * min(cap, base * (2 ** attempt))

def retry(call, max_attempts=6, deadline_s=20):
    start = time.time()
    for attempt in range(max_attempts):
        ok, res, err, retry_after = call()
        if ok:
            return res
        if time.time() - start >= deadline_s:
            break
        if retry_after:
            time.sleep(min(retry_after, max(0.05, deadline_s - (time.time() - start))))
        else:
            time.sleep(sleep_time(attempt))
    raise RuntimeError("deadline or attempts exhausted")
````

### Decorrelated jitter

```python
import random

def deco_jitter(prev, base=0.25, cap=10.0):
    return min(cap, random.uniform(base, prev * 3 or base))
```

Choose one strategy and stick to it across clients and workers.

---

## Queue consumers and jobs

* Acknowledge only after the effect is sealed. See [idempotency\_dedupe.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/idempotency_dedupe.md).
* Use per message deadlines and per topic concurrency caps.
* Backoff queues on provider 429 or store saturation.
* Include `idempotency_key`, `attempt`, and `first_seen_at` in logs.

---

## HTTP client rules

* Honor Retry After in seconds or HTTP date.
* Propagate `X Request Id` and a stable `Idempotency Key` for writes.
* Set `Request Deadline` header for end to end visibility.
* Stop retries on 4xx except 408. Stop after deadline or attempts.

---

## Single flight pattern

Coalesce identical misses so one worker computes the result.

```python
key = f"wf:{hash(request_body)}"
if redis.set(f"lock:{key}", "1", nx=True, px=30000):
    try:
        val = compute()
        redis.set(f"ans:{key}", serialize(val), ex=60)
    finally:
        redis.delete(f"lock:{key}")
else:
    val = wait_poll(f"ans:{key}", timeout_ms=1500)
return val
```

---

## YAML policy you can paste

```yaml
# opsdeploy/retry_backoff.yml
retry:
  strategy: full_jitter
  base_s: 0.25
  cap_s: 10
  max_attempts: 6
  honor_retry_after: true
deadlines:
  read_ms: 2000
  write_ms: 3000
class_rules:
  retriable:   [408, 429, 500, 502, 503, 504]
  nonretry:    [400, 401, 403, 404]
  conflict_ok: [409]
single_flight:
  enabled: true
  lease_ms: 30000
observability:
  log_fields:
    - request_id
    - idempotency_key
    - attempt
    - retry_after
    - sleep_ms
    - deadline_ms
decision:
  abort_when:
    timeout_rate_p95: ">=0.02"
    ds_p95_drift: ">=0.15"
    error_rate: ">=0.01"
```

---

## Observability you must log

* Attempts, sleep times, adherence to Retry After.
* Deadline budget spent and remaining at each hop.
* 429 and 5xx counts by endpoint and tenant.
* Success after retry ratio and time to success.
* Quality under pressure, ΔS and coverage, λ states.

---

## Symptom to fix map

| Symptom                        | Likely cause                          | Open this                                                                                                                                                                                                                                                   |
| ------------------------------ | ------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Retry storms after deploy      | no jitter, no global cap              | [rate\_limit\_backpressure.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/rate_limit_backpressure.md)                                                                                                                   |
| Double writes on retry         | missing idempotency fences            | [idempotency\_dedupe.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/idempotency_dedupe.md)                                                                                                                              |
| Mixed answers across versions  | cache keys not partitioned by pins    | [cache\_warmup\_invalidation.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/cache_warmup_invalidation.md)                                                                                                               |
| First call fails after cutover | boot order or index pointer wrong     | [bootstrap-ordering.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md), [vector\_index\_build\_and\_swap.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/vector_index_build_and_swap.md) |
| Tail latency explodes          | unbounded concurrency or no deadlines | [rate\_limit\_backpressure.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/rate_limit_backpressure.md)                                                                                                                   |

---

## Common pitfalls

* Retrying nonretriable 4xx and burning budget.
* Ignoring Retry After and syncing retries across clients.
* No deadline at the client so retries outlive the user.
* No idempotency for writes so duplicates slip in.
* Retries that cross a blue green boundary without version pins.

---

### 🔗 Quick-Start Downloads (60 sec)

| Tool                       | Link                                                                                                                                       | 3-Step Setup                                                                             |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------- |
| **WFGY 1.0 PDF**           | [Engine Paper](https://github.com/onestardao/WFGY/blob/main/I_am_not_lizardman/WFGY_All_Principles_Return_to_One_v1.0_PSBigBig_Public.pdf) | 1️⃣ Download · 2️⃣ Upload to your LLM · 3️⃣ Ask “Answer using WFGY + \<your question>”   |
| **TXT OS (plain-text OS)** | [TXTOS.txt](https://github.com/onestardao/WFGY/blob/main/OS/TXTOS.txt)                                                                     | 1️⃣ Download · 2️⃣ Paste into any LLM chat · 3️⃣ Type “hello world” — OS boots instantly |

---

<!-- WFGY_FOOTER_START -->

### Explore More

| Layer | Page | What it’s for |
| --- | --- | --- |
| ⭐ Proof | [WFGY Recognition Map](/recognition/README.md) | External citations, integrations, and ecosystem proof |
| ⚙️ Engine | [WFGY 1.0](/legacy/README.md) | Original PDF tension engine and early logic sketch (legacy reference) |
| ⚙️ Engine | [WFGY 2.0](/core/README.md) | Production tension kernel for RAG and agent systems |
| ⚙️ Engine | [WFGY 3.0](/TensionUniverse/EventHorizon/README.md) | TXT based Singularity tension engine (131 S class set) |
| 🗺️ Map | [Problem Map 1.0](/ProblemMap/README.md) | Flagship 16 problem RAG failure taxonomy and fix map |
| 🗺️ Map | [Problem Map 2.0](/ProblemMap/wfgy-rag-16-problem-map-global-debug-card.md) | Global Debug Card for RAG and agent pipeline diagnosis |
| 🗺️ Map | [Problem Map 3.0](/ProblemMap/wfgy-ai-problem-map-troubleshooting-atlas.md) | Global AI troubleshooting atlas and failure pattern map |
| 🧰 App | [TXT OS](/OS/README.md) | .txt semantic OS with fast bootstrap |
| 🧰 App | [Blah Blah Blah](/OS/BlahBlahBlah/README.md) | Abstract and paradox Q&A built on TXT OS |
| 🧰 App | [Blur Blur Blur](/OS/BlurBlurBlur/README.md) | Text to image generation with semantic control |
| 🏡 Onboarding | [Starter Village](/StarterVillage/README.md) | Guided entry point for new users |

If this repository helped, starring it improves discovery so more builders can find the docs and tools.  
[![GitHub Repo stars](https://img.shields.io/github/stars/onestardao/WFGY?style=social)](https://github.com/onestardao/WFGY)

<!-- WFGY_FOOTER_END -->

