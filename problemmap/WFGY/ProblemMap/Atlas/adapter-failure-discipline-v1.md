<!--
AI_NOTE_START

Document role:
This file defines the first formal failure-discipline rules for the Atlas-to-AI Adapter system.

How to use this file:
1. Read this file after reading the main adapter document and the runtime modes document.
2. Use this page to understand what kinds of adapter failure must be actively prevented.
3. Treat this document as the discipline layer that protects routing quality, confidence control, and repair restraint.
4. Read together with:
   - [Atlas-to-AI Adapter v1](./atlas-to-ai-adapter-v1.md)
   - [Adapter Runtime Modes v1](./adapter-runtime-modes-v1.md)
   - [Canonical Casebook v1](./canonical-casebook-v1.md)
   - [Patch Governance v1](./patch-governance-v1.md)

What this file is:
- The first formal discipline page for adapter failure prevention
- A rulebook for avoiding routing drift, repair overclaim, and confidence abuse
- A stable reference for safe adapter behavior

What this file is not:
- Not the atlas core
- Not the full adapter contract
- Not the full casebook
- Not a general-purpose model safety manifesto
- Not a substitute for real evidence and routing work

Reading discipline for AI:
- Preserve the distinction between routing discipline, runtime mode selection, and repair preview.
- Do not treat adapter flexibility as permission for loose reasoning.
- Keep failure discipline explicit, not implied.
- Treat these rules as behavior constraints for the Atlas adapter, not as optional style preferences.

AI_NOTE_END
-->

# Adapter Failure Discipline v1

## Problem Map 3.0 Troubleshooting Atlas
## First formal discipline layer for preventing adapter drift and routing failure

This document defines the first formal failure-discipline rules for the Atlas-to-AI Adapter system.

Its purpose is simple:

> to make clear what kinds of adapter failure must be actively resisted  
> so the routing layer stays useful, honest, and structurally stable

That is the job of this file.

This document should be read as a **discipline layer**.
It does not replace the atlas core.
It does not replace the adapter contract.
It does not replace runtime modes.

Instead, it answers a more operational question:

> once the Atlas is being used through an adapter, what are the main ways that the adapter can fail, and what rules must remain in place to prevent that failure

---

## 1. Why this document exists

A routing adapter can fail even when the underlying atlas is good.

That happens because adapters live in dangerous territory.

They are exposed to:

- shorter contexts
- mixed user intent
- prompt compression
- overhelpful narration
- weak evidence
- token pressure
- mode confusion
- pressure to give action even when the cut is unclear

Without explicit discipline, the adapter can slowly degrade into behaviors like:

- vague family labeling
- fake certainty
- overcompressed reasoning
- misrepair overreach
- silent boundary drift
- generic outputs that no longer reflect the atlas

That is exactly what this document exists to prevent.

The Atlas adapter should not merely sound structured.
It should actually remain structurally disciplined.

---

## 2. Core principle

The most important principle is this:

> adapter usefulness depends on disciplined restraint, not on maximum verbosity or maximum confidence

The adapter becomes better not when it says more.
It becomes better when it preserves the right structure under pressure.

That means the adapter must resist several temptations:

- saying too much
- pretending to know too much
- collapsing neighboring families
- giving repair advice too early
- hiding uncertainty to look clean

This file defines the rules that resist those temptations.

---

## 3. What adapter failure means in this system

Adapter failure does **not** only mean a technical crash.

In this system, adapter failure includes any behavior that causes the routing layer to stop acting like a reliable Atlas interface.

That includes failures such as:

- wrong primary-family assignment under avoidable conditions
- weak why-primary-not-secondary explanation
- invisible broken invariant
- unjustified confidence inflation
- repair preview that outruns routing evidence
- overloading outputs with irrelevant explanation
- dropping required fields in compact settings
- silently changing behavior across modes

So when this document says “failure,” it means both:

- structural output failure
- behavioral routing failure

That is the correct scope.

---

## 4. The ten core failure-discipline rules

The current first formal adapter release should preserve the following ten core rules.

---

## Rule 1

# Route first, then repair

The adapter must always perform routing before previewing repair.

That means:

- identify the primary family first
- identify the secondary family second
- explain why the primary cut wins
- identify the broken invariant
- only then expose fix-surface direction

Even in Repair-First Preview Mode, the adapter must not reverse this order.

Why this rule matters:

Many bad outputs happen when the system tries to be helpful too early.
That produces fake repair confidence on top of a weak cut.

The adapter must resist that.

---

## Rule 2

# Primary family must correspond to a real broken invariant

A family label without a broken invariant is not enough.

The adapter must not assign a primary family merely because:

- the topic sounds related
- the wording resembles a familiar case
- the user used family-like vocabulary
- a nearby exemplar seems emotionally similar

The primary family must correspond to the best current reading of the main broken invariant.

