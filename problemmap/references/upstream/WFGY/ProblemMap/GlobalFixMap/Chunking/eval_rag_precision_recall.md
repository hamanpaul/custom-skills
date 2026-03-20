# RAG precision/recall evaluation

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


A compact, repeatable harness to measure retrieval precision, recall, and coverage after you change chunking, OCR, or indexing. This page also defines ΔS and λ probes so you can gate rollouts with hard numbers.

## Open these first
- Chunk ids and stability: [chunk_id_schema.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/chunk_id_schema.md)  
- Title tree numbering: [title_hierarchy.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/title_hierarchy.md)  
- Section boundary rules: [section_detection.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/section_detection.md)  
- Typed blocks (code, tables, figures): [code_tables_blocks.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/code_tables_blocks.md)  
- PDF, layout, OCR normalization: [pdf_layouts_and_ocr.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/pdf_layouts_and_ocr.md)  
- Traceable results and cite schema: [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)  
- Payload contracts for RAG: [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)  
- Visual recovery map and ops: [rag-architecture-and-recovery.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)

## What this measures

- **Precision@k**: fraction of retrieved snippets among top-k that truly answer the question.  
- **Recall@k**: fraction of all relevant snippets that appear in top-k.  
- **Coverage**: proportion of questions whose final answer can be justified by at least one cited snippet.  
- **Citation accuracy**: percentage of answers where `section_id` and offsets match the gold.  
- **ΔS(question, retrieved)**: semantic distance. Stable ≤ 0.45, transitional 0.40–0.60, risk ≥ 0.60.  
- **λ_observe**: convergence state across paraphrases and seeds.

These metrics tell you if a chunking or index change helps retrieval without breaking traceability.

## Acceptance targets

- Coverage ≥ 0.70 on the project’s gold set.  
- ΔS(question, retrieved) ≤ 0.45 for the cited snippet of each answered item.  
- Citation accuracy ≥ 0.95 for `section_id` + offsets.  
- λ remains convergent on three paraphrases and two seeds.  
- No drop in Recall@k compared with the previous index beyond 2 percent absolute.

---

## Gold set construction

1) **Scope 200–400 items** that span headings, code regions, tables, and prose.  
2) **Write three paraphrases** per question with identical intent.  
3) **Annotate relevant blocks** using canonical ids from [chunk_id_schema.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/chunk_id_schema.md).  
4) **Mark hard negatives** near the true section to test boundary quality.  
5) **Freeze** the canonical text and store byte offsets after normalization from [pdf_layouts_and_ocr.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/pdf_layouts_and_ocr.md).

Gold rows should look like:

