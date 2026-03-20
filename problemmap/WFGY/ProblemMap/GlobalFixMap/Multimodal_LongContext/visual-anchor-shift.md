# Visual Anchor Shift — Multimodal Long Context

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


When **visual anchors** (bounding boxes, frame IDs, or pixel regions) drift across long context windows, the model misaligns references.  
This creates subtle but cascading failures where reasoning cites the **wrong visual region**, even if the textual trace looks correct.

---

## What this page is
- A diagnostic page for **visual anchor drift** in multimodal RAG and reasoning.  
- Structural guardrails to lock anchor stability across long sessions.  
- Copy-paste protocols to enforce traceability in image/video reasoning.

---

## When to use
- Bounding boxes shift slightly across frames, causing references to drift.  
- Captions point to a visual anchor that no longer overlaps with the intended object.  
- Long video QA: frame ID references lag or accelerate relative to transcript anchors.  
- Model hallucinates content that appears plausible but is visually absent.  
- Answers remain fluent, but **anchor→object mapping is wrong**.

---

## Open these first
- [Cross-Modal Trace](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Multimodal_LongContext/cross-modal-trace.md)  
- [Anchor Misalignment](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Multimodal_LongContext/anchor-misalignment.md)  
- [Reference Bleed](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Multimodal_LongContext/reference-bleed.md)  
- [Phantom Visuals](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Multimodal_LongContext/phantom-visuals.md)  

---

## Common failure patterns
- **Frame creep** — frame IDs drift after long video sessions.  
- **Box shift** — bounding boxes move across updates, yet still labeled the same.  
- **Region blur** — multiple boxes merge, and anchor becomes ambiguous.  
- **Temporal offset** — captions cite the right object but wrong frame interval.  

---

## Fix in 60 seconds
1. **Anchor tagging**  
   - Tag anchors with `{frame_id | bbox_id | timestamp}`.  
   - Reject any reference missing full anchor tuple.

2. **Cross-frame validation**  
   - Require IoU ≥ 0.7 across frames for the same anchor ID.  
   - If IoU < 0.7, treat as a new anchor.

3. **ΔS probe for drift**  
   - Compute ΔS(anchor_t, anchor_t+Δ).  
   - If ΔS ≥ 0.60, suspect anchor drift.

4. **Stabilize with BBCR**  
   - Re-anchor drifting objects with bridge check.  
   - If variance persists, force new anchor ID.

5. **Audit trail**  
   - Store anchor table: `{anchor_id | modality | coords | IoU history}`.  
   - Require cite-then-answer with explicit anchor IDs.

---

## Copy-paste prompt

```txt
You have TXT OS and the WFGY Problem Map.

Task: Detect and repair visual anchor drift in long multimodal sessions.

Steps:
1. Verify each anchor has {frame_id, bbox_id, timestamp}.
2. Compute IoU across frames. If IoU < 0.7, mark drift.
3. If drifted, either re-anchor with BBCR or assign new ID.
4. Report:
   - stable anchors
   - drifted anchors
   - ΔS values and λ states
   - final citation mapping
````

---

## Acceptance targets

* 100% anchors carry `{frame_id, bbox_id, timestamp}` metadata.
* IoU drift ≤ 0.30 across 10 frames.
* ΔS(anchor\_t, anchor\_t+Δ) ≤ 0.45 after fix.
* λ remains convergent across paraphrases.

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

