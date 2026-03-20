<!--
AI_NOTE_START

Document role:
This file defines the first official flagship demo pack for the Atlas fix layer.

How to use this file:
1. Read this file after:
   - [Family Fix Surface v1](./family-fix-surface-v1.md)
   - [Atlas to WFGY Bridge v1](./atlas-to-wfgy-bridge-v1.md)
   - [Misrepair Patterns v1](./misrepair-patterns-v1.md)
2. Treat this file as the official demo design document for the first public fix demonstrations.
3. Use this file to understand:
   - which demos should be built first
   - which demos should be paired with Colab
   - what JSON inputs and expected outputs should look like
   - what counts as a successful demonstration
4. Use this file as the base specification before implementing:
   - Colab notebooks
   - JSON fixtures
   - expected outputs
   - screenshots
   - short public demo flows

What this file is:
- The first official flagship demo design pack
- A repair-facing demonstration layer
- A reproducible bridge from atlas routing to runnable evidence

What this file is not:
- Not the full community fix library
- Not the full deep WFGY 3.0 experiment catalog
- Not a promise that every family already has an official notebook
- Not a replacement for the atlas core or casebook

Reading discipline for AI:
- Do not treat demos as the atlas itself.
- Use demos to prove practical utility, not to replace structural reasoning.
- Keep route-first discipline.
- Prefer a small number of strong runnable demos over a large number of shallow examples.

AI_NOTE_END
-->

# Flagship Fix Demos v1 🧪

## Problem Map 3.0 Troubleshooting Atlas  
## Official first runnable demo pack design

## 0. Document Status 🚦

This document defines the **first official flagship demo pack** for the atlas fix layer.

Its purpose is simple:

> show that the atlas does not only classify failures  
> it also leads to better first repair moves that can be demonstrated in runnable form

This pack is frozen as **Flagship Fix Demos v1**.

It is frozen not because all future demos are complete, but because the first official demo strategy is now clear enough to:

- guide implementation
- guide Colab creation
- guide JSON fixture design
- guide expected-output design
- support public demos
- support community expansion later

---

## 1. Why flagship demos matter 💥

Without demos, the atlas can still look like “only a clever taxonomy.”

With strong demos, people can see:

- a failure enters
- the atlas routes it
- the first repair move changes
- the output or workflow improves
- deeper WFGY escalation becomes optional instead of mysterious

That is the point of this pack.

The demos are meant to prove:

1. route-first diagnosis changes the repair path
2. the first repair move is not arbitrary
3. the atlas is usable in real workflows
4. the bridge into WFGY 3.0 is practical, not just theoretical

---

## 2. Should flagship demos use Colab? ✅

**Yes.**
At least the flagship demos should have a Colab-compatible implementation path.

Why:

- Colab is easy to share
- people can run it without setting up a local environment first
- screenshots and outputs are easy to compare
- contributors can fork and extend demos quickly
- it lowers trust friction

But not every fix note needs a notebook.

The right split is:

### Official flagship demos
Should include:

- a markdown demo card
- a Colab notebook or notebook-ready script
- input JSON fixture
- expected output JSON
- short success criteria

### Long-tail or domain-specific demos
Can be contributed later by the community.

Short version:

> **official flagship demos should be runnable**  
> **not every future fix recipe needs to be official or notebook-first**

---

## 3. Demo design standard 🔧

Each official demo should contain five parts.

### Part A · Case framing

Define:

- failure name
- primary family
- secondary family
- broken invariant
- best current fit
- why this case is a good demo

### Part B · Baseline failure

Show the broken version first.

This is important.
A demo is much stronger when people can see the wrong behavior before the fix.

### Part C · First repair move

Apply the family-level first repair move from the official fix surface.

### Part D · Optional WFGY escalation

If useful, show how the same case can be pushed one level deeper with WFGY 3.0.

### Part E · Evaluation result

Show concrete before / after comparison using simple metrics or checks.