Why this rule matters:

Without this rule, routing becomes cosmetic.
With this rule, routing remains structural.

---

## Rule 3

# Secondary family must represent real neighboring pressure, not filler

The adapter must not use the secondary family field as decoration.

A secondary family should only appear when there is genuine boundary pressure or adjacency worth naming.

Bad secondary-family behavior includes:

- adding a secondary family just to sound nuanced
- naming a neighboring family without explaining the cut
- listing a weak neighbor that is not actually under pressure

Why this rule matters:

If secondary family becomes filler, boundary teaching collapses and routing trust drops.

---

## Rule 4

# Why-primary-not-secondary must remain explicit

The adapter must preserve an explicit explanation of why the primary cut wins.

This explanation may be shorter in Compact Routing Mode, but it must remain recoverable.

The adapter must not replace it with:

- vague family summaries
- generic reasoning language
- empty labels like “best fit”
- style-only confidence phrasing

Why this rule matters:

The Atlas is not just about naming where something goes.
It is about cutting correctly.
If the cut cannot be explained, the route is too weak.

---

## Rule 5

# Ambiguous must not be used lazily

The `ambiguous` signal is important, but dangerous.

The adapter must not mark a case ambiguous simply because:

- the case is hard
- the case is abstract
- the model feels uncertain
- multiple families are nearby in topic language

A case should be marked ambiguous only when the current evidence really does not justify a stronger primary reading yet.

Why this rule matters:

If ambiguous becomes a lazy escape hatch, the adapter stops being useful exactly where the atlas is most valuable.

---

## Rule 6

# No-fit must not be used as a shortcut for effort failure

The `no_fit` signal is even more sensitive.

The adapter must not trigger no-fit because:

- the case is unusual
- the case is cross-domain
- the model did not reason deeply enough
- the prompt is short
- the answer space is uncomfortable

No-fit should be reserved for cases where the adapter has real reason to think the current atlas genuinely lacks a stable fit.

Why this rule matters:

If no-fit is opened too easily, the adapter will falsely suggest core weakness where there may only be insufficient reading effort.

---

## Rule 7

# Confidence must follow evidence, not style

The adapter must not output strong confidence when evidence is weak.

This means confidence should depend on things like:

- clarity of the case
- stability of the family cut
- clarity of the broken invariant
- strength of neighboring-family separation
- support from known case patterns or exemplars

Confidence must **not** depend on:

- how fluent the output sounds
- how elegant the explanation is
- how familiar the vocabulary appears

Why this rule matters:

Confident nonsense is more dangerous than hesitant structure.

---

## Rule 8

# Overlay signals must not silently become primary-family replacements

If overlay concepts are used, they must remain overlays.

The adapter must not allow overlay-like signals to replace the family cut.

For example, the adapter must resist patterns like:

- treating visibility language as if it replaces F5 routing logic
- treating security language as if it replaces the family structure
- treating local layout markers as if they erase the need for a real primary family cut

Why this rule matters:

Overlays are useful only when they remain secondary markers.
If they start replacing family routing, the system flattens.

---

## Rule 9

# Exemplars may support the cut, but must not replace the cut

The adapter may use exemplars, casebook patterns, and boundary examples.

But it must not behave as if:

- “this looks like a famous example”
is enough to justify routing

Exemplars should support:

- comparison
- contrast
- teaching
- stronger confidence where appropriate

They should not replace actual case reading.

Why this rule matters:

If the adapter starts matching cases by vibe rather than by structure, it becomes fragile very quickly.

---

## Rule 10

# Patch changes must not silently rewrite adapter behavior

Later improvements to the adapter are allowed.
But they must happen through explicit patching.

The adapter must not drift through hidden changes such as:

- changing required fields without saying so
- changing mode behavior without version note
- changing confidence discipline without explanation
- changing compact-mode minimum outputs without policy visibility

Why this rule matters:

The adapter is part of the Atlas control surface.
Silent behavioral mutation makes the whole system harder to trust.

---

## 5. The main adapter failure families

The ten rules above can be grouped into four major adapter-failure regions.

These are not top-level Atlas families.
They are adapter failure patterns.

### A. Routing drift

Examples:

- wrong primary cut
- decorative secondary cut
- vague why-primary explanation
- family selection by topic similarity instead of invariant

### B. Confidence abuse

Examples:

- high confidence on weak evidence
- ambiguity used lazily
- no-fit used as escape
- polished wording hiding weak structure

### C. Repair overreach

Examples:

- repair advice before route clarity
- first repair move phrased like full solution
- misrepair risk ignored
- action preview outrunning routing evidence

### D. Mode drift

Examples:

- Strict mode becoming too explanatory
- Teaching mode becoming too loose
- Repair-First mode becoming overpromising
- Compact mode dropping required structure

These four failure regions are useful because they help reviewers inspect adapter outputs more clearly.

