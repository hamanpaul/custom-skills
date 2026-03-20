# WFGY Global Debug Card · Machine-Readable Specs

This folder contains the machine-readable protocol layer for the **WFGY Global Debug Card**.

The purpose of this layer is to make the same debugging logic usable by:

- agent runners
- CI workflows
- internal debugging tools
- replay and comparison pipelines
- future automation layers

This does not replace the image-first workflow.  
It gives the same protocol a stable, tool-friendly format.

## Why this folder exists

The Global Debug Card already works as a human-readable debugging layer.

A user can:

1. upload the card image
2. provide `(Q, E, P, A)`
3. ask a strong LLM to diagnose the failure
4. receive likely modes, fixes, and verification steps

That is the human entry point.

This folder defines the machine entry point.

It is designed to make the same workflow easier to:

- replay
- compare
- store
- validate
- integrate into software systems

## Planned spec files

This folder is expected to contain:

- `wfgy_problem_catalog_v1.json`
- `wfgy_debug_packet_v1.json`

## Spec roles

### 1) `wfgy_problem_catalog_v1.json`

This file is the machine-readable mode catalog.

Its role is to encode the problem vocabulary behind the Global Debug Card, including:

- mode IDs
- mode names
- lane / family grouping
- observable signals
- default repair directions
- verification hints

This file is not a full replacement for the narrative documentation.  
It is a compact protocol-facing index for tools.

### 2) `wfgy_debug_packet_v1.json`

This file is the machine-readable result format for one diagnosis run.

Its role is to store a structured debug result, including:

- input summary
- detected failure type
- likely modes
- selected repair actions
- verification plan
- before / after result structure

This file is the core handoff object between diagnosis and automation.

## Wave 0 scope

The first public spec wave is intentionally narrow.

Wave 0 focuses on the parts needed to support the first Colab MVP and one reproducible repair loop.

That means the first version will prioritize:

- **No.1** retrieval wrong or off-topic
- **No.5** semantic vs embedding mismatch
- **No.8** missing evidence visibility
- **No.2** interpretation collapse

The spec can expand later, but the first version should stay simple and stable.

## Relationship to other folders

- `ProblemMap/colab/README.md` explains the runnable notebook layer
- `ProblemMap/examples/README.md` will explain reproducible demo cases and before/after packet examples
- `ProblemMap/wfgy-rag-16-problem-map-global-debug-card.md` remains the main human-readable protocol page

## Current status

Work in progress.

This folder is being prepared as the first public machine-readable layer for the Global Debug Card.  
The first JSON files will be added step by step.

## Main entry point

If you are starting from the image workflow, begin here:

[WFGY 3.0 · RAG 16 Problem Map · Global Debug Card](https://github.com/onestardao/WFGY/blob/main/ProblemMap/wfgy-rag-16-problem-map-global-debug-card.md)

If you want the runnable notebook layer, go here:

[Colab MVP README](https://github.com/onestardao/WFGY/blob/main/ProblemMap/colab/README.md)