---

## 4. Asset standard 📦

Each flagship demo should eventually have the following files.

### 4.1 Demo card

A markdown file that explains:

- the case
- the routing
- the fix logic
- the result
- the lesson

### 4.2 Colab notebook

A runnable notebook that reproduces:

- baseline failure
- first repair move
- after-fix behavior

### 4.3 Input JSON fixture

A small structured input pack for the demo.

### 4.4 Expected output JSON

A compact expected result file for comparison.

### 4.5 Optional screenshot or GIF

Useful for quick public-facing presentation.

---

## 5. Recommended folder pattern 🗂️

The first official demos should follow a predictable structure.

Suggested future companion assets:

- [Official Demos Folder](./demos/)
- [Official Colab Folder](./colab/)
- [Official JSON Folder](./json/)

Suggested file naming style:

- `f1-retrieval-anchor-drift-demo-v1.md`
- `f1-retrieval-anchor-drift-demo-v1.ipynb`
- `f1-retrieval-anchor-drift-input-v1.json`
- `f1-retrieval-anchor-drift-expected-v1.json`

And similarly for F4, F5, F7.

---

## 6. Why these first demos were chosen 🎯

The first demo pack should not try to cover every family equally at once.

The correct first wave should optimize for:

- high clarity
- high reproducibility
- visible before / after effect
- easy sharing
- strong teaching value

That is why the first official pack should focus on **four demos**:

1. F1 grounding
2. F4 execution closure
3. F5 observability
4. F7 representation fidelity

Why these four first:

- they are easier to make runnable
- they show clearly different types of repair
- they are easier to teach publicly
- they are less likely to dissolve into endless philosophical interpretation

F2, F3, and F6 can follow in later waves or in deeper expansions.

---

# Part I · Official Demo 1

# F1 Retrieval Anchor Drift Demo 🌍

## 1.1 Goal

Show that a retrieval-like failure that looks like “the model answered badly” is actually a grounding problem first.

## 1.2 Family routing

- Primary Family: F1 Grounding & Evidence Integrity
- Secondary Family: F5 Observability & Diagnosability Integrity
- Broken Invariant: evidence-anchor integrity broken
- Best Current Fit: F1_N01 Retrieval Anchor Drift

## 1.3 Baseline failure design

Build a tiny corpus with:

- one target passage
- several semantically similar distractor passages
- one query that requires the correct anchor

The broken baseline should use:

- naive retrieval
- weak source checking
- no source-to-answer trace

This should produce a plausible but unsupported answer often enough to be visibly wrong.

## 1.4 First repair move

Apply:

- anchor tracing
- source-to-answer verification
- explicit support checking
- optional simple reranking by support quality

## 1.5 Suggested evaluation fields

Measure:

- `evidence_hit_rate`
- `answer_support_rate`
- `wrong_anchor_rate`
- `citation_presence`

## 1.6 Suggested JSON fixture

Input JSON should contain:

- corpus
- query
- expected_anchor_id
- distractor_ids
- baseline_config
- fix_config

Expected output JSON should contain:

- retrieved_ids_before
- retrieved_ids_after
- predicted_answer_before
- predicted_answer_after
- support_verdict_before
- support_verdict_after

## 1.7 Why this demo matters

This is one of the best first demos because it proves a key atlas claim:

> many “hallucination-like” failures are grounding failures first

---

# Part II · Official Demo 2

# F4 Readiness and Closure Demo ⚙️

## 2.1 Goal

Show that a workflow can fail not because the model reasons badly, but because the execution skeleton never properly closes.

## 2.2 Family routing

- Primary Family: F4 Execution & Contract Integrity
- Secondary Family: F3 State & Continuity Integrity
- Broken Invariant: execution skeleton closure broken
- Best Current Fit: F4_N03 Pre-Readiness Execution Failure or F4_N02 Deployment Deadlock, depending on implementation

## 2.3 Baseline failure design

