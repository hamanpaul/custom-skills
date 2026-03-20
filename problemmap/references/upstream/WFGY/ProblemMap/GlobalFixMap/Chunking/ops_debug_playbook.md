# RAG ops debug playbook

<details>
  <summary><strong>🧭 Quick Return to Map</strong></summary>

<br>

  > You are in a sub-page of **Chunking**.  
  > To reorient, go back here:  
  >
  > - [**Chunking** — text segmentation and context window management](./README.md)  
  > - [**WFGY Global Fix Map** — main Emergency Room, 300+ structured fixes](../README.md)  
  > - [**WFGY Problem Map 1.0** — 16 reproducible failure modes](../../README.md)  
  >
  > Think of this page as a desk within a ward.  
  > If you need the full triage and all prescriptions, return to the Emergency Room lobby.
</details>


A fast triage guide for incidents after you change chunking, OCR, embedding, or index settings. The goal is to localize the failing layer in minutes and apply a reversible fix.

## Open these first
- Chunk ids and stability: [chunk_id_schema.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/chunk_id_schema.md)
- Title tree numbering: [title_hierarchy.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/title_hierarchy.md)
- Section boundary rules: [section_detection.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/section_detection.md)
- Typed blocks (code, tables, figures): [code_tables_blocks.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/code_tables_blocks.md)
- PDF layout and OCR normalization: [pdf_layouts_and_ocr.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/pdf_layouts_and_ocr.md)
- Rebuild without breaking citations: [reindex_migration.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/reindex_migration.md)
- Eval harness and gates: [eval_rag_precision_recall.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/eval_rag_precision_recall.md)
- Live probes and alerts: [live_monitoring_rag.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/live_monitoring_rag.md)
- Retrieval trace schema: [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)
- Payload contracts: [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)
- Reranker controls: [rerankers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)
- Similarity vs meaning: [embedding-vs-semantic.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)
- Prompt injection: [prompt-injection.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/prompt-injection.md)
- Visual recovery map: [rag-architecture-and-recovery.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)

## Golden acceptance
- ΔS(question, retrieved) ≤ 0.45
- Coverage ≥ 0.70 to the target section
- λ_observe convergent across three paraphrases and two seeds
- Citation offsets within 30 bytes of the ground block

## Symptom to fix map

| Symptom | Quick probe | Likely root | Open this | Minimal fix |
|---|---|---|---|---|
| Coverage drops after index rebuild | Check `index_hash` change with same build id | Bad boot sequence or partial ingest | [reindex_migration.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/reindex_migration.md) | Rebuild with frozen normalizers, fence ingestion, re-point alias after eval pass |
| Citations point to wrong offsets | Validate 30 byte window around cited chunk | OCR or layout normalization drift | [pdf_layouts_and_ocr.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/pdf_layouts_and_ocr.md) | Re-run layout pass and regenerate chunk ids with stable scheme |
| High similarity yet wrong meaning | Compare ΔS to anchor section and to decoy | Metric or analyzer mismatch | [embedding-vs-semantic.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md) | Switch metric or normalize text, add rerank pass |
| Answers flip between reruns | Three paraphrase test and λ flip count | Prompt header reorder or rerank shuffle | [rerankers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md) | Lock header order and rerank seeds, clamp variance |
| Tables or code never cited | Check block `type` in top k | Block typing lost during chunking | [code_tables_blocks.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/code_tables_blocks.md) | Preserve block types, add type-aware rerank feature |
| One doc dominates retrieval | Top k doc entropy and author field | Fragmentation or duplicate shards | [reindex_migration.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/reindex_migration.md) | Rebalance shards, dedupe, enable cross doc rerank |
| Tool loops or JSON fails | Inspect tool schema and free text fields | Contract too loose, injection | [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md), [prompt-injection.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/prompt-injection.md) | Tighten schema, add cite first and role fences |

## Seven step incident routine

1) **Freeze context**  
Capture `build`, `index_hash`, `metric`, `analyzer`, `embed_model`, retriever params, reranker.

2) **Reproduce**  
Run three paraphrases and two seeds. Log ΔS per candidate, λ states, coverage, citation offsets.

3) **Verify structure**  
Check chunk id format from [chunk_id_schema.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/chunk_id_schema.md) and title tree from [title_hierarchy.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/title_hierarchy.md).

4) **Boundary audit**  
Confirm the cited block sits inside one detected section from [section_detection.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/section_detection.md).

5) **Content type audit**  
Ensure tables and code blocks survive extraction per [code_tables_blocks.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/code_tables_blocks.md).

6) **Meaning check**  
If ΔS stays high on every k, suspect metric or index mismatch. Open [embedding-vs-semantic.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md) and [rerankers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md).

7) **Decide fix module**  
Retrieval drift → BBMC with contracts  
Reasoning collapse → BBCR bridge plus BBAM clamp  
Dead ends in long chains → BBPF alternate path

## Copy probes you can paste

**SQL like probe for vector stores**

```sql
-- sample ten queries that failed coverage in the last hour
select qid, question, topk_ids, topk_scores, index_hash, embed_model
from rag_logs
where ts > now() - interval '1 hour'
  and coverage = false
limit 10;
````

**LLM triage prompt**

```
You have TXTOS and WFGY Problem Map.

Given logs for {N} queries with ΔS lists, λ states, citations, and index fingerprints:
1) Name the failing layer: boundary, typing, metric, rerank, OCR, contract.
2) Return exact pages to open next.
3) Propose a minimal reversible fix and a verification test.
Return JSON {layer, pages[], fix, test}.
```

## Rollback and canary

* Roll back if two of the live gates from [live\_monitoring\_rag.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/live_monitoring_rag.md) fire in two consecutive windows.
* Canary new index at five percent. Promote only if coverage and citation accuracy meet gates from [eval\_rag\_precision\_recall.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/eval_rag_precision_recall.md).

## Postmortem template

* Incident summary
* Impact window and scope
* Root layer and evidence
* Fix that shipped and verification
* Prevention items: contracts, monitors, checklists

## Prevention checklist

* Stable chunk ids and title tree are present in every snippet payload
* Cite first prompting and strict data contracts are enforced
* OCR and layout normalizers are frozen for production builds
* Rerank seed and header order are locked during canary
* Live probes for ΔS, λ, coverage, citation accuracy are enabled

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

下一頁建議：**`ProblemMap/GlobalFixMap/Chunking/chunking_checklist.md`**
這一頁是現場交付的簡潔檢查表，會把上面所有規則壓成二十條可勾選項，給運維和標準化使用。
