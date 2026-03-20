# Context Drift — Long Reasoning Chain Instability

<details>
  <summary><strong>🧭 Quick Return to Map</strong></summary>

<br>

  > You are in a sub-page of **MemoryLongContext**.  
  > To reorient, go back here:  
  >
  > - [**MemoryLongContext** — extended context windows and memory retention](./README.md)  
  > - [**WFGY Global Fix Map** — main Emergency Room, 300+ structured fixes](../README.md)  
  > - [**WFGY Problem Map 1.0** — 16 reproducible failure modes](../../README.md)  
  >
  > Think of this page as a desk within a ward.  
  > If you need the full triage and all prescriptions, return to the Emergency Room lobby.
</details>


When reasoning spans 20–40 hops or more, attention shifts accumulate and context drifts.  
This page explains how to diagnose λ divergence, stabilize reasoning chains, and repair collapsed context.

---

## When to use this page
- Long reasoning plans (~20+ steps) start with logic but later flip or contradict.  
- Multi-agent workflows repeat or miss earlier facts.  
- Citations remain valid, but final answers drift from original question.  
- λ flips divergent after harmless paraphrases.  
- Answers alternate between runs with identical inputs.

---

## Core acceptance targets
- ΔS(question, retrieved) ≤ 0.45  
- Retrieval coverage ≥ 0.70 for target section  
- λ remains convergent across three paraphrases  
- Chain length stable up to 40 hops without collapse  
- Entropy variance remains bounded in mid-to-late steps  

---

## Structural fixes

- **Three-paraphrase probe**  
  Re-ask the same question three ways. Log ΔS and λ at each hop.  
  If λ flips, schema is unstable.

- **Clamp with BBAM**  
  Apply variance clamp when λ flips across harmless paraphrases.

- **Bridge with BBCR**  
  Insert bridge nodes when long chains stall. Anchor back to earlier stable nodes.

- **Enforce snippet fences**  
  Require each reasoning step cite snippet_id. Forbid cross-section reuse.

- **Re-anchor with anchors**  
  Compare ΔS(question, anchor) vs ΔS(question, decoy).  
  If ΔS is close, re-chunk corpus.

---

## Fix in 60 seconds
1. **Log ΔS and λ** across 3 paraphrases.  
2. **Clamp** with BBAM if λ flips.  
3. **Bridge** with BBCR if reasoning halts.  
4. **Re-anchor** using anchor triangulation.  
5. **Verify** coverage ≥ 0.70 and ΔS ≤ 0.45.  

---

## Copy-paste prompt

```

You have TXT OS and the WFGY Problem Map.

Goal: Detect and repair context drift in long reasoning chains.

Protocol:

1. Ask the same question three ways.
2. Log ΔS(question, retrieved) for each.
3. Log λ states across all hops.
4. If λ flips:

   * Apply BBAM clamp.
   * If reasoning stalls, apply BBCR and anchor bridge.
5. Require snippet\_id at each step.
6. Report:

   * ΔS(question, retrieved)
   * λ states across paraphrases
   * bridge nodes inserted
   * final answer with citations

```

---

## Common failure patterns
- **Chain stall**: reasoning halts after ~25–30 hops.  
- **Paraphrase drift**: harmless rewordings flip λ.  
- **Repeating answers**: earlier snippets loop back with filler.  
- **Contradictions**: late chain contradicts early reasoning.  

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