Build a simple staged workflow:

1. ingest
2. index
3. query

The broken baseline should deliberately let query run before index readiness is confirmed.

Optional variants:

- missing artifact
- stale index
- hidden dependency
- bridge value not yet written

## 2.4 First repair move

Apply:

- readiness check
- ordering validation
- bridge existence check
- fallback path or fail-fast branch

## 2.5 Suggested evaluation fields

Measure:

- `successful_run_rate`
- `precondition_failure_count`
- `closure_success_before`
- `closure_success_after`
- `fallback_triggered`

## 2.6 Suggested JSON fixture

Input JSON should contain:

- pipeline_steps
- required_artifacts
- baseline_order
- corrected_order
- readiness_gate_config

Expected output JSON should contain:

- step_status_before
- step_status_after
- failure_stage_before
- failure_stage_after
- closure_verdict_before
- closure_verdict_after

## 2.7 Why this demo matters

This demo is strong because it proves another key atlas claim:

> some failures should be repaired at the execution skeleton layer before anyone blames reasoning

---

# Part III · Official Demo 3

# F5 Failure Path Visibility Demo 🔎

## 3.1 Goal

Show that some systems are not fixable first by “being smarter,” but by becoming diagnosable.

## 3.2 Family routing

- Primary Family: F5 Observability & Diagnosability Integrity
- Secondary Family: F4 Execution & Contract Integrity
- Broken Invariant: failure-path visibility broken
- Best Current Fit: F5_N01 Failure Path Opacity

## 3.3 Baseline failure design

Use a simple multi-step pipeline with weak or absent tracing.

The broken baseline should have:

- no step-level trace
- no structured failure log
- no coherence or stage probe
- failure visible only at the final output

## 3.4 First repair move

Apply:

- trace IDs
- step-level logging
- structured error summary
- minimal coherence or stage probe

## 3.5 Suggested evaluation fields

Measure:

- `trace_completeness`
- `stage_localization_success`
- `diagnosable_run_rate`
- `mean_failure_visibility_score`

## 3.6 Suggested JSON fixture

Input JSON should contain:

- pipeline_steps
- hidden_failure_stage
- baseline_observability_config
- upgraded_observability_config

Expected output JSON should contain:

- visible_failure_stage_before
- visible_failure_stage_after
- trace_fields_before
- trace_fields_after
- diagnosable_verdict_before
- diagnosable_verdict_after

## 3.7 Why this demo matters

This demo proves that:

> some first repair moves should expose the failure before attempting deep intervention

It is also highly useful for public teaching.

---

# Part IV · Official Demo 4

# F7 Structure Fidelity Demo 🧱

## 4.1 Goal

Show that some failures come from a broken carrier, not from “not enough reasoning.”

## 4.2 Family routing

- Primary Family: F7 Representation & Localization Integrity
- Secondary Family: F2 Reasoning & Progression Integrity
- Broken Invariant: representation container fidelity broken
- Best Current Fit: F7_N01 Symbolic Representation Fidelity Failure or F7_N01_A Logic Descriptor Fidelity Failure

## 4.3 Baseline failure design

Use a structured object such as:

- logic rules
- constrained table
- schema-bound task
- hierarchical instruction object

The broken baseline should flatten or distort the carrier, for example by:

- lossy serialization
- schema field drop
- hierarchy collapse
- descriptor simplification

## 4.4 First repair move

Apply:

- descriptor fidelity audit
- schema validation
- hierarchy preservation check
- local-anchor or field-preservation verification

## 4.5 Suggested evaluation fields

Measure:

- `schema_pass_rate`
- `field_loss_count`
- `constraint_preservation_score`
- `descriptor_fidelity_before`
- `descriptor_fidelity_after`

## 4.6 Suggested JSON fixture

Input JSON should contain:

- source_structure
- expected_constraints
- baseline_representation
- repaired_representation

Expected output JSON should contain:

