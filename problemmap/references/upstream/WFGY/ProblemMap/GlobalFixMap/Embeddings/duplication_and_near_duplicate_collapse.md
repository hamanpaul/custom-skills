# Duplication and Near Duplicate Collapse — Guardrails and Fix Patterns

<details>
  <summary><strong>🧭 Quick Return to Map</strong></summary>

<br>

  > You are in a sub-page of **Embeddings**.  
  > To reorient, go back here:  
  >
  > - [**Embeddings** — vector representations and semantic search](./README.md)  
  > - [**WFGY Global Fix Map** — main Emergency Room, 300+ structured fixes](../README.md)  
  > - [**WFGY Problem Map 1.0** — 16 reproducible failure modes](../../README.md)  
  >
  > Think of this page as a desk within a ward.  
  > If you need the full triage and all prescriptions, return to the Emergency Room lobby.
</details>


Use this page when repeated or slightly varied snippets crowd the index, citations look repetitive, or the right section is hidden behind many near copies. The goal is to detect exact and near duplicates before or during indexing, collapse them to a canonical record, and verify with ΔS, coverage, and λ.

## Open these first

* Visual map and recovery: [rag-architecture-and-recovery.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)
* End to end retrieval knobs: [retrieval-playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)
* Traceability and cite first: [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)
* Snippet schema and audits: [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)
* Chunking checklist: [chunking-checklist.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/chunking-checklist.md)
* Vector metric pitfalls: [vectorstore-metrics-and-faiss-pitfalls.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/vectorstore-metrics-and-faiss-pitfalls.md)
* Rerank safety net: [rerankers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)

## When to use this page

* Many hits look the same or cite the same wording with different URLs
* Boilerplate or footer text dominates top k
* Small edits produce new vectors that push anchors down
* OCR produces minor variants that inflate recall but hurt precision
* Crawls from mirrors or CDNs duplicate the same document

## Acceptance targets

* ΔS(question, retrieved) ≤ 0.45
* Coverage of the target section ≥ 0.70
* λ remains convergent across three paraphrases and two seeds
* Duplicate inflation reduced by at least 90 percent on the gold set

---

## Failure signatures → likely cause

* Ten snippets from similar URLs push the correct anchor to rank 8 or worse
  Likely cause. No canonicalization or collapse of mirrors and tracking params.

* Boilerplate repeats on every page and often ranks ahead of substance
  Likely cause. No boilerplate mask at chunk time and no duplicate filter.

* OCR corpus looks noisy with hyphenation and line wrap variants
  Likely cause. OCR cleanup not applied before hashing or embedding.

* Same paragraph exists in multiple language folders with small changes
  Likely cause. No language aware duplicate detection and no cluster level tie break.

---

## Fix in 60 seconds

1. **Canonicalize first**
   Normalize URL and source keys. Remove tracking parameters. Pick a canonical per mirror set.

2. **Fingerprint text before embedding**
   Store `text_sha256` on normalized text. Add a near duplicate signature such as MinHash or SimHash. Refuse ingest if `text_sha256` already exists for the same `(source_id, section_id, rev)`.

3. **Collapse near duplicates**
   Cluster by MinHash or SimHash then by cosine on vectors inside each cluster. Keep one canonical. Mark others as `duplicate_of`.

4. **Prefer a deterministic tie break**
   Choose the latest `rev`, highest `ocr_conf`, canonical domain, and longest snippet that still respects the section boundary.

5. **Verify**
   Three paraphrases and two seeds. Require coverage ≥ 0.70 and ΔS ≤ 0.45. Count unique sources in top k.

---

## Canonicalization rules

* Normalize URL path. Lowercase host. Strip UTM and session params. Map known mirrors to a single `source_id`.
* Normalize text. Unicode NFC. Collapse whitespace. Fix OCR soft hyphens. Preserve code blocks and citations that users will query.
* Keep section anchors stable, for example `parent_id` plus `section_id`.

---

## Fingerprints to store

* **Exact**
  `text_sha256` on the final normalized `text`.

* **Near duplicate text**

  * MinHash over 5 or 7 word shingles with LSH buckets.
  * SimHash 64 bit over character 5 grams.

* **Near duplicate vector**
  Cosine threshold inside a small candidate set, for example neighbors at k equals 50 per section.

---

## Collapse policy

* Form clusters from near duplicate candidates.
* Select a canonical item per cluster using stable priority: `canonical_domain` then `latest_rev` then `ocr_conf` then `longer_snippet_with_same_anchor`.
* Write only the canonical vector to the retriever collection.
* Keep `duplicate_of` pointers and `duplicate_cluster_id` for audits.
* Surface non canonical variants only in UI expansion, never in the top k pool.

---

## Contract fields to add

```json
{
  "canonical_domain": "docs.example.com",
  "canonical_url": "https://docs.example.com/guide#a1",
  "duplicate_cluster_id": "dup:9e44c...",
  "duplicate_of": null,
  "text_sha256": "sha256:...",
  "minhash_sig": ["...","...","..."],
  "simhash64": "0x8f32c1aa44d0beef",
  "ocr_conf": 0.97,
  "boilerplate_mask": "footer,nav,ads",
  "collapse_policy": "canonical_domain>latest_rev>ocr_conf>longer_snippet"
}
```

---

## Probes you can paste into a notebook

```
Probe A — duplicate rate
Sample 10k snippets. Group by text_sha256. Report pct with count>1. Target < 2 percent after collapse.

Probe B — near duplicate clustering
Run MinHash LSH → sample 100 clusters → within each cluster compute median pairwise cosine. If median > 0.90, collapse is safe.

Probe C — anchor displacement
Before and after collapse run 50 gold queries. Record anchor rank and ΔS. Expect anchor rank to improve or hold and ΔS to drop.

Probe D — boilerplate dominance
Measure fraction of top-20 tokens coming from masked regions. If > 0.20, improve boilerplate mask and re-chunk.
```

---

## Common edge cases and fixes

* **Code examples duplicated across pages**
  Preserve code fences. Add a feature flag to down weight boilerplate code unless the query is code scoped.

* **Press releases syndicated across domains**
  Use `canonical_domain` mapping and collapse clusters across domains.

* **Multilingual near matches**
  Do not collapse across languages by default. Only collapse if anchors and citations are identical and the user domain is monolingual.

* **Versioned docs**
  Keep the latest `rev` as canonical unless the query explicitly requests an older version.

---

## Verification checklist

* Duplicate inflation drops by at least 90 percent on the gold set
* Coverage ≥ 0.70 and ΔS ≤ 0.45 across three paraphrases and two seeds
* λ convergent and top k unique source count increases
* No anchor regression after collapse on the held out suite

---

## Copy paste prompt for the LLM step

```
TXT OS and the WFGY Problem Map are loaded.

My issue: duplicates and near duplicates crowd top-k and hide the correct anchor.
Traces:
- duplicate_rate=...
- cluster_examples=[...]
- ΔS(question,retrieved)=..., coverage=..., λ across 3 paraphrases

Tell me:
1) the failing layer and why,
2) the exact WFGY page to open next,
3) a minimal collapse policy and tie break that I should implement,
4) a verification plan to reach coverage ≥ 0.70 and ΔS ≤ 0.45.
Use BBMC, BBCR, BBPF, BBAM when relevant.
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