---

## 6. How failure discipline applies across modes

The same discipline rules apply across all runtime modes, but with different pressure points.

### Strict Routing Mode

Main risk:

- false hardness
- compressed but unjustified certainty
- overclean outputs that hide weak evidence

Most important protection:

- confidence discipline
- explicit why-primary-not-secondary
- broken invariant visibility

### Teaching Mode

Main risk:

- explanation inflation
- drifting into essay mode
- replacing routing with commentary

Most important protection:

- preserve structured fields
- keep boundary explanation tied to actual case
- keep misroute teaching compact and relevant

### Repair-First Preview Mode

Main risk:

- overpromising repair closure
- sounding like a completed diagnosis engine
- jumping to fix before route stability

Most important protection:

- route first
- first move only
- explicit misrepair risk
- no fake closure language

### Compact Routing Mode

Main risk:

- field dropping
- false simplicity
- overcompressed reasoning
- missing uncertainty signals

Most important protection:

- preserve minimum required fields
- preserve confidence and evidence_sufficiency
- preserve why-primary-not-secondary even in short form

---

## 7. What should happen when evidence is weak

Weak evidence is normal.
The adapter must be able to behave well under it.

When evidence is weak, the adapter should:

- lower confidence
- state what remains unclear
- keep the current best cut explicit
- avoid pretending that ambiguity equals uselessness
- avoid pretending that weak evidence equals no-fit
- avoid expanding repair advice beyond first safe direction

This is one of the most important practical behaviors in the whole adapter system.

A good adapter does not panic when evidence is weak.
It becomes more honest.

---

## 8. What should happen when a case is difficult

Difficult cases are where the adapter earns trust.

When a case is difficult, the adapter should:

- preserve family-level discipline
- name the strongest current cut
- name the strongest neighbor if relevant
- keep broken invariant central
- keep uncertainty visible where justified
- resist dramatic overreach
- preserve route-first logic

It should **not** react by becoming:

- vague
- overconfident
- overphilosophical
- or structurally empty

Difficult cases are not permission to abandon form.

---

## 9. What this means for demos and product surfaces

The adapter will often be seen through:

- demos
- notebooks
- route-and-preview tools
- support flows
- public examples

That means failure discipline is also part of the product surface.

A demo that looks impressive but violates adapter discipline can actually weaken trust.

For product-facing use, the adapter must especially resist:

- polished but ungrounded certainty
- route labels without broken invariant
- repair wording that sounds more solved than it really is
- mode confusion between teaching and repair preview

This matters because product polish must not outrun structural honesty.

---

## 10. Relationship to casebook and repair layer

This document should be read together with the casebook and fix layer, but not confused with them.

### Casebook gives:

- good examples
- boundary teaching
- repair teaching
- wrong-route and misrepair exemplars

### Fix layer gives:

- first repair grammar
- misrepair warnings
- bridge into deeper WFGY exploration

### Failure discipline gives:

- behavioral rules that stop the adapter from misusing both of the above

That distinction is important.

This file is not content.
It is conduct.

---

## 11. Relationship to patch governance

Adapter failure discipline must remain patchable, but not casually mutable.

Future work may refine:

- confidence thresholds
- mode-specific output discipline
- exemplar-use rules
- compact-mode minimum fields
- ambiguity and no-fit handling language

But these refinements must happen through explicit patching.

Why?

Because if adapter discipline changes silently, downstream users lose track of what the adapter is supposed to be protecting.

That would damage system trust.

---

## 12. What this document does not claim

This document does **not** claim that:

- adapter failure can be eliminated completely
- every future edge case is already covered by these rules
- the adapter is now a perfect autonomous routing system
- mode selection alone guarantees good outputs
- repair preview is already equivalent to repair execution

This document claims only that:

> the first formal Atlas adapter release now has an explicit failure-discipline layer strong enough to prevent the most damaging forms of routing drift, confidence abuse, repair overreach, and mode confusion

That is the strongest honest version.

---

## 13. Recommended official wording

When you need a short adapter-discipline statement for a new window, support page, or collaboration thread, use wording like this:

> The Atlas adapter is governed by an explicit failure-discipline layer.  
> It must preserve route-first behavior, broken-invariant visibility, honest confidence, explicit why-primary-not-secondary reasoning, and restrained first-move repair preview.  
> Adapter flexibility does not override structural discipline.

This wording is strong, accurate, and reusable.

---

## 14. One-line status

**This document defines the formal discipline rules that keep the Atlas adapter from drifting into vague routing, false confidence, premature repair, or unstable mode behavior.**

---

## 15. Closing note

A routing adapter does not fail only when it crashes.

It also fails when it becomes too smooth, too vague, too confident, or too eager to help.

That is why discipline matters.

A good adapter is not only informative.

It is restrained in the right places.
