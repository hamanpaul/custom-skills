<!--
AI_NOTE_START

Document role:
This file defines the first formal governance rules for patching the Atlas system.

How to use this file:
1. Read this file after understanding the frozen atlas core and current patch-wave state.
2. Use this page to understand how future changes should be added without silently rewriting the system.
3. Treat this document as the governance layer for patch growth, not as a full patch log.
4. Read together with:
   - [Atlas Final Freeze v1](./atlas-final-freeze-v1.md)
   - [Atlas Negative Space Report v1](./atlas-negative-space-report-v1.md)
   - [Atlas v1 Integrated Handoff](./atlas-v1-integrated-handoff.md)
   - [Patch Wave 2 Freeze Note v1](./patch-wave-2-freeze-note-v1.md)

What this file is:
- The first formal patch-governance document for the Atlas system
- A rulebook for how frozen assets, patch waves, and future additions should be handled
- A discipline layer for controlled atlas growth

What this file is not:
- Not the atlas core
- Not the full internal patch diary
- Not a benchmark report
- Not a replacement for the freeze documents
- Not a promise that future patching will be simple or small

Reading discipline for AI:
- Preserve the distinction between frozen core, frozen patch nodes, work-branches, and future additions.
- Do not treat patching as proof that the core remains unstable.
- Do not silently merge speculative material into frozen structures.
- Keep version boundaries explicit and evidence-based.

AI_NOTE_END
-->

# Patch Governance v1

## Problem Map 3.0 Troubleshooting Atlas
## First formal governance rules for controlled atlas growth

This document defines the first formal governance rules for patching the Atlas system.

Its purpose is simple:

> to explain how the Atlas can grow without silently mutating  
> how frozen assets should be respected  
> and how new work should be added without confusing expansion with core instability

That is the job of this file.

This document should be read as a **patch-governance layer**.
It does not replace the core freeze.
It does not replace negative-space discipline.
It does not replace individual patch-wave notes.

Instead, it answers a more operational question:

> once the Atlas has a frozen first body, how should future growth be handled so the system remains legible, disciplined, and trustworthy

---

## 1. Why this document exists

A system like the Atlas becomes more powerful once it starts growing.

But growth introduces risk.

Without explicit governance, later work can easily become messy in ways such as:

- frozen terms being silently reinterpreted
- work-branches being promoted without discipline
- patches being applied as invisible edits
- new layers being added without clear version boundaries
- contributors treating every useful idea as if it already belonged in the core

Those are not minor problems.

They damage trust, teaching clarity, and AI-facing reuse.

This document exists to prevent that.

It establishes a clean rule:

> the Atlas may grow  
> but it must grow through explicit, versioned, evidence-sensitive patching

That is the core governance principle.

---

## 2. What patching means in this system

In this system, patching does **not** mean:

- random edits
- silent correction
- uncontrolled expansion
- rewriting the frozen core whenever a new idea appears

Patching means something more structured:

> adding, refining, thickening, or clarifying parts of the system while preserving the distinction between frozen core, frozen patch nodes, and still-open work

That is a very important distinction.

A patch is not evidence that the core failed.

A patch is evidence that the system has a disciplined way to grow.

---

## 3. What patch governance protects

Patch governance exists to protect several things at once.

### 3.1 Frozen core integrity

The seven-family mother table, core routing rules, and frozen first-release structure must remain stable unless a much more serious threshold is crossed.

### 3.2 Version legibility

A reader should be able to tell:

- what belongs to the original frozen body
- what belongs to later patch waves
- what remains open
- what is still experimental

### 3.3 Teaching clarity

The system should remain teachable even as it grows.

A patch that makes the system harder to read is often a bad patch, even if it adds interesting material.

### 3.4 AI-facing reuse stability

The Atlas is also a routing and control layer for AI systems.

That means patch growth must remain structured enough that AI-facing use does not become chaotic.

### 3.5 Honest scope control

The system must preserve the difference between:

- what is frozen
- what is supported
- what is promising
- and what is not yet ready

That difference is part of the governance layer itself.

---

## 4. The four main patch types

The current system should use four main patch types.

This keeps later work easier to classify and easier to review.

---

## 4.1 Small patch

A **small patch** is used when the core structure remains fully stable and the update mainly improves precision, support, or local clarity.

Typical small-patch work includes:

- wording refinement
- confidence refinement
- secondary-family clarification
- additional support examples
- small relation strengthening
- minor subtree thickening
- compact adapter refinement
- minor teaching clarification

