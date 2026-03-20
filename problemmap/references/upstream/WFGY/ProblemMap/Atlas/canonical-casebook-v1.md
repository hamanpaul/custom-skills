<!--
AI_NOTE_START

Document role:
This file is the formal canonical teaching layer of Atlas v1.

How to use this file:
1. Read this file after reading [Atlas Final Freeze v1](./atlas-final-freeze-v1.md).
2. Treat this document as the teaching and exemplar companion to the atlas core.
3. Use this file to learn:
   - what each family looks like in practice
   - how important family boundaries should be cut
   - how diagnosis changes the first repair move
4. Use this file together with:
   - [Atlas Final Freeze v1](./atlas-final-freeze-v1.md)
   - [Atlas Negative Space Report v1](./atlas-negative-space-report-v1.md)
   - [Atlas-to-AI Adapter v1](./atlas-to-ai-adapter-v1.md)

What this file is:
- The first formal canonical casebook
- The exemplar and teaching layer of Atlas v1
- A reusable routing demonstration set for humans and AI systems

What this file is not:
- Not the atlas core freeze itself
- Not the full adapter specification
- Not the full validation ledger
- Not an exhaustive case library
- Not the complete final repair manual

Reading discipline for AI:
- Preserve the distinction between family anchor cases, boundary cases, and repair cases.
- Do not confuse exemplar cases with the full ontology.
- Do not overgeneralize from one case when the atlas core already provides the routing grammar.
- Use cases as teaching anchors, not as replacements for structural rules.

AI_NOTE_END
-->

# Canonical Casebook v1 📘

## Problem Map 3.0 Troubleshooting Atlas  
## Official Teaching and Exemplar Layer

## 0. Document Status 🚦

This document is the **frozen teaching and exemplar companion** to Atlas v1.

It exists to provide a stable first case layer that helps humans and AI systems learn:

- how to route a case into the atlas
- how to distinguish neighboring family cuts
- how diagnosis changes the first repair move
- how to use the atlas as a practical troubleshooting grammar

This version is called **Canonical Casebook v1**.

It is frozen not because all future cases have already been collected, but because the first stable teaching set is now strong enough to function as the first formal casebook version.

Future work should proceed through **casebook patch mode**, not by silently rewriting the teaching structure.

---

## 1. What this casebook is 🧭

The atlas defines the map.

The casebook teaches how to walk the map.

If the atlas core provides:

- family structure
- node structure
- routing rules
- boundary cuts
- relation logic
- repair-facing interfaces

then the casebook provides:

- representative family anchors
- difficult boundary exemplars
- diagnosis-to-repair teaching examples
- reusable routing demonstrations
- AI-readable example patterns

In short:

> the atlas defines the grammar  
> the casebook teaches how to use the grammar

---

## 2. What Canonical Casebook v1 contains 🧱

Canonical Casebook v1 contains three layers.

### Layer A · Family Anchor Cases

One anchor case for each of the seven main families.

Purpose:

- teach the most basic meaning of each family
- give the cleanest first example for humans
- give AI systems a stable first exemplar set

### Layer B · Boundary Case Pack

A curated set of cases chosen because they sit near important family boundaries.

Purpose:

- teach why a case belongs to one family instead of a neighboring family
- teach the core knife-cuts of the atlas
- reduce confusion in high-pressure routing zones

### Layer C · Repair Case Pack

A curated set of cases chosen because they best demonstrate diagnosis-to-repair flow.

Purpose:

- show how correct routing changes the first repair move
- show how misrepair begins when routing goes wrong
- connect the atlas to repair-facing thinking without pretending the full repair system is already complete

---

## 3. What Canonical Casebook v1 claims ✅

Canonical Casebook v1 claims that the following are now stable enough to freeze:

- the first 7 family anchor cases
- the first 6 boundary teaching cases
- the first 6 repair teaching cases
- the first stable case format
- the first reusable diagnosis-to-repair teaching layer
- the first reusable exemplar pack for AI-facing routing

This means the casebook is now stable enough to support:

- onboarding
- README explanation
- product copy support
- demo storyboard design
- AI routing exemplars
- future casebook patch waves

---

## 4. What Canonical Casebook v1 does not claim 🔍

