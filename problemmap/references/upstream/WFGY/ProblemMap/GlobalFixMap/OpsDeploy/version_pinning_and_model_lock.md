# Version Pinning & Model Lock — OpsDeploy

<details>
  <summary><strong>🧭 Quick Return to Map</strong></summary>

<br>

  > You are in a sub-page of **OpsDeploy**.  
  > To reorient, go back here:  
  >
  > - [**OpsDeploy** — operations automation and deployment pipelines](./README.md)  
  > - [**WFGY Global Fix Map** — main Emergency Room, 300+ structured fixes](../README.md)  
  > - [**WFGY Problem Map 1.0** — 16 reproducible failure modes](../../README.md)  
  >
  > Think of this page as a desk within a ward.  
  > If you need the full triage and all prescriptions, return to the Emergency Room lobby.
</details>


Lock models, prompts, embeddings, rerankers, tokenizers, and analyzers so prod can’t drift.  
Use this page to make “what ran” exactly the same as “what you tested,” and to detect any silent shift before a rollout.

---

## Open these first
- Readiness gate: [rollout_readiness_gate.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/rollout_readiness_gate.md)
- Boot & deploy traps: [bootstrap-ordering.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md), [deployment-deadlock.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/deployment-deadlock.md), [predeploy-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md)
- Retrieval integrity: [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md), [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)
- Embedding vs meaning: [embedding-vs-semantic.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)
- Query split & reranking: [pattern_query_parsing_split.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_query_parsing_split.md), [rerankers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md)

---

## What to pin (and where)
| Layer | Pin fields | Why it matters |
|---|---|---|
| **LLM model** | `MODEL_VER`, provider model ID, decoding params | Minor provider updates shift ΔS/λ; force exact version and params. |
| **Prompt pack** | `PROMPT_VER`, header checksum | Header order changes λ; lock and audit. |
| **Embedding** | `EMBED_MODEL_VER`, `EMBED_DIM`, `NORM`, metric | Any mismatch breaks neighborhood semantics. |
| **Reranker** | `RERANK_CONF`, model/ver, cutoff | Top-k order flips alter ΔS and coverage. |
| **Tokenizer/Analyzer** | `TOK_VER`, `ANALYZER_CONF` | CJK/diacritics/full/half width change token boundaries. |
| **Chunker** | `CHUNK_SCHEMA_VER`, overlap, window | Alters anchor alignment and traceability. |
| **Index** | `INDEX_HASH`, build time, doc schema | Guarantees the retriever sees the tested graph. |
| **Tools/Functions** | `TOOL_SCHEMA_VER` | JSON looseness raises ΔS and loop risk. |

---

## Acceptance targets
- Prod = Staging for: `MODEL_VER`, `PROMPT_VER`, `EMBED_MODEL_VER`, `EMBED_DIM`, `NORM`, `metric`, `RERANK_CONF`, `TOK_VER`, `ANALYZER_CONF`, `CHUNK_SCHEMA_VER`, `INDEX_HASH`.  
- ΔS(question, retrieved) ≤ 0.45 and coverage ≥ 0.70 on gold set after pinning.  
- λ convergent across 3 paraphrases and 2 seeds with the pinned headers.  
- First call cold-start passes in ≤ 5 minutes.

---

## 60-second lock checklist
1) **Freeze versions in config**  
   Single source of truth (env or KV) for all fields above; deny deploy if any are unset.
2) **Emit version headers on every request**  
   Log and return: all pins + `BUILD_ID` and `GIT_SHA`. Refuse if missing.
3) **Index integrity**  
   Retriever must assert `INDEX_HASH` matches; otherwise hard-fail with fix tip.
4) **Semantic sanity**  
   Run 20–40 gold items; verify ΔS/coverage/λ targets before canary.

---

## CI/CD gate (paste-ready)
```yaml
# opsdeploy/version_lock.yml
checks:
  require_fields:
    - MODEL_VER
    - PROMPT_VER
    - EMBED_MODEL_VER
    - EMBED_DIM
    - NORM
    - metric
    - RERANK_CONF
    - TOK_VER
    - ANALYZER_CONF
    - CHUNK_SCHEMA_VER
    - INDEX_HASH
  assert_equal_envs:
    - { field: MODEL_VER, envs: [staging, prod] }
    - { field: PROMPT_VER, envs: [staging, prod] }
    - { field: EMBED_MODEL_VER, envs: [staging, prod] }
    - { field: INDEX_HASH, envs: [staging, prod] }
  deny_if_missing: true
  deny_if_changed_without_alias_swap: [INDEX_HASH]
decision:
  on_fail: block_rollout
  on_pass: proceed
artifacts:
  - logs/version_manifest.json
  - logs/index_hash.txt
````

---

## Runtime header contract (client/server)

**Client must send**
`X-WFGY: MODEL_VER,PROMPT_VER,EMBED_MODEL_VER,EMBED_DIM,NORM,metric,RERANK_CONF,TOK_VER,ANALYZER_CONF,CHUNK_SCHEMA_VER,INDEX_HASH,BUILD_ID,GIT_SHA`

**Server must validate**

* All fields present.
* Exact match to server’s pins.
* If mismatch: return 409 + a JSON diff and links to fix pages.

---

## Typical failure → exact fix

* High similarity but wrong meaning after “minor” update
  → [embedding-vs-semantic.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)
* Top-k order unstable between runs
  → [rerankers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md), [pattern\_query\_parsing\_split.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/patterns/pattern_query_parsing_split.md)
* CJK/diacritics behavior changes post-deploy
  → tokenizer/analyzer pins; verify with [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)
* First call crashes or uses old index
  → [bootstrap-ordering.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md), [predeploy-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md)

---

## Version manifest example

```json
{
  "MODEL_VER": "gpt-4o-2025-07-15",
  "PROMPT_VER": "p-2025.08.31-h1",
  "EMBED_MODEL_VER": "text-embedding-3-large",
  "EMBED_DIM": 3072,
  "NORM": "l2",
  "metric": "cosine",
  "RERANK_CONF": "bge-rerank-v2@top32",
  "TOK_VER": "tiktoken-2025.07",
  "ANALYZER_CONF": "icu-cjk-folding-v3",
  "CHUNK_SCHEMA_VER": "s128/o32",
  "INDEX_HASH": "a1d9f0...e7",
  "BUILD_ID": "2025.08.31.01",
  "GIT_SHA": "abcdef1"
}
```

---

## Rollback note

If any pin drifts in prod, treat as outage. Block writes, flip to Blue/previous alias, then reopen with:
[blue\_green\_switchovers.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/OpsDeploy/blue_green_switchovers.md)

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

