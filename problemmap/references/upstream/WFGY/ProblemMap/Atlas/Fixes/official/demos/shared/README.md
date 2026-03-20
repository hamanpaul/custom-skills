<!--
AI_NOTE_START

Document role:
This file is the shared helper and discipline index for the official flagship demo pack.

How to use this file:
1. Read this file before creating or editing any shared helper used by the official demo notebooks.
2. Treat this folder as the reusable support layer for the four flagship demos.
3. Use this file to understand:
   - what belongs in shared
   - what does not belong in shared
   - how replay-first notebooks should share logic
   - why the first MVP keeps helper code small, explicit, and auditable
4. Read together with:
   - [Flagship Runnable Demo Pack](../README.md)
   - [Family Fix Surface v1](../../family-fix-surface-v1.md)
   - [Atlas to WFGY Bridge v1](../../atlas-to-wfgy-bridge-v1.md)

What this file is:
- The main index for shared demo helpers
- The discipline page for reusable demo support assets
- The rulebook for keeping official demo code small and clear

What this file is not:
- Not the atlas core
- Not the full demo pack
- Not a generic utilities dump
- Not a place for heavy framework code
- Not a replacement for per-demo README explanation

Reading discipline for AI:
- Preserve the distinction between shared support logic and demo-specific teaching logic.
- Keep shared helpers minimal and reusable.
- Do not move core case explanation into shared code.
- Do not turn this folder into a hidden mini-framework.

AI_NOTE_END
-->

# Shared Demo Helpers 🧰

## Problem Map 3.0 Troubleshooting Atlas
## Official reusable support layer for flagship demos

This folder contains the shared support assets used by the official flagship demo pack.

Its purpose is simple:

> keep each demo readable  
> keep repeated support logic reusable  
> keep the notebooks small enough to audit

This folder exists so that the demo pack can stay clean, teachable, and maintainable.

It should never become a dumping ground.

It should also be read as part of the **official demo surface**, not as a separate mini-project.

---

## What this folder is for

The official flagship demos are meant to be:

- small
- sharp
- readable
- replay-friendly
- optionally runnable where it adds real proof value
- easy to extend later

If every notebook repeats the same support logic, the code becomes noisy very quickly.

So this shared folder exists to hold only the support pieces that are:

- small
- generic enough to reuse
- stable across multiple official demos
- not part of the main teaching story

In short:

> demo-specific teaching stays inside each demo folder  
> reusable support logic lives here

---

## Current MVP reality

The current flagship demo pack is **replay-first by design**.

At the moment:

- **Demo 1** includes a live notebook because live comparison adds direct proof value
- **Demo 2** is replay-first, with the cleaner v2 replay notebook serving as the recommended entry point
- **Demo 3** is replay-first, with the cleaner v2 replay notebook serving as the recommended entry point
- **Demo 4** is replay-first, with the cleaner v2 replay notebook serving as the recommended entry point

This matters because shared helpers should reflect the real teaching center of the pack.

### What this means in practice

The first version of `shared/` should primarily support:

- replay fixture loading
- compact route display
- before / after formatting
- consistent notebook labels
- small, explicit mode handling

It should **not** assume that all demos are evolving toward a heavy live runtime layer.

### Honest design rule

Use shared helpers to support the strongest current teaching mode.

Right now, that means:

> replay-first support is the default  
> live support remains small and optional

---

## Current files in this folder 📂

At the current MVP stage, this folder already has a small real support layer.

### `README.md`

This file.

Purpose:

- define folder role
- define discipline
- define scope
- define boundaries

### `demo_utils.py`

Current purpose:

- lightweight reusable helper functions
- JSON loading
- compact output formatting
- simple route rendering
- small replay / live mode helpers

This file is intended to be imported by notebooks.  
It is a support module, not a standalone demo.

### `display_helpers.py`

Current purpose:

- before / after result formatting
- compact comparison rendering
- display cleanup for notebook readability
- small output presentation helpers

This file exists to improve clarity, not to introduce a custom display framework.

### `routing_schema.md`

Current purpose:

- document the stable output fields used across demo notebooks
- explain what each output field means
- keep naming consistent across demos

This file helps the official demos stay aligned without flattening away their teaching differences.

---

## How notebooks should use this folder

The shared layer is meant to be used in a small and explicit way.

