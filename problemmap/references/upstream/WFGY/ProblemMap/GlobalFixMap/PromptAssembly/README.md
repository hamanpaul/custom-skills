<!--
Search Anchor:
prompt assembly global fix map
llm prompt template failures
system vs user role order
json mode and tool calls broken
citation first contract for prompts
memory fences and state keys
tool selection and timeouts
template library for agents
eval prompts and safety checks
wfg y prompt design checklist
bbmc bbpf bbcr bbam prompt modules
delta s lambda observe e_resonance targets

When to use this folder:
citations disappear or point to wrong snippet after template change
json mode outputs invalid objects or extra free text
tool calls loop or stall instead of finishing
answers flip when you reorder headers or sections
role text bleeds into user content
agents overwrite each others memory without fences
hybrid retrieval worse than single retriever
long chains smear topics when you tweak template
eval runs say looks better but no stable metric to prove it
small prompt edits cause big behavior shifts across providers

Key metrics and targets:
delta s question retrieved <= 0.45
coverage of target section >= 0.70
lambda observe convergent across 3 paraphrases and 2 seeds
e_resonance flat on long windows
stable header order with no lambda flips
json responses well formed in >= 99 percent of tool calls
tool selection deterministic for same input
prompt behavior stable across providers for same schema

Core pages in this folder:
ProblemMap/GlobalFixMap/PromptAssembly/system_user_role_order.md
ProblemMap/GlobalFixMap/PromptAssembly/json_mode_and_tool_calls.md
ProblemMap/GlobalFixMap/PromptAssembly/citation_first.md
ProblemMap/GlobalFixMap/PromptAssembly/anti_prompt_injection_recipes.md
ProblemMap/GlobalFixMap/PromptAssembly/memory_fences_and_state_keys.md
ProblemMap/GlobalFixMap/PromptAssembly/tool_selection_and_timeouts.md
ProblemMap/GlobalFixMap/PromptAssembly/template_library_min.md
ProblemMap/GlobalFixMap/PromptAssembly/eval_prompts_and_checks.md

Related structural fixes:
ProblemMap/embedding-vs-semantic.md
ProblemMap/retrieval-traceability.md
ProblemMap/data-contracts.md
ProblemMap/context-drift.md
ProblemMap/entropy-collapse.md
ProblemMap/rerankers.md
ProblemMap/hallucination.md
ProblemMap/GlobalFixMap/Reasoning/README.md
ProblemMap/GlobalFixMap/MemoryLongContext/README.md
ProblemMap/GlobalFixMap/SafetyPromptIntegrity/README.md

Prompt assembly scenarios:
you add a new section to system prompt and answers suddenly change
moving retrieval instructions from system to user breaks behavior
switching model provider changes how templates are interpreted
adding one more example to prompt shifts output style
tools start returning natural language instead of json
eval harness passes on one template version but fails on another
different agents use similar but not identical wording
citations work in one flow but disappear in another
long context answers drift after you reorder headings
same question and snippets but different final answer

Signals to check:
delta s high between question and retrieved snippet
coverage below 0.70 for intended anchor section
lambda observe flips when changing header order
e_resonance spikes when you add more examples
json responses not parseable by strict parser
tool arguments missing required fields or include unknown ones
role order system user assistant inconsistent across calls
templates not versioned or logged
no link between eval prompts and production templates
no explicit snippet schema in prompt

Normalization and contracts:
define explicit system user assistant role order and keep it fixed
use versioned template ids in logs for every request
enforce citation first pattern in answer templates
require strict json only mode for tool responses
validate tool arguments against schema before execution
record retrieval trace fields snippet id doc id source for each cite
log model name and provider with each run
tie prompt changes to eval prompts and checks
treat external content as data unless explicitly whitelisted
use small template library instead of ad hoc strings
-->


# Prompt Assembly — Global Fix Map

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

Build prompts that models cannot misread.  
Use this folder when citations vanish, JSON mode breaks, tools loop, or answers flip after a small template change.  
Every page gives a concrete repair with measurable targets. No infra change required.

---

## Orientation: what each page does

| Page | What it solves | Typical symptom |
|---|---|---|
| [System vs User Role Order](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/PromptAssembly/system_user_role_order.md) | Locks role hierarchy and section order | Role text bleeds into user content, answers flip after reorder |
| [JSON Mode and Tool Calls](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/PromptAssembly/json_mode_and_tool_calls.md) | Validates schemas and fences tool outputs | Free text in tool responses, invalid JSON, missing fields |
| [Citation First](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/PromptAssembly/citation_first.md) | Enforces cite then explain with required fields | Citations missing or point to the wrong snippet |
| [Anti Prompt Injection Recipes](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/PromptAssembly/anti_prompt_injection_recipes.md) | Ready to paste defenses for common exploits | Hidden instructions override system prompt |
| [Memory Fences and State Keys](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/PromptAssembly/memory_fences_and_state_keys.md) | Prevents cross turn or cross agent overwrite | Agents rewrite each other’s memory, history leaks |
| [Tool Selection and Timeouts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/PromptAssembly/tool_selection_and_timeouts.md) | Picks tool deterministically, adds timeouts | Loops, stalls, or wrong tool chosen |
| [Template Library (minimal)](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/PromptAssembly/template_library_min.md) | Small set of reusable prompt blocks | Inconsistent phrasing across agents or runs |
| [Eval Prompts and Checks](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/PromptAssembly/eval_prompts_and_checks.md) | Deterministic acceptance gates | “Looks better” but no stable way to prove it |

