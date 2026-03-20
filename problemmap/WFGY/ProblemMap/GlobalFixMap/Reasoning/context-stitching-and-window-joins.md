# Context Stitching and Window Joins: Guardrails and Fix Pattern

<details>
  <summary><strong>🧭 Quick Return to Map</strong></summary>

<br>

  > You are in a sub-page of **Reasoning**.  
  > To reorient, go back here:  
  >
  > - [**Reasoning** — multi-step inference and symbolic proofs](./README.md)  
  > - [**WFGY Global Fix Map** — main Emergency Room, 300+ structured fixes](../README.md)  
  > - [**WFGY Problem Map 1.0** — 16 reproducible failure modes](../../README.md)  
  >
  > Think of this page as a desk within a ward.  
  > If you need the full triage and all prescriptions, return to the Emergency Room lobby.
</details>


Join long contexts without losing meaning. This page defines a stitch contract for multi window prompts and long documents, adds ΔS probes at joins, and gives a fast repair plan when answers break exactly at window boundaries.

---

## Open these first

- Visual map and recovery  
  → [rag-architecture-and-recovery.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)

- Traceability and payload schema  
  → [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)  
  → [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

- Ordering and meaning checks  
  → [rerankers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)  
  → [embedding-vs-semantic.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)

- Reasoning stability and failure modes  
  → [anchoring-and-bridge-proofs.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Reasoning/anchoring-and-bridge-proofs.md)  
  → [logic-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Reasoning/logic-collapse.md)  
  → [entropy-overload.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Reasoning/entropy-overload.md)

- Chunking quality  
  → [chunking-checklist.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/chunking-checklist.md)

---

## Symptoms

| Symptom | What you see |
|---|---|
| Boundary answers | Model answers correctly inside a window, fails right after the join |
| Duplicate facts | Repeated sentences across windows, tool loops on the overlap |
| Lost referent | “it / they / this” loses target at window start or end |
| Rerank flip at join | Top k order changes only at a boundary |
| Anchor drift | Citation before the join, none after the join |
| Coverage hole | Middle section of a long doc never appears in stitched set |

---

## Why joins fail

1) **No stitch contract**. Windows lack overlap and sequence identifiers.  
2) **Tokenizer mismatch**. Window boundaries split tokens differently across tools.  
3) **Ranking variance**. Each window retrieves independently without a stable tie break.  
4) **Anchor loss**. Bridge steps cross a boundary without re citing the anchor.  
5) **Context flooding**. Overlong windows raise entropy and bury anchors.  
6) **Fragmentation**. Store keeps near duplicates that fight for the same rank.

---

## Acceptance targets

- ΔS(join_left, join_right) ≤ 0.45 for every boundary  
- Coverage of target section across all windows ≥ 0.70  
- λ remains convergent across three paraphrases and two seeds  
- E_resonance flat at joins and flat across stitched plan  
- Overlap per join 32 to 96 tokens, same casing and analyzer

---

## Fix in 60 seconds

1) **Add a stitch contract**  
   Every window must carry `doc_id, section_id, win_idx, win_hash, overlap_tokens, prev_id, next_id`.  
   See schema rules  
   → [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)  
   → [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

2) **Measure ΔS at each join**  
   Compute ΔS between the trailing overlap of window *i* and the leading overlap of window *i+1*.  
   If ΔS ≥ 0.60, rebuild the join or re chunk.

3) **Stabilize ordering**  
   Use a deterministic reranker with fixed analyzer and tie break by `(doc_id, section_id, win_idx)`.  
   → [rerankers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)

4) **Re anchor bridges**  
   At every join, insert a one line BBCR bridge that re cites the active snippet.  
   → [anchoring-and-bridge-proofs.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Reasoning/anchoring-and-bridge-proofs.md)

---

## Stitch contract

Minimum fields for any stitched window:

