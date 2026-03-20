# Privacy and PII Edges for Serverless and Edge

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


A field guide to prevent PII from leaking through serverless runtimes, edge functions, logs, vector pipelines, and third-party webhooks. Build a measurable privacy boundary that does not break retrieval quality.

## Open these first

* Boundary schemas: [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md) · [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)
* Adversarial inputs: [Prompt Injection](https://github.com/onestardao/WFGY/blob/main/ProblemMap/prompt-injection.md) · [Bluffing Controls](https://github.com/onestardao/WFGY/blob/main/ProblemMap/bluffing.md)
* Ops companions: [Egress Rules and Webhooks](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Cloud_Serverless/egress_rules_and_webhooks.md) · [Secrets Rotation](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Cloud_Serverless/secrets_rotation.md) · [Observability and SLO](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Cloud_Serverless/observability_slo.md)
* Data lifecycle: [Data Retention and Backups](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Cloud_Serverless/data_retention_and_backups.md) · [Edge Cache Invalidation](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Cloud_Serverless/edge_cache_invalidation.md)

---

## Core acceptance

* **Zero PII in logs**
  Random 1 percent log sampling shows 0 findings across 7 days for names, emails, phones, addresses, national IDs, payment tokens, secrets.

* **PII detection coverage ≥ 0.95**
  Gold set with labeled traces across API, edge, queue, storage. False negatives are zero on critical classes.

* **Egress allowlist is enforced**
  All outbound webhooks and calls flow through an allowlist and DLP filter with redact or block. No raw PII leaves your account.

* **Semantic quality holds after redaction**
  Median ΔS(question, retrieved) ≤ 0.45 and coverage ≥ 0.70 after masked or tokenized fields. λ remains convergent across three paraphrases.

* **DSR path is verified**
  Delete or export requests complete within policy. Evidence stored with counts and checksums.

---

## Fix in 60 seconds

1. **Measure reality**
   Run a log sample and store scan for PII classes. Tag hits by edge, function, and sink.

2. **Add a redaction gate**
   Place a single pre-inference filter that masks PII at the prompt-builder and tool-argument layers. Keep a reversible token only when business-critical.

3. **Lock egress**
   Route all webhooks and HTTP clients through an allowlist and DLP transform. Block unknown domains.

4. **Verify retrieval**
   Re-run ΔS and coverage probes on your gold questions. If quality drops, update the chunking recipe or token map.

Open: [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md) · [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md)

---

## Design the privacy boundary

**Collection**

* Show purpose tags and consent flags at capture.
* Normalize fields at the edge: email → lowercased hash for joins, phone → E.164 masked form.

**Transit**

* TLS everywhere. mTLS for webhooks that carry sensitive payloads.
* Encrypt PII subsets with KMS before leaving the VPC or account.

**Processing**

* Build prompts from structured fields only. Forbid free-text concatenation that mixes policy and user content.
* Redact PII classes at the prompt-builder and tool argument marshaling.

**At rest**

* Separate PII store from product data. Distinct KMS keys and IAM paths.
* Keep a token map with rotation windows and short TTL for re-identification.

**Egress**

* Require allowlist, DLP transform, and signed requests.
* Log outbound diff before and after transform with content hashes.

Open: [Egress Rules and Webhooks](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Cloud_Serverless/egress_rules_and_webhooks.md)

---

## Redaction and tokenization patterns

* **Mask-in-place**
  Keep surface form for model context, mask internals: `john.smith@example.com` → `j***@example.com`.

* **Deterministic token**
  Stable join keys for analytics without exposure: `EMAIL_TOKEN = HMAC_SHA256(k, email)`.

* **Pseudonym dictionary**
  Replace entities with class-aware tags: `PERSON_014`, `ORG_022`, `ADDR_105`. Maintain a scoped map per tenant.

* **Secrets and high-entropy**
  Detect 32 to 64 char base64 and hex blobs and known prefixes. Always drop, never mask.

* **Vector store safety**
  Prevent raw PII from entering embeddings. Use a preprocess step that replaces PII with pseudonyms and carries a sidecar map. Rehydrate only for authorized views.
  Open: [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md)

---

## Common failure smells and exact fix

* **“We never log PII” but alerts show emails in traces**
  Turn off request body logging and header dumps. Add a scrubber to log sinks and test with a gold set.
  Open: [Observability and SLO](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Cloud_Serverless/observability_slo.md)

* **LLM answers include live tokens or IDs**
  Tighten tool schemas and forbid free text in argument fields.
  Open: [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md) · [Prompt Injection](https://github.com/onestardao/WFGY/blob/main/ProblemMap/prompt-injection.md)

* **Webhook mirrors full customer records to third parties**
  Move the DLP step before the HTTP client. Enforce allowlist by hostname and path.
  Open: [Egress Rules and Webhooks](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Cloud_Serverless/egress_rules_and_webhooks.md)

* **Restores re-introduce raw PII into vectors**
  Validate index manifests and re-run the preprocessing recipe after restore.
  Open: [Data Retention and Backups](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Cloud_Serverless/data_retention_and_backups.md)

* **Key rotation breaks token maps**
  Version tokens and carry `token_v`. Rotate with overlap and dual-read, single-write.
  Open: [Secrets Rotation](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Cloud_Serverless/secrets_rotation.md)

---

## Verification suite

* **PII scanners** on logs, storage, vector payloads, prompts, tool args.
* **ΔS and coverage probes** on a masked vs unmasked evaluation set.
* **Egress audits** with counts by destination and transform status.
* **DSR drills**: export and delete flows, evidence with counts and checksums.

Open: [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) · [Live Monitoring for RAG](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/live_monitoring_rag.md) · [Debug Playbook](https://github.com/onestardao/WFGY/blob/main/ProblemMap/ops/debug_playbook.md)

---

## Copy-paste LLM prompt for PII audits

```txt
You have TXT OS and the WFGY Problem Map loaded.

Audit my privacy boundary:

- entry points: [edge functions, APIs, queues]
- detectors: [regex, entropy, NER]
- egress routes: [domains, auth, DLP steps]
- vector policy: [preprocess recipe, sidecar map]
- log scans: [last 7 days summary]

Tell me:
1) where PII can leak and which WFGY pages to open,
2) the minimal redaction+tokenization plan that preserves ΔS ≤ 0.45 and coverage ≥ 0.70,
3) the allowlist+DLP rules for egress,
4) a short JSON with risk classes, counts, and next fixes.
Keep it auditable and short.
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