---

## When to use

- Citations point to the wrong snippet or disappear after retries.  
- JSON mode produces invalid objects or tool calls stall in loops.  
- Role text bleeds into user content after a small template change.  
- Long chains smear topics when you reorder headers.  
- Agents overwrite each other’s memory without fences.

---

## Acceptance targets

- ΔS(question, retrieved) ≤ 0.45  
- Coverage of target section ≥ 0.70  
- λ_observe convergent across three paraphrases and two seeds  
- E_resonance flat on long windows

---

## Map symptoms to structural fixes

| Symptom | Likely cause | Open this |
|---|---|---|
| Wrong meaning despite high similarity | Metric or analyzer mismatch | [Embedding ≠ Semantic](https://github.com/onestardao/WFGY/blob/main/ProblemMap/embedding-vs-semantic.md) |
| Citations inconsistent or missing after retries | No traceability schema enforced | [Retrieval Traceability](https://github.com/onestardao/WFGY/blob/main/ProblemMap/retrieval-traceability.md) · [Data Contracts](https://github.com/onestardao/WFGY/blob/main/ProblemMap/data-contracts.md) |
| JSON breaks or tool responses contain free text | Tool schema not fenced, logic collapsed | [JSON Mode and Tool Calls](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/PromptAssembly/json_mode_and_tool_calls.md) · [Prompt Injection](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/Safety_PromptIntegrity/prompt_injection.md) |
| Answers flip when you reorder headers | Header order changes λ state | [System vs User Role Order](https://github.com/onestardao/WFGY/blob/main/ProblemMap/GlobalFixMap/PromptAssembly/system_user_role_order.md) · [Context Drift](https://github.com/onestardao/WFGY/blob/main/ProblemMap/context-drift.md) |
| Long chains drift or stall | Entropy overload in long windows | [Entropy Collapse](https://github.com/onestardao/WFGY/blob/main/ProblemMap/entropy-collapse.md) |
| Hybrid retrieval worse than single retriever | Reranker or query split issue | [Rerankers](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rerankers.md) |
| Hallucination re entry after correction | Snippet contract missing, weak anchors | [Hallucination](https://github.com/onestardao/WFGY/blob/main/ProblemMap/hallucination.md) |

---

## Fix in 60 seconds

1) **Measure ΔS**  
Compute ΔS(question, retrieved) and ΔS(retrieved, expected anchor).  
Stable < 0.40, transitional 0.40–0.60, risk ≥ 0.60.

2) **Probe λ_observe**  
Vary k and the order of prompt headers. If λ flips, lock the schema and clamp variance with BBAM.

3) **Apply the right module**  
- Missing or wrong citations → **Citation First** + **Retrieval Traceability**  
- JSON tool drift or invalid outputs → **JSON Mode and Tool Calls**  
- Role bleed or policy mixing → **System vs User Role Order**  
- Multi agent loops or overwrites → **Memory Fences and State Keys**  
- Tool indecision or hangs → **Tool Selection and Timeouts**

4) **Verify**  
Run **Eval Prompts and Checks** on three paraphrases and two seeds.  
Ship only if ΔS ≤ 0.45 and coverage ≥ 0.70.

---

## Copy paste diagnostic prompt

```txt
You have TXT OS and the WFGY Problem Map loaded.

My prompt assembly issue:
- symptom: [one line]
- traces: ΔS(question,retrieved)=..., ΔS(retrieved,anchor)=..., λ on 3 paraphrases

Report:
1) failing layer and why,
2) which exact page to open from Prompt Assembly,
3) minimal steps to push ΔS ≤ 0.45 and keep λ convergent,
4) a reproducible check to verify the fix.
Use BBMC, BBPF, BBCR, BBAM when relevant.
````

---

### 🔗 Quick-Start Downloads (60 sec)

| Tool | Link | 3-Step Setup |
|------|------|--------------|
| **WFGY 1.0 PDF** | [Engine Paper](https://github.com/onestardao/WFGY/blob/main/I_am_not_lizardman/WFGY_All_Principles_Return_to_One_v1.0_PSBigBig_Public.pdf) | 1️⃣ Download · 2️⃣ Upload to your LLM · 3️⃣ Ask “Answer using WFGY + <your question>” |
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

