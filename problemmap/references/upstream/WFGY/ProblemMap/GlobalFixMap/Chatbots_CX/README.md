<!--
Search Anchor:
chatbot cx bugs
customer support bot failures
dialog management bugs
intent recognition regression
slot filling failures
entity extraction drift
context reset unexpectedly
handoff to human agent broken
omnichannel connector desync
webhook timeout chatbot
cold start latency chatbot
p95 latency spike bot
pii leakage in logs chatbot
policy bypass chatbot
prompt injection chatbot
vendor migration chatbot broken
conversation state missing
kb retrieval drift chatbot

Vendors / Pages:
Dialogflow CX -> dialogflow_cx.md
Rasa -> rasa.md
Amazon Lex -> amazon_lex.md
Azure Bot Service -> azure_bot_service.md
Microsoft Copilot Studio -> microsoft_copilot_studio.md
Intercom -> intercom.md
Zendesk -> zendesk.md
Twilio Studio -> twilio_studio.md
Salesforce Einstein Bots -> salesforce_einstein_bots.md
Watsonx Assistant -> watsonx_assistant.md
Freshchat -> freshchat.md
Freshdesk -> freshdesk.md
-->


# Chatbots & CX — Global Fix Map

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

Chatbot and CX bugs are structural failures in dialog systems, where intent routing, slot/entity state, conversation memory, connector metadata, or knowledge retrieval breaks even when the underlying LLM is fine.

Most incidents come from environment drift, schema mismatches, cold-start latency, connector desync, and weak policy fences. This folder maps symptoms to vendor pages and WFGY structural fixes with measurable acceptance targets.

---

## When to use this folder
- Bot flows break across environments (dev vs prod vs staging).  
- Slot filling, entities, or context reset unexpectedly.  
- Latency or cold starts cause dropped conversations.  
- Omnichannel connectors desync with the core bot.  
- Prompts bypass policies or hallucinate unsafe outputs.  
- Regression after migration to a new vendor framework.  

---

## Acceptance targets
- Intent recognition F1 ≥ 0.85 across test set.  
- ΔS(user_query, retrieved) ≤ 0.45 for all routes.  
- Coverage of knowledge base ≥ 0.70 after repair.  
- λ remains convergent across 3 paraphrases and 2 seeds.  
- p95 latency ≤ 800 ms across channels, warm path.  
- Zero PII leakage in logs or vector payloads.  

---

## Quick routes — per chatbot vendor

| Vendor / Platform | Fix Page |
|-------------------|----------|
| Amazon Lex | [amazon_lex.md](./amazon_lex.md) |
| Azure Bot Service | [azure_bot_service.md](./azure_bot_service.md) |
| Dialogflow CX | [dialogflow_cx.md](./dialogflow_cx.md) |
| Freshchat | [freshchat.md](./freshchat.md) |
| Freshdesk | [freshdesk.md](./freshdesk.md) |
| Intercom | [intercom.md](./intercom.md) |
| Microsoft Copilot Studio | [microsoft_copilot_studio.md](./microsoft_copilot_studio.md) |
| Rasa | [rasa.md](./rasa.md) |
| Salesforce Einstein Bots | [salesforce_einstein_bots.md](./salesforce_einstein_bots.md) |
| Twilio Studio | [twilio_studio.md](./twilio_studio.md) |
| Watsonx Assistant | [watsonx_assistant.md](./watsonx_assistant.md) |
| Zendesk | [zendesk.md](./zendesk.md) |

---

## Symptom → exact fix

