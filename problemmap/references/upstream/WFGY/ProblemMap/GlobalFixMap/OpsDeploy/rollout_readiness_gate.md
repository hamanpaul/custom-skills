# Rollout Readiness Gate — OpsDeploy

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


A pre-ship gate that decides ship or no-ship using measurable targets.  
Use this page to wire a single checkpoint in CI or CD that blocks risky changes before they hit users.

## What this page is
- A compact, provider-agnostic checklist that verifies retrieval, reasoning, orchestration, and infra order.
- Direct jumps to the exact Problem Map fixes.
- Copy-paste templates you can drop into CI or a workflow runner.

## When to use
- Before any production rollout that changes retrievers, embeddings, chunkers, prompts, model versions, or tool schemas.
- After index rebuilds, data migrations, or secret rotation.
- When answers recently started flipping between runs or a canary looks unstable.

## Open these first
- Visual map and recovery: [RAG Architecture & Recovery](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)  
- Retrieval knobs: [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)  
- Traceability schema: [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)  
- Snippet and citation contract: [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)  
- Embedding vs meaning: [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)  
- Hallucination and chunk boundaries: [Hallucination](https://github.com/onestardao/WFGY/blob/main/ProblemMap/hallucination.md)  
- Long chains and entropy: [Context Drift](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md), [Entropy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/entropy-collapse.md)  
- Logic collapse and recovery: [Logic Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/logic-collapse.md)  
- Prompt injection fences: [Prompt Injection](https://github.com/onestardao/WFGY/blob/main/ProblemMap/prompt-injection.md)  
- Boot order and deploy traps: [Bootstrap Ordering](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md), [Deployment Deadlock](https://github.com/onestardao/WFGY/blob/main/ProblemMap/deployment-deadlock.md), [Pre-Deploy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md)  
- Live ops after ship: [Live Monitoring for RAG](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/live_monitoring_rag.md), [Debug Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/debug_playbook.md)

## Acceptance targets for ship
- ΔS(question, retrieved) ≤ 0.45 on three paraphrases.  
- Coverage of target section ≥ 0.70.  
- λ remains convergent across two seeds.  
- E_resonance stays flat on long windows.  
- No schema drift in citation fields `{snippet_id, section_id, source_url, offsets, tokens}`.

## 60-second gate checklist
1) **Warmup and invariants**  
   - Secrets present. Version lock consistent. `INDEX_HASH` matches retriever build.  
   - Boot order ok. See [Bootstrap Ordering](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md).

2) **RAG quality probe**  
   - Run a 20–40 item gold set.  
   - Score with: [RAG Precision/Recall Eval](https://github.com/onestardao/WFGY/blob/main/ProblemMap/eval/eval_rag_precision_recall.md) and [Semantic Stability Eval](https://github.com/onestardao/WFGY/blob/main/ProblemMap/eval/eval_semantic_stability.md).  
   - Fail if any target above is missed.

3) **Hallucination fence**  
   - Enforce cite-then-explain. Verify with [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) and [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md).  
   - Block if citations are missing or cross-section reuse appears.

4) **Index and metric sanity**  
   - If nearest neighbors look right but meaning is wrong, rebuild. See [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md).  
   - If recall varies with HyDE or BM25, lock the two-stage query and rerank. See [Query Parsing Split](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_query_parsing_split.md).  
   - Fragmented stores: see [Vectorstore Fragmentation](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_vectorstore_fragmentation.md).

5) **Chain stability**  
   - If chains exceed safe length and entropy rises, split and bridge. See [Context Drift](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md) and [Entropy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/entropy-collapse.md).

6) **Decision**  
   - Ship if all targets pass on two seeds and three paraphrases.  
   - Else block and open the linked fix page.

## CI gate template you can paste

```yaml
# opsdeploy/rollout_readiness_gate.yml
gates:
  warmup_invariants:
    checks:
      - secrets_present: true
      - index_hash_matches: true
      - version_lock: strict
      - boot_order_ok: true  # see Bootstrap Ordering
  rag_quality:
    evals:
      - name: rag_precision_recall
        spec: ProblemMap/eval/eval_rag_precision_recall.md
        min_coverage: 0.70
      - name: semantic_stability
        spec: ProblemMap/eval/eval_semantic_stability.md
        max_delta_s: 0.45
        paraphrases: 3
        seeds: 2
  hallucination_fence:
    schema: ProblemMap/data-contracts.md
    require_citations: true
  index_metric_sanity:
    actions_on_fail:
      - open: ProblemMap/embedding-vs-semantic.md
      - open: ProblemMap/patterns/pattern_query_parsing_split.md
      - open: ProblemMap/patterns/pattern_vectorstore_fragmentation.md
decision:
  on_fail: block_rollout
  on_pass: proceed_to_canary
artifacts:
  - logs/delta_s.json
  - logs/coverage.json
  - logs/lambda_states.json
````

## Escalation map

* Targets fail after re-run. Open [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md) and rebuild with the semantic chunking checklist.
* First call in a fresh deploy crashes. Open [Pre-Deploy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md).
* Live traffic unstable. Wire probes from [Live Monitoring for RAG](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/live_monitoring_rag.md) and follow the [Debug Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/debug_playbook.md).

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

