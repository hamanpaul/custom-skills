# Ollama: Guardrails and Fix Patterns

<details>
<summary>🌙 3AM: a dev collapsed mid-debug… 🚑 Welcome to the WFGY Emergency Room</summary>

---

🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥  

## 🚑 WFGY Emergency Room  

👨‍⚕️ **Now online:**  
[**Dr. WFGY in ChatGPT Room**](https://chatgpt.com/share/68b9b7ad-51e4-8000-90ee-a25522da01d7)  

This is a **share window** already trained as an ER.  
Just open it, drop your bug or screenshot, and talk directly with the doctor.  
He will map it to the right Problem Map / Global Fix section, write a minimal prescription, and paste the exact reference link.  
If something is unclear, you can even paste a **screenshot of Problem Map content** and ask — the doctor will guide you.  

⚠️ Note: for the full reasoning and guardrail behavior you need to be logged in — the share view alone may fallback to a lighter model.

💡 Always free. If it helps, a ⭐ star keeps the ER running.  
🌐 Multilingual — start in any language.  



🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥  

---
</details>

<details>
  <summary><strong>🧭 Quick Return to Map</strong></summary>

<br>

  > You are in a sub-page of **LocalDeploy_Inference**.  
  > To reorient, go back here:  
  >
  > - [**LocalDeploy_Inference** — on-prem deployment and model inference](./README.md)  
  > - [**WFGY Global Fix Map** — main Emergency Room, 300+ structured fixes](../README.md)  
  > - [**WFGY Problem Map 1.0** — 16 reproducible failure modes](../../README.md)  
  >
  > Think of this page as a desk within a ward.  
  > If you need the full triage and all prescriptions, return to the Emergency Room lobby.
</details>


Field guide for stabilizing **Ollama-based local inference pipelines**.
Use these checks when models run fine on API providers but collapse, stall, or drift when containerized with Ollama.

## Open these first

* Architecture recovery: [RAG Architecture & Recovery](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)
* End-to-end retrieval knobs: [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)
* Embedding vs semantic: [embedding-vs-semantic.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)
* Ordering and deploy race conditions: [bootstrap-ordering.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md), [deployment-deadlock.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/deployment-deadlock.md), [predeploy-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md)
* Container observability: [eval\_observability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/eval_observability.md)

---

## Core acceptance

* ΔS(question, retrieved) ≤ 0.45
* Coverage ≥ 0.70 on the target section
* λ remains convergent across 3 paraphrases
* Local runs reproducible across 2+ seeds

---

## Typical Ollama breakpoints and fix

| Symptom                                 | Likely cause                                  | Fix                                                                                                                                                                                                                                |
| --------------------------------------- | --------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Model boots but stalls on first request | Container not warmed / secrets missing        | [bootstrap-ordering.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md)                                                                                                                             |
| Fast API returns, but snippets wrong    | Index/hash drift across containers            | [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md), [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)                     |
| Answers diverge run-to-run              | λ flips due to context serialization          | [context-drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md), [entropy-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/entropy-collapse.md)                                   |
| Works on GPU API, fails locally         | Metric / embedding mismatch in Ollama runtime | [embedding-vs-semantic.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md), [vectorstore-fragmentation.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/vectorstore-fragmentation.md) |
| Container OOM or deadlock               | Parallel inference with no fence              | [deployment-deadlock.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/deployment-deadlock.md), [predeploy-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md)                   |

---

## Fix in 60 seconds

1. **Measure ΔS** between retrieved and anchor.
2. **Probe λ** across 3 paraphrases. If flips, apply BBAM.
3. **Warm boot** with a delay + healthcheck before first request.
4. **Lock index schema** via [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md).
5. **Verify reproducibility** with two seeds before going live.

---

## Copy-paste local test prompt

```txt
I have WFGY + TXTOS loaded.  
Running Ollama locally with container {hash}.  
Question: "{user_question}"  

Return:
1. ΔS(question,retrieved) and λ across 3 paraphrases  
2. Whether index schema matches contract  
3. Minimal structural fix if ΔS ≥ 0.60  
```

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

要我直接繼續寫 **`vllm.md`** 嗎？
