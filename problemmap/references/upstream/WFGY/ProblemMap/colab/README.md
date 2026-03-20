# WFGY Global Debug Card · Colab MVP

This folder contains the first runnable notebook demo for the **WFGY Global Debug Card**.

The goal of this MVP is not to fully automate every RAG repair.  
The goal is to prove that the Global Debug Card can move from:

- image-based diagnosis
- structured triage
- machine-readable debug packets
- a reproducible first-pass repair loop

## What this Colab MVP is for

The notebook in this folder is designed to run one failing case built from:

- `Q` = user question
- `E` = retrieved evidence
- `P` = final prompt sent to the model
- `A` = model output

It will then:

1. run a first-pass diagnosis
2. emit a debug packet
3. apply one constrained repair action
4. run one verification pass
5. show a simple before/after result

This makes the notebook useful for:

- reproducible triage
- protocol validation
- small repair experiments
- future agent integration

## Wave 0 scope

The first public MVP is intentionally narrow.

Wave 0 focuses on the modes that are most suitable for constrained repair loops:

- **No.1** retrieval wrong or off-topic
- **No.5** semantic vs embedding mismatch
- **No.8** missing evidence visibility
- **No.2** interpretation collapse

These are the strongest first targets because they can often improve through:

- retrieval parameter changes
- query rewrite
- evidence visibility upgrades
- constrained prompt repair

## Minimum completion standard

The Colab MVP is considered complete when it can:

1. ingest one `(Q, E, P, A)` case
2. emit one machine-readable debug packet
3. apply one constrained repair action
4. return one verification result

That is the minimum public Wave 0 bar.

## Planned files

This folder will contain:

- `wfgy_global_debug_card_colab_mvp.ipynb`

Related files in nearby folders:

- `ProblemMap/specs/wfgy_problem_catalog_v1.json`
- `ProblemMap/specs/wfgy_debug_packet_v1.json`
- `ProblemMap/examples/cases/retrieval_offtopic_case_v1.json`
- `ProblemMap/examples/packets/retrieval_offtopic_before_v1.json`
- `ProblemMap/examples/packets/retrieval_offtopic_after_v1.json`

## Current status

Work in progress.

This folder is being prepared as the first public runnable demo layer for the Global Debug Card.  
The notebook, example case, and packet specs will be added step by step.

## Main entry point

If you are looking for the image-first protocol page, start here:

[WFGY 3.0 · RAG 16 Problem Map · Global Debug Card](https://github.com/onestardao/WFGY/blob/main/ProblemMap/wfgy-rag-16-problem-map-global-debug-card.md)

If you want the machine-readable protocol layer, the next step will be:

- `ProblemMap/specs/README.md`

If you want reproducible demo inputs and outputs, the next step will be:

- `ProblemMap/examples/README.md`
