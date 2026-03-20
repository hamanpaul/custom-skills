<!--
AI_NOTE_START

Document role:
This file is the formal AI-facing routing and diagnosis adapter for Atlas v1.

How to use this file:
1. Read this file after:
   - [Atlas Final Freeze v1](./atlas-final-freeze-v1.md)
   - [Canonical Casebook v1](./canonical-casebook-v1.md)
2. Treat this document as the model-facing operational layer of the atlas.
3. Use this file to understand:
   - the adapter contract
   - the routing stack
   - casebook exemplar injection
   - runtime modes
   - patch discipline
   - failure discipline
4. Use this file when compressing atlas logic into prompts, TXT packs, routing flows, or AI-facing debugging systems.

What this file is:
- The AI-facing adapter layer
- The routing and diagnosis control layer
- The operational bridge between atlas structure and model usage

What this file is not:
- Not the atlas core itself
- Not the casebook itself
- Not the full fix manual
- Not a general-purpose autonomous agent design
- Not a license to silently rewrite the atlas through prompt behavior

Reading discipline for AI:
- Preserve the distinction between atlas core, casebook exemplars, adapter logic, repair-facing layer, and patch layer.
- Route first, then repair.
- Do not overclaim confidence when evidence is weak.
- Do not let exemplars override structural rules.
- Do not let overlays replace family routing.

AI_NOTE_END
-->

# Atlas-to-AI Adapter v1 🤖

## Problem Map 3.0 Troubleshooting Atlas  
## Official AI-Facing Routing and Diagnosis Layer

## 0. Document Status 🚦

This document is the **frozen first formal AI-facing adapter** for Atlas v1.

Its purpose is to turn atlas logic into a reusable operational layer for:

- AI-assisted routing
- debugging support
- issue triage
- workflow diagnosis
- benchmark failure classification
- teaching and onboarding
- compact model-facing routing

This document is frozen as **Atlas-to-AI Adapter v1**.

It is frozen not because all future adapter work is complete, but because the first stable adapter body is now strong enough to support real use, teaching, reuse, and patch-driven growth.

Future work should proceed through **adapter patch mode**, not through silent rewriting of the adapter contract.

---

## 1. What this adapter is 🧭

The atlas defines the structural grammar.

The casebook teaches how that grammar behaves through examples.

The adapter turns that grammar into a model-facing routing layer.

In short:

> the atlas defines the map  
> the casebook teaches the map  
> the adapter lets AI systems operate on the map

This adapter exists to help a model do five things more reliably:

1. route a case into the correct family
2. distinguish primary from secondary family pressure
3. state the broken invariant explicitly
4. point to the best current fit
5. give the correct first repair direction without pretending full root-cause closure

---

## 2. What Atlas-to-AI Adapter v1 contains 🧱

Atlas-to-AI Adapter v1 contains five major layers.

### A. Core Contract v1

This defines:

- minimum input expectations
- minimum output structure
- mandatory routing fields
- confidence discipline
- evidence discipline

### B. Routing Prompt Stack v1

This defines:

- the order of reasoning constraints
- the role of atlas rules
- the role of boundary rules
- the role of fit discipline
- the role of output discipline

### C. Casebook Injection Layer v1

This defines:

- when to use family anchors
- when to use boundary exemplars
- when to use repair exemplars
- how many exemplars to use
- how exemplars should support, but not replace, structural routing

### D. Runtime Mode Pack v1

This defines four operational modes:

- Strict Routing Mode
- Teaching Mode
- Repair-First Preview Mode
- Compact Routing Mode

### E. Patch Interface and Failure Discipline v1

This defines:

- how future adapter updates should happen
- what counts as small, medium, or large patch
- what the adapter must never do, even when compressed or optimized

---

## 3. What this adapter claims ✅

Atlas-to-AI Adapter v1 claims that the following are now stable enough to freeze:

- the first adapter contract
- the first routing prompt stack
- the first casebook injection rules
- the first runtime mode system
- the first adapter patch interface
- the first formal adapter failure discipline

This means the adapter is now stable enough to support:

