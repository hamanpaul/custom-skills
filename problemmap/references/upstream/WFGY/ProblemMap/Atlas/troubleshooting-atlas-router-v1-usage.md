<!--
AI_NOTE_START

Document role:
This file is the usage guide for Troubleshooting Atlas Router v1.

How to use this file:
1. Read this file after obtaining `troubleshooting-atlas-router-v1.txt`.
2. Use this page to understand when to use the Router, how to provide a case, and how to interpret the output.
3. Treat this document as the practical usage guide for the Router product.
4. Read together with:
   - [Problem Map 3.0 Troubleshooting Atlas](../wfgy-ai-problem-map-troubleshooting-atlas.md)
   - [Atlas Final Freeze v1](./atlas-final-freeze-v1.md)
   - [Troubleshooting Atlas Router v1 Freeze Note](./troubleshooting-atlas-router-v1-freeze-note.md)

What this file is:
- The main usage guide for the Router TXT pack
- A practical onboarding page for humans and AI-facing workflows
- A bridge between the Router pack and real troubleshooting use

What this file is not:
- Not the Atlas core
- Not the full casebook
- Not the full adapter specification
- Not a promise of full autonomous repair
- Not a benchmark sheet

Reading discipline for AI:
- Preserve the distinction between route-first classification, first repair direction, and deeper exploration.
- Treat the Router as a compact operational pack, not as the whole Atlas.
- Do not overclaim that the Router guarantees full diagnosis or full repair closure.
- Keep the order clear: route first, then first repair direction.

AI_NOTE_END
-->

# Troubleshooting Atlas Router v1 Usage Guide

## Problem Map 3.0 Troubleshooting Atlas
## How to use the first route-first TXT troubleshooting pack

Quick links:

- [Back to Atlas landing page](../wfgy-ai-problem-map-troubleshooting-atlas.md)
- [Get the Router TXT Pack](./troubleshooting-atlas-router-v1.txt)
- [Router Freeze Note](./troubleshooting-atlas-router-v1-freeze-note.md)
- [Atlas Hub](./README.md)
- [Official Flagship Demos](./Fixes/official/demos/README.md)

---

This document explains how to use `Troubleshooting Atlas Router v1`.

Its purpose is simple:

> show what the Router is for,  
> when to use it,  
> what kind of input to provide,  
> what kind of output to expect,  
> and how to read that output correctly

This is a usage guide.  
It is not the full Atlas.  
It is not the full teaching layer.  
It is not the full repair engine.

It is the practical onboarding page for using the Router well.

---

## Quick start

If you want the shortest practical path, do this:

1. download the [Router TXT Pack](./troubleshooting-atlas-router-v1.txt)
2. paste the TXT into ChatGPT, Claude, Gemini, Copilot, Cursor, or your preferred model
3. paste one real case below it
4. use the minimal prompt below
5. read the output in this order:
   - `primary_family`
   - `why_primary_not_secondary`
   - `broken_invariant`
   - `first_fix_direction`
   - `misrepair_risk`
   - `confidence`
   - `evidence_sufficiency`

If that already works for you, you do not need to read the whole page first.

---

## Minimal prompt pattern

Here is the simplest way to use the Router.

### Minimal usage prompt

```text
Use the attached Troubleshooting Atlas Router v1.

Route the following case using the Router output contract.

Case:
[paste your bug, issue, trace, workflow failure, or structured-output failure here]
````

That is enough for a first pass.

---

## Tiny example

Here is a small example of the kind of case that already works well.

```text
Use the attached Troubleshooting Atlas Router v1.

Route the following case using the Router output contract.

Case:
The agent keeps producing valid-looking JSON, but the schema parser fails because required fields appear in inconsistent places across steps.

Expected behavior:
Stable schema-compatible output.

