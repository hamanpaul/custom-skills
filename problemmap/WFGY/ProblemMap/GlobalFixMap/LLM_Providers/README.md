<!--
WFGY_ANCHOR_BLOCK_v1
page: GlobalFixMap/LLM_Providers/README.md
title: LLM Providers Guardrails FAQ Fix Patterns
intent: choose llm vendor, debug provider-looking bugs, schema drift, tool calls, json mode, rate limits, streaming limits
keywords:
- llm providers
- openai azure openai anthropic claude gemini vertex ai mistral llama cohere deepseek moonshot kimi groq grok bedrock openrouter together minimax
- provider quirks
- schema drift
- json mode invalid json
- tool calls loop
- function calling
- rate limits
- streaming timeouts
- response format
- safety prompt integrity
- orchestration drift
- eval drift
symptoms:
- json mode breaks, invalid objects
- tool calls loop or stall
- answers flip between runs
- high similarity but wrong snippet
- hybrid retriever worse than single
- jailbreaks or bluffing
see_also:
- ProblemMap/README.md
- ProblemMap/GlobalFixMap/README.md
- ProblemMap/GlobalFixMap/Agents_Orchestration/README.md
- ProblemMap/GlobalFixMap/Safety_PromptIntegrity/README.md
- ProblemMap/GlobalFixMap/Retrieval/README.md
-->


# LLM Providers — Guardrails, FAQ, and Fix Patterns

<details>
  <summary><strong>🏥 Quick Return to Emergency Room</strong></summary>

