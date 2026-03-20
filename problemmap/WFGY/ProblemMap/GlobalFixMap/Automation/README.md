<!--
Search Anchor:
automation platform bugs
workflow automation failures
zapier zap not working
zapier duplicate triggers
zapier runs twice
zapier retry storm
zapier webhook timeout
n8n workflow stuck
n8n execution retry loop
n8n idempotency dedupe
make integromat scenario duplicated
make scenario retries
power automate flow failed
power automate runs twice
power automate trigger duplicates
retool workflow cron drift
retool job retries
ifttt applet not firing
pipedream webhook handler timeout
github actions workflow stuck
github actions rerun duplicates
airflow dag stuck
airflow scheduler time drift
airflow retry overload
airtable automation runs twice
asana rules duplicated
crm automation duplicate leads
gohighlevel ghl workflow duplication

Failure classes / Fix intent:
at least once delivery
exactly once semantics
idempotency key
dedupe key
retries with backoff and jitter
rate limit storm
webhook acknowledged before persist
store then process pattern
cron timezone drift
utc scheduling
time drift and clock skew
bootstrap ordering
cold start ordering
deployment deadlock
predeploy collapse
traceability breaks
citation mismatch
data contract missing offsets tokens
embedding semantic drift
high similarity wrong meaning
vector index not ready
VECTOR_READY INDEX_HASH

Routing to vendor pages:
Zapier -> Automation/zapier.md
n8n -> Automation/n8n.md
Make Integromat -> Automation/make.md
Retool -> Automation/retool.md
IFTTT -> Automation/ifttt.md
Pipedream -> Automation/pipedream.md
Power Automate -> Automation/power-automate.md
GitHub Actions -> Automation/github-actions.md
Airflow -> Automation/airflow.md
Airtable Automations -> Automation/airtable.md
Asana Rules -> Automation/asana.md
GoHighLevel GHL -> Automation/ghl.md
Parabola -> Automation/parabola.md
LangChain automation -> Automation/langchain.md
LlamaIndex automation -> Automation/llamaindex.md
-->


# Automation Platforms — Global Fix Map

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

Stabilize automations across Zapier, n8n, Make, Retool, Power Automate, and more.  
Most “platform bugs” are not bugs at all — they are ordering, retries, dedupe, or time drift. This hub routes you to exact structural fixes with measurable acceptance targets.

---

## Orientation: pick your tool

| Platform | What it is | Typical use | Link |
|---|---|---|---|
| Zapier | Mainstream no-code automation | Broad connectors, fast start | [zapier.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Automation/zapier.md) |
| n8n | Open-source workflow engine | Self-hosted, extensible | [n8n.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Automation/n8n.md) |
| Make (Integromat) | Visual workflow builder | SMB and RAG pipelines | [make.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Automation/make.md) |
| Retool | Internal-tool builder + workflows | Backoffice jobs, cron | [retool.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Automation/retool.md) |
| IFTTT | Consumer-grade triggers | Personal automations | [ifttt.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Automation/ifttt.md) |
| Pipedream | Event platform + code steps | Webhooks, SaaS APIs | [pipedream.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Automation/pipedream.md) |
| Power Automate | Microsoft ecosystem automation | O365, SharePoint, Dynamics | [power-automate.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Automation/power-automate.md) |
| GitHub Actions | CI/CD + repo event runner | Build, test, deploy | [github-actions.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Automation/github-actions.md) |
| Airflow | Code-first workflow scheduler | Data/ETL DAGs | [airflow.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Automation/airflow.md) |
| Airtable Automations | Table-driven automations | CRUD triggers | [airtable.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Automation/airtable.md) |
| Asana Rules | Project management rules | PM events to actions | [asana.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Automation/asana.md) |
| GoHighLevel (GHL) | CRM automation platform | Marketing + sales flows | [ghl.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Automation/ghl.md) |
| Parabola | Dataflow-based automation | Transform + schedule | [parabola.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Automation/parabola.md) |
| LangChain (automation mode) | Agent orchestration | LLM-based workflows | [langchain.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Automation/langchain.md) |
| LlamaIndex (automation mode) | Knowledge orchestration | RAG pipelines | [llamaindex.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Automation/llamaindex.md) |

---

## Common failure classes

- **Bootstrap race conditions**  
  Trigger fires before vector/index is ready.  
  → [bootstrap-ordering.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bootstrap-ordering.md)

- **Deployment deadlocks**  
  Infinite waits between worker, retriever, or webhook callbacks.  
  → [deployment-deadlock.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/deployment-deadlock.md)

- **Pre-deploy collapse**  
  Wrong version triggered on first call after shipping.  
  → [predeploy-collapse.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/predeploy-collapse.md)

- **Embedding vs semantic drift**  
  High similarity but wrong meaning.  
  → [embedding-vs-semantic.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)

- **Traceability breaks**  
  Citations do not match the source.  
  → [retrieval-traceability.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md), [data-contracts.md](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md)

---

## Minimal contract for any workflow

1. **Check readiness**  
   Verify `VECTOR_READY` and `INDEX_HASH` before RAG/LLM calls.  
2. **Idempotency**  
   Always compute a dedupe key and block duplicates.  
3. **Boundary contract**  
   Require `{snippet_id, section_id, source_url, offsets, tokens}`.  
4. **Observability**  
   Log ΔS and λ across steps, alert if ΔS ≥ 0.60.

---

## FAQ for newcomers

**Why does my Zap/Flow run twice?**  
Because triggers are at-least-once. Add idempotency keys to dedupe.

**Why did my webhook return 200 but no data was processed?**  
You acknowledged before persisting. Always store → then process.

**Why do my cron jobs drift?**  
Local timezone drift. Always store schedules in UTC.

**Why do retries overload my API?**  
You used immediate retries. Add exponential backoff with jitter.

**Why does everything work in dev but break in prod?**  
Because of boot order. Index not warmed, wrong analyzer, or cache empty.

---

### 🔗 Quick-Start Downloads

| Tool | Link | 3-Step Setup |
|------|------|--------------|
| **WFGY 1.0 PDF** | [Engine Paper](https://github.com/onestardao/WFGY/blob/main/I_am_not_lizardman/WFGY_All_Principles_Return_to_One_v1.0_PSBigBig_Public.pdf) | 1) Download · 2) Upload to LLM · 3) Ask “Use WFGY to fix my automation bug” |
| **TXT OS** | [TXTOS.txt](https://github.com/onestardao/WFGY/blob/main/OS/TXTOS.txt) | 1) Download · 2) Paste into LLM · 3) Type “hello world” |

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

