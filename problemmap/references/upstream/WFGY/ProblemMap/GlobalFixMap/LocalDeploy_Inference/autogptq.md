# AutoGPTQ: Guardrails and Fix Patterns

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


AutoGPTQ is a widely used library for quantizing large language models into lower-bit formats (INT4/INT8) for efficient local inference.  
This page maps the common failure modes when deploying AutoGPTQ and provides structural fixes with measurable targets.

---

## Open these first

- Visual map and recovery: [RAG Architecture & Recovery](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)  
- End-to-end retrieval knobs: [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)  
- Embedding vs meaning: [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)  
- Chunk schema and stability: [Chunking Checklist](https://github.com/onestardao/WFGY/blob/main/ProblemMap/chunking-checklist.md)  
- Collapse and entropy: [Logic Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/logic-collapse.md), [Entropy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/entropy-collapse.md)  
- Boot order and deployment: [Bootstrap Ordering](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md), [Predeploy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md)  

---

## Core acceptance

- ΔS(question, retrieved) ≤ 0.45  
- Coverage ≥ 0.70 to the target section  
- λ remains convergent across three paraphrases and two seeds  
- E_resonance stable across quantized vs full-precision runs  

---

## Typical AutoGPTQ breakpoints and the right fix

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Model loads but outputs garbage tokens | Misaligned quantization config (bits, group size) | Rebuild with correct group size; validate with ΔS probes |
| GPU memory still OOM despite quantization | Offloading not configured or weights pinned to VRAM | Enable `device_map=auto`, verify shard placement |
| Drastic accuracy drop vs FP16 baseline | Quantization schema mismatch or bad calibration | Run small calibration dataset; enforce consistent tokenizer |
| Inference stalls or crashes | CUDA/driver mismatch, kernels not compiled | Rebuild kernels for your GPU arch; fallback to CPU for test |
| Wrong snippet chosen during RAG | Retrieval mismatch amplified by quantized logits | Apply [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) + rerankers |

---

## Fix in 60 seconds

1. **Quantization check**  
   Verify config: `bits`, `group_size`, `sym/asym`. Run ΔS on 10 QA pairs.

2. **GPU memory probe**  
   Monitor memory before/after load. If OOM persists, enforce CPU/GPU split.

3. **Calibration**  
   Use a gold dataset (100–500 samples). Ensure ΔS gap between FP16 and INT4 ≤ 0.10.

4. **Inference stability**  
   Run 3 paraphrases × 2 seeds. λ must stay convergent.

---

## Deep diagnostics

- **Entropy vs precision**: If entropy collapses earlier in quantized runs, enable double-check rerankers.  
- **Traceability**: Log both FP16 and INT4 snippet selections. Divergence >20% means schema fix needed.  
- **Anchor triangulation**: Compare ΔS on FP16 vs INT4 to the same section. If drift >0.15, retrain quantizer.  

---

## Copy-paste config snippet

```python
from auto_gptq import AutoGPTQForCausalLM, BaseQuantizeConfig

quantize_config = BaseQuantizeConfig(
    bits=4,
    group_size=128,
    desc_act=False
)

model = AutoGPTQForCausalLM.from_pretrained(
    "your-model",
    quantize_config=quantize_config,
    device_map="auto"
)
````

*Checklist*: After loading, test with ΔS probe and λ convergence.

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

