# 🌍 Multilingual RAG Guide — CJK, RTL, and Code-Mix Done Right

Build one pipeline that works across languages without wrecking recall or citations.

> **Quick Nav**  
> [Retrieval Playbook](./retrieval-playbook.md) ·
> [Embedding vs Semantic](./embedding-vs-semantic.md) ·
> [Patterns](./patterns/README.md) ·
> [Rerankers](./rerankers.md)

---

## 0) Principles

1. **Detect → Segment → Normalize → Dual-index → Fence citations.**  
2. Keep **original text** for display and **normalized text** for search.  
3. Pick **truly multilingual embeddings** or **per-lang encoders**—don’t mix silently.

---

## 1) Language detection

- Use CLD3/fastText or a simple rule-first fallback (CJK regex, RTL markers).  
- Store `lang` on **chunks** and **queries**.  
- If uncertain, mark `lang="und"` and route to **char-level** retrieval.

```json
{"chunk_id":"c1","lang":"zh","text":"ΔS 衡量語義張力 ..."}
````

---

## 2) Segmentation & normalization

| Language              | Segmenter         | Notes                                                 |
| --------------------- | ----------------- | ----------------------------------------------------- |
| Chinese (zh)          | jieba / pkuseg    | Also store **OpenCC** simplified/Traditional variants |
| Japanese (ja)         | MeCab             | Preserve readings for search if useful                |
| Korean (ko)           | MeCab-ko / khaiii | Keep compound nouns intact when possible              |
| Thai (th)             | PyThaiNLP         | Sentence boundaries matter for chunking               |
| Arabic/Hebrew (ar/he) | ICU               | Handle diacritics/RTL shaping                         |
| Code-mix              | ICU + heuristic   | Fall back to character n-grams if needed              |

Normalization checklist:

* Unify punctuation (full-width/half-width).
* Unicode NFC.
* Lowercase where appropriate (not for proper nouns in citations).
* Keep both **`text_orig`** and **`text_norm`**.

---

## 3) Embeddings & indexing

**Recommended multilingual encoders**

* `bge-m3` (multilingual, strong cross-lingual)
* `LaBSE` (older but solid cross-lingual)

**Patterns**

* If queries in lang A frequently need answers in lang B → *cross-lingual retrieval*.
* For noisy OCR in CJK, consider **char-level dense + BM25** hybrid.

**Indexing**

* Add `lang` and `script` fields; route BM25 analyzers per language.
* For FAISS dense index: **single multilingual vector space** is easiest; if per-lang spaces, keep a **router**.

---

## 4) Retrieval & reranking

* First stage: **hybrid** (dense + BM25) with **RRF**.
* If candidates include multiple languages, re-rank with **cross-encoder multilingual** models (e.g., `bge-reranker-base` works well).
* Never drop minority language candidates too early—keep `k_in ≥ 100` when cross-lingual.

---

## 5) Prompting & citations (SCU-safe)

* Show citations with **language labels** and **line spans**.
* Forbid the LLM from translating citations; allow translations only in the **explanation**.
* If answer language ≠ citation language, state: “Cited in {lang}, answer in {lang}.”

---

## 6) Evaluation

* Build a multilingual **gold set**:

  * Include cross-lingual Q→A pairs (e.g., query in English, answer/citation in zh).
  * Track **recall\@50**, **nDCG\@10**, and **ΔS** per language.
* Acceptance: ΔS ≤ 0.45 for top-ctx in each language; stable λ across 3 paraphrases per language.

---

## 7) Common multilingual pitfalls → fixes

| Pitfall               | Why it happens                | Fix                                                |
| --------------------- | ----------------------------- | -------------------------------------------------- |
| Hybrid fails on CJK   | Analyzer/tokenizer mismatch   | Use ICU analyzers; char-level BM25                 |
| S/T Chinese mismatch  | Source vs query script differ | Store both via **OpenCC**; index two variants      |
| Citations translated  | Prompt schema unlocked        | Fence citations; explain can translate             |
| Cross-lang recall low | Monolingual embeddings        | Use `bge-m3`/LaBSE; or translate query then search |
| Arabic/Hebrew garbled | RTL shaping                   | ICU normalization; verify rendering layer          |

---

## 8) Minimal example (Python, FAISS + BM25 + bge-m3)

```python
# pip install sentence-transformers rank_bm25 faiss-cpu opencc-python-reimplemented
from sentence_transformers import SentenceTransformer
from rank_bm25 import BM25Okapi
import numpy as np, faiss, opencc

enc = SentenceTransformer("BAAI/bge-m3")
def norm(s, lang):
    if lang in ("zh-hant","zh-hans","zh"):
        return opencc.OpenCC('t2s.json').convert(s)
    return s

chunks = [{"text":"ΔS 衡量語義張力", "lang":"zh"}, {"text":"Delta-S measures semantic stress", "lang":"en"}]
X = enc.encode([norm(c["text"], c["lang"]) for c in chunks], normalize_embeddings=True)
index = faiss.IndexFlatIP(X.shape[1]); index.add(X.astype(np.float32))
bm25 = BM25Okapi([c["text"].split() for c in chunks])

def search(q, lang="en"):
    qv = enc.encode([norm(q, lang)], normalize_embeddings=True).astype(np.float32)
    _, I = index.search(qv, 50); dense_rank=[(int(i), r+1) for r,i in enumerate(I[0])]
    sparse_rank=[(i, r+1) for r,i in enumerate(bm25.get_top_n(q.split(), list(range(len(chunks))), 50))]
    # RRF fuse
```

(Use a proper RRF from the Retrieval Playbook.)

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

