# Atlas adapter core

## Source of truth
- Upstream repo: `WFGY/ProblemMap/Atlas/atlas-to-ai-adapter-v1.md`
- Companion: `WFGY/ProblemMap/Atlas/troubleshooting-atlas-router-v1.txt`

## Purpose
This is the core AI-facing routing contract for ProblemMap 3.0 Atlas.

## Minimum input shapes
- issue report
- failing output
- workflow collapse description
- structured failure note

## Minimum output fields
- `primary_family`
- `secondary_family`
- `why_primary_not_secondary`
- `broken_invariant`
- `best_current_fit`
- `confidence`
- `evidence_sufficiency`

## Core route-first order
1. classify the primary family
2. explain the primary cut vs the secondary cut
3. state the broken invariant
4. state the best current fit
5. only then preview the first repair direction

## Skill-specific note
This skill adds PM1 candidates on top of the Atlas contract. PM1 does not replace Atlas, and Atlas does not replace PM1.