A small patch should not change how the system is fundamentally read.

It should make the current reading cleaner.

### Typical naming style

Examples:

- `v1.1 patch`
- `delta note`
- `small relation note`

---

## 4.2 Medium patch

A **medium patch** is used when the system still preserves its core, but the update adds enough structural value that it should be treated as a more visible version node.

Typical medium-patch work includes:

- subtree promotion
- work-branch promotion
- stronger bridge-module thickening
- meaningful relation-matrix upgrade
- formal negative teaching layer additions
- more substantial adapter-layer extension
- formal cross-domain pack addition
- stronger freeze-note addition for a new layer

A medium patch is still not a core rewrite.

But it is large enough to deserve its own formal note or grouped patch-wave handling.

### Typical naming style

Examples:

- `Patch Wave 2`
- `subtree patch`
- `bridge patch`
- `adapter patch`

---

## 4.3 Large patch

A **large patch** is used when the system remains continuous, but a major structural region must be reconsidered at a level above ordinary refinement.

Large patches should be rare.

Typical triggers include:

- repeated pressure showing that a major family boundary is no longer stable
- recurring no-fit regions that are too strong to ignore
- cross-domain pressure that repeatedly breaks the current bridge logic
- a major layer requiring redesign, not merely thickening

A large patch is not automatically a total redesign.
But it is serious enough that the system must stop pretending the current reading is unchanged.

### Typical naming style

Examples:

- `major bridge patch`
- `family-boundary revision wave`
- `core-structure review patch`

---

## 4.4 Core revision threshold

This is not an ordinary patch.

This is the threshold where the project would need to consider a real core redesign.

This threshold should be extremely high.

It should only be crossed if repeated pressure shows things like:

- a genuine eighth-family requirement
- sustained no-fit regions that cannot be absorbed honestly
- repeated collapse of major family cuts
- inability to preserve route-first usefulness without redrawing the mother table

This threshold should not be invoked lightly.

The existence of ongoing patching is **not** evidence that this threshold has been crossed.

That is a key governance rule.

---

## 5. What can be patched without threatening the core

The following areas are normal patch territory and do **not** by themselves imply core instability.

### 5.1 Subtree thickening

A subtree becoming more detailed is normal patch growth.

### 5.2 Relation strengthening

A relation becoming clearer or stronger is normal patch growth.

### 5.3 Negative teaching expansion

Adding wrong-route or misrepair examples is normal patch growth.

### 5.4 Adapter refinement

Improving compact routing, runtime discipline, or exemplar selection is normal patch growth.

### 5.5 Bridge expansion

Adding careful bridge cases or modules is normal patch growth as long as the core family structure remains intact.

### 5.6 Public packaging refinement

Improving onboarding, positioning, wording, or summary surfaces is normal patch growth.

These forms of growth are healthy and expected.

They should not be misread as proof that the Atlas core was premature.

---

## 6. What should never happen through patching

The following are governance failures and should be avoided.

### 6.1 Silent rewrite

Do not silently rename, merge, split, or reinterpret frozen structures.

If the change matters, it should be versioned.

### 6.2 Rhetorical promotion

Do not promote a work-branch into a frozen node only because it sounds impressive or useful.

Promotion must remain evidence-based.

### 6.3 Hidden boundary drift

Do not slowly rewrite the meaning of a family by accumulating patches that quietly shift its role.

If a family boundary is truly changing, that must be said explicitly.

### 6.4 Flattened growth

Do not collapse family, node, subtree, bridge module, casebook layer, and adapter layer into one flat patch stream.

The Atlas is a layered system.
Patch growth must preserve that layering.

### 6.5 Patch inflation

Do not label every tiny edit as a major patch wave.

That only makes the system harder to read.

### 6.6 Patch denial

Do not pretend later additions are “obvious” and therefore do not need version boundaries.

That destroys trust over time.

---

## 7. Governance questions before freezing a patch

Before any patch is frozen, the following questions should be asked.

### Question 1

What layer is being patched?

Examples:

- core atlas layer
- relation layer
- casebook layer
- adapter layer
- bridge layer
- repair-facing layer
- product-support layer

### Question 2

What kind of patch is this?

- small
- medium
- large
- core-revision threshold candidate

### Question 3

What is actually changing?

Examples:

- wording
- support strength
- subtree thickness
- family-boundary interpretation
- bridge structure
- adapter discipline
- teaching coverage