Canonical Casebook v1 does **not** claim that:

- all important cases have already been collected
- every family boundary is fully covered by examples
- every repair family already has all best possible exemplars
- all cross-domain exemplars are already included
- no future casebook patching is needed

Canonical Casebook v1 claims only that:

> the first stable teaching set of family anchors, boundary cuts, and diagnosis-to-repair exemplars has been completed and frozen as the first formal casebook version

---

## 5. Standard Case Format 🧩

All canonical cases in v1 use the following stable structure:

1. Case ID / Name
2. Primary Family
3. Secondary Family
4. Why Primary Not Secondary
5. Broken Invariant
6. Best Current Fit
7. Fix Surface Direction
8. Why This Case Matters

This format is frozen in v1 because it is:

- compact enough for repeated use
- clear enough for engineering readers
- structured enough for AI systems
- reusable in future patch waves

For format discipline, see also [Case Format v1](./case-format-v1.md).

---

# Part I · Family Anchor Cases 🌟

These seven cases serve as the first anchor teaching set for the seven-family mother table.

---

## Anchor Case 1

### No.1 Hallucination & Chunk Drift

**Primary Family**  
F1 Grounding & Evidence Integrity

**Secondary Family**  
F5 Observability & Diagnosability Integrity

**Why Primary Not Secondary**  
The main failure is not merely that the error is hard to inspect.  
The main failure is that the answer no longer remains anchored to the relevant evidence or retrieval source.

**Broken Invariant**  
evidence-anchor integrity broken

**Best Current Fit**  
F1_N01 Retrieval Anchor Drift

**Fix Surface Direction**

- re-grounding
- chunk-to-target trace
- evidence verification
- anchor re-check

**Why This Case Matters**  
This is one of the best introductory cases for teaching that many “hallucination-like” failures are grounding failures first.

---

## Anchor Case 2

### No.2 Interpretation Collapse

**Primary Family**  
F2 Reasoning & Progression Integrity

**Secondary Family**  
None

**Why Primary Not Secondary**  
The primary failure lies in the breakdown of interpretation and reasoning progression, not in continuity, grounding, or representation.

**Broken Invariant**  
interpretation progression integrity broken

**Best Current Fit**  
F2_N01 Interpretation Collapse

**Fix Surface Direction**

- decomposition reset
- alternate parse validation
- interpretation checkpoint insertion

**Why This Case Matters**  
This is one of the cleanest examples of a genuine reasoning-first failure.

---

## Anchor Case 3

### No.7 Memory Breaks Across Sessions

**Primary Family**  
F3 State & Continuity Integrity

**Secondary Family**  
None

**Why Primary Not Secondary**  
The primary failure lies in cross-session continuity loss, not in protocol closure or execution skeleton failure.

**Broken Invariant**  
session continuity broken

**Best Current Fit**  
F3_N01 Memory Continuity Failure

**Fix Surface Direction**

- memory persistence guard
- session carryover audit
- continuity restoration

**Why This Case Matters**  
This is one of the best cases for teaching what a continuity-first failure actually looks like.

---

## Anchor Case 4

### No.15 Deployment Deadlock

**Primary Family**  
F4 Execution & Contract Integrity

**Secondary Family**  
None

**Why Primary Not Secondary**  
The primary failure lies in liveness collapse and execution deadlock, not in reasoning or visibility.

**Broken Invariant**  
deployment liveness closure broken

**Best Current Fit**  
F4_N02 Deployment Deadlock

**Fix Surface Direction**

- liveness watchdog
- deadlock break routine
- fallback execution route

**Why This Case Matters**  
This case shows that the atlas can handle runtime and deployment-level failures, not just language-level mistakes.

---

## Anchor Case 5

### No.8 Debugging Is a Black Box

**Primary Family**  
F5 Observability & Diagnosability Integrity

**Secondary Family**  
F4 Execution & Contract Integrity

**Why Primary Not Secondary**  
The main failure is that the failure path itself is not visible enough to diagnose.  
Execution may or may not later prove to be broken, but diagnosability fails first.

**Broken Invariant**  
failure-path visibility broken

**Best Current Fit**  
F5_N01 Failure Path Opacity

**Fix Surface Direction**

