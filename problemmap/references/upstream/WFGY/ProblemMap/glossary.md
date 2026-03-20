# 📚 Glossary — Terms, Symbols, and Short Definitions

> **Quick Nav**  
> [Retrieval Playbook](./retrieval-playbook.md) ·
> [Patterns](./patterns/README.md) ·
> [Eval](./eval/README.md)

---

## Core instruments

- **ΔS (delta-S)** — *Semantic stress.* `ΔS = 1 − cos(I, G)` where `I` is item embedding, `G` is ground/anchor.  
  Thresholds: `<0.40` stable · `0.40–0.60` transitional · `≥0.60` high risk.

- **λ_observe** — *Layered observability state.*  
  Symbols: `→` convergent · `←` divergent · `<>` recursive · `×` chaotic.

- **E_resonance** — *Coherence indicator.* Rolling mean of |residual| under BBMC; rising E with high ΔS ⇒ apply BBCR/BBAM.

---

## Repair operators (WFGY modules)

- **BBMC** — *Boundary-Bounded Memory Chunks.* Reduce semantic residue vs anchors; align chunks/sections with tasks.  
- **BBPF** — *Branch-Bounded Prompt Frames.* Explore multiple semantic paths safely; stabilize context windows.  
- **BBCR** — *Break-Before-Crash Reset.* Detect collapse, insert bridge node, restart cleanly.  
- **BBAM** — *Attention Modulation.* Reduce variance in attention to avoid entropy melt on long contexts.

---

## Retrieval, ranking & prompting

- **RRF (Reciprocal Rank Fusion)** — Fuse ranks from multiple retrievers via `1/(k + rank)`.  
- **MMR (Maximal Marginal Relevance)** — Diversify candidates balancing relevance and novelty.  
- **BM25** — Sparse lexical scoring for exact term match; strong for code/IDs.  
- **HyDE** — Hypothetical document expansion; creates a synthetic query/doc to improve recall.  
- **Cross-encoder reranker** — Jointly encodes `[query ⊕ doc]` for precision@k gains.

---

## Patterns (named failure modes)

- **SCU (Symbolic Constraint Unlock)** — Model merges sources or violates “cite-then-explain” schema. Fix: per-source fences + locked schema.  
- **Query Parsing Split** — Dense and sparse retrievers use different analyzers/tokenizers; hybrid breaks.  
- **Vectorstore Fragmentation** — Index contains “ghost” gaps; facts exist but never retrieved; fix shard/id audits.  
- **Memory Desync** — State flips between sessions/tabs; require `mem_rev`+`mem_hash`.  
- **Role Drift** — Multi-agent persona swap; tag agent IDs and lock via BBCR.

---

## Multi-agent

- **Agent boundary** — Contract that limits what an agent can read/write; prevents overwrite.  
- **ΔS peer check** — Measures divergence between agents’ plans to catch conflicts early.

---

## Data & ops

- **Gold set** — Small set (10–50) of realistic Q/A with citations; used for CI (recall@50, nDCG@10, ΔS).  
- **Traceability** — Provenance from answer → prompt → citations → chunks → source file.

---

## Notation quickies

- `I` — item (retrieved chunk) embedding; `G` — ground/anchor embedding.  
- `‖B‖ ≥ B_c` — collapse threshold on residual magnitude (BBCR).  
- *Convergent λ* — layer is stable across paraphrases; *divergent λ* — layer is drifting.

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

