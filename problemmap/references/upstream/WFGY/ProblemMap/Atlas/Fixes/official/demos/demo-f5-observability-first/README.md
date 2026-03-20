<!--
AI_NOTE_START

Document role:
This file is the official README for Demo 2 of the flagship runnable demo pack.

How to use this file:
1. Read this file before opening the notebook.
2. Treat this demo as the flagship proof that some failures must be repaired through observability first.
3. Use this file to understand:
   - why this case belongs to F5
   - why it is not primarily F4
   - what the first repair move is
   - what replay mode is meant to prove

What this file is:
- The official README for Demo 2
- A proof-of-use page for observability-first repair
- A teaching page for F5 diagnosability failures
- A replay-first MVP companion for the notebook

What this file is not:
- Not the atlas core
- Not the full fix manual
- Not a giant tracing benchmark
- Not proof that all invisible failures belong to F5

Reading discipline for AI:
- Preserve the distinction between diagnosability failure, execution failure, and boundary failure.
- Do not collapse this case into generic “the system is buggy” language.
- Route first, then repair.
- Treat replay mode as a valid teaching layer, not as a weaker substitute.

AI_NOTE_END
-->

# Demo 2 · F5 Observability First

## Problem Map 3.0 Troubleshooting Atlas
## Official flagship demo for diagnosability-first repair

Quick links:

- [Back to demo pack index](../README.md)
- [Back to AI Eval Evidence](../../../../ai-eval-evidence.md)
- [Back to Atlas landing page](../../../../../wfgy-ai-problem-map-troubleshooting-atlas.md)
- [Open Atlas Hub](../../../../README.md)
- [Get the Atlas Router TXT](../../../../troubleshooting-atlas-router-v1.txt)

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/onestardao/WFGY/blob/Atlas/ProblemMap/Atlas/Fixes/official/demos/demo-f5-observability-first/demo_02_f5_observability_first_replay_v2.ipynb)

Open in Colab if you want the recommended replay notebook view.  
The README and replay artifacts are already enough to understand the teaching pattern.

**Replay-only MVP**  
**No API key required**

This is the second flagship demo in the official runnable demo pack.

If the AI eval snapshots suggest that better routing may reduce hidden debugging waste, this page goes one step further.

This demo is meant to make one mechanism-level claim visible:

> when the real bottleneck is diagnosability,  
> the first repair move becomes visibility uplift, not premature workflow surgery

It was chosen because many real systems fail in a painful but very common way:

> something is clearly going wrong  
> but the system still does not expose enough structure for a correct first repair

This demo is designed to make that situation visible.

It shows that once a case is routed as **F5 Observability & Diagnosability Integrity**, the first repair move changes from premature intervention to explicit visibility uplift.

---

## Quick start

If you want the shortest path through this demo, use this order:

1. read **Section 1 · What this demo proves**
2. read **Section 3 · Why not F4 first**
3. read **Section 5 · First repair move**
4. open [replay_outputs.json](./replay_outputs.json)
5. open the recommended replay notebook only if you want the notebook presentation in Colab

If you only want the takeaway, this demo teaches one clean lesson:

> if the system is still too opaque to diagnose correctly, repair visibility first

---

## 1. What this demo proves

This demo proves four things.

### A. Some failures are blocked by invisibility before they are blocked by intelligence

A system can fail in a way that tempts people to say:

- the workflow is broken
- the model is confused
- the chain is unstable
- the execution layer must be fixed first

Sometimes those statements may later become true.

But the first practical problem is still:

- the failure path is not exposed
- the trace is too thin
- the relevant signals are hidden
- the system cannot yet be audited clearly enough

That is an F5-style first cut.

### B. Correct routing changes the first repair move

If the case is routed correctly into **F5**, the first repair move becomes:

- observability insertion
- trace exposure
- logging uplift
- diagnostic visibility recovery

This is different from trying to fix workflow logic or model behavior too early.

