<!--
AI_NOTE_START

Document role:
This file defines the first formal runtime-mode layer for the Atlas-to-AI Adapter system.

How to use this file:
1. Read this file after reading the main adapter document.
2. Use this page to understand when different runtime modes should be used.
3. Treat this document as the mode policy and behavior layer for AI-facing atlas routing.
4. Read together with:
   - [Atlas-to-AI Adapter v1](./atlas-to-ai-adapter-v1.md)
   - [Canonical Casebook v1](./canonical-casebook-v1.md)
   - [Patch Governance v1](./patch-governance-v1.md)
   - [Release and Freeze Policy v1](./release-and-freeze-policy-v1.md)

What this file is:
- The first formal runtime-mode document for the Atlas adapter
- A behavior guide for strict, teaching, repair-first, and compact routing
- A stable mode-reference page for human and AI-facing usage

What this file is not:
- Not the atlas core
- Not the full adapter contract
- Not the full casebook
- Not the full repair system
- Not a hidden agent runtime framework

Reading discipline for AI:
- Preserve the distinction between routing mode, teaching mode, repair preview, and compact routing.
- Do not silently merge these modes into one generic behavior profile.
- Keep mode selection explicit and task-sensitive.
- Treat runtime modes as controlled adapter behaviors, not as replacements for the atlas core.

AI_NOTE_END
-->

# Adapter Runtime Modes v1

## Problem Map 3.0 Troubleshooting Atlas
## First formal runtime-mode layer for Atlas-to-AI Adapter

This document defines the first formal runtime modes for the Atlas-to-AI Adapter system.

Its purpose is simple:

> to explain how the same atlas routing layer should behave differently under different usage conditions  
> while still preserving the same route-first discipline

That is the job of this file.

This document should be read as a **runtime behavior layer**.
It does not replace the atlas core.
It does not replace the adapter contract.
It does not replace the casebook.

Instead, it answers a different question:

> once the atlas is being used by humans, notebooks, workflows, or AI systems, what mode should the adapter run in, and what output discipline should that mode preserve

---

## 1. Why this document exists

The Atlas adapter is meant to be reused across different settings.

But not every setting needs the same behavior.

A human onboarding flow may need more explanation.
A benchmark triage loop may need harder structure.
A compact model may need shorter outputs.
A product demo may need a repair preview after routing.

Without runtime modes, these different settings can easily become muddled.

That creates several problems:

- outputs become inconsistent
- mode drift becomes invisible
- teaching behavior leaks into strict routing
- repair-preview behavior overclaims closure
- compact mode drops essential fields
- readers stop knowing what the adapter is trying to do

This document exists to prevent that.

It establishes a clean rule:

> one atlas  
> one adapter contract  
> multiple disciplined runtime modes

That is the correct design.

---

## 2. Core runtime principle

All runtime modes must preserve the same core ordering:

> route first  
> explain the cut  
> only then preview repair when the mode allows it

This means runtime modes may change:

- verbosity
- explanation depth
- exemplar use
- repair-preview presence
- output compactness

But they must not change the basic logic of the system.

The modes are not different ontologies.
They are different controlled views over the same routing grammar.

---

## 3. The four formal runtime modes

The current adapter has four formal runtime modes.

They are:

1. Strict Routing Mode
2. Teaching Mode
3. Repair-First Preview Mode
4. Compact Routing Mode

These four modes are enough for the current first formal adapter release.

They do not claim to cover every possible future mode.
They are the first stable set.

---

## 4. Mode 1

# Strict Routing Mode

## One-line definition

Strict Routing Mode is the default high-discipline mode for stable case routing, where classification accuracy, structural clarity, and boundary discipline matter more than extended explanation.

---

## Main purpose

This mode exists for settings where the adapter should behave like a careful routing layer rather than like a teacher or assistant narrator.

Its job is to answer:

- what is the primary family
- what is the secondary family
- why is the primary cut better
- what invariant is broken
- what is the best current fit
- what is the first repair direction

without unnecessary narrative expansion.

---

## Typical use cases

Strict Routing Mode is best for:

- issue triage
- benchmark failure routing
- workflow incident routing
- batch case sorting
- model-side routing control
- notebook outputs where structure matters more than prose

This is the most generally reusable mode.

---

## Behavioral profile

In this mode, the adapter should:

- prioritize family routing first
- explicitly state why primary beats secondary
- explicitly state the broken invariant
- preserve fit-level clarity
- keep repair direction to first move only
- avoid drift into long teaching prose
- avoid drifting into speculative closure

This is the mode that best reflects the system’s routing backbone.

---

## Required output discipline

Strict Routing Mode should normally preserve the following fields:

- primary_family
- secondary_family
- why_primary_not_secondary
- broken_invariant
- best_current_fit
- fit_level
- ambiguous
- no_fit
- fix_surface_direction
- confidence
- evidence_sufficiency

If ambiguity or no-fit is present, the reason must remain explicit.

---

## Exemplar use

This mode should use exemplar support conservatively.

Typical behavior:

