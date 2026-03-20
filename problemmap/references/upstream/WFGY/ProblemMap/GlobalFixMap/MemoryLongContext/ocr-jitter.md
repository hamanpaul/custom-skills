# OCR Jitter — Guardrails and Fix Pattern

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


When OCR engines process scanned text with inconsistent spacing, width variants, or mixed character forms,  
the output may look visually correct but introduces **false token differences** that destabilize retrieval and reasoning.

---

## Symptoms
- OCR transcript looks fine to the eye, but semantic retrieval drifts.  
- Words alternate between **half-width / full-width** forms.  
- Invisible characters (zero-width joiners, non-breaking spaces) trigger token mismatches.  
- Capitalization inconsistent across the same word in long transcripts.  
- Citations fail even though the snippet visually matches the source.

---

## Root causes
- OCR confidence below threshold but output still accepted.  
- Normalization skipped (NFC vs NFD forms mixed).  
- Scanner artifacts (speckles, warped lines) inject invisible characters.  
- Language-specific width forms (CJK fullwidth vs ASCII halfwidth) untreated.  
- No post-processing pass to unify tokens before embedding.

---

## Fix in 60 seconds
1. **Gate by confidence**
   - Drop lines with OCR confidence < 0.85.  
   - Flag low-confidence tables and equations for manual review.  

2. **Normalize Unicode**
   - Convert to **NFC** form.  
   - Replace non-breaking spaces with plain space.  
   - Strip zero-width characters.  

3. **Unify width and case**
   - Map fullwidth and halfwidth characters consistently.  
   - Apply case-folding for ASCII text.  

4. **Re-stamp clean snippets**
   - After normalization, reassign line numbers.  
   - Ensure `section_id | start_line | end_line | citation` schema updated.  

5. **Verify joins**
   - Run ΔS across adjacent chunks.  
   - If join ΔS ≥ 0.50, suspect hidden jitter — repeat normalization.  

---

## Copy-paste diagnostic prompt
```txt
You have TXTOS and the WFGY Problem Map.

Task: Detect and repair OCR jitter.

Protocol:
1. Normalize all snippets:
   - Unicode NFC
   - Strip zero-width, NBSP
   - Map fullwidth → halfwidth
   - Apply case-fold
2. Drop snippets with OCR confidence < 0.85.
3. Re-stamp Snippet Table with {section_id, start_line, end_line, citation}.
4. Measure ΔS across adjacent chunks:
   - Target ≤ 0.50 at each join.
5. Report ΔS(question, retrieved) and λ states.
````

---

## Acceptance targets

* OCR confidence ≥ 0.85 for all retained lines.
* No mixed width or hidden characters in final text.
* ΔS(question, retrieved) ≤ 0.45 and joins ≤ 0.50.
* λ remains convergent across three paraphrases.
* Snippets traceable and citations reproducible.

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

