# Rate Limit and Backpressure — OpsDeploy Guardrails

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


Keep your pipeline stable under load. This page gives concrete limits, retry rules, and queuing patterns that prevent 429 storms, tail spikes, and cascading failure. Store and model agnostic.

---

## Open these first
- Readiness gate: [rollout_readiness_gate.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/rollout_readiness_gate.md)
- Canary staging: [staged_rollout_canary.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/staged_rollout_canary.md)
- Boot and index state: [bootstrap-ordering.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md), [vector_index_build_and_swap.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/vector_index_build_and_swap.md)
- Cache discipline: [cache_warmup_invalidation.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/cache_warmup_invalidation.md)
- Idempotent fences: [idempotency_dedupe.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/idempotency_dedupe.md)
- Live ops: [live_monitoring_rag.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/live_monitoring_rag.md), [debug_playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/debug_playbook.md)

---

## Acceptance targets
- 429 rate ≤ 0.5% per minute at steady state. Burst window p95 ≤ 2%.  
- Queue wait p95 ≤ 200 ms for read paths. Write paths use deadlines not exceeding 1× p95 service time.  
- End to end p95 latency within +15% of baseline when limiters are active.  
- Drop rate = 0 for idempotent endpoints and exactly-once jobs.  
- ΔS(question, retrieved) ≤ 0.45 and coverage ≥ 0.70 remain stable while throttled. λ stays convergent across 2 seeds.

---

## 60-second stabilization plan
1) **Admission control**  
   Set hard concurrency caps per endpoint and per tenant. Keep avg utilization near 0.7 under peak.
2) **Token bucket on read paths**  
   Rate r, burst b. Use per-tenant buckets and a global bucket. Enforce at edge and at service.
3) **Leaky queue with deadlines**  
   Put a deadline on each request. If queue wait exceeds deadline, fail fast with a retry hint.
4) **Retries with full jitter**  
   Exponential backoff with randomization. Honor provider Retry-After when present.
5) **Circuit breaker**  
   Open on consecutive errors or saturation. Shed load and degrade features instead of timing out.

---

## Patterns

### Token bucket in Redis (pseudo)
```python
def take(bucket, now, rate, burst):
    # bucket: {tokens, last_ts}
    b = redis.hgetall(bucket) or {"tokens": burst, "last_ts": now}
    delta = max(0, now - float(b["last_ts"]))
    tokens = min(burst, float(b["tokens"]) + rate * delta)
    if tokens < 1:
        return False
    pipe = redis.pipeline()
    pipe.hset(bucket, mapping={"tokens": tokens - 1, "last_ts": now})
    pipe.expire(bucket, 3600)
    pipe.execute()
    return True
````

### Backoff with full jitter (pseudo)

```python
def backoff(retry, base=0.25, cap=10.0):
    import random, math
    return random.random() * min(cap, base * (2 ** retry))
```

### Nginx edge limiter (example)

```nginx
limit_req_zone $binary_remote_addr zone=wfgy_rps:10m rate=20r/s;
server {
  location /api {
    limit_req zone=wfgy_rps burst=40 nodelay;
    proxy_pass http://wfgy_upstream;
  }
}
```

### Priority and fairness

* Two lanes: interactive queries vs batch jobs. Assign separate buckets.
* Per-tenant fairness: bucket per tenant plus a shared global bucket.
* Cost-aware limits: heavier chains consume more tokens.

### Degrade strategies

* Reduce chain length or switch to cached answer if queue wait exceeds threshold.
* Lower k or skip rerank under pressure.
* Return cite-only with links when reason step exceeds deadline.

---

## Symptom to fix map

| Symptom                       | Likely cause                                     | Open this                                                                                                                                                 |
| ----------------------------- | ------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 429 spikes after deploy       | missing jitter, shared retry stampede            | [cache\_warmup\_invalidation.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/cache_warmup_invalidation.md)             |
| Tail latency p99 explodes     | unbounded concurrency or queue with no deadlines | [staged\_rollout\_canary.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/staged_rollout_canary.md)                     |
| Mixed answers across versions | cache keys not partitioned by `INDEX_HASH`       | [version\_pinning\_and\_model\_lock.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/version_pinning_and_model_lock.md) |
| Duplicate side effects        | no idempotency fences under retry                | [idempotency\_dedupe.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/idempotency_dedupe.md)                            |
| Cascading failures to stores  | no circuit breaker or bulkhead                   | [debug\_playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/debug_playbook.md)                                                       |

---

## Observability you must log

* Per endpoint: tokens remaining, throttle events, 429 count, queue depth, wait time, service time.
* Per tenant: admissions vs evictions, burst usage, fairness ratio.
* Quality under pressure: ΔS, coverage, λ states.
* Retry metrics: attempts, Retry-After adherence, success after retry.

---

## Policy template you can paste

```yaml
# opsdeploy/limits.yml
limits:
  default:
    rps: 20
    burst: 40
    concurrent: 64
    deadline_ms: 2000
    backoff:
      base_s: 0.25
      cap_s: 10
      jitter: full
  endpoints:
    /rag/retrieve:
      rps: 50
      burst: 100
      concurrent: 128
      deadline_ms: 800
    /rag/reason:
      rps: 20
      burst: 40
      concurrent: 64
      deadline_ms: 2000
  tenants:
    premium: { multiplier: 2.0 }
    free:    { multiplier: 0.5 }
decision:
  shed_when:
    queue_wait_p95_ms: 300
    error_rate: 0.01
```

---

## Rollback rule

If 429 rate stays above 2% for one full evaluation window or tail latency p99 exceeds 2× baseline, shed load, open the breaker, and roll back to previous version or index pointer. Then follow the [debug\_playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/debug_playbook.md).

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

