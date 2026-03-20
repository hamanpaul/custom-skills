# AWQ (Activation-aware Weight Quantization): Guardrails and Fix Patterns

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


AWQ/AutoAWQ applies activation-aware quantization to compress weights into 4/8-bit, aiming for higher throughput on local inference with minimal accuracy loss.  
This page maps typical AWQ failure modes to structural fixes in the WFGY Problem Map and defines measurable acceptance gates.

---

## Open these first
- Visual map and recovery: [RAG Architecture & Recovery](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)  
- End-to-end retrieval knobs: [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)  
- Why this snippet: [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)  
- Embedding vs meaning: [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)  
- Chunk schema: [Chunking Checklist](https://github.com/onestardao/WFGY/blob/main/ProblemMap/chunking-checklist.md)  
- Collapse and entropy: [Logic Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/logic-collapse.md), [Entropy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/entropy-collapse.md)  
- Boot order and deploy: [Bootstrap Ordering](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md), [Pre-deploy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md)  

---

## Core acceptance
- ΔS(question, retrieved) ≤ 0.45  
- Coverage ≥ 0.70 of the target section  
- λ remains convergent across 3 paraphrases and 2 seeds  
- Compared to FP16 baseline, ΔS drift ≤ 0.10, and entropy curve remains stable on long sequences  

---

## Typical AWQ breakpoints → exact fix

| Symptom | Likely cause | Open this |
|---|---|---|
| PPL rises significantly after quantization, answers drift | Calibration dataset mismatch, wrong `q_group_size` | [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md), [Chunking Checklist](https://github.com/onestardao/WFGY/blob/main/ProblemMap/chunking-checklist.md) |
| Snippets retrieved correctly but synthesis drifts | Logit jitter from quantization, unstable header ordering | [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md), [Logic Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/logic-collapse.md) |
| GPU still OOM or no throughput gain | Layer fusion disabled, device map misaligned | [Bootstrap Ordering](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md) |
| Long-chain reasoning collapses earlier | Faster entropy accumulation, no rerank or bridge | [Entropy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/entropy-collapse.md), [Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md) |
| JSON tool outputs unstable | Small errors amplified, schema too loose | [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md) |

---

## Fix in 60 seconds

1) **Measure ΔS**  
   Run 10 QA pairs with FP16 and AWQ. Compare ΔS(question, retrieved) and ΔS(retrieved, anchor).  
   If ΔS drift > 0.10, recalibrate.  

2) **Probe λ_observe**  
   Vary k = 5/10/20, shuffle headers.  
   If λ flips, lock header ordering and apply BBAM variance clamp.  

3) **Apply the module**  
   - Retrieval drift → BBMC + [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)  
   - Reasoning collapse → BBCR + BBAM  
   - Long-chain dead ends → BBPF alternative path + reranker  

4) **Verify**  
   Three paraphrases × two seeds. Coverage ≥ 0.70, λ convergent.  

---

## Deep diagnostics

- **Calibration set sanity**  
  Use a calibration set that matches production distribution. If only short or domain-limited data is used, quantized model will misbehave.  

- **Anchor triangulation**  
  Compare ΔS to anchor section and adjacent distractor. If gap ≤ 0.05, semantic boundaries are flattened → redo calibration or adjust `w_bit`, `q_group_size`.  

- **Entropy vs length**  
  Plot entropy per step on long sequences. If AWQ rises earlier than FP16, enable deterministic sampling, raise temperature floor, and add reranker.  

---

## Copy-paste recipes

### A) Load a pre-quantized AutoAWQ model
```python
from autoawq import AutoAWQForCausalLM, AutoTokenizer

model_id = "your-awq-model"
tokenizer = AutoTokenizer.from_pretrained(model_id, use_fast=True)
model = AutoAWQForCausalLM.from_pretrained(
    model_id,
    fuse_layers=True,
    safetensors=True,
    device_map="auto"
)
# Run ΔS/λ regression tests vs FP16 baseline
````

### B) Online quantization with custom config

```python
from autoawq import AutoAWQForCausalLM, AutoTokenizer

base_id = "your-fp16-model"
tokenizer = AutoTokenizer.from_pretrained(base_id, use_fast=True)
model = AutoAWQForCausalLM.from_pretrained(base_id, device_map="auto")

quant_config = {
    "zero_point": True,
    "q_group_size": 128,
    "w_bit": 4,
    "version": "GEMM"
}
model.quantize(tokenizer, quant_config)
# Export and cache, then immediately run ΔS regression
```

---

## Ops checklist

* Verify driver + compute capability before loading kernels
* Always test single-GPU ΔS/λ vs FP16 before scaling parallelism
* Track VRAM + throughput together with ΔS, λ, coverage metrics

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