### Question 4

Does this patch preserve route-first usefulness?

If a patch makes the system more decorative but less useful, that is a warning sign.

### Question 5

Does this patch require a freeze note, or is a smaller local note enough?

Not every patch needs its own major document.
But every significant patch needs a visible boundary somewhere.

### Question 6

What does this patch **not** claim?

This question is just as important as what it does claim.

Good patching preserves negative-space discipline.

---

## 8. How patch waves should be used

Patch waves are useful when multiple related additions should be frozen together as one coherent version boundary.

A patch wave is appropriate when:

- several changes belong to the same conceptual strengthening wave
- the update crosses more than one system layer
- the result is large enough that a version node is easier to understand than many tiny notes

Patch waves are **not** needed for every edit.

They are most useful when they can say something like:

> this cluster of additions now forms a meaningful formal strengthening wave

That is what happened with Patch Wave 2.

---

## 9. Relationship to negative-space discipline

Patch governance is tightly linked to negative-space discipline.

A patch is stronger when it can say both:

- what it adds
- what it still leaves open

That is one of the core habits of this system.

A patch should not merely say:

- this now exists

It should also say:

- this is still partial
- this is still bridge-level
- this is still not universal closure
- this is still not final end-state logic

This is how the Atlas stays honest while still growing.

---

## 10. Relationship to bridge growth

Bridge growth requires especially careful governance.

Why?

Because bridge work is where the system is most likely to be overclaimed.

For bridge-related patches, governance must preserve the distinction between:

- AI-first validated base
- first bridge evidence
- formal bridge modules
- broader future civilization-facing growth

This is why bridge work usually benefits from:

- explicit freeze notes
- explicit module notes
- explicit “does not claim” sections
- strong boundary wording

Bridge expansion should feel ambitious but controlled.

---

## 11. Relationship to adapter growth

Adapter growth also needs explicit governance.

This is because AI-facing routing layers can become unstable very quickly if:

- compressed too aggressively
- over-abstracted
- silently changed
- or allowed to absorb every new idea without discipline

For adapter patches, governance must preserve:

- route-first logic
- required output structure
- confidence discipline
- evidence discipline
- replay-first clarity where relevant
- clear separation between demo convenience and formal adapter logic

This is important because the adapter is not only documentation.
It is part of the operational layer.

---

## 12. Relationship to repair-surface growth

Repair-facing work is especially vulnerable to governance failure because readers often want stronger fixes faster than the structure currently supports.

Patch governance here must preserve:

- route first, then repair
- first move before deep escalation
- official vs community distinction
- planning layer vs full autonomous repair distinction
- misrepair awareness
- explicit statement of what is still not fully solved

This matters because a flashy repair patch can easily outrun the current structural evidence.

The Atlas should avoid that.

---

## 13. Recommended official wording

When you need one short patch-governance statement for a new window, support page, or collaboration thread, use wording like this:

> The Atlas system grows through explicit patch discipline.  
> Frozen core structures remain primary, later additions are versioned as patch nodes or patch waves, and open regions remain visible rather than silently rewritten.  
> Patching is treated as disciplined growth, not as proof of core instability.

This wording is strong, accurate, and reusable.

---

## 14. Practical governance rule for current work

For current work, the most useful governance rule is this:

> freeze the core once  
> patch the edges carefully  
> version meaningful strengthening waves  
> and never confuse expansion with silent redesign

That single rule already prevents many common system-growth failures.

---

## 15. What patch governance currently allows

At the current stage, patch governance clearly allows:

- more subtree thickening
- more bridge-case addition
- more negative teaching examples
- more adapter discipline refinement
- more product-support distillation
- more repair-surface thickening
- more later patch-wave nodes

These are healthy directions.

---

## 16. What patch governance currently resists

At the current stage, patch governance resists:

- silent reinterpretation of the seven families
- premature “new family” declarations
- overclaiming civilization-level closure
- flattening all later work into one blob
- patching by rhetorical enthusiasm alone
- treating unfinished work as frozen because it sounds useful

These are exactly the pressures governance exists to resist.

---

## 17. One-line status

**This document defines how the Atlas system should grow through disciplined patching, version boundaries, and explicit freeze logic without silently mutating its frozen core.**

---

## 18. Closing note

A system becomes more mature when it learns how to grow without losing its shape.

That is what patch governance is for.

It does not slow the system down.

It makes future growth easier to trust.