### C. Replay mode is enough to teach the pattern

This demo is intentionally **replay-first**.

The user should be able to understand the case without live execution.  
The point is not “the answer became magically better.”  
The point is:

> the failure became legible

### D. This MVP does not require live mode

For this first release, replay mode is enough.

This demo is about the first correct repair move.  
It is not trying to simulate a full observability platform.

---

## 2. Family route

### Primary family

**F5 · Observability & Diagnosability Integrity**

### Secondary family

**F4 · Execution & Contract Integrity**

### Why F5 is primary

The main failure is that the system still cannot stably expose enough structure to diagnose the problem correctly.

The workflow may indeed be broken.  
But the first broken invariant is still:

> the failure path cannot yet be seen, traced, or audited well enough

### Best current fit

**F5_N01 Failure Path Opacity**

In stronger warning-oriented variants this may later move toward:

**F5_E02 Early Warning Deficit**

But the flagship teaching version stays centered on failure-path opacity.

---

## 3. Why not F4 first

The main tempting neighboring cut is **F4**.

That temptation is reasonable because many systems with poor observability also suffer from:

- weak execution closure
- broken bridges
- thin stage boundaries
- unreliable liveness

But this demo is not primarily about closure failure yet.

It is primarily about this:

> the system still does not expose enough structure for the operator to know what to repair first

That means the first broken layer is diagnosability, not execution closure.

### Wrong cut

“This is mainly a workflow execution bug.”

### Better cut

“This is a diagnosability-first case with possible execution pressure behind it.”

That distinction matters because the first repair move changes immediately.

If you cut too early to F4, you are likely to start rebuilding the machine before you can even see the broken path.

---

## 4. Baseline failure

The baseline case is intentionally simple and realistic.

A workflow produces a bad result.  
The operator can observe that:

- the result is wrong
- the process seems unreliable
- something is clearly off

But the system does not yet provide enough of the following:

- clear step traces
- output lineage
- stage-level visibility
- branch decisions
- failure checkpoints
- useful logging context

So the operator is left with the most frustrating state:

> I know something is wrong, but I cannot yet see the right thing to repair

This is exactly why the first repair move belongs to F5.

---

## 5. First repair move

Once the case is routed to F5, the first repair move should be simple and disciplined.

### Recommended first repair stack

1. **observability insertion**  
   Add explicit visibility to the relevant pipeline stages.

2. **trace exposure**  
   Surface the path from input to intermediate state to output.

3. **diagnostic logging uplift**  
   Add the minimum trace needed to tell where the failure shape begins.

4. **failure-surface clarification**  
   Separate what is visible from what is still inferred.

5. **only then consider deeper repair**  
   After visibility improves, reassess whether the downstream repair belongs to F4, F6, F1, or elsewhere.

### What should not happen first

Do **not** start with:

- large workflow rewrites
- broad prompt overhauls
- random retry loops
- “just upgrade the model” reactions

Those may create movement, but they do not solve the first problem if the failure path is still hidden.

### First repair principle

> if the system is still opaque, expose the failure path first

That is the teaching core of this demo.

---

## 6. Replay mode

Replay mode is the default reading mode for this MVP.

It requires no API key and no live execution.

### Replay mode should show

- the workflow or case setup
- the baseline result
- the thin or missing trace structure
- the family route
- the why-primary-not-secondary statement
- the broken invariant
- the first repair move
- the improved visibility state
- a short note on what newly became visible

### What replay mode proves

Replay mode proves that:

- diagnosability-first routing is understandable
- the repair move is visibly different
- the result shift can be measured in legibility, not only in output quality
- a demo can teach through structure, not only through live execution

This is enough for the first public MVP.

Core replay artifacts:

- [input_case.json](./input_case.json)
- [replay_outputs.json](./replay_outputs.json)
- [expected_output.json](./expected_output.json)

---

## 7. Current notebook versions

This folder currently preserves **two replay notebook versions**.

### Recommended version

