# Rollback and Fast Recovery — OpsDeploy Guardrails

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


Bring production back to a good state fast. This page gives you the exact levers and a 60-second checklist to reverse a bad rollout, recover service, and preserve data integrity.

---

## Open these first
- Canary staging: [staged_rollout_canary.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/staged_rollout_canary.md)
- Blue green cutover: [blue_green_switchovers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/blue_green_switchovers.md)
- Version fences: [version_pinning_and_model_lock.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/version_pinning_and_model_lock.md)
- Index swap: [vector_index_build_and_swap.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/vector_index_build_and_swap.md)
- Feature flags: [feature_flags_safe_launch.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/feature_flags_safe_launch.md)
- Rate and retry: [rate_limit_backpressure.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/rate_limit_backpressure.md), [retry_backoff.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/retry_backoff.md)
- Cache and dedupe: [cache_warmup_invalidation.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/cache_warmup_invalidation.md), [idempotency_dedupe.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/idempotency_dedupe.md)
- First-run traps: [bootstrap-ordering.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md), [deployment-deadlock.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/deployment-deadlock.md), [predeploy-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md)
- Live ops: [live_monitoring_rag.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/live_monitoring_rag.md), [debug_playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/debug_playbook.md)

---

## When to pull this page
- ΔS drift p95 over 0.15 or coverage under 0.60 on the canary window.  
- λ flips rise above 0.20 or tool loops detected.  
- 5xx over 1 percent or 429 storms that do not subside with backoff.  
- p99 latency doubles, cache poisoning, mixed answers across versions.  
- Suspicion of duplicate side effects or index mismatch.

---

## Recovery exit targets
- User visible error rate back under 0.5 percent within ten minutes.  
- ΔS and coverage match the pinned baseline window.  
- p95 latency within plus 15 percent of baseline.  
- Duplicate side effects equal zero during and after rollback.

---

## 60-second rollback checklist
1) **Capture state**  
   Dump `BUILD_ID`, `GIT_SHA`, `MODEL_VER`, `PROMPT_VER`, `INDEX_HASH`, `RERANK_CONF`, `TOK_VER`, `ANALYZER_CONF`, sample ΔS and coverage. Keep for the postmortem.
2) **Freeze writes**  
   Pause non-idempotent writers and queue consumers. Confirm fences are active. See [idempotency_dedupe.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/idempotency_dedupe.md).
3) **Pick the fastest lever**  
   - Feature flag kill switch  
   - Blue to Green pointer back to Blue  
   - Index alias from `docs_vB` back to `docs_vA`  
   - Version unpin to the last known good set
4) **Flip one pointer**  
   Single operation. DNS or Ingress or alias or service selector. See the blue green and index swap pages.
5) **Rotate cache namespace**  
   Keys must include `INDEX_HASH` and `PROMPT_VER`. Do not delete in place. See cache page.
6) **Throttling on**  
   Global token budget and circuit breaker while the system cools. See rate and retry pages.
7) **Watch for green**  
   Hold ten to fifteen minutes. Confirm targets are met. Then unfreeze writers.

---

## Rollback decision tree
- **Quality regression**  
  Revert prompt pack or model by flag, then warm cache and verify.  
- **Retriever wrong or mixed answers**  
  Alias index back to previous `docs_vA`. Keys rotate by `INDEX_HASH`.  
- **Hot cost or tail latency**  
  Degrade chain length, return cite only when deadline is tight, enforce global caps.  
- **Duplicate effects**  
  Block writes, enable fences, reconcile receipts, then reopen.

---

## Paste-ready snippets

### Kubernetes service selector flip
```yaml
apiVersion: v1
kind: Service
metadata: { name: wfgy-live }
spec:
  selector: { app: wfgy-blue }   # flip back to blue
  ports: [ { port: 80, targetPort: http } ]
````

### Vector index alias rollback

```bash
vec alias update docs_live --to docs_vA
```

### Feature flag kill switch

```yaml
# opsdeploy/flags/off.yml
flags:
  prompt_pack_vNplus1:
    traffic: { baseline_weight: 1.0, canary_weight: 0.0 }
    abort_rules:
      hard:
        - kind: "global_off"
```

---

## Fast recovery patterns

* **Degrade mode**
  Skip rerank, lower k, or return cite only with links.
* **Sticky routing**
  Keep users pinned to the same arm while the window stabilizes.
* **Single-flight**
  Collapse identical work on misses to avoid stampede.
* **Region by region**
  Roll back one region at a time with audit hashes.

---

## Post-rollback audit

* Verify the pins you expect are actually in logs for every request.
* Confirm cache namespace rotation took effect.
* Validate ΔS, coverage, λ on the warmed gold set.
* Reconcile any side effects created during the incident.
* Open the debug playbook and file the root cause link.

---

## Observability to pin

* Version pins and `INDEX_HASH` on every request.
* ΔS(question,retrieved) and ΔS(retrieved,anchor).
* Coverage and λ states.
* Error rates, 429, queue waits, breaker state.
* Side effect receipts and dedupe decisions.

---

## Common pitfalls

* Rolling back traffic without rotating cache namespace.
* Two writers active during the flip.
* Client only flags that drift from server reality.
* Forgetting to unfreeze jobs after stability returns.
* No captured evidence for the postmortem.

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