- observability insertion
- trace exposure
- diagnostic logging uplift

**Why This Case Matters**  
This is one of the strongest demonstrations of why F5 must exist as its own family.

---

## Anchor Case 6

### Alignment Boundary Drift

**Primary Family**  
F6 Boundary & Safety Integrity

**Secondary Family**  
F5 Observability & Diagnosability Integrity

**Why Primary Not Secondary**  
The primary failure lies in boundary instability itself, not merely in missing visibility or oversight.

**Broken Invariant**  
alignment boundary integrity broken

**Best Current Fit**  
F6_N01 Alignment Boundary Drift

**Fix Surface Direction**

- alignment guard
- target-boundary re-anchor
- proxy-goal separation

**Why This Case Matters**  
This is a flagship case for teaching what a real boundary-first failure looks like.

---

## Anchor Case 7

### Logic Descriptor Collapse

**Primary Family**  
F7 Representation & Localization Integrity

**Secondary Family**  
F2 Reasoning & Progression Integrity

**Why Primary Not Secondary**  
The primary failure lies in the inability of the formal or logical descriptor to faithfully carry reasoning structure.

**Broken Invariant**  
formal descriptor fidelity broken

**Best Current Fit**  
F7_N01_A Logic Descriptor Fidelity Failure

**Fix Surface Direction**

- descriptor fidelity audit
- formal adequacy validation
- logic-structure preservation

**Why This Case Matters**  
This is one of the clearest examples of a container-first rather than progression-first failure.

---

# Part II · Boundary Case Pack ✂️

These cases are selected because they teach the most important family cuts in the current atlas.

---

## Boundary Case 1

### No.5 Semantic Meaning Is Not Vector Similarity

**Primary Family**  
F1 Grounding & Evidence Integrity

**Secondary Family**  
F7 Representation & Localization Integrity

**Why Primary Not Secondary**  
The main failure is that proxy similarity is incorrectly treated as true semantic alignment.  
This is grounding-first, not container-first.

**Broken Invariant**  
semantic target grounding broken

**Best Current Fit**  
F1_N02 Semantic Grounding Mismatch

**Fix Surface Direction**

- semantic anchor checks
- proxy / true-meaning separation
- target-reference audit

**Why This Case Matters**  
This is one of the best teaching cases for the F1 / F7 boundary.

---

## Boundary Case 2

### No.11 Symbolic Collapse

**Primary Family**  
F7 Representation & Localization Integrity

**Secondary Family**  
F2 Reasoning & Progression Integrity

**Why Primary Not Secondary**  
The symbolic or formal carrier itself fails to remain faithful enough to support reasoning structure.  
The main failure is in the representational shell, not in reasoning progression first.

**Broken Invariant**  
symbolic carrier fidelity broken

**Best Current Fit**  
F7_N01 Symbolic Representation Fidelity Failure  
More specifically: F7_N01_A Logic Descriptor Fidelity Failure

**Fix Surface Direction**

- descriptor fidelity audit
- formal adequacy validation
- logic-structure preservation

**Why This Case Matters**  
This is one of the strongest cases for teaching the F2 / F7 cut.

---

## Boundary Case 3

### Value / Information / Knowledge Coherence

**Primary Family**  
F5 Observability & Diagnosability Integrity

**Secondary Family**  
F6 Boundary & Safety Integrity

**Why Primary Not Secondary**  
The main failure currently appears first in coherence visibility, meaning-profile visibility, and auditability of value / information / knowledge structure.  
Boundary pressure is strong, but not the first failure layer.

**Broken Invariant**  
coherence-profile visibility broken

**Best Current Fit**  
F5 / F6 boundary-edge fit

**Fix Surface Direction**

- coherence visibility uplift
- meaning-profile tracing
- normative consistency audit
- then boundary stabilization if needed

**Why This Case Matters**  
This is one of the most important high-abstract boundary cases for the F5 / F6 cut in v1.

---

## Boundary Case 4

### Synthetic Truth Extraction

**Primary Family**  
F1 Grounding & Evidence Integrity

**Secondary Family**  
F7 Representation & Localization Integrity

**Why Primary Not Secondary**  
The main failure lies in extracting truth-like anchors from synthetic worlds, not in the synthetic container itself failing first.