Typical use looks like this:

1. a notebook stays inside its own demo folder
2. the notebook imports a small helper from `shared/`
3. the notebook still loads its own local JSON fixtures
4. the teaching logic remains inside the notebook and that demo’s README

That means shared code should support the notebook, not replace it.

In short:

> shared provides the small tools  
> each demo still tells its own story

---

## What belongs in `shared/`

The following types of assets belong here.

### 1. Lightweight display helpers

These are small helpers that make before / after results easier to read.

Examples:

- route summary rendering
- before / after comparison formatting
- compact fixture preview formatting
- replay output pretty-print helpers

These should help the user see the demo faster.
They should not become a custom UI framework.

---

### 2. Minimal schema loaders

These are tiny helpers for loading and validating the common demo JSON files.

Examples:

- reading `input_case.json`
- reading `replay_outputs.json`
- reading `expected_output.json`
- checking required top-level keys

These should remain minimal and explicit.

---

### 3. Small mode helpers

These are small helpers for handling the notebook execution mode safely and clearly.

Examples:

- replay mode defaults
- optional live mode switch
- minimal API key intake helper for the one live notebook
- small prompt loading helper if clearly reused

These helpers should only support the demos.
They should not become a full execution framework.

---

### 4. Common notebook constants

These include small shared constants that make the notebooks more consistent.

Examples:

- file naming conventions
- common field names
- output labels
- route display labels
- replay mode defaults

These should reduce duplication, not add abstraction for its own sake.

---

### 5. Tiny documentation references

If needed, this folder may hold small reference notes that are clearly reusable across the official demos.

Examples:

- routing output field list
- demo JSON field description
- minimal notebook expectations

These should remain short and clearly tied to the official demo pack.

---

## What does **not** belong in `shared/` ❌

This matters just as much.

The following should **not** be placed here.

### 1. Full case explanations

Each demo’s teaching story belongs in that demo’s own `README.md`.

Do not move:

- case meaning
- why-primary-not-secondary explanation
- misrepair explanation
- family teaching notes

into shared helpers.

That would make the demos harder to read and easier to blur together.

---

### 2. Large framework code

Do not turn this folder into a mini product runtime.

Avoid putting in:

- large orchestration layers
- giant helper classes
- hidden workflow engines
- over-abstracted adapter logic
- generic AI platform wrappers

The flagship demo pack is meant to stay inspectable.

---

### 3. Secret management logic beyond minimal safe input

This folder may contain a tiny helper for runtime API key input.

It should **not** contain:

- stored keys
- repo secrets
- hidden environment hacks
- service-specific credential systems
- anything that makes the demos harder to audit

---

### 4. Per-demo logic

If a helper is really only used by one demo, it probably belongs in that demo folder, not here.

The shared folder is for genuinely reusable support, not for lazily centralizing unrelated logic.

---

### 5. Community contributions

This folder is part of the **official flagship demo pack**.

Community utilities, experiments, or alternate demo helpers should live under the community side, not here.

See [Community Fix Lab](../../../community/README.md) for that path.

---

## Design principles for shared helpers 🧭

This folder should follow five design principles.

### Principle 1 · Small over clever

Prefer short, obvious helpers over smart abstractions.

A reader should be able to understand a helper in one glance.

### Principle 2 · Reusable over magical

If a helper only works because of hidden assumptions, it is probably too magical for this folder.

Shared helpers should be boring in a good way.

### Principle 3 · Teaching-first

The demos are teaching assets, not just runnable code.

Shared helpers should support teaching clarity, not hide the logic that users came to learn.

### Principle 4 · Replay-first compatibility

Replay mode is the public teaching baseline.

Any shared helper should make replay mode easier, not accidentally make live mode the default center.

### Principle 5 · Auditability matters

A contributor or reviewer should be able to inspect this folder quickly and understand what each file does.

If the folder starts to feel like a black box, it has already gone too far.

---

## Relationship to replay mode and live mode

This folder supports both modes, but the balance matters.

### Replay mode

Replay mode is the most important public teaching mode.

Shared helpers should support replay mode through:

- clean JSON loading
- structured formatting
- readable comparison display
- compact route summaries

### Live mode

Live mode is currently secondary in the official MVP pack.

Shared helpers may support live mode through:

- minimal API key intake
- small request helpers
- prompt loading
- response normalization

