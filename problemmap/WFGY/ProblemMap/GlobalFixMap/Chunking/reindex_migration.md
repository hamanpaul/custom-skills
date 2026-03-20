# Reindex migration

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


A safe, auditable procedure to rebuild chunks and embeddings after edits while keeping references stable. This page shows how to preserve ids, remap offsets, and roll out without breaking citations or downstream apps.

## Open these first
- Canonical chunk ids: [chunk_id_schema.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/chunk_id_schema.md)
- Title tree and numbering: [title_hierarchy.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/title_hierarchy.md)
- Section boundary rules: [section_detection.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/section_detection.md)
- Typed blocks (code, tables, figures): [code_tables_blocks.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/code_tables_blocks.md)
- PDF layouts and OCR: [pdf_layouts_and_ocr.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/pdf_layouts_and_ocr.md)
- Traceable retrieval results: [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)
- Payload contracts for RAG: [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)
- Visual recovery map: [rag-architecture-and-recovery.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)

## Acceptance targets
- Old citations keep working via a migration map. Redirect coverage ≥ 0.995 on a 200 sample set.
- Byte offset drift ≤ 0.5 percent of file length for unchanged paragraphs.
- ΔS(question, retrieved) stays ≤ 0.45 on a stable gold set after switchover.
- No duplicate live ids after cutover. Id collision rate = 0.
- Shadow read A/B returns identical citations on ≥ 0.98 of queries. The rest must report a mapped replacement with a reason.

---

## What causes drift

- Edits change paragraph boundaries and shift byte offsets.
- OCR or layout normalization tweaks alter tokenization.
- Title renumbering moves sections and cascades into child ids.
- Table and code detection improves, lifting text into typed blocks.

You cannot freeze content, so you must **freeze identity**. The goal is stable ids, traceable offsets, and deterministic remaps.

---

## Deterministic id strategy

Use the schema in [chunk_id_schema.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/chunk_id_schema.md). In short:

- **Prefix** encodes doc and section path, not raw titles.  
- **Type tag** for `prose | code | table | figure | caption`.  
- **Local key** derives from a normalized content fingerprint:
  - lowercase prose without spaces and punctuation for the first 96 bytes,
  - or a code line fingerprint ignoring indentation and trailing spaces,
  - or a caption fingerprint trimmed to the first sentence.

Ids remain stable when wording changes slightly. Large edits cause a new id, and we map the old one to the new target.

---

## Migration table

Produce a table per document version `v → v'`:

```json
{
  "doc_id": "DOC.wfgy.2025.08",
  "from_version": "v12",
  "to_version": "v13",
  "mappings": [
    {
      "old_block_id": "S.2.1.p.Bk013",
      "new_block_id": "S.2.1.p.Bk013",
      "move": "shift",
      "old_off": [204455, 205122],
      "new_off": [204612, 205279],
      "conf": 0.997
    },
    {
      "old_block_id": "S.3.4.p.Bk044",
      "new_block_id": "S.3.4.p.Bk044a",
      "move": "split",
      "old_off": [309221, 310998],
      "new_parts": [
        { "id": "S.3.4.p.Bk044a", "off": [309240, 310001] },
        { "id": "S.3.4.p.Bk044b", "off": [310002, 311110] }
      ],
      "conf": 0.982
    },
    {
      "old_block_id": "S.1.2.p.Bk007a",
      "new_block_id": "S.1.2.p.Bk007",
      "move": "merge",
      "old_off": [14511, 15133],
      "new_off": [14511, 15892],
      "conf": 0.973
    }
  ]
}
````

Store this JSON next to the index for lookup at query time and for bulk rewrites.

---

## Offset alignment

1. Build a **canonical text** for `v` and `v'` as in [pdf\_layouts\_and\_ocr.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/pdf_layouts_and_ocr.md).
2. For each old block, choose the top candidate in `v'` by content fingerprint plus shingled Jaccard.
3. Run a local LCS on a ±1k window to compute an offset transform.
4. If overlap ≥ 0.85 and the local edit distance ≤ threshold, mark **shift**.
5. If multiple disjoint segments match, mark **split**. If several old blocks map to one new, mark **merge**.

