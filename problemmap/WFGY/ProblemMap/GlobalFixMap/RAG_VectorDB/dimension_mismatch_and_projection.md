# Dimension Mismatch and Projection — Guardrails and Fix Pattern

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


Use this page when **embeddings break because vector dimensions do not match the store or runtime index**.  
This happens if you switch models (e.g. 1536 → 1024 dims) or if the store silently coerces vectors.

---

## Open these first

- Visual map and recovery: [RAG Architecture & Recovery](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)  
- Embedding drift vs semantic mismatch: [embedding-vs-semantic.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)  
- Chunking and index alignment: [chunking-checklist.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/chunking-checklist.md)  
- Retrieval knobs: [retrieval-playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)  

---

## Core acceptance

- All embeddings in a store share identical dimension length.  
- ΔS(question, retrieved) ≤ 0.45 after dimension fix.  
- Coverage ≥ 0.70 across three paraphrases.  
- λ remains convergent when switching embedding models.  

---

## Typical breakpoints and the right fix

- **Store rejects insert** with `dimension mismatch` error.  
  → Rebuild index with correct `dim` parameter.  

- **Store accepts but pads/truncates silently**.  
  → Causes random retrieval drift.  
  → Explicitly validate vector length on every ingestion.  

- **Multiple models used** → Some 1024-d, some 1536-d vectors.  
  → Project to common dimension space with PCA/linear map.  

- **Migration between providers** (e.g. OpenAI → Cohere).  
  → Use adapter layer: re-embed corpus or apply projection matrix.  

---

## Fix in 60 seconds

1. **Probe corpus**  
   Sample 100 embeddings, assert uniform `len(vec)`.

2. **Detect hidden coercion**  
   Compute L2 norm variance. If unusually high, store is truncating.

3. **Apply projection**  
   If mixing models, fit PCA/linear map on overlap dataset.  

4. **Rebuild index**  
   Always reset store with explicit `dim=…` before production.  

---

## Example projection (Python, pseudo)

```python
from sklearn.decomposition import PCA
import numpy as np

# Fit projection from 1536-d → 1024-d
pca = PCA(n_components=1024)
pca.fit(corpus_vecs_1536)

projected = pca.transform(new_vecs_1536)
````

Target: after projection, ΔS variance ≤ 0.05 vs original gold set.

---

## Common gotchas

* Store CLI defaults to wrong dimension (FAISS index built at 768, model outputs 1024).
* Silent fallback in wrappers (LangChain auto-pads zeros).
* Mixing sparse + dense without explicit projection weights.

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

