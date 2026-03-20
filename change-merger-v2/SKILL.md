---
name: change-merger-v2
description: Merge and reconcile multi-source changes with quick/governed modes, minimal diff policy, and explicit risk/validation outputs.
---

# change-merger-v2

## Trigger
Use when user asks to merge patches/branches, resolve conflicts, or reconcile overlapping changes.

## Mode
- `quick`: low-risk, same subsystem, small scope.
- `governed`: cross-module, risky, or release-bound work.

## Workflow
1. Collect sources: branches, patch files, issue references, and target files.
2. Classify conflicts by type:
   - textual conflict
   - behavioral conflict
   - interface conflict
3. Apply `minimal diff` policy:
   - avoid unrelated refactor
   - keep existing style and structure
4. Build merge proposal:
   - selected strategy and rationale
   - risk and rollback notes
5. Validate:
   - run available tests/checks
   - list skipped checks with reason
6. Produce outputs:
   - merged patch summary
   - risk table
   - rollback plan

## Outputs
- `merge-summary.md`
- `merge-risks.md`
- optional `merge.patch`