- AI routing prompts
- AI-assisted troubleshooting
- model-facing routing demos
- onboarding and teaching
- product-facing AI flows
- TXT pack construction
- future adapter patch waves

---

## 4. What this adapter does not claim 🔍

Atlas-to-AI Adapter v1 does **not** claim that:

- every model will route perfectly under all conditions
- all prompts, platforms, and contexts behave identically
- all future compact forms are already optimized
- the adapter already contains the full repair system
- the adapter replaces the atlas core
- the adapter replaces the casebook
- no future adapter patching is needed

Atlas-to-AI Adapter v1 claims only that:

> the first stable AI-facing routing and diagnosis layer of the atlas now exists and is strong enough to freeze as a formal reusable version

---

## 5. Core Contract v1 📜

The core contract is the minimum discipline that keeps the adapter stable.

### 5.1 Minimum input expectation

The adapter expects some form of failure-bearing input, such as:

- an issue report
- a failing output
- a benchmark failure case
- a workflow collapse description
- a short debugging scenario
- a casebook-like teaching case
- a structured internal failure note

The adapter does **not** require perfect completeness.
But it does require enough content to justify a routing attempt.

### 5.2 Minimum output expectation

A valid adapter output must preserve routing structure.

At minimum, the adapter should be able to produce:

- primary family
- secondary family
- why primary not secondary
- broken invariant
- best current fit
- fit level
- fix surface direction
- confidence
- evidence sufficiency

Where ambiguity or no-fit is materially relevant, those fields must also be made explicit.

### 5.3 Contract principle

The adapter is not allowed to skip structural justification in order to sound smoother, more confident, or more fluent.

Correct routing discipline is more important than rhetorical polish.

---

## 6. Routing Prompt Stack v1 🧠

The routing stack defines how the adapter should think in ordered layers.

### Layer 1 · Core routing objective

First determine:

- what kind of failure this is
- which family is primary
- which neighboring family exerts secondary pressure

### Layer 2 · Boundary discipline

Before final routing, check the major cuts:

- F1 vs F7
- F5 vs F6
- F3 vs F4
- F2 vs F7
- F4 vs F5
- F1 vs F5

If the case sits near a known high-pressure cut, this must be reflected in the output.

### Layer 3 · Broken invariant discipline

The adapter must state what invariant is broken first.

This matters because family assignment without invariant language becomes too soft and too rhetorical.

### Layer 4 · Best-fit discipline

The adapter should map the case into:

- family
- node or family-entry
- or edge-fit wording when the case sits at a strong boundary

The adapter should not pretend full subtree closure if the fit is still local, edge-based, or patch-sensitive.

### Layer 5 · Repair-facing discipline

Only after routing should the adapter provide first repair direction.

Repair output must remain:

- routing-sensitive
- first-move oriented
- non-grandiose
- honest about uncertainty

---

## 7. Casebook Injection Layer v1 📚

The adapter is allowed to use canonical exemplars, but only under discipline.

### 7.1 Purpose of exemplar injection

Exemplars exist to support:

- family teaching
- boundary teaching
- repair-preview teaching

They do **not** exist to replace structural routing rules.

### 7.2 Injection hierarchy

#### Pack A · Family Anchor Pack

Use when the goal is to help stabilize a first family interpretation.

#### Pack B · Boundary Teaching Pack

Use when the case sits near a major family cut and needs stronger why-not-neighbor reasoning.

#### Pack C · Repair Teaching Pack

Use when the case is already routed and the system needs a more stable first repair preview.

### 7.3 Injection rule

Exemplars may support routing, but they must never override:

- frozen family rules
- frozen boundary rules
- broken-invariant discipline
- evidence discipline

### 7.4 Minimal injection principle

Use as little exemplar support as needed.

The adapter should not become exemplar-heavy by default.
It should remain rule-first, exemplar-supported.

---

## 8. Runtime Mode Pack v1 ⚙️

Atlas-to-AI Adapter v1 defines four formal runtime modes.

---

### Mode 1 · Strict Routing Mode

**Purpose**  
Stable classification and routing.

