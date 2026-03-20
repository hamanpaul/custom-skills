# Tokenization and Casing — Guardrails and Fix Pattern

<details>
  <summary><strong>🧭 Quick Return to Map</strong></summary>

<br>

  > You are in a sub-page of **RAG_VectorDB**.  
  > To reorient, go back here:  
  >
  > - [**RAG_VectorDB** — vector databases for retrieval and grounding](./README.md)  
  > - [**WFGY Global Fix Map** — main Emergency Room, 300+ structured fixes](../README.md)  
  > - [**WFGY Problem Map 1.0** — 16 reproducible failure modes](../../README.md)  
  >
  > Think of this page as a desk within a ward.  
  > If you need the full triage and all prescriptions, return to the Emergency Room lobby.
</details>


Use this page when **retrieval fails because the text was chunked or embedded with inconsistent tokenization or casing rules**.  
This is common when corpus ingestion applies one tokenizer (e.g. sentencepiece, BPE) and queries use another, or when upper/lowercase mismatches create drift.

---

## Open these first

- Visual map and recovery: [RAG Architecture & Recovery](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)  
- Chunking checklist: [chunking-checklist.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/chunking-checklist.md)  
- Retrieval traceability: [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)  
- Embedding vs meaning: [embedding-vs-semantic.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)  

---

## Core acceptance

- Corpus and query tokenizers are identical.  
- ΔS(question, retrieved) ≤ 0.45, stable under three paraphrases.  
- λ remains convergent across casing variants.  
- Coverage ≥ 0.70 for the target section.  

---

## Typical breakpoints and the right fix

- **Different tokenizers for corpus vs query**  
  → Rebuild index with unified tokenizer. See [chunking-checklist.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/chunking-checklist.md).  

- **Casing drift** (retrieval fails if query has capitalized or accented terms)  
  → Apply consistent lowercasing or case-fold normalization before embedding.  

- **Unicode variants** (fullwidth vs halfwidth, accents vs base letters)  
  → Normalize text with NFC/NFKC before chunking.  

- **Mixed language tokenization** (CJK vs Latin vs Indic split differently)  
  → Align multilingual tokenizer to match model embedding assumptions.  

---

## Fix in 60 seconds

1. **Check tokenizer logs**  
   Sample corpus and query text, run through the same tokenizer, compare token IDs.

2. **Case-fold**  
   Apply `.lower()` or Unicode case-fold to both corpus and queries before embedding.

3. **Normalize Unicode**  
   Use `unicodedata.normalize("NFKC", text)` to ensure consistency.

4. **Re-index if drift found**  
   If tokenization differs, rebuild embedding index after enforcing preprocessing rules.

---

## Copy-paste probe

```python
import unicodedata

def normalize_and_lower(text):
    return unicodedata.normalize("NFKC", text).lower()

sample = "Résumé vs Resume"
print(normalize_and_lower(sample))
# → "resume vs resume"
````

Target: queries and corpus map to the same normalized form.

---

## Common gotchas

* Chunked with sentencepiece but queries fed through default BPE → mismatch.
* Different language casing (Turkish dotted i, German ß) → normalize before embed.
* Multilingual queries that mix scripts → ensure same tokenizer config across corpora.

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

