<!--
AI_NOTE_START

Document role:
This file defines the stable routing and output field conventions used across the official flagship demo pack.

How to use this file:
1. Read this file before creating a new official demo notebook or editing an existing one.
2. Use this file to keep field names, route summaries, and replay outputs aligned across demos.
3. Treat this file as the shared schema guide for the official flagship demo pack.
4. Read together with:
   - [Flagship Runnable Demo Pack](../README.md)
   - [Shared Demo Helpers](./README.md)

What this file is:
- The schema guide for official demo JSON files
- The naming guide for common route fields
- The alignment layer for replay-first notebook outputs

What this file is not:
- Not a strict production API contract
- Not the atlas core ontology
- Not a replacement for per-demo README explanations
- Not a promise that every field will be identical across every future community demo

Reading discipline for AI:
- Preserve the difference between stable shared fields and demo-specific extensions.
- Do not over-normalize away the teaching purpose of each demo.
- Keep route fields consistent, but allow case-specific content where needed.

AI_NOTE_END
-->

# Routing Schema v1

## Problem Map 3.0 Troubleshooting Atlas
## Shared field conventions for official flagship demos

This document defines the stable routing and output field conventions used across the **official flagship demo pack**.

Its purpose is simple:

> keep the demo notebooks aligned  
> keep JSON fixtures readable  
> keep replay outputs comparable across demos

This is not meant to be a giant formal spec.
It is a practical schema guide for the first official MVP demo pack.

---

## 1. Scope

This schema applies to the official flagship demos under:

- `demo-f1-grounding-anchor`
- `demo-f5-observability-first`
- `demo-f4-execution-closure`
- `demo-f7-container-fidelity`

It focuses on the three common JSON files used across those demos:

- `input_case.json`
- `replay_outputs.json`
- `expected_output.json`

It also defines the shared route-summary fields that may be rendered in notebooks or README explanations.

---

## 2. Design rule

The official demos are **aligned**, but not artificially flattened.

That means:

- the same core route fields should stay stable
- the same file roles should stay stable
- replay outputs should look structurally familiar across demos

But also:

- each demo may include case-specific fields
- each demo may have its own teaching emphasis
- not every replay output must use identical secondary keys

In short:

> keep the shared spine stable  
> allow the teaching layer to stay local

---

## 3. Common file roles

### `input_case.json`

Purpose:

- define the case
- define the target route
- define the main teaching context
- provide the notebook with the minimum case bundle

### `replay_outputs.json`

Purpose:

- define the baseline state
- define the repaired or improved state
- define the before / after teaching contrast
- support replay-first inspection

### `expected_output.json`

Purpose:

- define the clean target structure
- define the expected routing result
- define the minimum success contract for the demo

---

## 4. Stable shared fields in `input_case.json`

The following fields are recommended as the stable shared layer.

### Required top-level fields

- `demo_id`
- `demo_version`
- `case_id`
- `title`
- `task_type`
- `family_target`
- `user_question`

### Required shared sub-object

#### `family_target`

Recommended stable fields:

- `primary_family`
- `secondary_family`
- `best_current_fit`
- `broken_invariant`

These four fields form the official shared route spine.

### Example shared structure

