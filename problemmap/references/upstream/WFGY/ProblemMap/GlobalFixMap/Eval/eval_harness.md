# Eval Harness — Guardrails and Minimal Contract

<details>
  <summary><strong>🧭 Quick Return to Map</strong></summary>

<br>

  > You are in a sub-page of **Eval**.  
  > To reorient, go back here:  
  >
  > - [**Eval** — model evaluation and benchmarking](./README.md)  
  > - [**WFGY Global Fix Map** — main Emergency Room, 300+ structured fixes](../README.md)  
  > - [**WFGY Problem Map 1.0** — 16 reproducible failure modes](../../README.md)  
  >
  > Think of this page as a desk within a ward.  
  > If you need the full triage and all prescriptions, return to the Emergency Room lobby.
</details>

> **Evaluation disclaimer (eval harness)**  
> This page sketches a harness for running structured evaluations on AI pipelines.  
> Any metrics or labels that pass through such a harness remain heuristic outputs of models, scripts and annotators.  
> They do not become scientific proof just because they flow through this structure.  
> Use the harness to compare variants inside a controlled scenario, and avoid presenting those numbers as universal claims about model quality beyond that scenario.

---

A minimal yet strict harness to run repeatable evaluations for RAG and agent pipelines. It fixes the two usual failures. First, non-reproducible runs. Second, noisy metrics that cannot explain drift. Everything here maps to WFGY pages with measurable targets.

## Open these first

* Visual map and recovery: [RAG Architecture & Recovery](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md)
* End to end retrieval knobs: [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md)
* Why this snippet schema: [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)
* Payload schema and fences: [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)
* Chunk quality before metrics: [Chunking Checklist](https://github.com/onestardao/WFGY/blob/main/ProblemMap/chunking-checklist.md)
* Similarity vs meaning: [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)

## Acceptance targets for this harness

* ΔS(question, retrieved) ≤ 0.45 on the gold set
* Coverage of the target section ≥ 0.70
* λ remains convergent across 3 paraphrases and 2 seeds
* Re-runs with identical seed produce metrics drift ≤ 0.5 percentage point

## Folder layout and contracts

```
eval/
  datasets/
    gold/
      qa.jsonl            # minimal gold set
      citations.jsonl     # expected snippet anchors
    probes/
      paraphrases.jsonl   # 3 paraphrases per item
  runs/
    2025-08-29_seed42/
      config.yaml
      metrics.csv
      traces.jsonl
  config/
    harness.yaml          # store, retriever, reranker, seeds, k
```

### Input schema

`datasets/gold/qa.jsonl` one JSON per line.

```json
{
  "id": "Q_0001",
  "question": "How is vector contamination detected in FAISS indexes",
  "answer_ref": "PM:vectorstore-metrics-and-faiss-pitfalls#detect-contamination",
  "expected_doc": "ProblemMap/vectorstore-metrics-and-faiss-pitfalls.md",
  "section_id": "detect-contamination"
}
```

`datasets/gold/citations.jsonl`

```json
{
  "id": "Q_0001",
  "snippet_id": "S_18823",
  "section_id": "detect-contamination",
  "source_url": "https://github.com/onestardao/WFGY/blob/main/ProblemMap/vectorstore-metrics-and-faiss-pitfalls.md",
  "offsets": [1380, 1540],
  "tokens": [310, 352]
}
```

Contract rules come from
[Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) and
[Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md).

## Repro knobs

* `seed`: integer. Set for the retriever, reranker, and LLM sampler if available.
* `k`: top k per retriever. Test 5, 10, 20.
* `λ_observe`: record λ state for retrieve, assemble, reason. See [lambda\_observe.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Eval_Observability/lambda_observe.md).
* ΔS probe: compute ΔS(question, retrieved) and ΔS(retrieved, expected anchor). See [deltaS\_thresholds.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Eval_Observability/deltaS_thresholds.md).

## Execution flow

1. **Warm up fence**. Verify index hash, vector ready, secrets. If not ready, stop.
   Open: [Bootstrap Ordering](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md).

2. **Retrieval step**. Run with fixed metric and analyzer. Save raw hits with snippet fields from the contract page.

3. **ΔS and λ probes**. Log both per item. If ΔS ≥ 0.60 flag as structural risk.

4. **Reasoning step**. LLM reads TXT OS and uses the cite then explain schema. Refuse answers without citations.

5. **Metrics**. Compute precision, recall, citation hit, coverage. See [eval\_rag\_precision\_recall.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/eval/eval_rag_precision_recall.md) and [Retrieval Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-playbook.md).

6. **Trace sink**. Write `traces.jsonl` with `id, seed, k, ΔS, λ_state, snippet_id, section_id, INDEX_HASH`.

7. **Gate**. If coverage < 0.70 or ΔS > 0.45 fail the run. See [regression\_gate.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Eval_Observability/regression_gate.md).

## Sixty second quick start

1. Place a ten item gold set into `datasets/gold/qa.jsonl` and `citations.jsonl`.
2. Copy `config/harness.yaml` from a previous good run. Set `seed: 42`, `k: 10`.
3. Run your script to produce `runs/<date>_seed42/metrics.csv` and `traces.jsonl`.
4. Verify the acceptance targets above. If any gate fails jump to the right fix below.

## Common failures and the exact fix

* Wrong meaning despite high similarity.
  Open: [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)

* Citations do not match the referenced section.
  Open: [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) and
  [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

* Hybrid retrieval worse than single retriever.
  Open: [pattern\_query\_parsing\_split.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_query_parsing_split.md) and
  [rerankers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)

* Runs flip across deployments or first run crashes.
  Open: [deployment-deadlock.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/deployment-deadlock.md),
  [predeploy-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md)

* Long chains collapse.
  Open: [context-drift.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md) and
  [entropy-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/entropy-collapse.md)

## CI gates and artifacts

* Block merge if any of these is true

  1. ΔS median > 0.45 on gold
  2. Coverage < 0.70
  3. λ flips on 2 of 3 paraphrases
  4. Metrics drift from last green run > 0.5 percentage point

* Store artifacts
  `metrics.csv`, `traces.jsonl`, `harness.yaml`, `INDEX_HASH`, `MODEL_HASH`.

## Copy paste prompts for the reasoning step

```
You have TXTOS and the WFGY Problem Map loaded.

Question: "{question}"
Retrieved snippets: [{snippet_id, section_id, source_url, offsets, tokens}]

Do:
1) Cite then explain. If citation is missing or mismatched, fail fast and return the minimal structural fix.
2) If ΔS(question, retrieved) ≥ 0.60 propose the smallest repair. Use retrieval-playbook, retrieval-traceability, data-contracts, rerankers.
3) Return JSON:
   {"citations":[...], "answer":"...", "λ_state":"→|←|<>|×", "ΔS":0.xx, "next_fix":"..."}
Keep it short and auditable.
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

