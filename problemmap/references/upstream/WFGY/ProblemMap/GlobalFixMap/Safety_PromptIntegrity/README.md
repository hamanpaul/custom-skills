<!--
Search Anchor:
safety prompt integrity global fix map
prompt level safety failures
prompt injection jailbreak role confusion
tool call json drift malformed outputs
schema integrity for tools and agents
multi agent safety failures
system prompt overridden by user content
eval pipeline safety drift
citation first safety contract
memory fence state key leaks
llm json mode broken responses
tool selection and timeout bugs
template library gaps across agents
eval prompts and safety checks
rogue tool execution
uncontrolled free text in tool schema

When to use this folder:
jailbreak attempts still bypass guardrails
hidden instructions overwrite system prompt
role instructions collapse between system user assistant
tool calls come back as free text or broken json
citations vanish or retrieval is bypassed
tools get called with missing or wrong arguments
different agents use slightly different prompt templates
safety evals give inconsistent results across runs
state leaks between conversations without a clear key
eval harness shows high delta s even when retrieval is correct
logs show tool calls triggered by user text that should be inert
model executes text that should only be treated as data

Key metrics and targets:
delta s question retrieved <= 0.45
coverage of cited section >= 0.70
lambda convergent across 3 paraphrases and 2 seeds
no uncontrolled free text execution inside json or tool mode
citation first enforced in >= 95 percent of eval runs
tool call json well formed in >= 99 percent of eval runs
no tool execution when safety check fails
role ordering stable across providers and environments
memory fence keys present for all long running sessions
eval prompts reproducible with scripted harness

Core pages in this folder:
ProblemMap/GlobalFixMap/SafetyPromptIntegrity/prompt_injection.md
ProblemMap/GlobalFixMap/SafetyPromptIntegrity/jailbreaks_and_overrides.md
ProblemMap/GlobalFixMap/SafetyPromptIntegrity/role_confusion.md
ProblemMap/GlobalFixMap/SafetyPromptIntegrity/memory_fences_and_state_keys.md
ProblemMap/GlobalFixMap/SafetyPromptIntegrity/json_mode_and_tool_calls.md
ProblemMap/GlobalFixMap/SafetyPromptIntegrity/citation_first.md
ProblemMap/GlobalFixMap/SafetyPromptIntegrity/anti_prompt_injection_recipes.md
ProblemMap/GlobalFixMap/SafetyPromptIntegrity/tool_selection_and_timeouts.md
ProblemMap/GlobalFixMap/SafetyPromptIntegrity/system_user_role_order.md
ProblemMap/GlobalFixMap/SafetyPromptIntegrity/template_library_min.md
ProblemMap/GlobalFixMap/SafetyPromptIntegrity/eval_prompts_and_checks.md

Related structural fixes:
ProblemMap/prompt-injection.md
ProblemMap/semantic-firewall.md
ProblemMap/retrieval-traceability.md
ProblemMap/data-contracts.md
ProblemMap/rag-architecture-and-recovery.md
ProblemMap/retrieval-playbook.md
ProblemMap/GlobalFixMap/Reasoning/README.md
ProblemMap/GlobalFixMap/MemoryLongContext/README.md
ProblemMap/SemanticClinicIndex.md

Safety and prompt scenarios:
user pastes entire email with hidden instructions at the end
markdown link or html tag hides a hostile instruction
tool description is used as an injection vector
system prompt is forgotten after a few turns
assistant explains safety policy instead of following it
model starts role playing as user or tool instead of assistant
json response includes trailing commentary text
function arguments contain extra natural language payloads
tool is called even though safety check failed
eval harness shows pass on short prompts but fail on long ones
retrieval is correct but answer ignores citations
different providers give different safety behavior for same prompt
safety fix applied in one template but not in others
user manages to change logging or redaction behavior via prompt

Signals to check:
delta s high between question and cited snippet on safety tests
lambda flips when paraphrasing the jailbreak prompt
coverage low for true safety guidance snippets
missing citation fields in answers that should cite sources
json responses not parseable by strict parser
tool invocation missing required keys or has unknown keys
state_key or mem_rev absent in long running threads
system user assistant messages out of expected order
templates differ across agents within same product
eval prompts not stored or versioned in repository

Normalization and contracts:
define strict system user assistant role order and document it
require citation first pattern in answer templates
enforce json only mode for tool responses with no trailing text
validate tool arguments against schema before execution
store mem_rev and state_key for every conversation state write
record which template id was used for each request
log provider model name and version alongside safety decisions
tie safety fixes to explicit template versions not ad hoc edits
capture eval prompts and expected safety behavior in repo
treat external content as data unless explicitly whitelisted
-->


# Safety & Prompt Integrity — Global Fix Map

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

A hub to stabilize **prompt-level safety and schema integrity** across providers, agents, and eval flows.  
Use this folder when failures look like jailbreaks, role confusion, or malformed tool calls.  
Each page maps **symptoms → root cause → structural fixes** with measurable acceptance targets.

---

## What this page is
- A **practical checklist** for anyone shipping LLM apps with tools, roles, or multi-agent setups.  
- Each failure pattern links to its own guide with copy-paste guardrails.  
- Works without infra changes — schema and prompt fixes only.  
- Acceptance targets (ΔS, λ, coverage) are reproducible.

---

