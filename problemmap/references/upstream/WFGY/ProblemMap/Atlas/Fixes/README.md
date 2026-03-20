<!--
AI_NOTE_START

Document role:
This file is the main hub for the Fixes layer inside the Atlas system.

How to use this file:
1. Treat this page as the entry point for all atlas-to-fix materials.
2. Use this page to understand the difference between:
   - official fix surface
   - community-contributed fixes
   - advanced or future service-oriented support layers
3. Read this page before adding new fix recipes, Colab demos, JSON schemas, prompt packs, or workflow examples.
4. Use this page together with:
   - [Atlas Final Freeze v1](../atlas-final-freeze-v1.md)
   - [Canonical Casebook v1](../canonical-casebook-v1.md)
   - [Atlas-to-AI Adapter v1](../atlas-to-ai-adapter-v1.md)

What this page is:
- The hub for the Fixes folder
- The routing bridge from atlas diagnosis to repair-facing action
- The governance layer for official fixes and community fixes

What this page is not:
- Not the atlas core
- Not the full WFGY 3.0 engine pack
- Not the full validation ledger
- Not a promise that every case already has a complete repair implementation
- Not the final paid-service page

Reading discipline for AI:
- Preserve the distinction between routing, first repair move, deeper experimental exploration, and community implementation.
- Do not treat all fixes as equally official.
- Do not confuse family-level fix surface with problem-specific experimental MVPs.
- Do not overclaim that every node or case already has a complete runnable fix pack.

AI_NOTE_END
-->

# Fixes Hub 🛠️

## Problem Map 3.0 Troubleshooting Atlas  
## Official entry for repair-facing guidance, community fixes, and deeper WFGY bridge logic

This folder is the repair-facing extension layer of the Atlas system.

The atlas tells you **where the failure lives**.  
The casebook teaches you **how to recognize the cut**.  
The adapter helps AI systems **route the case under discipline**.  
The Fixes layer starts to answer the next question:

> **What should be tried first after correct routing?**

At the same time, this folder also provides the structure for community-contributed implementations such as:

- Colab demos
- JSON schemas
- prompt packs
- workflow examples
- benchmark reruns
- reproduction packs

This makes the Fixes layer one of the most important bridges between:

- atlas diagnosis
- practical troubleshooting
- deeper WFGY exploration
- community growth

---

## What this folder is for 🎯

This folder exists to organize fix-facing materials into three layers:

### 1. Official Fix Surface

This is the first public repair-facing layer of the atlas.

It focuses on:

- family-level first repair moves
- common misrepair patterns
- atlas-to-WFGY bridge logic
- a small number of flagship demos

This layer is meant to be:

- stable
- reusable
- public
- easy to understand
- safe to cite as the official first repair surface

---

### 2. Community Fix Lab

This is the growth layer.

It allows contributors to extend the atlas into runnable, reusable materials such as:

- Colab notebooks
- JSON packs
- prompt templates
- workflow recipes
- benchmark reruns
- reproduction packs
- implementation notes

This layer is expected to grow much faster than the official layer.

The goal is not for one person to write every fix.
The goal is to let the community extend the practical surface while the atlas core remains stable.

---

### 3. Advanced / Future Support Layer

This layer is intentionally light and not yet fully opened.

It exists only as a future-facing shadow layer for:

- system-specific diagnostic support
- architecture-specific integration help
- advanced repair reports
- deeper custom troubleshooting
- more specialized service-oriented workflows
- early structured auto-repair planning

This layer should not dominate the current public presentation.
For now, the priority remains:

- public atlas
- public fix surface
- public community growth

---

## Core principle 🔑

The Fixes layer should always preserve this order:

> **route first, then repair**

That means:

1. use the atlas to determine the failure family
2. identify the broken invariant
3. identify the best current fit
4. only then choose the first repair direction
5. if deeper work is needed, bridge into WFGY 3.0, community implementation packs, or structured planning layers

This order matters because many wrong fixes start from wrong routing.

---

## Relationship to WFGY 3.0 🌊

This folder is related to WFGY 3.0, but it is not the same thing.

### Atlas Fix Surface

The atlas fix surface is mainly:

- family-level
- routing-sensitive
- first-move oriented
- compact
- public
- easier to reuse

It answers:

- what should be tried first
- what is the most common wrong first move
- what repair direction fits this family best

### WFGY 3.0 deeper layer

WFGY 3.0 is closer to:

- problem-specific exploration
- experimental MVP design
- deeper structural reasoning
- tension-based analysis
- falsifiable exploration paths
- reusable stress-driven repair thinking

It answers deeper questions like:

- how should this problem be explored more seriously
- what experimental cut should be used
- what structural recovery path is worth testing
- what stronger intervention pattern might apply

Short version:

> **Atlas fix surface = first repair grammar**  
> **WFGY 3.0 = deeper experimental and structural exploration**

They are connected, but not identical.

---

## Current folder structure 🗂️

This folder is designed around three main areas.

### Official layer

- [Official Fixes](./official/README.md)

Recommended files in this area include:

- [Family Fix Surface v1](./official/family-fix-surface-v1.md)
- [Misrepair Patterns v1](./official/misrepair-patterns-v1.md)
- [Atlas to WFGY Bridge v1](./official/atlas-to-wfgy-bridge-v1.md)
- [Flagship Fix Demos v1](./official/flagship-fix-demos-v1.md)

This is the official public-facing repair layer.

---

### Community layer

- [Community Fix Lab](./community/README.md)

