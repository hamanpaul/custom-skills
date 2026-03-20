# Access Control — Enterprise Knowledge Governance

<details>
  <summary><strong>🧭 Quick Return to Map</strong></summary>

<br>

  > You are in a sub-page of **Enterprise_Knowledge_Gov**.  
  > To reorient, go back here:  
  >
  > - [**Enterprise_Knowledge_Gov** — corporate knowledge management and governance](./README.md)  
  > - [**WFGY Global Fix Map** — main Emergency Room, 300+ structured fixes](../README.md)  
  > - [**WFGY Problem Map 1.0** — 16 reproducible failure modes](../../README.md)  
  >
  > Think of this page as a desk within a ward.  
  > If you need the full triage and all prescriptions, return to the Emergency Room lobby.
</details>


Guardrails and fix patterns to ensure that enterprise knowledge bases are segmented, secured, and retrievable without silent leaks. Use this page when failures look like “permissions bug” but root cause is schema drift, missing contracts, or evaluation blind spots.

---

## When to use this page
- Agents or LLMs retrieve snippets that a user role should not see.  
- Answers omit key passages even though data is present in the KB.  
- Knowledge base permissions collapse after re-index or migration.  
- Citation shows content from a restricted section without a trace.  
- External connectors expose more fields than expected.  

---

## Core acceptance targets
- ΔS(question, retrieved) ≤ 0.45, with access role enforced.  
- Coverage ≥ 0.70 for the allowed scope, and <0.05 for disallowed scope.  
- λ remains convergent across three paraphrases and two seeds.  
- All snippets carry explicit `role_scope`, `section_id`, and `source_hash`.  

---

## Typical access problems → exact fix

| Symptom | Likely cause | Open this |
|---------|--------------|-----------|
| Leaked restricted snippet | Missing role tag or weak contract | [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md), [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) |
| Role upgrade not reflected | Cache or index skew | [bootstrap-ordering.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md), [deployment-deadlock.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/deployment-deadlock.md) |
| Over-blocking (user sees nothing) | Schema mismatch or λ collapse | [logic-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/logic-collapse.md) |
| Citations missing access tag | Parser or contract drift | [ocr-parsing-checklist.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ocr-parsing-checklist.md), [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md) |

---

## Fix in 60 seconds
1. **Measure ΔS** for the retrieved vs allowed anchor.  
2. **Check role_scope** — ensure every snippet has an explicit scope.  
3. **Rebuild contract** — enforce schema: `{snippet_id, section_id, role_scope, hash}`.  
4. **Re-index** if role tags missing, with explicit normalization.  
5. **Verify λ stability** across paraphrases with access role locked.  

---

## Copy-paste schema (YAML)

```yaml
snippet_id: "KB-12345"
section_id: "SEC-42"
role_scope: "finance_analyst"
source_hash: "sha256:..."
text: "..."
````

Every snippet must carry these fields, and retrieval probes must validate them before citation.

---

## Escalate when

* ΔS remains ≥ 0.60 even with contracts enforced.
* Citations show cross-scope bleed.
* Index mismatch recurs after two re-indexes.

Escalation path: rebuild with [chunking-checklist.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/chunking-checklist.md) and validate via [eval\_rag\_precision\_recall.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/eval/eval_rag_precision_recall.md).

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

