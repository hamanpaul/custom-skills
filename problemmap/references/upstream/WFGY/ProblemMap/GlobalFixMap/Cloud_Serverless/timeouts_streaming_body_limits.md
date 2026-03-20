# Timeouts, Streaming, and Body Limits — Guardrails

<details>
  <summary><strong>🧭 Quick Return to Map</strong></summary>

<br>

  > You are in a sub-page of **Cloud_Serverless**.  
  > To reorient, go back here:  
  >
  > - [**Cloud_Serverless** — scalable functions and event-driven pipelines](./README.md)  
  > - [**WFGY Global Fix Map** — main Emergency Room, 300+ structured fixes](../README.md)  
  > - [**WFGY Problem Map 1.0** — 16 reproducible failure modes](../../README.md)  
  >
  > Think of this page as a desk within a ward.  
  > If you need the full triage and all prescriptions, return to the Emergency Room lobby.
</details>


A provider-agnostic repair guide for serverless and edge paths. Use this page when calls time out, streams drop mid-response, or request and response bodies hit size caps. Every action maps to Problem Map pages with measurable targets.

## When to use this page

* Requests succeed locally but fail behind API gateway or edge proxy.
* Streaming starts then stalls after a fixed idle period.
* First byte arrives very late or never on cold hits.
* Large inputs cause 413 or silent truncation.
* Long JSON responses get cut and fail to parse.

## Open these first

* Visual recovery map: [rag-architecture-and-recovery.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)
* Retrieval controls and ΔS probes: [retrieval-playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)
* Payload contract to keep requests small and auditable: [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)
* Live ops and tracing: [ops/live\_monitoring\_rag.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/live_monitoring_rag.md) · [ops/debug\_playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/debug_playbook.md)
* Boot order and first-call failures: [bootstrap-ordering.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md) · [predeploy-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md)

## Acceptance targets

* **ΔS(question, retrieved) ≤ 0.45** for streamed and non-streamed paths.
* **Coverage ≥ 0.70** to the target section after repair.
* **Stream drop rate ≤ 1 percent** on P95 windows.
* **TTFB cold ≤ 1500 ms** after warm-up fence is in place.
* **No truncated JSON**. Parser sees a complete closing brace or the stream sentinel.

---

## Fix in 60 seconds

1. **Classify the timeout**
   Record five numbers: connect time, TLS time, time to headers, time to first byte, idle-gap between chunks.
   If the idle-gap is a constant number, it is a proxy idle timeout not model latency.
   See: [ops/debug\_playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/debug_playbook.md)

2. **Choose a delivery mode**

* For answers that fit within gateway limits: keep HTTP JSON with a short total timeout and strict schema.
  Contract: [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)
* For long answers or tool loops: switch to streaming with server-sent events or chunked transfer. Send a heartbeat every 10–20 seconds and flush after each token batch. Add a final `"[END]"` sentinel.

3. **Bound the body and upgrade transport**

* Inputs larger than a safe inline threshold should be uploaded to object storage. Send only `{object_id, offsets, tokens}` through the edge.
  Contract: [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)
* If the model output exceeds gateway limits, stream or write to storage and return a handle.

4. **Stabilize retrieval under time pressure**
   Probe ΔS on a short context and on a compressed context. If ΔS improves on the compressed one, reduce payload or add reranking.
   See: [retrieval-playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)

---

## Typical breakpoints → exact fix

* **Gateway hard timeout shorter than function timeout**
  The edge kills the connection while the function keeps working. Align timeouts and prefer streaming for long generations.
  Open: [ops/live\_monitoring\_rag.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/live_monitoring_rag.md)

* **Proxy buffers the stream and releases it at the end**
  Client sees no chunks then everything lands at once. Disable proxy buffering and set cache control to no store. Add periodic heartbeats to keep the connection alive.
  Open: [ops/debug\_playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/debug_playbook.md)

* **413 on request or silent truncation on response**
  Enforce an input contract and route large payloads to blob storage. Stream the response and finish with a sentinel token.
  Open: [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

* **Cold path only: long TTFB then timeout**
  Dependencies are not ready. Add a warm-up fence and retry with capped backoff.
  Open: [bootstrap-ordering.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md) · [predeploy-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md)

* **Streaming flips answer quality**
  Headers or chunk sizes reorder the prompt and citations. Lock the prompt schema and verify with ΔS probes.
  Open: [rag-architecture-and-recovery.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)

---

## Minimal recipes you can copy

### A) Streaming pipeline

```txt
Client:
- Open SSE connection with 60–120s read timeout.
- AbortController on the client to cancel cleanly.
- Accept lines with {type, data}. Accumulate tokens until "[END]".
- If 10–20s pass without data, show heartbeat and remain connected.

Edge:
- Set headers to allow streaming and prevent buffering.
- Forward flushes immediately.

Function:
- warmup_fence()
- retrieval() → {snippet_id, section_id, source_url, offsets, tokens}
- stream tokens in batches of 20–50 with a newline flush
- send {"type":"metrics","data":{"ΔS":0.xx,"λ":"state"}} every 5–10s
- finish with {"type":"end","data":"[END]"}
```

### B) Large input with handle

```txt
Client:
- Upload document to object storage. Get object_id.
- Call API with {object_id, section_hints?}.

Function:
- validate object size and type
- retrieve with section_hints and small k
- if response size > edge limit → write to storage and return {result_id}
- else return JSON directly
```

---

## Observability you must add

* **connect\_time, tls\_time, headers\_time, ttfb, idle\_gap\_p95**
* **stream\_duration, bytes\_sent, truncated\_response flag**
* **ΔS, λ\_state, coverage** for streamed and non-streamed paths
  Open: [ops/live\_monitoring\_rag.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/live_monitoring_rag.md)

## Verification

* Run three variants on the same prompt: JSON, streaming, large-input handle.
* Expect ΔS ≤ 0.45 and coverage ≥ 0.70 on each path.
  Open: [eval/eval\_rag\_precision\_recall.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/eval/eval_rag_precision_recall.md)

## When to escalate

* If streaming is still buffered by intermediaries, fall back to handle based delivery and poll status.
* If ΔS collapses only when streaming, lock the prompt header order and re-test with reranking.
  Open: [retrieval-playbook.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)

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

