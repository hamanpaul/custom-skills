# Caption Collapse — Multimodal Long Context

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


When captions or annotations break down under long windows, multimodal pipelines lose alignment and factual grounding.  
This page focuses on stabilizing caption integrity for images, videos, and diagrams in extended sessions.

---

## What this page is
- A diagnostic page for caption degradation in multimodal contexts.  
- Structural guardrails to keep captions aligned with visual evidence.  
- Acceptance targets for ΔS and λ across captions and snippets.

---

## When to use
- Image captions are accurate at the start but drift after 20k+ tokens.  
- Captions compress multiple regions into one vague statement.  
- Video scene captions skip events or merge distinct frames.  
- Diagram labels appear but reasoning no longer references them correctly.  
- Captions look fluent but introduce objects not in the frame.

---

## Open these first
- [Entropy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/entropy-collapse.md)  
- [Context Drift](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md)  
- [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)  
- [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)  
- [Chunking Checklist](https://github.com/onestardao/WFGY/blob/main/ProblemMap/chunking-checklist.md)  

---

## Common failure patterns
- **Vague compression**: distinct objects collapsed into one generic caption.  
- **Temporal merge**: video events blended into a single description.  
- **Phantom detail**: captions include invented objects or properties.  
- **Citation loss**: captions lack bounding boxes or region ids.  
- **Context slip**: captions reference prior images instead of the current one.

---

## Fix in 60 seconds
1. **Stamp captions with anchors**  
   - Add `{region_id | bbox | frame_time}` to each caption.  
   - Require ΔS(caption, region) ≤ 0.45.

2. **Enforce one-to-one mapping**  
   - Each object/region must have a unique caption line.  
   - Forbid merges without explicit evidence.

3. **Normalize caption schema**  
   - Require `{subject | attribute | action}` fields.  
   - Disallow free-form hallucinations.

4. **Clamp entropy**  
   - Apply BBAM when variance rises across caption tokens.  
   - Apply BBCR bridge if captions diverge from visual anchors.

5. **Trace joins**  
   - Log {region_id, caption_id, ΔS, λ_state}.  
   - Fail if any caption has no visual anchor.

---

## Copy-paste prompt

```txt
You have TXT OS and the WFGY Problem Map.

Task: Stabilize captions across long multimodal contexts.

Steps:
1. Print each caption with {region_id | bbox | frame_time}.
2. Require cite-then-caption, forbid phantom objects.
3. Compute ΔS(caption, region). If ≥ 0.60, propose fix with data-contracts or chunking-checklist.
4. Apply BBAM if entropy rises. Apply BBCR if λ diverges.
5. Return: {Caption Table, Alignment Log, Final Answer}.
````

---

## Acceptance targets

* ΔS(caption ↔ region) ≤ 0.45
* Each caption tied to a valid region\_id or frame\_time
* λ remains convergent across three paraphrases
* No phantom objects or invented attributes
* Captions maintain one-to-one mapping with objects

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