**Best for**

- issue triage
- benchmark fail routing
- workflow failure routing
- real debugging pipelines
- batch case routing

**Behavior**

- family routing first
- explicit why-primary-not-secondary
- explicit broken invariant
- explicit fit level
- fix direction restricted to first move
- no unjustified high confidence under weak evidence

**Style**

Short, hard, structured, low-noise.

**Risk posture**

This is the safest and least hallucination-prone default mode.

---

### Mode 2 · Teaching Mode

**Purpose**  
Teach users or AI systems how and why a case is being cut in a particular way.

**Best for**

- onboarding
- documentation support
- learning sessions
- collaborator training
- boundary explanation

**Behavior**

- preserves full structural output
- explains why-not-neighbor more fully
- may name the relevant boundary rule
- may explain what goes wrong if the case is cut incorrectly

**Style**

More explanatory than Strict Mode, but still structure-first.

**Risk posture**

Teaching must not degrade into freeform essay behavior.
The adapter still needs to respect the contract.

---

### Mode 3 · Repair-First Preview Mode

**Purpose**  
Give a useful first repair move after correct routing.

**Best for**

- demos
- product UX
- assistant workflows
- route-and-suggest systems
- first-step debug support

**Behavior**

- route first
- then give 1 to 3 first repair directions
- may mention misrepair risk
- does not provide a full repair screenplay

**Style**

Structured, slightly more action-oriented.

**Risk posture**

This mode must not overpromise.
It gives the first move, not full closure.

---

### Mode 4 · Compact Routing Mode

**Purpose**  
Support short context, low-token, or embedded routing situations.

**Best for**

- short-window models
- batch routing
- embedded pipeline use
- lightweight agent layers
- low-cost deployment

**Behavior**

- outputs the shortest viable structure
- keeps a compressed why-primary-not-secondary line
- preserves fit level
- preserves confidence
- preserves evidence sufficiency
- keeps repair direction to 1 or 2 items at most

**Style**

Short, hard, token-conscious.

**Risk posture**

Compact mode is allowed to compress, but not to erase structural essentials.

---

## 9. Runtime Mode Matrix v1 📊

| Mode | Core purpose | Exemplar use | Explanation depth | Repair strength | Best use case |
|------|--------------|--------------|-------------------|-----------------|---------------|
| Strict Routing | stable classification | low | medium | low | real routing and triage |
| Teaching | teaching cuts | medium | high | low to medium | onboarding and teaching |
| Repair-First Preview | route then first repair move | medium to high | medium | medium | demos and engineering helpers |
| Compact Routing | low-token fast routing | very low | low | very low | short-window and batch use |

This matrix is frozen because it provides a clean first operational grammar for deployment.

---

## 10. Minimum Output Schema 🧩

The adapter must preserve different minimum requirements by mode.

### 10.1 Strict Routing minimum output

Must include:

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

### 10.2 Teaching Mode minimum output

Must include everything in Strict Mode, plus:

- boundary_rule_explanation
- misroute_risk_note

### 10.3 Repair-First Preview minimum output

Must include everything in Strict Mode, plus:

- clearer first repair move note
- misrepair risk note

### 10.4 Compact Routing minimum output

Must include:

- primary_family
- secondary_family
- why_primary_not_secondary
- broken_invariant
- best_current_fit
- fit_level
- fix_surface_direction
- confidence
- evidence_sufficiency

Compact mode may omit ambiguity and no-fit explanation only when both are false.
If ambiguity or no-fit is true, the reason must still be stated.

---

## 11. Confidence and Evidence Discipline 🔒

The adapter must obey two permanent disciplines.

### 11.1 Confidence discipline

The adapter must not use high confidence merely because a case sounds familiar, famous, or rhetorically strong.

Confidence must track actual structural evidence.

### 11.2 Evidence sufficiency discipline

If the input evidence is weak, sparse, or highly compressed, the adapter must say so.

Weak evidence should not be hidden behind fluent structural language.

These two disciplines matter because routing grammar collapses if decisiveness becomes disconnected from evidence.

