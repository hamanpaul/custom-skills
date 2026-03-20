<!--
AI_NOTE_START

Document role:
This file defines the first formal release and freeze policy for the Atlas system.

How to use this file:
1. Read this file after understanding the frozen atlas core and patch governance rules.
2. Use this page to understand when a document, layer, or wave is ready to be released or frozen.
3. Treat this file as the policy layer for release timing, freeze interpretation, and version-boundary discipline.
4. Read together with:
   - [Atlas Final Freeze v1](./atlas-final-freeze-v1.md)
   - [Atlas Negative Space Report v1](./atlas-negative-space-report-v1.md)
   - [Atlas v1 Integrated Handoff](./atlas-v1-integrated-handoff.md)
   - [Patch Governance v1](./patch-governance-v1.md)
   - [Patch Wave 2 Freeze Note v1](./patch-wave-2-freeze-note-v1.md)

What this file is:
- The first formal release policy for the Atlas system
- The first formal freeze policy for Atlas documents and system layers
- A rulebook for deciding when something is stable enough to publish, freeze, or carry forward as a version node

What this file is not:
- Not the atlas core itself
- Not the patch log
- Not the internal work diary
- Not a benchmark report
- Not a promise that every release must be feature-complete

Reading discipline for AI:
- Preserve the distinction between release status, freeze status, patch status, and work-in-progress status.
- Do not confuse “released” with “universally complete.”
- Do not confuse “frozen” with “never patch again.”
- Keep version boundaries explicit and layered.

AI_NOTE_END
-->

# Release and Freeze Policy v1

## Problem Map 3.0 Troubleshooting Atlas
## First formal policy for release timing, freeze boundaries, and version discipline

This document defines the first formal release and freeze policy for the Atlas system.

Its purpose is simple:

> to explain when something is ready to be released  
> when something is ready to be frozen  
> how those two states differ  
> and how future growth should remain legible

That is the job of this file.

This document should be read as a **policy layer**.
It does not replace the atlas core.
It does not replace patch governance.
It does not replace negative-space discipline.

Instead, it answers a more operational question:

> once the Atlas becomes a real multi-layer system, how do we decide what is stable enough to publish, what is stable enough to freeze, and what must remain visibly open

---

## 1. Why this document exists

A system like the Atlas can become confusing very quickly if release language is sloppy.

Without a formal policy, people may start to confuse:

- released with complete
- frozen with permanent
- public with fully validated
- patched with unstable
- work-in-progress with official structure

Those confusions damage trust.

This document exists to prevent that.

It establishes a disciplined reading:

> release is about formal publication readiness  
> freeze is about structural stability boundaries  
> patching is about controlled later growth  
> and none of these automatically imply universal completion

That distinction is essential.

---

## 2. Core policy distinction

The most important distinction in this document is this:

### Release

A release means a document, layer, or system component is ready to be used, referenced, and entered through official system navigation.

### Freeze

A freeze means a document, layer, or system component is stable enough that later changes should no longer happen through silent rewriting.

These two states are related, but not identical.

A component may be:

- released and frozen
- released but not yet strongly frozen
- internally stable but not yet released
- open and still under construction

The policy must preserve those differences.

---

## 3. What “released” means in this system

In the Atlas system, a release means the following:

- the asset is real enough to be linked from official system navigation
- the asset has a clear role
- the asset has enough coherence to be read on its own terms
- the asset is ready for public or semi-public reuse in its intended scope
- the asset is no longer only an internal rough draft

A release does **not** automatically mean:

- final
- exhaustive
- unpatchable
- globally complete
- universally validated

This matters because many strong systems need to release before they are globally complete.

That is healthy.

---

## 4. What “frozen” means in this system

In the Atlas system, a freeze means the following:

- the asset now has a stable interpretation boundary
- the asset should not be silently rewritten
- later growth should proceed through explicit notes, patches, or later version nodes
- readers may safely treat the current wording and structure as a stable reference point

A freeze does **not** automatically mean:

- finished forever
- immune to future patching
- maximally expanded
- final across all possible domains