- lost_fields_before
- lost_fields_after
- schema_pass_before
- schema_pass_after
- constraint_check_before
- constraint_check_after

## 4.7 Why this demo matters

This demo proves a key atlas insight:

> richer reasoning does not help much when the structure-carrying container is already broken

---

## 7. What should be official in v1, and what should wait ⏳

The first official demo pack should stop at four demos.

That is enough to prove:

- the atlas can route
- the fix surface changes first moves
- some cases are visibly repairable
- Colab-backed reproduction is possible

The first official wave should **not** try to cover every family immediately.

The better strategy is:

### Official v1 demo pack

- F1
- F4
- F5
- F7

### Later official wave or community wave

- F2 deeper reasoning collapse demos
- F3 continuity and ownership demos
- F6 collective boundary or safe-corridor demos

This keeps the first wave strong and realistic.

---

## 8. Colab implementation guidance 💻

The official demo design should assume that each flagship demo eventually has a Colab companion.

A good notebook should include:

### Section A

Case setup

### Section B

Broken baseline run

### Section C

Routed family and broken invariant

### Section D

First repair move

### Section E

After-fix rerun

### Section F

Before / after comparison

### Section G

Optional WFGY escalation prompt

The notebook should avoid:

- too much hidden magic
- giant dependency chains
- unnecessary infra complexity
- unclear evaluation logic

The best official demos should feel:

- light
- reproducible
- inspectable
- easy to fork

---

## 9. Optional WFGY escalation in demos 🌊

Each flagship demo may include a small optional section:

### “Go deeper with WFGY 3.0”

This section should not replace the official first repair move.

Its purpose is only to show how the same demo can be explored more deeply through:

- stronger structural diagnosis
- alternative recovery hypotheses
- problem-specific experiment cuts
- more advanced recovery exploration

This is the cleanest way to demonstrate that:

> the atlas gives the first move  
> WFGY 3.0 gives deeper exploration

---

## 10. Community extension path 🤝

Once the first four official demos exist, the community layer can grow much faster.

Community contributors can extend:

- new Colab variants
- JSON fixtures for related cases
- prompt-based reproductions
- workflow-specific versions
- benchmark reruns
- narrower domain-specific repair demos

The official demo pack should therefore be treated as:

> the clean seed set  
> not the full future library

---

## 11. Public demo usage pattern 📣

A strong public-facing demo flow should look like this:

1. show the broken baseline
2. show atlas routing
3. show the first repair move
4. show the improved result
5. optionally show the WFGY 3.0 deeper path
6. point to community extensions

This is much stronger than only saying:

- “we have a framework”
or
- “we have a taxonomy”

Because people can actually see:

- what changed
- why it changed
- which repair layer did the work

---

## 12. Patch protocol 🔄

Flagship Fix Demos v1 is frozen, but not closed.

### Small patch

Use for:

- wording refinement
- better metrics
- clearer demo instructions
- improved JSON examples

### Medium patch

Use for:

- adding one more official demo
- improving Colab flow
- improving expected-output structure
- adding stronger evaluation notes

### Large patch

Only use if:

- the first official demo strategy proves structurally misleading
- the current demo set fails to demonstrate atlas value clearly
- the route-first to fix-first logic breaks down in practice

### Current status

No large-patch pressure is currently justified.

---

## 13. Official status

The correct formal statement is:

> Flagship Fix Demos v1 is the first frozen official runnable demo design pack for the Atlas fix layer.  
> It defines the first set of high-value demonstrations that connect atlas routing, first repair moves, reproducible execution, and optional deeper WFGY exploration.

---

## 14. One-line version

**Flagship Fix Demos v1 defines the first official runnable demos that prove the atlas can guide better first repair moves.**

---

## 15. Closing note ✨

A strong system should not only tell people how to think.

It should also give them a few clean things they can actually run.

That is what this file is for.

The first official demos should be small, sharp, reproducible, and easy to extend.