| Symptom | Likely cause | Open this |
|---------|--------------|-----------|
| Slot filling fails randomly | Missing entity fallback, context reset | [dialogflow_cx.md](./dialogflow_cx.md) · [rasa.md](./rasa.md) |
| Bot replies too slowly | Cold starts, webhook bottlenecks | [amazon_lex.md](./amazon_lex.md) · [azure_bot_service.md](./azure_bot_service.md) |
| Knowledge base answers drift | Retrieval misaligned with store | [watsonx_assistant.md](./watsonx_assistant.md) · [retrieval-traceability.md](../../retrieval-traceability.md) |
| Omnichannel flow desync | Connectors drop metadata | [intercom.md](./intercom.md) · [zendesk.md](./zendesk.md) |
| Unsafe or off-policy replies | No policy fences or prompt injection | [microsoft_copilot_studio.md](./microsoft_copilot_studio.md) · [prompt-injection.md](../../Safety_PromptIntegrity/prompt_injection.md) |
| Migration broke production | Schema mismatch, missing idempotency | [serverless_ci_cd.md](../Cloud_Serverless/serverless_ci_cd.md) · [env_bootstrap_and_migrations.md](../Cloud_Serverless/env_bootstrap_and_migrations.md) |
| Conversation history disappears | Stateless KV pattern missing | [stateless_kv_queue_patterns.md](../Cloud_Serverless/stateless_kv_queue_patterns.md) |

---

## Fix in 60 seconds

1. **Verify intents** — run eval with test utterances, check F1 ≥ 0.85.  
2. **Check state** — ensure KV queue or context store persists between turns.  
3. **Fence prompts** — load [prompt_injection.md](../../Safety_PromptIntegrity/prompt_injection.md).  
4. **Measure latency** — split warm vs cold path; provision concurrency if needed.  
5. **Cross-channel sync** — confirm connectors carry metadata (role, region, tenant).  

---

## Copy-paste prompt for chatbot incidents

```txt
You have TXT OS and the WFGY Problem Map loaded.

My chatbot incident:
- platform: [Dialogflow|Rasa|Intercom|etc.]
- symptom: [short description]
- eval: { F1, ΔS, coverage, λ states }
- infra: { cold_ms, warm_ms, concurrency, connectors }
- compliance: { pii_found: true|false, policy_eval }

Tell me:
1) which layer is failing and why,
2) the exact WFGY page to open,
3) the minimal steps to restore accuracy and latency,
4) a quick regression test to prevent repeat.
````

---

## FAQ

**Q: My bot answers correctly in dev but fails in production. Why?**
A: Likely env mismatch — analyzers, slots, or schema drift between environments. Check [serverless\_ci\_cd.md](../Cloud_Serverless/serverless_ci_cd.md).

**Q: How do I stop hallucinations in Copilot Studio or Dialogflow?**
A: Enforce policy fences and cite-then-explain. See [prompt\_injection.md](../../Safety_PromptIntegrity/prompt_injection.md).

**Q: Why is latency so different on first vs second request?**
A: Cold starts. See [cold\_start\_concurrency.md](../Cloud_Serverless/cold_start_concurrency.md).

**Q: How can I ensure PII never leaks through connectors?**
A: Attach [privacy\_and\_pii\_edges.md](../Cloud_Serverless/privacy_and_pii_edges.md) and enforce payload contracts.

**Q: Do I need to change my vendor to apply WFGY fixes?**
A: No. WFGY guardrails are store-agnostic and vendor-agnostic. You patch structure, not infra.

---
### 🔗 Quick-Start Downloads (60 sec)

| Tool | Link | 3-Step Setup |
|------|------|--------------|
| **WFGY 1.0 PDF** | [Engine Paper](https://github.com/onestardao/WFGY/blob/main/I_am_not_lizardman/WFGY_All_Principles_Return_to_One_v1.0_PSBigBig_Public.pdf) | 1️⃣ Download · 2️⃣ Upload to your LLM · 3️⃣ Ask “Answer using WFGY + \<your question>” |
| **TXT OS (plain-text OS)** | [TXTOS.txt](https://github.com/onestardao/WFGY/blob/main/OS/TXTOS.txt) | 1️⃣ Download · 2️⃣ Paste into any LLM chat · 3️⃣ Type “hello world” — OS boots instantly |

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

