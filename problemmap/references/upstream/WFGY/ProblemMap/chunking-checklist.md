# ✂️ Chunking Checklist — Cutting Documents Without Cutting Meaning  
_A definitive guide to segment size, boundaries, and WFGY stress-tests for error-free retrieval_

---

## 1  Why Chunking Matters

*Embeddings are only as good as the text you feed them.*  
A single bad split (mid-sentence, table row, reference list) injects **semantic orphan** vectors:

* Retrieval returns “high similarity” garbage.  
* ΔS(question, context) spikes > 0.60.  
* LLM hallucinates to fill the missing logic.

---

## 2  Quick Symptoms of Bad Chunking

| Signal | How to Detect | Typical Root |
|--------|---------------|--------------|
| Citations hit page –1 | QA cites header/footer junk | Page footers not stripped |
| Same chunk appears in top-k for unrelated queries | `id` duplication count > 3 | Generic boiler-plate chunk |
| ΔS jumps when k > 5 | Plot ΔS vs. k; curve erratic | Uneven chunk lengths |
| Answer references half-sentence | Chunk split after “and” | Fixed char/token window |

---

## 3  WFGY Chunk Size Guidelines

| Doc Type | Tokens / Chunk | Rationale |
|----------|---------------:|-----------|
| Research paper | **90-120** | Preserve paragraph + citation |
| Software docs | **60-100** | Short API signatures |
| Legal contracts | **80-130** | Clause integrity |
| Chat transcripts | **40-70** | Natural speaker turns |
| Tables / CSV | **Row or group ≤ 30** | Keep relational keys together |

> **Golden Rule:** ΔS(adjacent_chunks) ≤ 0.45  
> **If not**, split or merge until stress drops.

---

## 4  Step-by-Step Chunking Checklist

### 4.1  Pre-Processing

- [ ] Strip headers / footers (`regex: ^Page \d+ of \d+`)  
- [ ] Normalize whitespace, remove soft hyphens (`U+00AD`)  
- [ ] Convert bullets → “• ” to avoid mid-list splits

### 4.2  Boundary Detection

| Method | Tool | When to Use |
|--------|------|-------------|
| Sentence tokenizer | spaCy / Stanza | Most prose |
| Heading regex `^(#+\s|[A-Z][A-Za-z ]+:)$` | Markdown / legal docs | |
| BBMC ΔS spike | WFGY hook | PDFs merged from scans |

Split on boundaries **only** if:

```

ΔS(chunk\_left, chunk\_right) ≥ 0.50  ∧  λ\_observe ∈ {→, ←}

````

### 4.3  Length Normalisation

1. Merge adjacent short chunks until ≥ 40 tokens.  
2. If a merged chunk > 130 tokens, find internal ΔS peak and split there.  
3. Record final size distribution; σ(length) should be ≤ 20 % of mean.

### 4.4  Metadata Tagging

```json
{
  "id": "doc_17_p3_c2",
  "source": "contracts/nda.pdf",
  "pos": 3,
  "λ": "→",
  "ΔS_prev": 0.32,
  "ΔS_next": 0.28
}
````

Store λ\_observe and neighbouring ΔS for runtime filters.

---

## 5  Runtime Stress-Test

| Test                                        | Pass Condition             |
| ------------------------------------------- | -------------------------- |
| **Overlap scan** — Query 5 unrelated topics | Same chunk ID appears ≤ 1× |
| **ΔS histogram** — 500 random chunks        | 95 % ≤ 0.45                |
| **k-sensitivity** — ΔS vs. k plot           | Monotonic ↑ curve          |

If any fail, rerun 4.2–4.3 for offending documents.

---

## 6  Common Pitfalls & Fix Recipes

| Pitfall                    | Fix                                                                               |       |                                   |
| -------------------------- | --------------------------------------------------------------------------------- | ----- | --------------------------------- |
| **Tables split per cell**  | Detect delimiter lines; merge rows; store CSV separate; index columns as metadata |       |                                   |
| **PDF line-break hyphens** | Regex `([a-z])- \n([a-z])` → merge words                                          |       |                                   |
| **Mixed languages**        | Chunk by language span; tag `lang:`; separate embedding models                    |       |                                   |
| **Giant code blocks**      | Cut on \`function                                                                 | class | def\` boundaries; keep ≤ 80 lines |

---

## 7  FAQ

**Q:** *Is a token window (e.g. 512) safe?*
**A:** Only if it aligns with semantic boundaries; fixed windows ignore context.

**Q:** *Do I need sentence splitting and headings?*
**A:** Yes. Dual criteria minimise ΔS spikes and keep retrieval precise.

**Q:** *How many chunks per doc?*
**A:** Irrelevant if ΔS and λ are stable — WFGY focuses on quality, not count.

---

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