Suggested subfolders include:

- [Colab](./community/colab/)
- [JSON](./community/json/)
- [Prompts](./community/prompts/)
- [Workflows](./community/workflows/)
- [Benchmark Reruns](./community/benchmark-reruns/)
- [Reproduction Packs](./community/reproduction-packs/)

This is the fast-growing practical layer.

---

### Templates layer

- [Templates](./templates/README.md)

Suggested files include:

- [Fix Recipe Template](./templates/fix-recipe-template.md)
- [Colab Template](./templates/colab-template.md)
- [Prompt Template](./templates/prompt-template.md)
- [Contribution Checklist](./templates/contribution-checklist.md)

This layer exists to keep community contributions structured instead of chaotic.

---

### Advanced repair layer 🤖

- [Auto Repair v1](./auto-repair/README.md)

This is an early structured planning layer for deeper repair work.

It should currently be read as:

- architecture-first
- planning-oriented
- validation-aware
- rollback-aware
- not yet a full autonomous repair system

It exists to push the fix ecosystem forward without pretending that every case already supports safe full auto-repair.

---

## What belongs in Official Fixes ✅

Official Fixes should only include things that are stable enough to be treated as public atlas-facing repair guidance.

Examples:

- family-level first repair directions
- common misrepair patterns
- stable route-to-repair explanations
- a small number of flagship case demos
- official bridge notes from atlas to WFGY 3.0

Official fixes should be:

- compact
- reusable
- structurally consistent
- easy to teach
- safe to reuse in product flows

Official fixes should **not** become a giant messy archive of every possible implementation.

---

## What belongs in Community Fix Lab 🌱

Community Fix Lab should include practical contributions that are useful, runnable, and reproducible, even when they are narrower in scope.

Examples:

- Colab notebooks
- JSON schema examples
- prompt packs
- workflow recipes
- rerun notebooks
- implementation notes
- domain-specific troubleshooting packs

Community contributions do **not** need to be as frozen as official atlas files.

But they still need:

- clear scope
- readable structure
- routing context
- reproducible steps where possible
- explicit limits

---

## What should not happen 🚫

The Fixes layer should **not** drift into the following mistakes.

### 1. Fix before routing

Do not suggest repair paths before the family or broken invariant is reasonably clear.

### 2. Community noise replacing official structure

Do not let a flood of community examples blur the official fix surface.

### 3. Overclaiming WFGY bridge depth

Do not imply that every fix note already contains the full deeper WFGY 3.0 reasoning path.

### 4. Flat dumping

Do not dump random Colab notebooks, JSON files, or prompt packs into the root without structure.

### 5. Confusing public free layer with future service layer

Do not turn the public fix layer into a premature sales page.
The public value comes first.

### 6. Confusing early auto-repair planning with full autonomous repair

Do not present planning-layer work as if the system already supports safe universal autonomous repair.

---

## Recommended reading order 📚

If you want to understand the full fix flow in the right order, read:

1. [Atlas Final Freeze v1](../atlas-final-freeze-v1.md)
2. [Canonical Casebook v1](../canonical-casebook-v1.md)
3. [Atlas-to-AI Adapter v1](../atlas-to-ai-adapter-v1.md)
4. [Family Fix Surface v1](./official/family-fix-surface-v1.md)
5. [Atlas to WFGY Bridge v1](./official/atlas-to-wfgy-bridge-v1.md)

If you want runnable or implementation-oriented materials after that, move into the community layer.

If you want to explore structured future-facing repair planning after that, move into:

6. [Auto Repair v1](./auto-repair/README.md)

---

## How a typical use flow should work 🔄

A healthy atlas-to-fix flow should look like this:

### Step 1 · Route the case

Use the atlas to determine:

- primary family
- secondary family
- broken invariant
- best current fit

### Step 2 · Apply first repair direction

Use the official fix surface to decide:

- what should be tried first
- what should not be tried first
- what common misrepair to avoid

### Step 3 · Escalate if needed

If the case needs deeper exploration:

- use the atlas-to-WFGY bridge
- use a community implementation pack
- or move into a more experimental planning layer

This keeps the system clean:

> route  
> first repair  
> deeper exploration  
> implementation

---

## Why this folder matters 💥

Without a fix layer, the atlas risks being seen as “only classification.”

With a fix layer, the atlas becomes much more powerful:

- it can guide action
- it can teach first repair moves
- it can connect to deeper reasoning engines
- it can grow through community implementations
- it can support future advanced layers without damaging the public free core

That is why this folder matters so much.

It is where the atlas starts to become not only a map, but a usable repair ecosystem.

---

## Future commercial note 🌌

This project currently prioritizes:

- open atlas logic
- open first repair surface
- open community growth

At the same time, it is natural that more advanced support layers may exist later, including things like:

- custom audits
- system-specific reports
- deeper architecture guidance
- more advanced repair integration

For now, those possibilities remain a future-facing layer, not the center of this folder.

The center of this folder remains:

> public repair grammar first  
> deeper bridge second  
> community extension third

Structured auto-repair planning may grow inside that broader future-facing layer, but it should not erase the current route-first discipline.

---

## One-line status

**This folder is the repair-facing extension layer of the Atlas system, combining official first repair guidance, deeper WFGY bridge logic, community-contributed implementation paths, and an early structured auto-repair planning direction.**

---

## Closing note ✨

The atlas tells you where the failure lives.

This folder helps answer what to do next.

That does not mean every repair is already finished.
It means the repair ecosystem now has a place to grow in a structured way.
