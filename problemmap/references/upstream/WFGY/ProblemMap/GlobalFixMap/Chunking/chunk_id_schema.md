# Chunk ID Schema: Deterministic addressing for citations and reranking

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


A practical spec to mint stable `chunk_id` values that survive re-ingest, reruns, and light edits. Use it to make citations auditable and to keep retrieval traces consistent across stores and seeds.

## Open these first
- Traceability and why-this-snippet: [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)
- Snippet schema and payload locks: [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)
- Build the section tree: [title_hierarchy.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/title_hierarchy.md), [section_detection.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/section_detection.md)
- Reindex and migrations: [reindex_migration.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/reindex_migration.md)

## Acceptance targets
- `chunk_id` is unique within the corpus and recomputable from source plus deterministic rules.
- Citation hit rate ≥ 0.90 on a gold set after re-ingest.
- ΔS(question, retrieved) ≤ 0.45 and λ stays convergent across 3 paraphrases when citing by `chunk_id`.
- Reindex migration preserves a one-to-one mapping for at least 0.95 of chunks, with redirects for the rest.

---

## Design goals

1) **Deterministic**  
   The same input text and layout produce the same `chunk_id`, regardless of store.

2) **Localizable**  
   Given a `chunk_id`, you can open the document and jump to the exact span without embeddings.

3) **Diff-tolerant**  
   Small edits should not re-key the entire document. Local block changes only.

4) **Human-inspectable**  
   IDs are compact but interpretable during manual audits.

---

## Canonical fields

Every chunk record must carry these fields in your payload. See the full schema in [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md).

```json
{
  "chunk_id": "docA|r=8c1e9a02|s=1.2.3|p=002|b=007",
  "section_id": "1.2.3",
  "source_url": "https://example.com/guide.pdf",
  "offsets": [12345, 12980],
  "tokens": 365,
  "hash": "sha1:cafebabe…",
  "block_type": "paragraph|table|code|formula",
  "anchor": "first salient assertion in this chunk"
}
````

* `offsets` are byte or character positions in the canonical text layer.
* `anchor` is used by cite-then-explain prompts and for ΔS triangulation.

---

## The `chunk_id` format

**Recommended canonical string**

```
<doc_uid>|r=<rev8>|s=<sect_path>|p=<page3>|b=<block3>
```

* `doc_uid`
  Stable document identifier. Prefer a repository or CMS id. If unknown, use `sha1_8(normalize(source_url))`.

* `rev8`
  Eight hex chars from `sha1(normalize_text(doc))`. Changes only when the whole document text meaningfully changes.

* `sect_path`
  Dot path from the section tree like `2.4.1`. If unknown, set to `p<page3>` and still fill `p`.

* `page3`
  Zero padded page number when page concepts exist. For HTML-only docs, set `000`.

* `block3`
  Zero padded index of the block within the section or page after applying block-aware splitting.

**Human alias**
If you also want a readable alias for logs, you may attach `#s02-04-01#p002-b007`. The canonical id remains the pipe form above.

---

## How to compute the parts

1. **doc\_uid**

   * If your source has a stable id, use it.
   * Else compute `doc_uid = sha1_8(canonicalize_url(source_url))`. Canonicalization removes querystrings except version pins and normalizes scheme and host.

2. **rev8**

   * Compute `sha1_8(normalize_text(doc))`.
   * `normalize_text` collapses whitespace, strips page headers and footers, and fixes OCR line breaks. See [pdf\_layouts\_and\_ocr.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/pdf_layouts_and_ocr.md).

3. **sect\_path**

   * Build the hierarchy with heading detection. See [title\_hierarchy.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/title_hierarchy.md) and [section\_detection.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/section_detection.md).
   * If headings are unreliable, synthesize `sect_path` as `page-major` like `p002` and keep `p` identical.

4. **block3**

   * Within each section or page, enumerate blocks after **block-aware** splitting. Paragraphs, tables, code, formulas are atomic. See [code\_tables\_blocks.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/code_tables_blocks.md).
   * Use zero padding to 3 digits for stability in lexicographic sort.

5. **offsets**

   * Record start and end offsets in the canonical text layer for trace and repair. Never omit.

---

## Examples

**PDF with headings**

```
doc_uid = "whitepaperX"
rev8    = "8c1e9a02"
sect    = "3.2"
page    = 014
block   = 006

chunk_id = "whitepaperX|r=8c1e9a02|s=3.2|p=014|b=006"
```

**HTML article without reliable headings**

```
doc_uid = sha1_8(url) = "b17a2c55"
rev8    = "e1d0aa91"
sect    = "p005"   // synthesized
page    = 005
block   = 004

chunk_id = "b17a2c55|r=e1d0aa91|s=p005|p=005|b=004"
```

**Notebook with code cells**

```
doc_uid = "nb_231107"
rev8    = "9af03bcd"
sect    = "2.1"
page    = 000
block   = 012
block_type = "code"

chunk_id = "nb_231107|r=9af03bcd|s=2.1|p=000|b=012"
```

---

## Collision and drift policy

* **Hash collision**
  If a collision is detected for `doc_uid|r`, extend `rev8` to `rev12`. Log a warning and continue.

* **Minor edits**
  If text within a section changes but the section path and block indices remain, keep `chunk_id`. Update `hash` and `offsets`.

* **Section renumbering**
  If `sect_path` changes due to new headings, create a redirect map from old ids to new ids during reindex. See [reindex\_migration.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/reindex_migration.md).

* **OCR repairs**
  If OCR fixes alter page counts, keep `doc_uid` and `rev` but synthesize `sect_path` using old to new page mapping and emit redirects.

---

## 60-second validator

Pass when the following hold on a 20-chunk sample:

* `uniq(chunk_id) == len(sample)`
* Sorting by `chunk_id` equals the natural reading order inside each section or page.
* `citation_match ≥ 0.90` comparing `offsets` to ground truth citations.
* Stable under re-ingest of the same source: all `chunk_id` values unchanged.

---

## Copy-paste generator (pseudocode)

```python
def make_chunk_id(doc_uid, rev8, sect_path, page_no, block_ix):
    page3  = f"{int(page_no):03d}"
    block3 = f"{int(block_ix):03d}"
    return f"{doc_uid}|r={rev8}|s={sect_path}|p={page3}|b={block3}"
```

Use this builder only after your pipeline has produced the section tree and block enumeration.

---

## What to do when audits fail

* Top-k returns the right area but citations miss the span
  → Rebuild the section tree and verify offsets. Open: [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md).

* Hybrid reranker prefers chunks from adjacent sections
  → Tighten block boundaries. Open: [code\_tables\_blocks.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/code_tables_blocks.md).

* Many ids change after a small doc edit
  → Check `rev8` computation and block numbering stability. Open: [reindex\_migration.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/reindex_migration.md).

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

要我繼續下一頁就說：**GO title\_hierarchy.md**