- default to core routing stack
- add only minimal exemplar support when needed
- avoid overloading the output with teaching packs

This keeps the mode hard, clean, and less prone to drift.

---

## Main risk

The main risk in this mode is overcompression that hides real uncertainty.

Strict mode should be concise, but not false-hard.

If evidence is weak, confidence must stay limited.

---

## Current status

**Strict Routing Mode is the default recommended adapter mode in the current formal release.**

---

## 5. Mode 2

# Teaching Mode

## One-line definition

Teaching Mode is the explanation-rich routing mode used when the goal is not only to classify the case, but also to teach how the cut works and why neighboring cuts are weaker.

---

## Main purpose

This mode exists for situations where readers need to understand the map itself.

Its job is to answer not only:

- what the route is

but also:

- why this route makes sense
- which boundary rule matters
- what a common wrong cut would have been
- how the atlas should be read in practice

This makes it useful for onboarding and guided learning.

---

## Typical use cases

Teaching Mode is best for:

- onboarding
- workshops
- explanation pages
- guided notebook commentary
- contributor education
- interactive learning settings
- casebook-style explanation

---

## Behavioral profile

In this mode, the adapter should:

- preserve the normal routing fields
- explain why the primary cut wins
- mention the most relevant neighbor boundary
- optionally mention common misroute risk
- remain structured rather than drifting into free prose
- stay faithful to the atlas rather than becoming a general essay engine

Teaching Mode should still feel like the atlas.
It should just be more explanatory.

---

## Required output discipline

Teaching Mode should preserve all Strict Routing fields, and usually add:

- boundary_rule_explanation
- misroute_risk_note
- brief explanation of why the wrong neighboring cut would fail

This should remain compact enough to teach clearly.

---

## Exemplar use

This mode may use exemplar injection more actively than Strict mode.

Typical behavior:

- use Routing Prompt Stack
- use family anchors when helpful
- use boundary exemplars for difficult cuts
- avoid excessive exemplar stacking that buries the live case

The mode should remain clear, not overloaded.

---

## Main risk

The main risk in this mode is explanation inflation.

Teaching Mode should not become vague, philosophical, or disconnected from the actual routing task.

It must still preserve route-first discipline.

---

## Current status

**Teaching Mode is the recommended mode for onboarding, case teaching, and explanation-heavy Atlas usage.**

---

## 6. Mode 3

# Repair-First Preview Mode

## One-line definition

Repair-First Preview Mode is the action-oriented routing mode that preserves route-first logic while allowing a clearer preview of the first repair move and the main misrepair risk.

---

## Main purpose

This mode exists for situations where users do not only want the route.
They also want a practical preview of what should happen next.

Its job is to say:

- where the failure lives
- why that cut is primary
- what should be tried first
- what common wrong first move should be avoided

This mode is especially useful for demos and assistant-like product flows.

---

## Typical use cases

Repair-First Preview Mode is best for:

- product demos
- route-and-suggest workflows
- troubleshooting copilots
- UI surfaces that need next-step clarity
- engineering support previews
- first-move decision assistance

---

## Behavioral profile

In this mode, the adapter should:

- complete routing first
- only then expose the first repair move more clearly
- keep repair scope limited to first move and immediate direction
- explicitly note misrepair risk where helpful
- avoid pretending that the full repair path is already solved
- avoid turning into a long auto-repair plan

This mode is stronger on action, but still disciplined.

---

## Required output discipline

Repair-First Preview Mode should preserve all Strict Routing fields, and usually add:

- first_repair_move_note
- misrepair_risk
- slightly clearer fix_surface_direction wording

It may also include a short note on why a tempting wrong repair would be premature.

---

## Exemplar use

This mode may use:

- family anchors
- selected boundary exemplars
- selected repair exemplars

It should do so carefully.

Too much exemplar support can make the mode sound more confident than the evidence warrants.

---

## Main risk

The main risk in this mode is overpromising.

This mode must never confuse:

- first repair move
with
- full root-cause closure

That boundary is essential.

---

## Current status

**Repair-First Preview Mode is the recommended mode for demo-facing and product-facing route-to-repair preview flows.**

---

## 7. Mode 4

# Compact Routing Mode

## One-line definition

Compact Routing Mode is the shortest disciplined routing mode for constrained-token settings, batch use, or smaller models that still need route-first structure.

---

## Main purpose

This mode exists for cases where the adapter must remain useful under tighter output limits.

Its job is not to teach deeply.
Its job is not to narrate.

Its job is to preserve the minimum viable routing structure under constraint.

This makes it especially important for practical deployment.

---

## Typical use cases

Compact Routing Mode is best for:

- small-context model usage
- low-cost routing layers
- batch routing
- embedded workflow use
- quick classification stages
- latency-sensitive support flows

---

## Behavioral profile

In this mode, the adapter should:

- compress wording aggressively
- preserve essential routing fields
- keep why-primary-not-secondary short but explicit
- keep broken invariant visible
- preserve confidence and evidence sufficiency
- shorten repair direction to one or two minimal moves
- avoid unnecessary narration