**Broken Invariant**  
synthetic truth-anchor grounding broken

**Best Current Fit**  
F1_E01 Synthetic Truth Grounding

**Fix Surface Direction**

- truth-like anchor check
- synthetic target grounding audit
- referent extraction validation

**Why This Case Matters**  
This is a flagship boundary case for the F1 / F7 synthetic cut.

---

## Boundary Case 5

### Multi-Agent Continuity Drift

**Primary Family**  
F3 State & Continuity Integrity

**Secondary Family**  
F6 Boundary & Safety Integrity

**Outer Pressure**  
F4 Execution & Contract Integrity

**Why Primary Not Secondary**  
The current best cut is that agent-level continuity threads fail first, not collective-boundary regime or protocol closure.

**Broken Invariant**  
multi-agent continuity thread broken

**Best Current Fit**  
F3_E01 Multi-Agent Continuity Instability

**Fix Surface Direction**

- role fencing
- ownership tracing
- continuity restoration
- then protocol or boundary repair if needed

**Why This Case Matters**  
This is one of the best cases for teaching the F3 / F4 / F6 outer-pressure boundary.

---

## Boundary Case 6

### Institutional Enforcement Drift

**Primary Family**  
F4 Execution & Contract Integrity

**Secondary Family**  
F6 Boundary & Safety Integrity

**Why Primary Not Secondary**  
The main failure currently appears first in rule-to-action closure, enforcement drift, and accountability thinning, not in collective boundary legitimacy first.

**Broken Invariant**  
institutional enforcement closure broken

**Best Current Fit**  
F4_E01 Institutional Enforcement Drift

**Fix Surface Direction**

- rule-to-action trace
- enforcement bridge checks
- accountability route repair

**Why This Case Matters**  
This is one of the strongest cases for teaching the F4 / F6 cut at the institutional layer.

---

# Part III · Repair Case Pack 🛠️

These cases are selected because they best demonstrate diagnosis-to-repair flow.

---

## Repair Case 1

### No.1 Hallucination & Chunk Drift

**Primary Family**  
F1 Grounding & Evidence Integrity

**Secondary Family**  
F5 Observability & Diagnosability Integrity

**Why Primary Not Secondary**  
The output is no longer tied to the correct evidence source, so grounding fails before diagnosis support becomes the main issue.

**Broken Invariant**  
evidence-anchor integrity broken

**Best Current Fit**  
F1_N01 Retrieval Anchor Drift

**Fix Surface Direction**

- re-grounding
- chunk-to-target trace
- evidence verification
- anchor re-check

**Why This Case Matters**  
This case teaches that hallucination-like behavior often requires a grounding-first repair move.

---

## Repair Case 2

### No.7 Memory Breaks Across Sessions

**Primary Family**  
F3 State & Continuity Integrity

**Broken Invariant**  
session continuity broken

**Best Current Fit**  
F3_N01 Memory Continuity Failure

**Fix Surface Direction**

- memory persistence guard
- session carryover audit
- continuity restoration

**Why This Case Matters**  
This case teaches that continuity failures usually require continuity infrastructure, not simply more instruction text.

---

## Repair Case 3

### No.15 Deployment Deadlock

**Primary Family**  
F4 Execution & Contract Integrity

**Broken Invariant**  
deployment liveness closure broken

**Best Current Fit**  
F4_N02 Deployment Deadlock

**Fix Surface Direction**

- liveness watchdog
- deadlock break routine
- fallback execution route

**Why This Case Matters**  
This case teaches that execution deadlocks require liveness repair first, not reasoning repair first.

---

## Repair Case 4

### No.8 Debugging Is a Black Box

**Primary Family**  
F5 Observability & Diagnosability Integrity

**Secondary Family**  
F4 Execution & Contract Integrity

**Broken Invariant**  
failure-path visibility broken

**Best Current Fit**  
F5_N01 Failure Path Opacity

**Fix Surface Direction**

- observability insertion
- trace exposure
- diagnostic logging uplift

**Why This Case Matters**  
This case teaches that sometimes the correct first repair move is to expose the failure path before committing to a deeper family repair.

---

## Repair Case 5

### Early Warning Deficit