Actual behavior:
Parse failures and downstream workflow breaks.
```

This is not the only valid format.
It is just a simple example of the level of signal that helps the Router cut cleanly.

---

## 1. What the Router is for

`Troubleshooting Atlas Router v1` is a compact TXT pack designed to help AI systems read troubleshooting cases through the Atlas family map.

Its job is not to do everything.

Its job is to do the most important early step well:

* classify the most likely failure family
* explain why that family is primary
* identify the most likely broken invariant
* suggest the first repair direction
* warn about likely misrepair
* stay honest when evidence is weak

Short version:

> the Router helps AI read failure cases more like a troubleshooting system and less like a guess generator

---

## 2. When to use it

Use the Router when you have a real troubleshooting case and want a faster route-first judgment.

Good use cases include:

* AI bug reports
* issue threads
* workflow failures
* agent step failures
* structured-output failures
* prompt and output mismatches
* strange model behavior with logs or traces
* system summaries where something is clearly wrong but the failure family is not obvious yet

This product is especially useful when the question is not only:

* what happened

but more like:

* what kind of failure is this
* why is it this kind
* what should be tried first
* what should not be tried first

---

## 3. When not to use it

Do not use the Router as if it were already:

* a full autonomous repair engine
* a full benchmark framework
* a full root-cause analysis suite
* a replacement for logs, traces, or actual debugging work
* a substitute for the full Atlas when deep study is needed

If you need:

* richer family definitions
* full teaching examples
* deeper bridge logic
* more careful case interpretation
* stronger repair design

then move from the Router back into the larger Atlas system.

Short version:

> use the Router for compact route-first help
> use the full Atlas when you need deeper structure

---

## 4. What you need before using it

At minimum, you need two things:

### 1. The Router TXT pack

You should have:

`troubleshooting-atlas-router-v1.txt`

### 2. A real case

The case can be small or medium-sized, but it should contain enough signal to support routing.

Useful forms of input include:

* a bug description
* an issue body
* an error summary
* a workflow trace excerpt
* expected vs actual behavior
* a prompt and output pair
* a JSON failure sample
* a short log snippet with context

You do not need a perfect formal schema.
But the better the case description, the better the route.

---

## 5. The basic usage flow

The Router is designed for a very simple flow.

### Step 1

Load or paste the Router TXT into the model context.

### Step 2

Paste your case below it.

### Step 3

Ask the model to route the case using the Router output contract.

### Step 4

Read the result in this order:

1. primary_family
2. secondary_family
3. why_primary_not_secondary
4. broken_invariant
5. best_current_fit
6. first_fix_direction
7. misrepair_risk
8. confidence
9. evidence_sufficiency

### Step 5

Decide whether the result is strong enough to act on directly, or whether you need:

* more evidence
* deeper Atlas reading
* deeper WFGY bridge exploration
* a real implementation step

That is the healthy use pattern.

---

## 6. Stronger prompt pattern

If you want a cleaner result, use a slightly more guided prompt.

### Stronger usage prompt

```text
Use Troubleshooting Atlas Router v1.

Please do the following in order:
1. identify the most likely primary family
2. identify the strongest neighboring family only if it is real
3. explain why the primary cut is stronger
4. identify the broken invariant
5. identify the best current fit at the highest honest resolution
6. give the first repair direction
7. warn about the most likely misrepair
8. report confidence and evidence sufficiency honestly

