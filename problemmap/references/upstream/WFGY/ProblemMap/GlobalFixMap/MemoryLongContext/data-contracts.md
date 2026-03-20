# Data Contracts — Enforcing Snippet Schema & Payload Integrity

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


RAG and long-context reasoning collapse quickly if payloads drift.  
**Data Contracts** define the minimal schema that every retrieval, citation, and reasoning step must satisfy to remain auditable and reproducible.

---

## When to use
- Citations appear but fields like `snippet_id` or `section_id` are missing.  
- JSON payloads change shape across runs.  
- Downstream agents receive free-text with no schema lock.  
- Long-context sessions silently lose attribution or overwrite fields.  
- Multi-agent handoffs mutate keys or flatten nested fields.  

---

## Root causes
- **Loose schemas**: free-form JSON without validation.  
- **Field drift**: different casing, missing offsets, or swapped names.  
- **Silent truncation**: long answers cut JSON blocks.  
- **Inconsistent contracts**: each component defines its own schema.  
- **Opaque citations**: only plain text without structured trace.  

---

## Core acceptance targets
- Every snippet payload must include:  
  `{snippet_id, section_id, start_line, end_line, source_url, offsets, tokens}`  
- Coverage ≥ 0.70 for the target section.  
- ΔS(question, retrieved) ≤ 0.45.  
- λ convergent across 3 paraphrases.  
- Contracts must validate under the same schema across sessions.  

---

## Structural fixes

- **Schema lock**  
  Define a JSON schema for citations and enforce validation at ingestion.  

- **Contract inheritance**  
  Pass the same schema downstream to every agent and reasoning step.  

- **Casing & normalization**  
  Enforce consistent field names and Unicode normalization.  

- **Fail fast**  
  If schema validation fails, block reasoning and return fix instructions.  

---

## Fix in 60 seconds
1. Define contract:  
   ```json
   {
     "snippet_id": "string",
     "section_id": "string",
     "start_line": "int",
     "end_line": "int",
     "source_url": "string",
     "offsets": [int],
     "tokens": [string]
   }
````

2. Validate every retrieval step against the contract.
3. Store the validated payload in the trace log.
4. Require cite-then-answer. Reject orphan claims.
5. Report ΔS and λ for each reasoning step.

---

## Copy-paste prompt

```
You have TXT OS and the WFGY Problem Map.

Task: enforce Data Contracts for retrieval and citation.

Protocol:
1. Validate that each snippet includes {snippet_id, section_id, start_line, end_line, source_url}.  
2. Reject orphans: if missing fields, stop and return fix tip.  
3. Require cite-then-answer.  
4. Log {ΔS(question,retrieved), λ_state, mem_rev, mem_hash}.  
5. Answer only with citations that pass contract validation.
```

---

## Common failure signals

* Citations alternate across runs → contract not enforced.
* JSON mode fails in provider → schema too loose.
* Free-text answers with no snippet\_id → orphan claims.
* Multi-agent pipelines mutate payloads → inconsistent contracts.

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