**Primary Family**  
F5 Observability & Diagnosability Integrity

**Secondary Family**  
F6 Boundary & Safety Integrity

**Broken Invariant**  
pre-failure warning visibility broken

**Best Current Fit**  
F5_E02 Early Warning Deficit  
More specifically:

- F5_E02_A Fragility Signature Blindness  
or
- F5_E02_B Regime-Shift Warning Delay

**Fix Surface Direction**

- fragility signature extraction
- warning horizon extension
- pre-transition detector
- delay-sensitive alerting

**Why This Case Matters**  
This case teaches that pre-failure warning capability is itself a first-class repair target, not just a supporting tool.

---

## Repair Case 6

### Alignment Boundary Drift

**Primary Family**  
F6 Boundary & Safety Integrity

**Secondary Family**  
F5 Observability & Diagnosability Integrity

**Broken Invariant**  
alignment boundary integrity broken

**Best Current Fit**  
F6_N01 Alignment Boundary Drift

**Fix Surface Direction**

- alignment guard
- target-boundary re-anchor
- proxy-goal separation
- control-path and intervention-margin review

**Why This Case Matters**  
This case teaches that some problems remain boundary-first even after visibility is improved.

---

# Part IV · Why this casebook matters 💡

Canonical Casebook v1 matters because it turns the atlas from a structural reference into a teaching and routing system.

It now teaches three things:

### 1. What each family fundamentally is

through the family anchor cases

### 2. How difficult family boundaries should be cut

through the boundary case pack

### 3. How correct diagnosis changes the first repair move

through the repair case pack

In other words:

> the atlas supplies the failure grammar  
> the casebook teaches how to use it

---

## 6. How to use this casebook 🧠

This casebook can now be used as:

- a teaching companion to [Atlas Final Freeze v1](./atlas-final-freeze-v1.md)
- a case-based onboarding document
- an AI routing exemplar set
- a README and documentation source
- a demo storyboard source
- a patch-wave baseline for future case additions

When using it in a new working context, treat it as the **frozen casebook mainline** and treat future additions as **casebook patches**.

---

## 7. Relationship to the atlas core 🔗

This document depends on the atlas core.

Use the atlas core to understand:

- family structure
- routing rules
- canonical layout
- subtree structure
- relation lines

Use this casebook to understand:

- what those structures look like in practice
- how boundary cuts behave in real teaching cases
- how first repair moves depend on correct routing

This is why the casebook should be read **after** the core atlas, not before it.

---

## 8. Relationship to the AI adapter 🤖

This casebook is also one of the foundations of the AI-facing adapter layer.

It supports:

- exemplar injection
- family anchor support
- boundary teaching support
- repair-preview support

That is why this document should be read alongside:

- [Atlas-to-AI Adapter v1](./atlas-to-ai-adapter-v1.md)

The adapter compresses the routing grammar.  
The casebook supplies the teaching exemplars that help make that compression stable.

---

## 9. Patch protocol 🔄

Canonical Casebook v1 is frozen, but not closed.

### Small patch

Use for:

- adding one or two new canonical cases
- confidence upgrades
- better secondary-family explanations
- improved fit notes

### Medium patch

Use for:

- adding a new boundary teaching pack
- adding a new repair teaching pack
- adding a cross-domain demonstration pack
- adding a negative example pack

### Large patch

Only use if:

- major family boundaries require re-teaching
- multiple canonical cases become unstable under new atlas patches
- the teaching structure itself must be redesigned

### Current status

No large-patch pressure is currently justified.

---

## 10. Current completion status ✅

Canonical Casebook v1 is now considered **formally frozen**.

Its current structure includes:

- 7 family anchor cases
- 6 boundary cases
- 6 repair cases

This means the first full teaching layer of the atlas now exists.

Further work should continue in patch mode.

---

## 11. One-line status

**Canonical Casebook v1 is frozen. Further casebook work proceeds in patch mode.**

---

## 12. Closing note ✨

A strong atlas is not enough by itself.

People and AI systems also need:

- clear first examples
- reliable boundary teaching
- repair-aware routing demonstrations

That is what this casebook is for.

If the atlas is the map, this document is the first formal guide for learning how to move through it.
