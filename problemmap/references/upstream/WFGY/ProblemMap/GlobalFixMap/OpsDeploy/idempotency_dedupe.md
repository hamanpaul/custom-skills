# Idempotency and Dedupe — OpsDeploy Guardrails

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


Stop double writes, webhook storms, and replayed jobs from creating extra side effects.  
This page gives drop-in fences, keys, and commit rules that keep effects exactly once under retries and failovers.

---

## Open these first
- Readiness gate: [rollout_readiness_gate.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/rollout_readiness_gate.md)
- Ordering and first-run traps: [bootstrap-ordering.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md), [deployment-deadlock.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/deployment-deadlock.md), [predeploy-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md)
- Version and cache discipline: [version_pinning_and_model_lock.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/version_pinning_and_model_lock.md), [cache_warmup_invalidation.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/cache_warmup_invalidation.md)
- Rate limits and backpressure: [rate_limit_backpressure.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/rate_limit_backpressure.md)
- Index swaps and cutovers: [vector_index_build_and_swap.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/vector_index_build_and_swap.md), [blue_green_switchovers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/blue_green_switchovers.md), [staged_rollout_canary.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/staged_rollout_canary.md)
- Traceability and contracts: [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md), [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)
- Live ops: [live_monitoring_rag.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/live_monitoring_rag.md), [debug_playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/debug_playbook.md)

---

## When to use
- Webhooks arrive more than once or out of order.  
- Retries create duplicate payments, tickets, or document ingests.  
- Queue consumers replay after a crash.  
- Batch workers and API calls both write the same record.  
- Region failover runs the same job twice.

---

## Acceptance targets
- Duplicate side effects rate equals 0 with retries and replays enabled.  
- All write endpoints require an idempotency key and enforce it server side.  
- For webhooks and jobs, de-duplication window covers the provider retry horizon plus safety margin.  
- Exactly once for business effect. At least once for delivery.  
- Logs include dedupe decision and the winning operation id.

---

## 60-second fix blueprint
1) **Define the idempotency key**  
   `key = sha256(source_type + source_id + revision + INDEX_HASH + action)`  
   Use fields that make the business effect unique. Never include timestamps or random values.

2) **Create a pre-commit fence**  
   Attempt to insert `key` into a fast store with set-if-absent and a TTL. If present, drop as duplicate and return the original receipt.

3) **Commit side effect then seal**  
   Perform the write or external call. On success, update the fence record with the final `effect_id` and a longer retention TTL.

4) **Return deterministic receipt**  
   Always return the same `effect_id` and citations for the same `key`.

---

## Key design and scope

- **Recommended fields**  
  - `source_type` like webhook provider, job name, endpoint.  
  - `source_id` like event id, document id, payment id.  
  - `revision` like content hash, version, ETag.  
  - `INDEX_HASH` when the effect depends on an index build.  
  - `action` like create, update, ingest, refund.

- **TTL rules**  
  - Webhooks. 7 to 14 days or provider retry horizon plus 2x margin.  
  - API writes. 24 to 72 hours.  
  - Batch jobs. Whole run window plus one day.

- **Collision policy**  
  - If a different payload tries the same `key`, return 409 with a diff. Do not apply.

---

## Webhook dedupe pattern

```python
# verify signature then dedupe
key = sha256(f"{provider}:{event_id}:{event_version}:{action}")
if not redis.set(f"idemp:{key}", "pending", nx=True, ex=14*24*3600):
    # already processed
    receipt = redis.get(f"idemp:done:{key}") or load_receipt(event_id)
    return 200, receipt

effect_id = apply_business_effect(event_payload)  # single writer or tx outbox
redis.set(f"idemp:done:{key}", effect_id, ex=14*24*3600)
return 200, {"effect_id": effect_id}
````

Notes

* Order by `event_created_at` if the provider sends sequences.
* Reject if `event_version` is older than the last sealed version for the same `source_id`.

---

## Queue consumer fence

```python
# exactly-once effect on at-least-once delivery
key = sha256(f"{topic}:{partition}:{message_key}:{message_dedupe_id}")
if not kv.put_if_absent(f"idemp:{key}", "pending", ttl=3*24*3600):
    ack(msg); return  # duplicate

try:
    effect_id = do_effect(msg)
    kv.update(f"idemp:{key}", f"done:{effect_id}", ttl=14*24*3600)
    ack(msg)
except TemporaryError:
    kv.delete(f"idemp:{key}")  # allow retry
    requeue(msg)
```

Rules

* Acknowledge only after the effect is sealed.
* For multi step effects use a transactional outbox or write ahead log.

---

## API write contract

* **Client must send** `Idempotency-Key` header. One effect per key.
* **Server must**

  * Persist the first request body associated with that key.
  * Return the same response body for the same key.
  * Reject future requests with the same key but a different body with 409 and a JSON diff.

---

## RAG specific fences

* **Document ingest**

  * `key = sha256("doc:"+doc_id+content_hash)`
  * Store `snippet_ids[]` created for that key. Re-ingest with same content returns previous `snippet_ids`.

* **Index jobs**

  * `key = sha256("index:"+INDEX_HASH)`
  * Run build once per hash. Alias swap reads the sealed effect only.

See also: [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md), [vector\_index\_build\_and\_swap.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/vector_index_build_and_swap.md)

---

## CI policy template

```yaml
# opsdeploy/idempotency.yml
require_headers:
  - Idempotency-Key
reject_on_body_mismatch: true
stores:
  fence: redis
  ttl:
    webhook_days: 14
    api_hours: 48
    batch_days: 3
logging:
  include_fields:
    - idempotency_key
    - effect_id
    - decision   # new, duplicate, conflict
    - source_type
    - source_id
on_conflict:
  status: 409
  include_diff: true
```

---

## Observability fields to log

* `idempotency_key`, `decision`, `effect_id`, `source_type`, `source_id`.
* Duplicate drops per endpoint and per tenant.
* Time between first seen and seal.
* Conflict count with body diff size.

---

## Symptom to fix map

| Symptom                          | Likely cause                              | Open this                                                                                                                                           |
| -------------------------------- | ----------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| Double charges or double tickets | no server side key or fence TTL too short | this page                                                                                                                                           |
| Mixed answers after retries      | cache keys not partitioned by version     | [cache\_warmup\_invalidation.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/cache_warmup_invalidation.md)       |
| Replayed jobs after crash        | ack before effect is sealed               | [rate\_limit\_backpressure.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/rate_limit_backpressure.md)           |
| Out of order webhook updates     | missing version checks                    | [feature\_flags\_safe\_launch.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/feature_flags_safe_launch.md)      |
| Index written twice during swap  | two writers and no alias fence            | [vector\_index\_build\_and\_swap.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/vector_index_build_and_swap.md) |

---

## Common pitfalls

* Client only keys. Always enforce on the server.
* Keys that include timestamps or random values. They defeat dedupe.
* Short TTLs that expire before provider retried the event.
* Acknowledging queue messages before the side effect is sealed.
* Sharing fences across tenants without tenant id in the key.

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