Emit `conf` from the alignment score so low confidence entries go to manual review or staged rollout only.

---

## Rollout plan

* **Index v' in shadow**. Keep the old index live.
* **Shadow read** each live query against v' and compare citations.
* **Threshold gate**. If mismatch rate ≤ 2 percent and all mismatches have valid migration rows, proceed.
* **Canary switch** on 10 percent of traffic. Monitor ΔS, coverage, and error logs.
* **Full cutover**. Keep the old index for rollback until two cycles of stable metrics.
* **Garbage collect** orphaned vectors only after you confirm no lookups reference them.

See RAG ops in [rag-architecture-and-recovery.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md).

---

## Redirect strategies

**At query time**

* When a citation contains an `old_block_id`, look up the migration row.
* Replace with `new_block_id` and reformat offsets for the current canonical text.
* Mark the answer with a short audit note so downstream can log migrations.

**Batch rewrite**

* Walk your citation store and apply the migration table once.
* Prefer this for analytics backfills and static sites.

All clients should accept both `id` and `id_prev` fields in the citation payload. Define that in [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md).

---

## Pseudocode

```python
def build_migration(doc_v, doc_vp):
    old_blocks = load_blocks(doc_v)      # ids, text, offsets
    new_blocks = load_blocks(doc_vp)

    idx = make_shingle_index(new_blocks) # token shingles → candidate blocks
    rows = []

    for ob in old_blocks:
        cands = idx.lookup(ob.text)
        best, score = best_candidate(ob, cands)

        if score < 0.60:
            rows.append(unmapped(ob))    # manual review
            continue

        lcs = local_align(ob.text, best.text)
        if lcs.coverage >= 0.85:
            rows.append(shift(ob, best, lcs))
        elif lcs.parts == 2 and lcs.coverage_sum >= 0.85:
            rows.append(split(ob, best, lcs))
        else:
            rows.append(merge_or_new(ob, best, lcs))

    return { "mappings": rows }
```

---

## Tests to put in CI

* **Small edit**. Change one sentence in a paragraph. Expect a shift with `conf ≥ 0.99`.
* **Split paragraph**. Insert a subtitle to cut a paragraph in two. Expect a split row with two new parts.
* **Merge paragraphs**. Remove a line break. Expect a merge with a longer `new_off`.
* **Title renumber**. Increment section numbers only. Expect ids stable via the section path rules from [title\_hierarchy.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/title_hierarchy.md).
* **OCR improvement**. Better hyphen repair. Expect shifts only, no id churn for prose in [pdf\_layouts\_and\_ocr.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/pdf_layouts_and_ocr.md).

---

## Common pitfalls and fixes

* **Id churn on minor edits**
  Your fingerprint is too sensitive. Trim to the first stable 96 bytes and strip punctuation. See [chunk\_id\_schema.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/chunk_id_schema.md).

* **Offset drift exceeds limit**
  You changed normalization rules between runs. Lock the same whitespace and hyphen policies as in the previous build.

* **Citations to code lines break**
  You forgot typed blocks. Ensure code and tables are lifted as blocks per [code\_tables\_blocks.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Chunking/code_tables_blocks.md).

* **Canary flips answers**
  Recheck ΔS and coverage probes, then pin rerank order for the canary group. See [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md).

---

## Copy paste prompt for an LLM audit

```
You have TXT OS and the WFGY Problem Map.

Task: Given two versions of the same document (v, v'):
1) Build a migration table mapping old block ids and offsets to new ones.
2) Mark each row as shift, split, merge, or unmapped with a confidence score.
3) Return a summary with redirect coverage and a list of high risk rows.

Return JSON:
{
  "coverage": 0.xx,
  "high_risk": ["S.3.4.p.Bk044", ...],
  "mappings": [ ... as specified in reindex_migration.md ... ]
}
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

要我繼續下一頁就說：**GO eval\_rag\_precision\_recall.md** 或指定別的檔名。