---

## 12. Adapter Failure Discipline v1 🛡️

The adapter must obey the following failure discipline.

1. route first, then repair
2. primary must correspond to the broken invariant
3. secondary must reflect real boundary pressure
4. ambiguity must not be opened merely because a case is difficult
5. no-fit must not be opened merely because a model is lazy
6. weak evidence must not produce high confidence
7. overlays must not silently become primary families
8. exemplars may support, but not override, structural rules
9. repair output must remain first-move level, not full-script theater
10. patches must be versioned, not silently rewritten

These ten rules are the safety rails of the adapter.

---

## 13. Relationship to Atlas Final Freeze v1 🔗

This adapter is not the atlas core.

It depends on the atlas core.

Use [Atlas Final Freeze v1](./atlas-final-freeze-v1.md) to determine:

- family structure
- routing grammar
- canonical node logic
- subtree structure
- relation logic

Use this adapter to make that structure operational for AI systems.

If the atlas changes through patch logic, the adapter must follow the atlas.
The adapter must never quietly redefine the atlas.

---

## 14. Relationship to Canonical Casebook v1 📘

This adapter also depends on the casebook.

Use [Canonical Casebook v1](./canonical-casebook-v1.md) to supply:

- family anchor exemplars
- boundary teaching exemplars
- repair teaching exemplars

The casebook stabilizes the adapter by providing reusable teaching cases.
The adapter operationalizes the casebook by deciding when and how those cases should be injected.

The two are complementary, not interchangeable.

---

## 15. Relationship to the Repair Layer 🛠️

Atlas-to-AI Adapter v1 does not contain the full repair system.

What it does contain is the **first repair-facing interface**.

That means:

- it can point to the correct repair family
- it can preview the first move
- it can warn about misrepair risk
- it can preserve route-first discipline

What it does not yet do in complete form is provide a full deep repair architecture for every branch.

For deeper repair-facing work, this adapter should later connect to:

- [Fix Surface v1](./fix-surface-v1.md)
- [Node-to-Fix Layer v1](./node-to-fix-layer-v1.md)
- [Atlas-to-WFGY Bridge v1](./atlas-to-wfgy-bridge-v1.md)

---

## 16. Patch Interface v1 🔄

The adapter is frozen, but not closed.

### Small Patch

Use for:

- wording refinement
- confidence tuning
- fit guidance improvement
- fix-direction wording adjustments
- exemplar injection default improvements

### Medium Patch

Use for:

- subtree-aware routing upgrades
- new high-pressure mini-stacks
- runtime behavior tuning
- compact routing optimization
- selector logic expansion

### Large Patch

Only use if:

- the atlas family structure changes
- major family cuts collapse repeatedly
- exemplar logic becomes systemically unstable
- runtime mode architecture must be redesigned

### Current status

No large-patch pressure is currently justified.

---

## 17. What this adapter enables 🚀

Atlas-to-AI Adapter v1 now makes the following possible:

- AI-assisted family routing
- compact model-facing classification
- teaching-oriented routing sessions
- route-first repair preview
- structured troubleshooting prompts
- TXT pack construction
- adapter patch waves
- AI reuse without flattening the atlas core

This is the first point where the atlas can be treated not only as a concept map, but as an operational AI-facing layer.

---

## 18. Official Freeze Statement

The correct formal statement is:

> Atlas-to-AI Adapter v1 is complete as the first formal AI-facing routing and diagnosis layer of the atlas system.  
> The adapter contract, routing stack, casebook injection layer, runtime modes, patch interface, and adapter failure discipline are now stable enough for formal reuse.  
> Future adapter work should proceed in patch mode.

---

## 19. One-line version

**Atlas-to-AI Adapter v1 is the first frozen AI-facing routing and diagnosis layer for Problem Map 3.0 Troubleshooting Atlas.**

---

## 20. Closing note ✨

A map is powerful.

A teaching system is more powerful.

A routing layer that lets AI systems use that map under discipline is even more powerful.

That is what this adapter is for.

It does not replace the atlas.
It makes the atlas operational.