```json
{
  "qid": "Q-0137",
  "paraphrases": [
    "How does SCU unlock safety refusals?",
    "Explain symbolic constraint unlock.",
    "SCU: what is it and when to use?"
  ],
  "relevant": ["S.4.2.p.Bk011a", "S.4.2.p.Bk011b"],
  "anchor_section": "S.4.2",
  "negatives": ["S.4.1.p.Bk010", "S.4.3.p.Bk014"]
}
````

---

## Logging schema for evaluation

Your retriever must emit a trace per query. Use the fields defined in [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) and [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md).

```json
{
  "qid": "Q-0137",
  "query": "Explain symbolic constraint unlock.",
  "topk": [
    {"id": "S.4.2.p.Bk011a", "score": 0.83, "offsets": [204611,205279], "type": "prose"},
    {"id": "S.4.1.p.Bk010",  "score": 0.79, "offsets": [198002,199112], "type": "prose"}
  ],
  "ΔS": [0.31, 0.59],
  "λ_state": "→",
  "anchor": "S.4.2",
  "index_hash": "faiss:v3:hnsw:cos",
  "ts": "2025-08-27T12:30:22Z"
}
```

---

## Offline evaluation (index only)

1. Run each paraphrase against the **shadow index**.
2. For each qid, compute:

   * **P\@k**: relevant ids ∩ top-k over k ∈ {1, 3, 5, 10}.
   * **R\@k**: relevant ids covered by top-k.
   * **Anchor hit**: any retrieved id with `section_id == anchor_section`.
   * **ΔS probes** for each retrieved item.
3. Aggregate by content type using `type ∈ {prose, code, table, figure}`.
4. Compare with the **live index** as a baseline and record deltas.

---

## Online shadow evaluation

* Mirror live questions to the shadow index.
* Require **cite-first** answers with the schema from [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md).
* For each answer, verify that at least one citation matches a gold `relevant` id or the `anchor_section`.
* Log ΔS for the chosen citation and the final λ state after reasoning.

---

## Metrics definitions

Let `G(q)` be the set of relevant ids for q. Let `R_k(q)` be the ids in top-k.

* **Precision\@k** = |G(q) ∩ R\_k(q)| / |R\_k(q)|
* **Recall\@k** = |G(q) ∩ R\_k(q)| / |G(q)|
* **Coverage** = fraction of questions where the answer cites at least one element in `G(q)` or any block within `anchor_section`.
* **Citation accuracy** = fraction where both `section_id` and byte offsets overlap the gold within a 30-byte window.
* **Anchor proximity** = average path distance in the title tree from the cited `section_id` to `anchor_section` using rules in [title\_hierarchy.md](https://github.com/github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/title_hierarchy.md).

---

## Pass and fail gates

A shadow index is **eligible for canary** if:

* Coverage ≥ 0.70 on gold.
* Citation accuracy ≥ 0.95.
* ΔS median ≤ 0.40 and 90-pct ≤ 0.55.
* Recall\@5 does not drop more than 2 points absolute vs live.
* λ convergent on ≥ 95 percent of paraphrase triplets.

If any fail, return to chunk boundary checks in [section\_detection.md](https://github.com/github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/section_detection.md) and typed block lifting in [code\_tables\_blocks.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/code_tables_blocks.md).

---

## Diagnosis map

* **High similarity yet wrong meaning** → [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)
* **Order flips across runs** → [Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)
* **Boundary leaks or mixed topics in a chunk** → revisit [section\_detection.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/section_detection.md)
* **Tables or code referenced as plain text** → [code\_tables\_blocks.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/code_tables_blocks.md)
* **OCR drift and offset mismatch** → [pdf\_layouts\_and\_ocr.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/pdf_layouts_and_ocr.md)
* **Index rebuilt, citations break** → [reindex\_migration.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/reindex_migration.md)

---

## Minimal evaluator pseudocode

```python
def score_run(gold, logs, k=5):
    p_hits, r_hits, cov_hits, cite_ok = [], [], 0, 0
    ds_med, ds_90 = [], []

    for q in gold:                         # q has qid, paraphrases, relevant, anchor_section
        items = logs[q.qid]["topk"][:k]
        got = {it["id"] for it in items}
        rel = set(q.relevant)

        prec = len(got & rel) / max(1, len(items))
        rec  = len(got & rel) / max(1, len(rel))
        p_hits.append(prec); r_hits.append(rec)

        ds = logs[q.qid]["ΔS"][:k]
        if ds: ds_med.append(median(ds)); ds_90.append(percentile(ds, 90))

        # coverage and citation accuracy from the final answer's first citation
        ans = logs[q.qid].get("answer_citations", [])
        if ans:
            cited = ans[0]["id"]
            off   = ans[0]["offsets"]
            if cited in rel or section_of(cited) == q.anchor_section:
                cov_hits += 1
            if cited in rel and overlaps(off, gold_offsets(cited)):
                cite_ok += 1

    return {
        "P@k": mean(p_hits),
        "R@k": mean(r_hits),
        "coverage": cov_hits / len(gold),
        "citation_accuracy": cite_ok / len(gold),
        "ΔS_med": median(ds_med) if ds_med else None,
        "ΔS_p90": median(ds_90) if ds_90 else None
    }
```

---

## Common pitfalls

* **Evaluating answers without enforcing cite-first**. You cannot measure coverage reliably. Fix the contract in [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md).
* **Mixing normalizers between builds**. Offsets will not compare. Lock the same whitespace and hyphen rules as in [pdf\_layouts\_and\_ocr.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/pdf_layouts_and_ocr.md).
* **Ignoring content types**. Aggregates hide failures in code or tables. Segment metrics by `type`.
* **k too small for long documents**. Use k ∈ {5, 10} when sections are dense.
* **Comparing across different rerankers**. Pin rerank during offline runs, then test rerankers separately in a controlled A/B.

---

## Copy-paste prompt for LLM-assisted scoring

```
You have TXT OS and the WFGY Problem Map.

Given:
- gold.json: gold questions with {qid, paraphrases[], relevant[], anchor_section}
- logs.jsonl: retriever traces with topk ids, ΔS per item, and answer_citations

Do:
1) Compute P@5, R@5, coverage, citation accuracy.
2) Report ΔS median and p90 for the cited snippet per question.
3) Flag any questions with coverage==0 or ΔS>0.60 and return their qids.
4) Summarize per-type breakdown for {prose, code, table, figure}.

Return compact JSON:
{ "P@5": 0.xx, "R@5": 0.xx, "coverage": 0.xx, "citation_accuracy": 0.xx,
  "ΔS_med": 0.xx, "ΔS_p90": 0.xx, "bad_qids": ["Q-..."], "by_type": {...} }
```

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

要我繼續下一頁就說：**GO live\_monitoring\_rag.md** 或指定別的檔名。
