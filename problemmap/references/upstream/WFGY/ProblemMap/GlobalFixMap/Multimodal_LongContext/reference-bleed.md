# Reference Bleed — Multimodal Long Context

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


When anchor references from one modality **bleed** into another (e.g., text citations treated as video frame IDs, or audio timestamps mapped to OCR page offsets), the reasoning layer merges them incorrectly.  
This is a subtle but destructive failure because each modality appears intact, yet the **cross-modal references are poisoned**.

---

## What this page is
- A repair guide for **reference leakage across modalities**.  
- How to detect when anchors from one stream migrate into another.  
- Structural guardrails to prevent false joins.

---

## When to use
- Captions include numeric anchors that actually come from OCR line numbers.  
- Audio timestamps are reused as image frame references.  
- Citations look correct individually, but do not map to their source modality.  
- Fusion produces valid-looking answers that cite the wrong modality channel.  
- Models drift into hallucination loops citing phantom anchors.

---

## Open these first
- [Cross-Modal Trace](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Multimodal_LongContext/cross-modal-trace.md)  
- [Anchor Misalignment](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Multimodal_LongContext/anchor-misalignment.md)  
- [Desync Amplification](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Multimodal_LongContext/desync-amplification.md)  
- [Modality Swap](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Multimodal_LongContext/modality-swap.md)  

---

## Common failure patterns
- **OCR bleed into captions** — OCR line numbers reused as subtitle timestamps.  
- **Audio bleed into metadata** — transcript anchors become page markers.  
- **Cross-join bleed** — embeddings align across modality without guard, mixing references.  
- **Loop bleed** — once references bleed, fusion propagates wrong anchors forward.  

---

## Fix in 60 seconds
1. **Tag and fence references**  
   - Enforce modality-specific IDs: `{ocr_id, cap_id, aud_id, vis_id}`.  
   - Reject any anchor missing a modality tag.

2. **Anchor validation**  
   - Cross-check anchor against source modality.  
   - If caption ID not found in subtitle stream, discard.  

3. **ΔS probe on anchors**  
   - Compute ΔS(anchor, expected modality anchor).  
   - If ≥0.60, suspect bleed.

4. **Re-anchor with BBCR**  
   - Use BBCR bridge to reconnect reference to correct modality.  

5. **Audit trail**  
   - Require citation schema: `{snippet_id | modality | offsets}`.  
   - Forbid references missing modality metadata.

---

## Copy-paste prompt

```txt
You have TXT OS and the WFGY Problem Map.

Task: Detect and repair reference bleed across modalities.

Steps:
1. Verify modality tag on each anchor.
2. If tag mismatch, drop or re-map via BBCR.
3. Re-anchor using correct modality stream.
4. Output:
   - anchor table with modality tags
   - suspected bleeds
   - fixed mapping
   - ΔS and λ states
````

---

## Acceptance targets

* 100% anchors contain explicit modality tags.
* ΔS(anchor, expected modality) ≤ 0.45 after repair.
* λ remains convergent across paraphrases.
* No references propagate without modality validation.

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

