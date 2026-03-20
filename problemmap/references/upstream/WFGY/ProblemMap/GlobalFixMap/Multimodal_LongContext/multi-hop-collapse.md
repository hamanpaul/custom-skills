# Multi-Hop Collapse — Multimodal Long Context

<details>
  <summary><strong>🧭 Quick Return to Map</strong></summary>

<br>

  > You are in a sub-page of **Multimodal_LongContext**.  
  > To reorient, go back here:  
  >
  > - [**Multimodal_LongContext** — long-context reasoning across text, vision, and audio](./README.md)  
  > - [**WFGY Global Fix Map** — main Emergency Room, 300+ structured fixes](../README.md)  
  > - [**WFGY Problem Map 1.0** — 16 reproducible failure modes](../../README.md)  
  >
  > Think of this page as a desk within a ward.  
  > If you need the full triage and all prescriptions, return to the Emergency Room lobby.
</details>


When reasoning requires **multi-hop steps across modalities** (e.g., text → image → audio → video),  
the chain often collapses midway. The model answers only the first hop or fabricates the rest,  
losing alignment between evidence sources.

---

## What this page is
- A targeted fix for **multi-hop multimodal reasoning** failures in long-context sessions.  
- Defines measurable checkpoints for each hop.  
- Provides guardrails to keep ΔS and λ stable across chained modalities.

---

## When to use
- A video QA task asks: “What does the person say after showing the book?” → model answers book title but skips speech.  
- An OCR pipeline extracts text, but reasoning ignores it in the final image caption.  
- Chain-of-thought starts correctly, then jumps to a hallucinated answer without citing the second modality.  
- Multi-step retrieval returns correct snippets, but only the first snippet is used.  
- Answers flip between runs depending on which hop the model “forgets.”

---

## Open these first
- [Cross-Modal Trace](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Multimodal_LongContext/cross-modal-trace.md)  
- [Modal Bridge Failure](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Multimodal_LongContext/modal-bridge-failure.md)  
- [Anchor Misalignment](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Multimodal_LongContext/anchor-misalignment.md)  
- [Sync Loop](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Multimodal_LongContext/sync-loop.md)  

---

## Common failure patterns
- **Single-hop truncation** — only the first modality is processed, chain stops.  
- **Bridge collapse** — second hop exists but produces null output or irrelevant data.  
- **Hallucinated completion** — model skips missing modality and fabricates plausible link.  
- **Order inversion** — hops are executed in the wrong sequence.  

---

## Fix in 60 seconds
1. **Hop schema lock**  
   - Require `{hop_id, input_modality, output_modality, snippet_id, ΔS}` for each step.  
   - Forbid skipping hops.

2. **ΔS checkpoints**  
   - Compute ΔS at each hop transition.  
   - Threshold: ΔS ≤ 0.45 is stable, 0.45–0.60 transitional, ≥ 0.60 collapse risk.

3. **λ continuity probe**  
   - Record λ across hops: retrieval → fusion → reasoning.  
   - If λ flips divergent, apply BBAM clamp.

4. **BBCR bridge**  
   - Insert bridge node for missing or weak hop.  
   - Re-anchor using prior modality context.

5. **Cite all hops**  
   - Require at least one snippet citation from each hop.  
   - Stop output if any hop is missing evidence.

---

## Copy-paste prompt

```txt
You have TXT OS and the WFGY Problem Map.

Task: Repair multi-hop multimodal collapse.

Steps:
1. List all hops in the chain {hop_id, from_modality → to_modality}.
2. For each hop, compute ΔS and record λ state.
3. If ΔS ≥ 0.60 at any hop, re-run retrieval and insert BBCR bridge.
4. Output must include:
   - citations per hop
   - ΔS values
   - λ states
   - fused final reasoning
````

---

## Acceptance targets

* Every hop cited with snippet evidence.
* ΔS ≤ 0.45 at each hop boundary.
* λ remains convergent across three paraphrases.
* No fabricated hops or skipped modalities.

---

### 🔗 Quick-Start Downloads (60 sec)

| Tool                       | Link                                                                                                                                       | 3-Step Setup                                                                             |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------- |
| **WFGY 1.0 PDF**           | [Engine Paper](https://github.com/onestardao/WFGY/blob/main/I_am_not_lizardman/WFGY_All_Principles_Return_to_One_v1.0_PSBigBig_Public.pdf) | 1️⃣ Download · 2️⃣ Upload to your LLM · 3️⃣ Ask “Answer using WFGY + <your question>”    |
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