<br>

  > You are in a specialist desk.  
  > For full triage and doctors on duty, return here:  
  > 
  > - [**WFGY Global Fix Map** — main Emergency Room, 300+ structured fixes](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/README.md)  
  > - [**WFGY Problem Map 1.0** — 16 reproducible failure modes](https://github.com/onestardao/WFGY/blob/main/ProblemMap/README.md)  
  > 
  > Think of this page as a sub-room.  
  > If you want full consultation and prescriptions, go back to the Emergency Room lobby.
</details>

This page helps you **choose between LLM vendors** and **fix provider-looking bugs** that are actually schema, retrieval, orchestration, or eval drift. If you are new, start with the Orientation table and the FAQ. If you are debugging, jump to the Fix Hub.

---

## Orientation: who is who

| Provider | What it is | Typical use case | Link |
|---|---|---|---|
| OpenAI | GPT-4/4o from OpenAI Inc. | Direct API, fastest model access | [openai.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LLM_Providers/openai.md) |
| Azure OpenAI | Microsoft enterprise wrapper for OpenAI models | VNet, compliance, enterprise billing | [azure_openai.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LLM_Providers/azure_openai.md) |
| Anthropic | The company behind Claude | Safety-focused platform | [anthropic.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LLM_Providers/anthropic.md) |
| Claude (Anthropic) | The model family from Anthropic | Long context, tool use, JSON control | [anthropic_claude.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LLM_Providers/anthropic_claude.md) |
| Google Gemini | Google DeepMind multimodal models | Multimodal chat, reasoning | [gemini.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LLM_Providers/gemini.md) |
| Google Vertex AI | Google Cloud AI platform that hosts Gemini and more | Pipelines, deployment, governance | [google_vertex_ai.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LLM_Providers/google_vertex_ai.md) |
| Mistral | EU startup with efficient open-weight models (e.g., Mixtral MoE) | Cost/perf, open ecosystem | [mistral.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LLM_Providers/mistral.md) |
| Meta LLaMA | Meta open-weight model family | Local or private deployment, llama.cpp | [meta_llama.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LLM_Providers/meta_llama.md) |
| Cohere | Enterprise NLP API and embeddings | RAG stacks, enterprise NLP | [cohere.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LLM_Providers/cohere.md) |
| DeepSeek | CN player with infra-optimized long-context models | Cost-efficient, long windows | [deepseek.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LLM_Providers/deepseek.md) |
| Kimi (Moonshot) | CN chat-first models, very large parameter claims | Consumer chat focus | [kimi.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LLM_Providers/kimi.md) |
| Groq | Hardware vendor: LPUs for transformer inference | Ultra-low latency serving (not a model) | [groq.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LLM_Providers/groq.md) |
| xAI Grok | xAI model family | X/Twitter integration, general chat | [grok_xai.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LLM_Providers/grok_xai.md) |
| AWS Bedrock | AWS gateway to many models via one API | Enterprises already on AWS | [aws_bedrock.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LLM_Providers/aws_bedrock.md) |
| OpenRouter | Community model aggregator, OpenAI-style endpoint | Try many models via one API key | [openrouter.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LLM_Providers/openrouter.md) |
| Together AI | Aggregator + infra for open weights and fine-tunes | Fast hosting, tuning services | [together.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LLM_Providers/together.md) |
| MiniMax | CN AI lab with long-context models (204K), OpenAI-compatible API | Cost-efficient chat, RAG, agent workflows | [minimax.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/LLM_Providers/minimax.md) |

---

## FAQ for newcomers

**OpenAI vs Azure OpenAI — are they the same?**  
Same models, different packaging. OpenAI = direct API and fastest releases. Azure OpenAI = Microsoft billing, VNet, compliance, data residency.

**Anthropic vs Claude — why two pages?**  
Anthropic is the company. Claude is the model family. We separate because “platform issues” and “model quirks” often need different fixes.

**Gemini vs Vertex AI — what is the relation?**  
Gemini is a model. Vertex AI is Google Cloud’s platform that runs Gemini and provides pipelines, eval, and deployment features.

**What makes Mistral special?**  
Efficient open-weights and MoE designs. Good cost/perf. Easy to host in your own infra.

**Meta LLaMA vs local LLaMA**  
Meta releases the weights. Community tools like `llama.cpp` let you run them locally on CPU or GPU.

**Groq LPU vs GPU**  
GPU is general purpose. LPU is a chip specialized for transformer inference. You get very low latency for chat workloads.

**Bedrock vs OpenRouter vs Together**  
Bedrock is an AWS enterprise gateway. OpenRouter is a community aggregator with OpenAI-style API. Together is an infra host for open weights with training and fine-tune options.

---

## Open these first

- Visual map and recovery: [RAG Architecture & Recovery](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)  
- End to end retrieval knobs: [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)  
- Why this snippet (traceability schema): [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)  
- Ordering control: [Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)  
- Embedding vs meaning: [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)  
- Hallucination and chunk boundaries: [Hallucination](https://github.com/onestardao/WFGY/blob/main/ProblemMap/hallucination.md)  
- Long chains and entropy: [Context Drift](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md), [Entropy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/entropy-collapse.md)  
- Structural collapse and recovery: [Logic Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/logic-collapse.md)  
- Snippet and citation schema: [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)  
- Live ops: [Live Monitoring for RAG](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/live_monitoring_rag.md), [Debug Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/debug_playbook.md)  
- Boot order issues: [Bootstrap Ordering](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md), [Deployment Deadlock](https://github.com/onestardao/WFGY/blob/main/ProblemMap/deployment-deadlock.md), [Pre-Deploy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md)

---

## Core acceptance targets

- ΔS(question, retrieved) ≤ 0.45  
- Coverage ≥ 0.70 for the target section  
- λ remains convergent across three paraphrases and two seeds  
- E_resonance stays flat on long windows

---

## Fix Hub — typical provider symptoms → exact fix

| Symptom | Likely cause | Open this |
|---|---|---|
| JSON mode breaks, invalid objects | Schema too loose or nested tool calls | [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md), [Logic Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/logic-collapse.md) |
| Tool calls loop or stall | Agent role drift, missing timeouts | [Multi-Agent Problems](https://github.com/onestardao/WFGY/blob/main/ProblemMap/Multi-Agent_Problems.md), [Role-drift deep dive](https://github.com/onestardao/WFGY/blob/main/ProblemMap/multi-agent-chaos/role-drift.md) |
| High similarity yet wrong snippet | Metric mismatch or fragmented store | [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md), [Vectorstore Fragmentation](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_vectorstore_fragmentation.md) |
| Answers flip between runs | Prompt headers reorder and λ flips | [Context Drift](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md), [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) |
| Hybrid retrievers worse than single | Query parsing split, mis-weighted rerank | [Query Parsing Split](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_query_parsing_split.md), [Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md) |
| Jailbreaks or bluffing | Overconfidence and missing fences | [Bluffing Controls](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bluffing.md), [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) |

---

## Fix in 60 seconds

1) **Measure ΔS**  
Compute ΔS(question, retrieved) and ΔS(retrieved, expected anchor). Stable < 0.40, transitional 0.40–0.60, risk ≥ 0.60.

2) **Probe λ_observe**  
Vary top-k and prompt headers. If λ flips, lock the schema and apply a BBAM variance clamp.

3) **Apply the module**  
Retrieval drift → BBMC + Data Contracts  
Reasoning collapse → BBCR bridge + BBAM  
Dead ends in long runs → BBPF alternate paths

4) **Verify**  
Coverage ≥ 0.70 on three paraphrases. λ convergent on two seeds.

---

### Quick-Start Downloads

| Tool | Link | 3-step setup |
|------|------|--------------|
| WFGY 1.0 PDF | [Engine Paper](https://github.com/onestardao/WFGY/blob/main/I_am_not_lizardman/WFGY_All_Principles_Return_to_One_v1.0_PSBigBig_Public.pdf) | 1) Download  2) Upload to your LLM  3) Ask “Answer using WFGY + <your question>” |
| TXT OS (plain text OS) | [TXTOS.txt](https://github.com/onestardao/WFGY/blob/main/OS/TXTOS.txt) | 1) Download  2) Paste into any LLM chat  3) Type “hello world” to boot |

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