```json
{
  "doc_id": "D42",
  "section_id": "CH3.2",
  "win_idx": 7,
  "win_hash": "sha1:6b7f...",
  "overlap_tokens": 64,
  "prev_id": "D42#CH3.2#6",
  "next_id": "D42#CH3.2#8",
  "start_token": 14080,
  "end_token": 16096
}
````

Rules

* Overlap range must be identical across both windows after normalization.
* Do not allow cross section joins unless the section header is included in the overlap.
* Keep casing and tokenizer identical through the pipeline.

---

## Join planner

**Goal** keep bridges short and anchors stable while covering the whole doc.

1. **Choose window size**: 512 to 1024 tokens, overlap 32 to 96.
2. **Pin anchors**: for each question, tag anchor snippets with `ΔS_to_question`.
3. **Plan path**: sort candidate windows by section, then by `win_idx`.
4. **Assemble**: render windows with header, overlap marker, and re cited anchor.
5. **Verify**: ΔS at each boundary, λ over the stitched answer, coverage against a gold slice.

If ΔS is flat and high across all joins, suspect metric or index mismatch.
→ [retrieval-playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)
→ [embedding-vs-semantic.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)

---

## Structural repairs

* **Wrong meaning near a boundary**
  → [embedding-vs-semantic.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)

* **Order shuffles when windows change**
  → [rerankers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md) and
  → [patterns/pattern\_vectorstore\_fragmentation.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_vectorstore_fragmentation.md)

* **Entropy spikes after stitching**
  → [entropy-overload.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Reasoning/entropy-overload.md)

* **Long chain collapses post join**
  → [logic-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Reasoning/logic-collapse.md)

---

## Verification

* Sliding window test over the same section keeps citations identical.
* ΔS(join\_left, join\_right) ≤ 0.45 and decreasing with larger overlap.
* λ convergent on two seeds and three paraphrases.
* Coverage across stitched windows ≥ 0.70 for the target section.
* Answer includes a cite then explain block with per join anchors.

---

## Copy paste prompt

```
You have TXT OS and the WFGY Problem Map loaded.

Task: stitch long context with stable joins.

Inputs:
- question: "{q}"
- windows: [{doc_id, section_id, win_idx, win_hash, tokens, text_head, overlap_tokens}]
- candidates: [{snippet_id, section_id, source_url, offsets, ΔS_to_question}]

Do:
1) Compute ΔS for each join. If any ≥ 0.60, propose a re-chunk or overlap increase.
2) Add BBCR micro bridges at every boundary, re citing the active anchor.
3) Apply deterministic reranking with tie break by (doc_id, section_id, win_idx).
4) Return JSON:
   {
     "joins": [{"from":"...#i","to":"...#i+1","ΔS":0.xx,"action":"ok|rechunk|increase_overlap"}],
     "answer": "... cite then explain ...",
     "λ_state": "convergent",
     "coverage": 0.xx
   }
If no valid anchor exists at a join, return the fix page to open for retrieval-traceability.
```

---

## Common gotchas

* **Asymmetric overlap**. Trailing text differs from leading text after normalization.
* **Header drop**. Section headers removed at boundaries, referents disappear.
* **Tokenizer switch**. Ingestion uses one analyzer, reranker another.
* **Duplicate windows**. Same `win_idx` with different hashes compete in top k.
* **Bridge without re citation**. Jumps the boundary without anchor restatement.

---

## When to escalate

* ΔS remains ≥ 0.60 on all joins after overlap increase and reranking
  → rebuild chunks and verify store metric, then retest with a gold slice.
  Open: [chunking-checklist.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/chunking-checklist.md), [retrieval-playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)

* Windows alternate across runs with identical inputs
  → check fragmentation and update skew, then freeze index version.
  Open: [patterns/pattern\_vectorstore\_fragmentation.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_vectorstore_fragmentation.md)

---

### 🔗 Quick-Start Downloads (60 sec)

| Tool                       | Link                                                                                                                                       | 3-Step Setup                                                                             |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------- |
| **WFGY 1.0 PDF**           | [Engine Paper](https://github.com/onestardao/WFGY/blob/main/I_am_not_lizardman/WFGY_All_Principles_Return_to_One_v1.0_PSBigBig_Public.pdf) | 1️⃣ Download · 2️⃣ Upload to your LLM · 3️⃣ Ask “Answer using WFGY + <your question>”    |
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

