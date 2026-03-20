# DB Migration Guardrails — OpsDeploy

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


Plan and execute schema or storage migrations with zero data loss and predictable retrieval quality. Applies to primary OLTP stores, vector stores, and search backends.

## Open these first
- Boot order and deploy traps: [Bootstrap Ordering](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md), [Deployment Deadlock](https://github.com/onestardao/WFGY/blob/main/ProblemMap/deployment-deadlock.md), [Pre-Deploy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md)
- Vector index lifecycle: [Vector Index Build & Swap](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/vector_index_build_and_swap.md)
- Version locks: [Version Pinning & Model Lock](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/version_pinning_and_model_lock.md)
- Backpressure and retries: [Rate Limit Backpressure](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/rate_limit_backpressure.md), [Retry Backoff](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/retry_backoff.md)

## Acceptance targets
- Data loss equals 0 verified by row counts and checksums
- Backfill completeness equals 100 percent with reconciliation pass
- ΔS drift between pre and post retrieval ≤ 0.02 on a gold set
- λ remains convergent across two seeds
- Cutover within the planned window with a reversible path

## 60-second checklist
1) **Preflight**  
   Freeze schema in source, create target with explicit charset, collations, index types, vector metric, analyzer. Verify privileges and connection pools.
2) **Dual-write flag**  
   Enable dual writes with idempotency keys. Record `op_id`, `source_rev`, `target_rev`, `index_hash`.
3) **Backfill**  
   Copy in batches with capped concurrency. Validate counts and checksums per table or collection.
4) **Shadow reads**  
   Use [Shadow Traffic Mirroring](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/shadow_traffic_mirroring.md) to compare answers and latency.
5) **Cutover**  
   Flip read source after a clean soak. Keep dual writes for a short tail.
6) **Rollback plan**  
   Document exact steps and TTL for the rollback window with checkpoints.

## Minimal playbook
- **Contracts**: protect schemas with [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md) so producers and consumers fail fast.  
- **Consistency**: validate referential and vector invariants after each batch.  
- **Indexing**: for vectors rebuild offline and swap atomically. See [Vector Index Build & Swap](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/vector_index_build_and_swap.md).  
- **Traffic**: rate limit heavy stages and prefer maintenance windows.  
- **Metrics**: log `migrated_rows`, `checksum_ok`, `dual_write_fail`, `ΔS_diff`, `λ_state`, `cutover_ms`.

## Common pitfalls → fix
- Metric mismatch after cutover produces wrong-meaning hits  
  → confirm vector metric and normalization. See [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md).  
- Read timeouts during backfill  
  → isolate reader replicas or use read-only mode during the heaviest phase. See [Read-Only Mode](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/read_only_mode_and_maintenance_window.md).  
- Dual-write divergence  
  → enforce idempotency keys and reconcile with drift queries. See [Idempotency & Dedupe](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/idempotency_dedupe.md).

## Escalate
Abort and rollback if data checksums diverge or ΔS drift exceeds 0.05 on the gold set for longer than 15 minutes. Publish an incident update and run a focused postmortem with [Postmortem & Regression Tests](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/postmortem_and_regression_tests.md).

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