But live mode must never force the whole folder to become heavy.

### Golden rule

> replay mode should remain first-class  
> live mode should remain optional

That rule should stay visible in every shared-helper decision.

---

## Suggested files in this folder 📂

The exact file list may evolve, but this is the recommended first set.

### `README.md`

This file.

Purpose:

- define folder role
- define discipline
- define scope
- define boundaries

---

### `demo_utils.py`

Recommended purpose:

- lightweight reusable helper functions
- file loading
- compact output formatting
- simple route rendering
- small replay / live mode switch helpers

This file should remain small.

---

### `routing_schema.md`

Recommended purpose:

- document the stable output fields used across demo notebooks
- explain what each output field means
- keep naming consistent across demos

This is especially useful now that the four flagship demos are being aligned more tightly.

---

### `display_helpers.py`

Recommended purpose:

- before / after result formatting
- route card formatting
- compact comparison helpers
- notebook display cleanup

This file should stay lightweight and readability-first.

---

### Optional tiny reference notes

Only add these if they clearly reduce duplication.

Examples:

- JSON field guide
- notebook field guide
- mode reference note

Do not create extra files just because the folder feels empty.

---

## Coding discipline for shared helpers 💻

If helper code is added here, it should follow these rules.

### 1. Keep functions short

Prefer small functions with explicit inputs and outputs.

### 2. Avoid hidden side effects

A helper should not silently modify environment state unless that behavior is obvious and necessary.

### 3. Keep imports minimal

Do not make the flagship demos depend on a long stack of packages unless absolutely necessary.

### 4. Keep names literal

Prefer names like:

- `load_input_case`
- `load_replay_outputs`
- `load_expected_output`
- `format_route_summary`
- `format_before_after`

Avoid vague names like:

- `engine`
- `manager`
- `controller`
- `runtime_core`

### 5. Keep notebook readers in mind

Someone reading a demo notebook should be able to understand what the helper does without opening ten other files.

---

## Review rules for this folder ✅

Anything added to `shared/` should pass these checks.

### Required review questions

1. Is this helper truly reused across multiple official demos?
2. Does this helper improve clarity, not just reduce duplication?
3. Does this helper preserve replay-first readability?
4. Is the file small enough to audit quickly?
5. Would moving this logic into a single demo folder actually be cleaner?

If the answer to the last question is yes, then the helper probably does not belong here.

---

## How this folder fits into the full repair system 🔗

This folder is not the repair system itself.

It is only a support layer for the flagship demo pack.

The larger system is:

1. the atlas routes the failure
2. the fix surface suggests the first repair move
3. the flagship demos make that shift visible
4. WFGY 3.0 supports deeper exploration if needed
5. the community grows long-tail runnable variations later

So this folder is only one small but useful piece of the picture.

It exists to make the demos cleaner, not to become the center of the architecture.

---

## Relationship to community growth 🌱

This folder supports the **official** demos.

That means it should stay conservative.

If the community later contributes:

- alternate notebook helpers
- different visualization utilities
- model-specific wrappers
- extra schema helpers

those should generally begin in the community area first.

Only helpers that become clearly useful for the official flagship demo pack should be promoted here.

This keeps the official layer stable and easy to review.

---

## What this folder proves

This folder may look small, but it proves something important:

> the demo pack is being designed as a real, reusable teaching system  
> not as four isolated notebooks thrown together in a rush

That matters for long-term growth.

It means:

- official demos can stay consistent
- future contributors can understand the structure
- later MVP code does not need to be rewritten from scratch

---

## What this folder does **not** prove

This folder does **not** prove that:

- the whole demo system is productionized
- every future demo should use the same helper structure
- the official demos need a large code layer
- community content should be merged into shared by default

This folder only proves that the first flagship demos are being built with clean reuse and review discipline.

That is enough.

---

## One-line version

**This folder contains the small, reusable support layer that keeps the official flagship demos readable, replay-first, and easy to audit.**

---

## Closing note ✨

A good demo pack should feel sharp, not messy.

This shared folder exists to support that goal.

If it stays small, clear, and disciplined, it will quietly make all four demos better.

If it grows into a hidden mini-framework, it will hurt the demos instead of helping them.

So the rule is simple:

> keep shared helpers useful  
> keep them small  
> keep the teaching story inside each demo