A freeze is a stability statement, not an eternity statement.

That is the correct reading.

---

## 5. The four major states

For practical use, Atlas assets should be read through four main states.

### State 1 · Work in progress

This means:

- the asset is still under active construction
- its role may still shift
- its wording may still change substantially
- it should not yet be treated as a stable reference

This state is normal for new branches, exploratory pages, and early work layers.

### State 2 · Released but light-freeze

This means:

- the asset is coherent enough to publish
- the role is already readable
- the system may officially link to it
- but the structure is still expected to receive meaningful short-term tightening

This state is useful for materials that are ready to be seen but not yet ready for stronger freeze claims.

### State 3 · Released and frozen

This means:

- the asset is coherent enough to publish
- stable enough to serve as a reference
- strong enough that later change should proceed through explicit patch discipline

This is the strongest normal status for a stable Atlas layer.

### State 4 · Archived or superseded

This means:

- the asset remains part of lineage or version history
- but a later document or note now serves as the preferred current reference

The Atlas system should preserve this status carefully to avoid confusion.

---

## 6. Release criteria

An Atlas asset should usually be released only when the following conditions are satisfied.

### 6.1 Role clarity

The document must have a clear job.

A document should not be released if a reader cannot tell whether it is:

- core structure
- teaching layer
- adapter layer
- bridge layer
- patch note
- governance page
- support page

### 6.2 Structural readability

The document must be readable enough to stand on its own.

That does not mean it must be small.
It means its internal logic should be understandable.

### 6.3 Consistent system placement

The document must fit the current system map.

Its location, naming, and link position should make sense inside the Atlas folder structure.

### 6.4 Claim discipline

The document must clearly signal what it does and does not claim.

This is especially important for bridge documents, repair-facing documents, and future-facing pages.

### 6.5 Stable enough wording

The document must not still depend on obvious placeholder wording or unresolved role confusion.

A release can still be patchable.
But it should not feel like an internal scratchpad.

---

## 7. Freeze criteria

An Atlas asset should usually be frozen only when the following stronger conditions are satisfied.

### 7.1 Stable interpretation boundary

Readers should be able to tell what the asset means without relying on unstable side context.

### 7.2 Stable role in the system

The asset should no longer be drifting between roles.

For example, a document should not be frozen if it still feels half like a patch note and half like a core document.

### 7.3 Sufficient pressure survival

The asset should have survived enough conceptual, structural, or system-level pressure to justify stability.

This does not always mean benchmark pressure.
It may mean:

- boundary pressure
- teaching pressure
- routing pressure
- bridge pressure
- governance pressure

### 7.4 Negative-space compatibility

A frozen document should be able to coexist with explicit limits.

If it can only look strong by hiding what remains open, it is probably not ready to freeze.

### 7.5 Patchable without silent rewrite

A frozen document should be strong enough that future growth can happen around it without constantly rewriting it from inside.

That is one of the most practical freeze criteria in the whole system.

---

## 8. When to use paired documents

Some Atlas layers are strongest when they are frozen as paired documents rather than as a single text.

This is already visible in the system.

### Example
`Atlas Final Freeze v1` and `Atlas Negative Space Report v1`

This pair works because one document defines:

- what is stable

and the other defines:

- where stability intentionally stops

This is often the correct pattern when a system must be both strong and honest.

Paired freezing should be considered when:

- one document would otherwise overclaim
- one document defines positive structure and the other defines limits
- the layer is important enough that stability and openness both need explicit wording

This is a feature, not a weakness.

---

## 9. Release and freeze by layer

Different Atlas layers should not all be judged by exactly the same release or freeze threshold.

### 9.1 Core atlas layer

This layer requires the strongest freeze threshold.

Examples include:

- mother table
- major boundary rules
- canonical node structure
- frozen top-level interpretation

This layer should be released carefully and frozen only after serious structural confidence exists.

### 9.2 Teaching layer

This layer may often be released earlier than the deepest structural layer, as long as its role is clear and it does not overclaim core finality.

Examples include:

- casebook pages
- negative teaching packs
- demo explanation pages

