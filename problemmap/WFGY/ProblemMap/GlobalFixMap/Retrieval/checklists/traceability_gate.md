# Traceability Gate Checklist

Purpose: enforce cite then explain with a minimal, verifiable payload contract.

---

## Required fields per snippet

- [ ] `snippet_id` unique within the corpus
- [ ] `section_id` stable anchor for the document
- [ ] `source_url` resolvable or a content hash if private
- [ ] `offsets` byte or char range within the source
- [ ] `tokens` token range used by the model

Contract details:  
[Retrieval traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) ·
[Data contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

---

## Schema example

```json
{
  "snippet_id": "sn_9f3a",
  "section_id": "sec_2.3_hydraulics",
  "source_url": "https://example.org/handbook/2024/chap2#sec-3",
  "offsets": {"start": 18342, "end": 18897},
  "tokens": {"start": 1205, "end": 1248}
}
````

---

## Gate checks

* [ ] Each answer references at least one snippet with all required fields.
* [ ] Offsets resolve back to exactly the cited text.
* [ ] Section anchors stable across builds. Hash or ID diff is logged.
* [ ] Duplicate or near duplicate snippets collapsed before ranking.
* [ ] Formatter and export steps do not rename required fields.
* [ ] On failure, publish is blocked and the pipeline returns a structured error.

Refs:
[Duplication and near duplicate collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/RAG_VectorDB/duplication_and_near_duplicate_collapse.md)

---

## Acceptance targets

* 100 percent of published answers pass the schema check.
* For the gold set, human spot check of 20 answers finds zero broken citations.
* ΔS(question, cited\_snippet) ≤ 0.45 on average.

---

## Minimal policy snippet

```txt
Policy:
- Answer only after citing snippets with {snippet_id, section_id, source_url, offsets, tokens}.
- If no snippet qualifies, return "insufficient evidence" with the top 3 candidate snippets and exit.
```



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