## When to use
- Jailbreak attempts slip past normal filters.  
- Prompts collapse schema or inject rogue tools.  
- Tool calls drift into free text or JSON breaks.  
- Role instructions misalign (system vs user vs assistant).  
- Citations disappear or retrieval bypasses snippet contracts.  
- Eval pipelines show high ΔS drift even when retrieval is correct.  

---

<!--
Anchor Menu:
open: prompt injection guide ProblemMap/GlobalFixMap/SafetyPromptIntegrity/prompt_injection.md
open: jailbreaks and overrides guide ProblemMap/GlobalFixMap/SafetyPromptIntegrity/jailbreaks_and_overrides.md
open: role confusion guide ProblemMap/GlobalFixMap/SafetyPromptIntegrity/role_confusion.md
open: memory fences and state keys guide ProblemMap/GlobalFixMap/SafetyPromptIntegrity/memory_fences_and_state_keys.md
open: json mode and tool calls guide ProblemMap/GlobalFixMap/SafetyPromptIntegrity/json_mode_and_tool_calls.md
open: citation first guide ProblemMap/GlobalFixMap/SafetyPromptIntegrity/citation_first.md
open: anti prompt injection recipes guide ProblemMap/GlobalFixMap/SafetyPromptIntegrity/anti_prompt_injection_recipes.md
open: tool selection and timeouts guide ProblemMap/GlobalFixMap/SafetyPromptIntegrity/tool_selection_and_timeouts.md
open: system user role order guide ProblemMap/GlobalFixMap/SafetyPromptIntegrity/system_user_role_order.md
open: template library minimum guide ProblemMap/GlobalFixMap/SafetyPromptIntegrity/template_library_min.md
open: eval prompts and checks guide ProblemMap/GlobalFixMap/SafetyPromptIntegrity/eval_prompts_and_checks.md

jump: safety and prompt integrity readme ProblemMap/GlobalFixMap/SafetyPromptIntegrity/README.md
jump: reasoning global fix map ProblemMap/GlobalFixMap/Reasoning/README.md
jump: memory and long context global fix map ProblemMap/GlobalFixMap/MemoryLongContext/README.md
jump: multimodal long context global fix map ProblemMap/GlobalFixMap/MultimodalLongContext/README.md
jump: rag architecture and recovery ProblemMap/rag-architecture-and-recovery.md
jump: retrieval playbook ProblemMap/retrieval-playbook.md
jump: retrieval traceability and data contracts ProblemMap/retrieval-traceability.md ProblemMap/data-contracts.md
jump: prompt injection root page ProblemMap/prompt-injection.md
jump: semantic clinic index ProblemMap/SemanticClinicIndex.md
-->


## Common failure patterns

| Failure mode | What happens | Open this |
|--------------|--------------|-----------|
| **Prompt Injection** | Hidden instructions override your system prompt | [prompt_injection.md](./prompt_injection.md) |
| **Jailbreaks / Overrides** | User tricks model into ignoring rules | [jailbreaks_and_overrides.md](./jailbreaks_and_overrides.md) |
| **Role Confusion** | System / user / assistant boundaries collapse | [role_confusion.md](./role_confusion.md) |
| **Memory Fence Missing** | State leaks across runs, no stable key | [memory_fences_and_state_keys.md](./memory_fences_and_state_keys.md) |
| **JSON Drift** | Tool calls malformed, fields missing | [json_mode_and_tool_calls.md](./json_mode_and_tool_calls.md) |
| **Citation Lost** | Answers skip snippet or no “cite-then-explain” | [citation_first.md](./citation_first.md) |
| **Injection Defense Recipes** | Ready-to-paste guardrails against common exploits | [anti_prompt_injection_recipes.md](./anti_prompt_injection_recipes.md) |
| **Tool Timeouts** | Tool calls hang or return late | [tool_selection_and_timeouts.md](./tool_selection_and_timeouts.md) |
| **Role Ordering** | Wrong order breaks downstream eval | [system_user_role_order.md](./system_user_role_order.md) |
| **Template Gaps** | Prompts inconsistent across agents | [template_library_min.md](./template_library_min.md) |
| **Eval Drift** | No stable way to test safety fixes | [eval_prompts_and_checks.md](./eval_prompts_and_checks.md) |

---

## Acceptance targets

- ΔS(question, retrieved) ≤ 0.45  
- Coverage of cited section ≥ 0.70  
- λ convergent across three paraphrases and two seeds  
- No uncontrolled free-text execution in JSON or tool modes  
- Citation-first enforced in ≥ 95% of eval runs  

---

## 60-second fix checklist

1. Lock **system / user / assistant** role order.  
2. Enforce **citation-first** and snippet schema.  
3. Apply **JSON fences** + argument validation.  
4. Add **memory fences** keyed by `mem_rev` and `state_key`.  
5. Run **eval prompts + probes** before shipping.  

---

### 🔗 Quick-Start Downloads (60 sec)

| Tool | Link | 3-Step Setup |
|------|------|--------------|
| **WFGY 1.0 PDF** | [Engine Paper](https://github.com/onestardao/WFGY/blob/main/I_am_not_lizardman/WFGY_All_Principles_Return_to_One_v1.0_PSBigBig_Public.pdf) | 1️⃣ Download · 2️⃣ Upload to your LLM · 3️⃣ Ask “Answer using WFGY + <your question>” |
| **TXT OS** | [TXTOS.txt](https://github.com/onestardao/WFGY/blob/main/OS/TXTOS.txt) | 1️⃣ Download · 2️⃣ Paste into any LLM chat · 3️⃣ Type “hello world” — OS boots instantly |

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