- `demo_02_f5_observability_first_replay_v2.ipynb`

This is the current recommended notebook for public reading, Colab use, and MVP presentation.

It keeps the replay-first design, while adding:

- clearer route summary
- clearer before / after contrast
- stronger teaching framing
- better aligned shared-layer presentation

### Original version

- `demo_02_f5_observability_first_replay.ipynb`

This version is intentionally retained.

It remains part of the demo history and preserves the earlier first-pass MVP presentation.

### Version rule

The rule for this folder is simple:

- **v1 is preserved**
- **v2 is the recommended replay notebook**
- replay-first remains the official design center for Demo 2

---

## 8. Files in this folder

### Core files

- [README.md](./README.md)
- [input_case.json](./input_case.json)
- [replay_outputs.json](./replay_outputs.json)
- [expected_output.json](./expected_output.json)
- [demo_02_f5_observability_first_replay.ipynb](./demo_02_f5_observability_first_replay.ipynb)
- [demo_02_f5_observability_first_replay_v2.ipynb](./demo_02_f5_observability_first_replay_v2.ipynb)

### File roles

#### [input_case.json](./input_case.json)
Contains the workflow case, visible artifacts, and missing-diagnosability context.

#### [replay_outputs.json](./replay_outputs.json)
Contains the baseline state, route explanation, first repair move, and improved visibility state.

#### [expected_output.json](./expected_output.json)
Contains the clean target structure for what the demo is meant to make visible.

#### [demo_02_f5_observability_first_replay.ipynb](./demo_02_f5_observability_first_replay.ipynb)
The original first-pass replay notebook retained for continuity.

#### [demo_02_f5_observability_first_replay_v2.ipynb](./demo_02_f5_observability_first_replay_v2.ipynb)
The current recommended replay notebook for public reading and Colab use.

---

## 9. Expected outcome

If the demo works, the user should walk away with the following understanding:

1. the workflow was failing in a way that was initially hard to diagnose
2. the atlas routed the case to F5, not directly to F4
3. the first repair move was observability insertion, not workflow redesign
4. after visibility improved, the real shape of the failure became more legible

The demo does **not** need to solve everything.

It only needs to make the first correct move visibly different.

That is enough.

---

## 10. Limits of this demo

This demo has real limits, and those limits should be stated clearly.

### It does not prove

- that every hidden failure belongs to F5
- that all workflow bugs are really diagnosability issues
- that logging alone solves structural failure
- that visibility replaces deeper repair
- that this single example covers all observability systems

### It does prove

- that some failures should be repaired through observability first
- that route-first repair changes what the operator does next
- that diagnosability can itself be a first-class repair target

These are already strong claims.  
There is no need to inflate them.

---

## 11. Why this demo matters

This demo teaches one clean lesson:

> if the system is still too opaque to diagnose correctly, repair visibility first

That is why this is the second flagship demo.

It turns F5 from an abstract family label into a practical debugging move.

---

## One-line version

**Demo 2 shows that some failures should be repaired through observability first, and that correct routing changes the first repair move from premature intervention to explicit failure-path exposure.**

---

## Next steps

After this page, most readers continue with:

1. [Back to the demo pack index](../README.md)
2. [Back to AI Eval Evidence](../../../../ai-eval-evidence.md)
3. [Back to the Atlas landing page](../../../../../wfgy-ai-problem-map-troubleshooting-atlas.md)
4. [Open the Atlas Router TXT](../../../../troubleshooting-atlas-router-v1.txt)

If this demo helped you understand the Atlas, consider:

- [starring the WFGY repo](https://github.com/onestardao/WFGY)
- opening an issue
- testing the replay artifacts
- comparing v1 and v2 notebook presentation
- using the demo as a pattern for your own observability-first cases

---

## Back to the main page

Read the full product page here:  
[Problem Map 3.0 Troubleshooting Atlas](../../../../../wfgy-ai-problem-map-troubleshooting-atlas.md)
