# Chunk Alignment — Guardrails and Fix Patterns

<details>
  <summary><strong>🧭 Quick Return to Map</strong></summary>

<br>

  > You are in a sub-page of **Retrieval**.  
  > To reorient, go back here:  
  >
  > - [**Retrieval** — information access and knowledge lookup](./README.md)  
  > - [**WFGY Global Fix Map** — main Emergency Room, 300+ structured fixes](../README.md)  
  > - [**WFGY Problem Map 1.0** — 16 reproducible failure modes](../../README.md)  
  >
  > Think of this page as a desk within a ward.  
  > If you need the full triage and all prescriptions, return to the Emergency Room lobby.
</details>


Make the model cite the exact evidence. This page gives you a reliable way to align chunks to semantic anchors, so retrieval points at the right spans and citations survive through generation.

References you may want open already:  
[RAG Architecture & Recovery](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md) ·
[Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md) ·
[Chunking Checklist](https://github.com/onestardao/WFGY/blob/main/ProblemMap/chunking-checklist.md) ·
[Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) ·
[Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md) ·
[Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)

---

## Acceptance targets

- ΔS(question, retrieved) ≤ 0.45  
- Anchor coverage ≥ 0.70 for the cited spans  
- Citation precision ≥ 0.85 and recall ≥ 0.75  
- λ stays convergent across 3 paraphrases and 2 seeds

If ΔS stays in the 0.40 to 0.60 band and coverage is low, the index is probably misaligned. Rebuild with this page.

---

## Symptoms → exact fix

| Symptom | Likely cause | Open this fix |
|---|---|---|
| High similarity but the cited span is near the answer, not on it | window cut ignores section headers and anchors | [Chunking Checklist](https://github.com/onestardao/WFGY/blob/main/ProblemMap/chunking-checklist.md) |
| Correct section id, wrong offsets | tokenizer or analyzer mismatch between write and read | [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md) |
| Same answer oscillates across two adjacent chunks | stride too large, missing overlap contract | [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md) |
| Coverage good offline, poor online | fragmented store or partial ingestion | [pattern_vectorstore_fragmentation.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_vectorstore_fragmentation.md) |
| Good chunk, bad generation | cite then explain missing in the prompt schema | [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) |

---

## Anchor method that never lies

You need a ground anchor per question. Each anchor is the minimal span that must be cited.

**Anchor fields**

- `section_id` stable across rebuilds  
- `snippet_id` unique within section  
- `offsets` `{start_token, end_token}` in the write-time tokenizer  
- `anchor_text` for human audit  
- `hash` over `section_id + snippet_id + offsets + anchor_text`

Contract spec for your pipeline:  
[Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

---

## How to align chunks to anchors

1) **Normalize the analyzer**  
Same lowercasing, unicode, punctuation, and stopword policy across write and read. If you change analyzers, invalidate and rebuild.

2) **Choose window and stride**  
Start with window 350 to 700 tokens, stride 30 to 60 percent of window. Increase stride if anchors often cross boundaries.

3) **Fence by structure**  
Reset window starts at structural cues like `h1..h3`, list starts, code fences, or paragraph breaks. This keeps semantic units together.

4) **Pin anchors after chunking**  
After chunks are built, re-map each anchor to an owning chunk. When an anchor spans two chunks, create a stitch record or adjust stride.

5) **Write the trace fields**  
Every retrieved item must carry `section_id`, `snippet_id`, `offsets`, `tokens`, `index_hash`.  
See: [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)

---

## PDF, HTML, and code specifics

- **PDF**  
Use logical reading order, not x-y positions. Collapse hyphenation. Treat figure captions as separate units. Reset at headings and table boundaries.

- **HTML**  
Strip boilerplate. Fence at `h2/h3`, `li`, and `pre`. Merge short sibling blocks to avoid tiny chunks.

- **Code**  
Chunk by symbol boundaries and docstrings. Keep signature plus the first paragraph together. Never split examples from the API they explain.

---

## A minimal rebuild checklist

- Same tokenizer family for write and read.  
- Window and stride validated on 40 to 120 gold items.  
- Anchor coverage ≥ 0.70 and citation precision ≥ 0.85.  
- ΔS falls below 0.45 for the majority after rebuild.  
- `index_hash` updated and logged in retrieval results.

---

## Alignment test you can run today

1) For each gold item, compute ΔS between the retrieved text and the anchor text.  
2) Compute coverage of cited spans against the anchor offsets.  
3) Compare to a decoy section with the same size and style. If ΔS is close for anchor and decoy, chunk again.

See the eval recipes:  
[Retrieval Evaluation Recipes](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Retrieval/retrieval_eval_recipes.md)

---

## Pseudocode: chunk and map anchors

```python
# Pseudocode only
def chunk(doc, window=512, stride=256, fences=None, analyzer="lc"):
    toks = tokenize(doc, analyzer)          # write-time tokenizer
    boundaries = structure_fences(doc, toks, fences=fences)
    chunks = []
    i = 0
    while i < len(toks):
        start = nearest_left_fence(i, boundaries)
        end = min(start + window, len(toks))
        text = detokenize(toks[start:end])
        chunks.append({"start": start, "end": end, "text": text})
        i = start + stride
    return chunks

def map_anchor_to_chunk(anchor, chunks):
    spans = []
    for c in chunks:
        if not (anchor["end"] <= c["start"] or anchor["start"] >= c["end"]):
            spans.append({"snippet_id": id_of(c), "offsets": [
                max(anchor["start"], c["start"]),
                min(anchor["end"], c["end"])
            ]})
    return spans
````

Store the mapping result inside your index metadata for audit and to power coverage scoring.

---

## Copy-paste prompt to audit alignment

```
You have TXT OS and the WFGY Problem Map loaded.

Input:
- question: "<q>"
- retrieved: {section_id, snippet_id, offsets, text}
- anchor: {section_id, snippet_id, offsets, text}
- decoy: {section_id, snippet_id, offsets, text}

Tasks:
1) Check cite-then-explain is followed.
2) Report ΔS(question, retrieved) and ΔS(retrieved, anchor) with short notes.
3) Compute anchor coverage from offsets.
4) If ΔS ≥ 0.60 or coverage < 0.70, propose the minimal rebuild step referencing:
   chunking-checklist, retrieval-playbook, data-contracts, retrieval-traceability.
Return a compact JSON: { "ΔS": ..., "coverage": ..., "why": "...", "next_fix": "..." }.
```

---

## When to escalate

* You rebuild chunking and analyzers but ΔS remains high and coverage low.
  Open: [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)

* Online runs drift after a deploy despite passing offline.
  Open: [Bootstrap Ordering](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md) and [Pre-Deploy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md)

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

要繼續下一頁請回「GO 5」。