```json
{
  "demo_id": "demo_f5_observability_first",
  "demo_version": "v1",
  "case_id": "f5_observability_case_001",
  "title": "Workflow failure with too little visibility for safe diagnosis",
  "task_type": "workflow_debugging",
  "family_target": {
    "primary_family": "F5",
    "secondary_family": "F4",
    "best_current_fit": "F5_N01 Failure Path Opacity",
    "broken_invariant": "failure_path_visibility_broken"
  },
  "user_question": "Why is the workflow returning irrelevant answers, and what should be fixed first?"
}
````

---

## 5. Demo-specific fields in `input_case.json`

Beyond the shared layer, each demo may include its own case-specific fields.

Examples include:

### F1-style fields

* evidence chunks
* relevant chunk ids
* misleading chunk ids
* anchor context

### F5-style fields

* thin trace
* observability uplift
* retrieval trace
* candidate trace
* post-check trace

### F4-style fields

* workflow stages
* readiness conditions
* bridge state
* closure failure markers

### F7-style fields

* intended structure target
* weak container form
* schema constraints
* descriptor notes

These are valid additions as long as they do not replace the shared route spine.

---

## 6. Stable shared fields in `replay_outputs.json`

The exact wording may vary by demo, but the replay file should preserve a familiar before / after structure.

### Recommended minimum shared layer

At minimum, replay outputs should expose:

* a baseline state
* a repaired or improved state
* a short note on why the baseline is weak
* a short note on what changed

### Recommended field families

The current official demos may use labels such as:

* `baseline_diagnosis`
* `baseline_problem`
* `repaired_diagnosis`
* `before_state`
* `after_state`

or similarly clear equivalents.

### Shared meaning of those fields

#### `baseline_diagnosis`

What the baseline path produces or how the baseline is initially interpreted.

#### `baseline_problem`

Why the baseline state is weak, unsafe, insufficient, or wrongly routed.

#### `repaired_diagnosis`

What becomes visible or more correct after the first repair move.

#### `before_state`

A short label for the baseline condition.

#### `after_state`

A short label for the improved condition.

### Important rule

The exact key names may expand later,
but every official replay file should preserve this teaching structure:

> baseline
> weakness of baseline
> repaired or improved state
> visible shift

---

## 7. Stable shared fields in `expected_output.json`

This file should stay as small and clear as possible.

### Recommended minimum shared layer

* `primary_family`
* `secondary_family`
* `best_current_fit`
* `broken_invariant`
* `first_repair_move`

This is the minimum official success contract.

### Example

```json
{
  "primary_family": "F5",
  "secondary_family": "F4",
  "best_current_fit": "F5_N01 Failure Path Opacity",
  "broken_invariant": "failure_path_visibility_broken",
  "first_repair_move": "observability insertion"
}
```

---

## 8. Route summary fields

The following fields should be treated as the canonical route summary spine.

* `primary_family`
* `secondary_family`
* `best_current_fit`
* `broken_invariant`

These four fields should be easy to display in any notebook, README excerpt, or replay preview.

### Why these four matter

Together they answer the minimum routing questions:

1. what family is primary
2. what neighboring family is the main alternative
3. what node or fit is currently best
4. what invariant is actually broken

This is the smallest route summary that still feels like Atlas routing rather than vague commentary.

---

## 9. Before / after conventions

The official demos should preserve a visible before / after contrast.

### Recommended labels

Use plain labels such as:

* `Before`
* `After`

or case-specific variants like:

* `Baseline`
* `Repaired`
* `Opaque`
* `Diagnosable`

### Goal

The point is not visual decoration.
The point is to make this shift obvious:

> route changes first repair move
> first repair move changes visible state

That is the shared teaching spine across all four demos.

---

## 10. Mode conventions

The official demo pack currently uses two practical public modes.

### Replay mode

Replay mode is the default teaching mode.

Recommended shared label:

* `MODE = "replay"`

Replay mode should work without an API key.

### Live mode

Live mode is currently only relevant where live comparison adds real proof value.

Recommended shared label:

* `MODE = "live"`

In the current MVP pack:

* Demo 1 supports live mode
* Demo 2 is replay-only
* Demo 3 is replay-only
* Demo 4 is replay-only

### Important rule

Shared helpers and notebook conventions must not assume that all official demos are live-first.

The pack is **replay-first by design**.

---

## 11. Naming conventions

### Notebook naming

Recommended notebook naming pattern:

* `demo_01_f1_grounding_anchor_recovery_live.ipynb`
* `demo_02_f5_observability_first_replay.ipynb`
* `demo_03_f4_execution_closure_replay.ipynb`
* `demo_04_f7_container_fidelity_replay.ipynb`

This pattern is preferred because it makes visible:

* demo number
* family
* theme
* mode

### JSON naming

The shared JSON naming pattern should remain:

* `input_case.json`
* `replay_outputs.json`
* `expected_output.json`

Do not invent a new filename pattern for each demo.

---

## 12. What should remain stable across official demos

The following should remain stable unless a later patch explicitly changes them.

### Stable elements

* the three JSON filenames
* the route summary spine
* replay-first public teaching logic
* expected output minimum fields
* mode labels
* notebook naming style

### Flexible elements

* case-specific content fields
* baseline wording
* repaired wording
* local notes
* case-specific replay labels

This balance is important.

Too much variation makes the demo pack messy.
Too much forced sameness makes the demos less teachable.

---

## 13. What this schema is trying to prevent

This schema exists to prevent three kinds of drift.

### 1. Naming drift

Where each demo starts using different route field names for the same concept.

### 2. Replay drift

Where each demo starts showing before / after in a different structure, making comparison harder.

### 3. Mode drift

Where helpers or notebooks silently assume live mode is central, even though the official pack is replay-first.

---

## 14. Patch discipline for this schema

This schema is stable, but not frozen forever.

### Small patch

Use for:

* wording cleanup
* minor field note clarification
* stronger examples
* naming consistency improvements

### Medium patch

Use for:

* adding one clearly reusable shared field
* changing replay output conventions across the official demo pack
* introducing a new stable field family used in multiple demos

### Large patch

Only use if:

* the official demo pack changes its core mode strategy
* the shared route spine changes
* the three-file structure is replaced
* a broader official runtime layer is introduced

At the current stage, no large patch is justified.

---

## 15. One-line version

**This file defines the small shared routing and output conventions that keep the official flagship demos aligned, replay-first, and easy to inspect.**

---

## Closing note

A good demo pack should feel like one system, not four unrelated notebooks.

This schema exists to support that goal.

It should keep the official demos aligned enough to feel coherent, while still leaving each demo enough room to teach its own case cleanly.

