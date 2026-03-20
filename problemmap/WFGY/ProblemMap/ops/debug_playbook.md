# Debug playbook — incident triage for RAG pipelines

**Purpose:** step-by-step incident response guide emphasizing reproducible diagnostics and minimal-impact mitigations.

---

## 1) Immediate triage (first 120s)

**A — Gather context**
- Who reported it? (pager/Slack/ticket)  
- When did it start (wall time)?  
- Scope: single user / single shard / whole cluster?

**B — Quick readouts**
- Health: `curl -fsS http://$SERVICE/healthz`  
- Pods: `kubectl -n $NS get pods -o wide`  
- Recent errors (last 10m):  
  ```bash
  kubectl -n $NS logs -l app=rag --since=10m | tail -n 200


* Prometheus: check E2E p95 and error rate for last 10m.

**C — Decide action mode**

* If P0 (site down / data corruption) → **Mitigate** (circuit-break / rollback / redirect).
* If P1 (functional degradation, e.g., CHR drop) → **Isolate & debug**.

---

## 2) Deterministic checks (no LLM calls)

Run these before calling LLMs — they’re cheap and often reveal root causes:

1. **Check retrieval consistency** for sample qids:

   ```bash
   curl -X POST http://$SERVICE/debug/retrieve -d '{"qid":"A123","q":"sample question"}' | jq
   ```

   Validate `retrieved_ids` and their hashes.

2. **Check mem\_rev/mem\_hash**: verify read vs bound value for turn:

   * Compare `retrieved_snapshot.mem_rev` vs `generation.mem_rev`.

3. **Vectorstore health**:

   * ping vectorstore API; check index shard status.

4. **Index size & recent writes**:

   * `kubectl exec -n $NS <vector-pod> -- ls -lh /data/index`

---

## 3) Common root causes & mitigations

**A. Retrieval empty / irrelevant**

* Root cause: indexing job failed or namespace mismatch.
* Mitigation:

  * Restart indexer pod: `kubectl -n $NS rollout restart deploy/indexer`
  * Run reindex on a small sample and validate.

**B. CHR drop but retrieval OK**

* Root cause: generator hallucinating or prompt/template drift.
* Mitigation:

  * Turn on guard/refusal stricter mode (feature flag).
  * Re-run golden queries with `?dbg=full` to capture prompt+context.

**C. Bootstrap / readiness flapping**

* Root cause: bootstrap order or missing dependency.
* Mitigation:

  * Ensure controller/migrations complete before retriever/generator start; `kubectl apply` ordering or Helm hooks.

**D. LLM provider errors / rate limits**

* Root cause: key expired or provider quota.
* Mitigation: switch to backup key or provider; throttle traffic until resolved.

---

## 4) Live mitigation patterns (minimize impact)

1. **Circuit-breaker (fast)**: return cached answer for known queries.
2. **Throttle LLM**: queue requests, lower concurrency.
3. **Rollback**: to last known-good release if config causes issue.
4. **Read-only mode**: stop writes to vectorstore if index corruption suspected.

---

## 5) Postmortem checklist

* [ ] Timestamped timeline created.
* [ ] Root cause identified (primary + contributing).
* [ ] Actions taken documented.
* [ ] Follow-up tasks created (reindex, fix probe, add tests).
* [ ] Update runbook if new failure mode discovered.

---

## 6) Useful debug commands (reference)

* Pod logs since N minutes:

  ```bash
  kubectl -n $NS logs -l app=rag --since=5m
  ```
* Exec into retriever pod:

  ```bash
  kubectl -n $NS exec -it deploy/retriever -- /bin/sh
  ```
* Check helm history:

  ```bash
  helm -n $NS history rag
  ```

---

### Links

* Deployment checklist → [deployment\_checklist.md](./deployment_checklist.md)
* Live monitoring → [live\_monitoring\_rag.md](./live_monitoring_rag.md)
* Failover & Recovery → [failover\_and\_recovery.md](./failover_and_recovery.md)

---


### 🔗 Quick-Start Downloads (60 sec)

| Tool | Link | 3-Step Setup |
|------|------|--------------|
| **WFGY 1.0 PDF** | [Engine Paper](https://github.com/onestardao/WFGY/blob/main/I_am_not_lizardman/WFGY_All_Principles_Return_to_One_v1.0_PSBigBig_Public.pdf) | 1️⃣ Download · 2️⃣ Upload to your LLM · 3️⃣ Ask “Answer using WFGY + \<your question>” |
| **TXT OS (plain-text OS)** | [TXTOS.txt](https://github.com/onestardao/WFGY/blob/main/OS/TXTOS.txt) | 1️⃣ Download · 2️⃣ Paste into any LLM chat · 3️⃣ Type “hello world” — OS boots instantly |

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