### 9.3 Adapter layer

This layer often benefits from staged release:

- release once usable
- freeze once output discipline and behavior stabilize
- patch later through explicit versioning

### 9.4 Bridge layer

This layer requires especially careful wording.

Bridge documents may be released once evidence exists, but frozen only when:

- the bridge is real enough to cite
- the limits are explicit
- the claims remain disciplined

### 9.5 Product-support layer

This layer may release relatively early, but should still preserve consistency with the frozen system.

Examples include:

- onboarding pages
- product positioning
- public copy
- demo storyboards

These can be more flexible, but should still remain version-aware.

---

## 10. Relationship to patching

Release and freeze policy must work together with patch governance.

The clean relationship is:

- **release** says something is ready to enter the system map
- **freeze** says something is stable enough to stop silent rewriting
- **patching** says how later change should happen after that boundary exists

That means later patching is not a contradiction of freezing.

On the contrary:

> patching becomes healthier once freezing exists

because the system now has stable reference points.

---

## 11. What should never happen

The following are policy failures and should be avoided.

### 11.1 Release inflation

Do not release every rough page just because it exists.

That makes the system noisy.

### 11.2 Freeze inflation

Do not freeze pages just because they feel useful.

Freeze is a stronger claim than usefulness.

### 11.3 Silent supersession

Do not allow a new page to quietly replace an older frozen page without explicit version signaling.

### 11.4 Frozen-core drift

Do not keep a frozen title while slowly rewriting its actual meaning.

That is one of the most dangerous policy failures.

### 11.5 Hidden status ambiguity

Do not leave readers unsure whether a page is:

- experimental
- official
- released
- frozen
- patch-only
- superseded

Status ambiguity is governance debt.

---

## 12. Recommended status language

To reduce confusion, Atlas assets should use a small number of consistent status phrases.

### Recommended release phrases

- in progress
- released
- released in MVP form
- released as first formal version
- released as official entry layer

### Recommended freeze phrases

- frozen
- formally frozen
- frozen at first-release level
- frozen as patch node
- frozen as bridge layer
- frozen with open edges

### Recommended caution phrases

- does not claim universal closure
- remains patch-sensitive
- remains open for later thickening
- not a final end-state document
- should not be silently rewritten

Consistency here matters more than style.

---

## 13. Practical release rules for current work

For current Atlas work, the most useful operational rules are these.

### Rule 1

Do not link a document from the main Atlas hub until its role is clear enough to stand on its own.

### Rule 2

Do not freeze a document until its interpretation boundary is strong enough to resist silent drift.

### Rule 3

If a document needs a strong “does not claim” section to stay honest, that is fine.
That may mean it is ready for a paired or cautious freeze, not that it is weak.

### Rule 4

If a layer is growing quickly, release can happen before stronger freeze.
But that status should be explicit.

### Rule 5

If later work materially changes how a frozen page should be read, write a patch note or later version node.
Do not quietly rewrite history.

These five rules already prevent many future problems.

---

## 14. Relationship to system trust

Release and freeze policy matter because trust is not built only by content.

Trust is also built by version behavior.

A reader trusts the Atlas more when they can see:

- what is stable
- what is new
- what is still open
- what changed
- what did not change

That visibility is part of the product, part of the documentation system, and part of the AI-facing reuse discipline.

This is why policy matters.

---

## 15. Recommended official wording

When you need one short release-and-freeze statement for a new window, support page, or collaboration thread, use wording like this:

> In the Atlas system, release means a document is ready to enter official system navigation, while freeze means its interpretation boundary is stable enough that later growth should proceed through explicit patching rather than silent rewrite.  
> Released does not mean universally complete, and frozen does not mean unpatchable.  
> The system grows by making those boundaries explicit.

This wording is strong, accurate, and reusable.

---

## 16. One-line status

**This document defines how Atlas documents and layers become released, frozen, patchable, or superseded without losing version clarity or structural trust.**

---

## 17. Closing note

A system becomes easier to trust when it knows how to name its own states.

That is what release and freeze policy does.

It does not make growth slower.

It makes growth readable.