Case:
[paste case here]
```

This version tends to reduce sloppy outputs.

---

## 7. What kind of input works best

The Router works best when the case contains enough material to expose the failure shape.

The most useful ingredients are:

* what was supposed to happen
* what actually happened
* where the failure appears
* what evidence or trace exists
* whether this is a content problem, workflow problem, observability problem, boundary problem, or structure-carrier problem
* any concrete artifact such as output, log, schema, or snippet

The Router is still usable on shorter descriptions.
But the best results usually come when the case includes:

* expected behavior
* actual behavior
* one concrete failure artifact

That gives the model something real to cut.

---

## 8. What the output means

The Router’s output is compact, but every field matters.

### `primary_family`

This is the most likely main failure region.

It tells you where the earliest decisive failure probably lives.

### `secondary_family`

This is the strongest neighboring pressure, if there is one.

It is optional.
A good output may say `none`.

### `why_primary_not_secondary`

This is the most important field after `primary_family`.

It explains the cut.

If this field is weak, the route itself is usually weak.

### `broken_invariant`

This tells you what kind of structural failure the model thinks happened.

This is the bridge between routing and repair.

### `best_current_fit`

This gives the highest honest resolution the case supports.

Sometimes this will be node-like.
Sometimes it should stay family-level.

### `first_fix_direction`

This tells you the first move, not the whole solution.

### `misrepair_risk`

This warns you what tempting wrong first move to avoid.

### `confidence`

This tells you how stable the cut is.

### `evidence_sufficiency`

This tells you whether the current case actually contained enough material to support the route strongly.

---

## 9. How to judge whether the output is good

A good Router output usually has these qualities:

* the primary family makes structural sense
* the neighboring family is real, not decorative
* the cut is explained clearly
* the broken invariant is specific enough to guide action
* the first fix direction is modest and plausible
* the misrepair warning feels real
* the confidence level matches the actual evidence

A bad Router output usually has one or more of these problems:

* family chosen by topic words only
* secondary family added for decoration
* vague why-primary explanation
* broken invariant too generic
* first fix direction too ambitious
* confidence too high for the evidence
* no mention of missing evidence when the case is thin

That is how you should read the result.

---

## 10. What to do when evidence is weak

Sometimes the Router will say:

* confidence is low
* evidence_sufficiency is low
* need_more_evidence is yes

That is not a failure.

That is often a sign that the Router is behaving honestly.

When this happens, the right next move is usually one of these:

* provide the actual output artifact
* provide expected vs actual behavior
* provide the relevant log or trace
* provide the schema or container that failed
* provide the step order or workflow context
* provide the evidence source that the answer was supposed to anchor to

Short version:

> weak evidence should usually trigger better case input, not anger at the Router

---

## 11. How to use the Router with different kinds of cases

The Router can be used across several common troubleshooting styles.

### A. RAG or grounding-style case

Useful input:

* user question
* retrieved chunk
* final answer
* what was wrong

Likely value:

* stronger F1 vs F7 vs F5 cuts
* better first move on re-grounding

### B. Workflow or agent case

Useful input:

* task description
* step order
* trace excerpt
* where the workflow failed

Likely value:

* stronger F3 vs F4 vs F5 cuts
* better first move on closure, continuity, or visibility

### C. Structured output case

Useful input:

* expected schema
* actual output
* parse failure
* model prompt if useful

Likely value:

* stronger F7 vs F2 vs F1 cuts
* better first move on container repair

### D. Safety or governance-style case

Useful input:

* observed failure behavior
* why it seems dangerous
* what is visible vs what is inferred
* whether the boundary itself is already drifting

Likely value:

* stronger F5 vs F6 separation
* fewer premature “danger means F6” mistakes

---

## 12. What the Router is especially good at

Router v1 is especially strong at these things:

### 1. Preventing early misclassification

It helps the model not jump to the loudest symptom too fast.

### 2. Forcing family cuts to be explained

It pushes the model to justify the cut.

### 3. Changing the first repair move

This is one of the biggest values in the whole system.

### 4. Keeping uncertainty visible

It helps resist fake certainty.

### 5. Making Atlas logic usable in small form

This is one of the biggest product thresholds the Router crosses.

---

## 13. What the Router is still limited at

Router v1 is useful, but it still has normal first-version limits.

It is still limited at:

* very thin cases with no real evidence
* extremely mixed cross-family cases
* very long workflow chains with missing trace details
* full repair planning
* full autonomous remediation
* deep cross-domain reasoning beyond the compact pack boundary

That is normal.

If you need stronger coverage, move up into:

* the full Atlas
* the Casebook
* the Adapter documents
* the deeper fix bridge
* deeper WFGY exploration

---

## 14. Relationship to the larger Atlas system

The Router should be seen as one layer in the larger system.

### Use the Router when you want:

* compact route-first behavior
* direct AI usage
* quick family cuts
* first-fix guidance

### Use the full Atlas when you want:

* deeper family structure
* teaching cases
* negative examples
* cross-domain bridge logic
* patch history
* system-level provenance and validation

The Router is strongest when used as a front layer, not when forced to become the whole system.

---

## 15. Suggested usage pattern for humans

If a human wants to use this product manually, the best pattern is:

1. paste the Router into the model
2. paste one real case
3. read the output fields in order
4. judge whether the cut feels structurally right
5. apply only the first repair move
6. do not escalate to full repair until the first cut looks sane
7. move into deeper Atlas or WFGY layers only if needed

This keeps the product useful and honest.

---

## 16. Suggested usage pattern for AI workflows

If the Router is used inside a workflow, the safest first-version pattern is:

1. case enters system
2. Router produces route-first output
3. system reads:

   * primary_family
   * broken_invariant
   * first_fix_direction
   * confidence
4. if confidence is high enough, continue into the first repair workflow
5. if confidence is low, request more evidence or escalate to a richer Atlas layer

This keeps the Router acting like a disciplined front-end classifier.

---

## 17. What not to do

To use Router v1 well, avoid these mistakes.

### Do not:

* treat it like a full repair engine
* expect perfect node-level diagnosis on tiny cases
* ignore `confidence` and `evidence_sufficiency`
* force `secondary_family` when it should be `none`
* jump directly from route to full implementation
* treat every dangerous-sounding case as F6
* treat every structured-output case as F7
* treat every hard case as ambiguous or no_fit

These are exactly the kinds of mistakes the Router is meant to reduce.

---

## 18. Recommended short wording

If you need a short explanation for a README, demo, or collaboration thread, use wording like this:

> Troubleshooting Atlas Router v1 is a compact TXT pack derived from Problem Map 3.0 Troubleshooting Atlas.
> It helps AI systems classify failures, explain the family cut, identify the likely broken invariant, and suggest the first repair direction without pretending to offer full repair closure.

This is strong, clear, and safe.

---

## 19. One-line status

**This guide explains how to use Troubleshooting Atlas Router v1 as a compact route-first TXT pack for failure classification and first-fix guidance.**

---

## 20. Next steps

If you want the shortest next path:

1. [Get the Router TXT Pack](./troubleshooting-atlas-router-v1.txt)
2. [Go back to the Atlas landing page](../wfgy-ai-problem-map-troubleshooting-atlas.md)
3. [See the Official Flagship Demos](./Fixes/official/demos/README.md)
4. [Open the Atlas Hub](./README.md)

If this guide helped you get started, consider:

* [starring the WFGY repo](https://github.com/onestardao/WFGY)
* sharing a real edge case
* opening an issue
* testing the Router on a difficult workflow

---

## 21. Closing note

A good troubleshooting tool does not need to solve the whole system in one jump.

Sometimes the biggest upgrade is earlier than that.

Sometimes the biggest upgrade is simply this:

> the model stops reading the case in the wrong way first

That is what Router v1 is for.

---

Back to the main entry:

[Problem Map 3.0 Troubleshooting Atlas](../wfgy-ai-problem-map-troubleshooting-atlas.md)