Compact mode should be short, but not sloppy.

---

## Required output discipline

Compact Routing Mode should preserve at least:

- primary_family
- secondary_family
- why_primary_not_secondary
- broken_invariant
- best_current_fit
- fit_level
- fix_surface_direction
- confidence
- evidence_sufficiency

If ambiguous or no_fit is true, the reasons must still be included.

These cannot be dropped just to save tokens.

---

## Exemplar use

Compact mode should use exemplars very sparingly.

Typical behavior:

- default to minimal routing stack
- avoid broad exemplar injection
- add only one highly relevant exemplar if the case is a hard boundary case

This is important for keeping the mode compact in a real way.

---

## Main risk

The main risk in this mode is false simplicity.

Compact mode must not become:

- vague
- overconfident
- field-dropping
- or structurally incomplete

Shorter output does not justify weaker discipline.

---

## Current status

**Compact Routing Mode is the recommended deployment mode for constrained-token and low-cost Atlas routing settings.**

---

## 8. Runtime mode comparison

The four modes can be summarized like this.

### Strict Routing Mode

- strongest structural routing discipline
- moderate explanation
- low repair preview
- best general default

### Teaching Mode

- strongest explanation depth
- higher boundary teaching value
- moderate exemplar use
- best for onboarding and learning

### Repair-First Preview Mode

- routing plus first repair preview
- stronger action orientation
- higher misrepair emphasis
- best for demos and assistant flows

### Compact Routing Mode

- shortest viable routing form
- lowest explanation depth
- strongest token efficiency
- best for constrained deployment

These are different operating views of the same adapter, not different systems.

---

## 9. Core invariants that must survive across all modes

No matter which mode is used, the following invariants must survive.

### 9.1 Route first

No mode may skip primary routing.

### 9.2 Broken invariant must remain visible

No mode may hide the structural failure behind generic language.

### 9.3 Why-primary-not-secondary must remain recoverable

Some modes compress it.
None may erase it.

### 9.4 Confidence must remain honest

Weak evidence must not produce strong certainty.

### 9.5 Repair must remain subordinate to routing

Even Repair-First Preview Mode must preserve the routing-first order.

These invariants are what make the mode system coherent.

---

## 10. How mode selection should work

Mode selection should be task-sensitive, not arbitrary.

A clean practical selection pattern is:

### Use Strict Routing Mode when

- the goal is clean classification
- the output may be reused programmatically
- the environment is triage-heavy
- there is no need for long teaching prose

### Use Teaching Mode when

- the reader needs to learn the map
- boundary explanation matters
- misroute teaching matters
- onboarding is the real goal

### Use Repair-First Preview Mode when

- the user wants a first move after routing
- the context is demo or support oriented
- the product needs visible next-step value

### Use Compact Routing Mode when

- output budget is tight
- the model is small
- the task is batch-heavy
- speed and cost matter strongly

This keeps the mode layer practical.

---

## 11. Relationship to casebook and demos

The runtime modes should not be confused with the casebook or the demos.

### Casebook

The casebook provides:

- stable teaching examples
- boundary teaching examples
- repair teaching examples

### Demos

The demo layer provides:

- visible proof-of-use
- route-to-repair illustration
- replay and live notebook teaching

### Runtime modes

The runtime modes define:

- how the adapter behaves while doing routing under different constraints

This distinction matters.

The mode system is a behavior layer, not a content library.

---

## 12. Relationship to future patching

The runtime modes are frozen in first formal form, but not permanently closed.

Future work may still patch:

- wording discipline
- exemplar selection rules
- compact-mode compression behavior
- repair-preview wording
- mode-specific field requirements

But these changes should happen through explicit patching, not silent drift.

That is especially important because adapter behavior can become inconsistent very quickly if mode boundaries are not preserved.

---

## 13. What this document does not claim

This document does **not** claim that:

- these four modes are the final permanent mode set
- every future deployment must use one of them exactly as written
- the adapter is already a full autonomous runtime framework
- mode selection can replace correct routing logic
- compact mode can sacrifice structural honesty

This document claims only that:

> the first formal Atlas adapter release now has a stable four-mode runtime layer that is strong enough to cite, teach, and reuse

That is the strongest honest version.

---

## 14. Recommended official wording

When you need a short runtime-mode statement for a new window, documentation page, or collaboration thread, use wording like this:

> The Atlas adapter currently supports four formal runtime modes: Strict Routing, Teaching, Repair-First Preview, and Compact Routing.  
> These modes do not change the atlas logic itself.  
> They change how the routing layer behaves under different usage conditions while preserving route-first discipline, broken-invariant visibility, and explicit confidence handling.

This wording is strong, accurate, and reusable.

---

## 15. One-line status

**This document defines the first four formal runtime modes of the Atlas adapter and explains how they preserve the same routing grammar under different use conditions.**

---

## 16. Closing note

A strong adapter should not behave the same way everywhere.

But it should still remain the same system.

That is why runtime modes matter.

They let the adapter change behavior without losing its shape.
