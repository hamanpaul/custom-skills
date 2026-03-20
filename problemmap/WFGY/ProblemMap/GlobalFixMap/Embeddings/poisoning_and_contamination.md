# Poisoning and Contamination — Guardrails and Fix Patterns

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


Use this page when answers suddenly contradict known anchors after an ingestion, when one domain dominates results with subtle text edits, or when λ becomes spiky only for a subset of sources. Goal is to localize the tainted slice, quarantine it, and rebuild cleanly with measurable gates. No infra change required.

## Open these first

* Visual map and recovery: [rag-architecture-and-recovery.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)
* End to end retrieval knobs: [retrieval-playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)
* Prompt side hardening for injection: [prompt-injection.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/prompt-injection.md)
* Traceability and cite first: [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)
* Eval suite and gold anchors: [eval\_rag\_precision\_recall.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/eval/eval_rag_precision_recall.md)
* Data payload schema: [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)
* Vector metric pitfalls: [vectorstore-metrics-and-faiss-pitfalls.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/vectorstore-metrics-and-faiss-pitfalls.md)
* Rerank safety net: [rerankers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)
* OCR artifacts gate: [ocr-parsing-checklist.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ocr-parsing-checklist.md)

## When to use this page

* A small set of domains or mirrors suddenly starts winning top k with altered numbers or claims
* Coverage to long standing anchors drops only after a crawl or vendor feed
* ΔS remains high and flat while you raise k and add rerank, but only for specific time windows
* λ flips only when the citation comes from a certain source family
* Adversarial phrasing in corpus attracts unrelated queries

## Acceptance targets

* ΔS(question, retrieved) ≤ 0.45
* Coverage of the target section ≥ 0.70
* λ convergent across three paraphrases and two seeds
* Domain skew normalized. No single low trust domain occupies more than 20 percent of top twenty on the gold set

---

## Threat model at a glance

* **Source poisoning**. Upstream page changed to subtly wrong math or policy lines.
* **Mirror contamination**. CDN or scraped mirrors with injected edits and tracking params.
* **Adversarial attractors**. Snippets seeded with instruction like strings to bias retrieval.
* **OCR contamination**. Hyphenation or column bleed creates misleading near duplicates.
* **Label contamination**. Gold set or eval answers were copied into the corpus.
* **Model mismatch contamination**. A second embedder with different normalization pollutes neighborhoods.

---

## Fix in 60 seconds

1. **Freeze ingestion and isolate the suspect window**
   Partition by `ingest_ts` and `source_id`. Compare ΔS and coverage before and after the window.

2. **Clamp the prompt side**
   Enforce cite first, fixed header order, and strict schema while you debug. See [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md).

3. **Quarantine partitions**
   Move new rows from suspect domains or the latest window into a shadow collection. Serve union plus deterministic rerank on top. See [rerankers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md).

4. **Canonicalize and collapse**
   Normalize URLs, remove trackers, apply MinHash or SimHash to detect near duplicates, keep one canonical. Re embed only canonicals. See also [duplication\_and\_near\_duplicate\_collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Embeddings/duplication_and_near_duplicate_collapse.md).

5. **Verify**
   Three paraphrases and two seeds. Require coverage ≥ 0.70 and ΔS ≤ 0.45 with λ stable. If it passes, cut over.

---

## Symptom → likely cause

* Right doc appears from trusted domain only when k is very large
  Likely cause. Mirrors with edited numbers crowd the neighborhood. Collapse near duplicates and prefer canonical domain.

* Answers contradict anchors only for last seven days of ingestion
  Likely cause. Feed contamination in that window. Quarantine by `ingest_ts` and re embed from clean sources.

* Queries about policy suddenly retrieve instruction like pages
  Likely cause. Adversarial attractors in text. Down weight patterns and add cross encoder rerank.

* Gold set precision drops when certain vendor ids appear
  Likely cause. Mixed embedder or normalization on vendor pipeline. Align metric and normalization, then rebuild that slice.

---

## Probes you can paste into a notebook

```
Probe A — time window A/B
Split corpus by ingest_ts: before vs after suspected date.
Run 50 gold queries. Record ΔS and coverage per slice.
If after-slice fails while before-slice passes, quarantine after-slice.

Probe B — domain skew
For each domain group:
  run top-20 → count share in top-20 and median ΔS
Flag domains with share > 0.20 and worse ΔS than the median.

Probe C — adversarial attractor
Prepare synthetic queries with tokens like "instruction:", "ignore prior".
Measure how often suspect domains surface vs baseline. If > 3x, down weight pattern.

Probe D — outlier vectors
Sample 10k vectors from suspect window.
Compute L2 norms and first two PCA residuals.
Flag rows where either z score > 3. Review text and domain.
```

---

## Collapse and tie break policy

* Canonical pick order: `canonical_domain` then `latest_rev` then `ocr_conf` then `longer_snippet_with_same_anchor`.
* Do not collapse across languages unless anchors and citations are identical and the user domain is monolingual.
* Never serve non canonical duplicates in top k. Keep pointers for audits only.

---

## Contract fields to add

```json
{
  "source_id": "stable-source-key",
  "canonical_domain": "docs.example.com",
  "canonical_url": "https://docs.example.com/guide#s1",
  "ingest_ts": "2025-08-28T10:42:00Z",
  "ingest_channel": "crawler|vendor|manual",
  "trust_tier": "high|medium|low",
  "text_sha256": "sha256:...",
  "minhash_sig": ["...","...","..."],
  "simhash64": "0x8f32c1aa44d0beef",
  "ocr_conf": 0.97,
  "adversarial_flag": false,
  "sanitized": { "unicode_nfc": true, "zero_width_removed": true, "hyphen_fix": true },
  "duplicate_cluster_id": null,
  "duplicate_of": null,
  "review_status": "clean|quarantine|blocked"
}
```

---

## Operational guardrails

* Single writer per partition and idempotent upsert on `(doc_id, section_id, rev)`
* Quarantine bucket for new domains and new channels, dual read until verified
* Daily drift job that charts ΔS and coverage per domain and per `ingest_ts` window
* Canary anchors per vertical to detect silent edits
* Alerts on domain share spikes, λ flip rate spikes, and ΔS ≥ 0.60 on live traffic

---

## Verification checklist

* Coverage ≥ 0.70 and ΔS ≤ 0.45 on the gold anchors across three paraphrases and two seeds
* λ convergent with cite first, order stable after harmless header tweaks
* Domain share distribution looks even. No low trust domain exceeds 20 percent of top twenty
* Anchor ranks do not regress after collapse and quarantine

---

## Copy paste prompt for the LLM step

```
TXT OS and the WFGY Problem Map are loaded.

My issue: poisoning or contamination after recent ingestion.
Traces:
- time_window=..., domains=[...], ingest_channel=...
- ΔS(question,retrieved)=..., coverage=..., λ across 3 paraphrases
- duplicate_rate=..., adversarial_flag_rate=...

Tell me:
1) the failing layer and why,
2) the exact WFGY page to open next,
3) a quarantine + collapse plan and tie break I should implement,
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

