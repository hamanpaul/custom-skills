<!--
AI_NOTE_START

Document role:
This file is a small community workflow recipe for an F1 grounding repair pattern.

How to use this file:
1. Read this page after routing a case to F1 or a nearby grounding-first region.
2. Use it as a compact route-first repair workflow.
3. Treat it as a community workflow example, not as official universal doctrine.

AI_NOTE_END
-->

# F1 Grounding Repair Workflow v1

## Community workflow recipe

This is a compact community workflow for a simple F1 grounding case.

It is designed for situations where the answer drifts because the wrong evidence anchor is driving the output.

---

## Routing assumption

This workflow assumes the case has already been routed to:

- F1 Grounding & Evidence Integrity

Best current fit:

- F1_N01 Retrieval Anchor Drift
- or a nearby grounding-first case

---

## Problem pattern

Typical symptoms include:

- fluent answer
- wrong or weak source anchor
- semantically adjacent evidence
- unsupported confidence

The key idea is simple:

> the answer is wrong because the anchor is wrong

---

## First repair move

### Step 1

Identify the verified evidence source.

### Step 2

Compare it against the misleading source or semantically adjacent source.

### Step 3

Drop the wrong anchor.

### Step 4

Rewrite the answer using only the verified source.

### Step 5

Check whether the corrected answer now matches the verified anchor.

---

## What not to do first

Do not start with:

- more stylistic prompting
- more chain-of-thought pressure
- bigger output requests
- container tightening
- high-level policy redesign

Those may matter later, but not as the first move in this case.

---

## Expected result

A successful first repair should produce:

- a clearer anchor
- a corrected answer
- less unsupported drift
- better source fidelity

---

## Escalation condition

Escalate only if:

- there is no verified source
- multiple anchors conflict with no resolution
- the case turns out to be a visibility-first problem
- the failure is actually deeper than simple anchor drift

---

## One-line status

**This workflow shows a small route-first repair sequence for a simple F1 grounding case.**
