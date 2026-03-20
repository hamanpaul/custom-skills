---
name: problemmap
description: Diagnose failing AI or agent sessions with ProblemMap PM1 + Atlas route-first routing, GitHub-backed reference fallback, GlobalFixMap handoff, and evolve-ready experience artifacts.
used_with:
  - evolve
related:
  - codex-project-insights
  - codex-lesson
---

# problemmap

## Trigger
Use when the user asks for or clearly needs:
- ProblemMap
- route-first diagnosis
- session postmortem
- failing AI or agent workflow triage
- broken invariant analysis
- failure family classification
- evolve-ready experience extraction from a failed session

## Goal
Turn a failing case into a structured dual-lens diagnosis:
- `pm1_candidates`: stable PM1 numbers
- `atlas`: route-first diagnosis fields
- `global_fix_route`: optional downstream handoff
- `experience_artifact`: optional evolve-ready output when confidence is high enough

## Default Mode
- default mode: `strict`
- reference loading order: `local curated -> existing upstream clone -> local dev seed if configured -> clone/update upstream -> fail loudly`
- upstream source of truth: `https://github.com/onestardao/WFGY` under `ProblemMap/`
- downstream repair layer: `GlobalFixMap`, but only after route stability is established

## Expected Inputs
Preferred inputs are:
- a session `.jsonl` file
- a failing command or tool output
- an expected vs actual summary
- a structured failure note from the user or operator

If the input is raw session history, extract a failure-bearing case first with `scripts/extract_failure_case.py`.

## Workflow
1. Build or load a structured failure-bearing case.
2. Read the local curated references needed for the current mode.
3. If required references are missing, run `scripts/ensure_upstream_problemmap.py` and read the needed upstream files.
4. Diagnose with route-first discipline using PM1 + Atlas.
5. Only after the route is stable, hand off to `GlobalFixMap` for downstream fix routing.
6. If the diagnosis passes the writeback gate, emit an experience artifact for `evolve` with `scripts/emit_problemmap_event.py`.

## Evolve routing policy
- Route `turn_aborted` to ProblemMap before writing generic AGENTS rules, so interruption events become case-level diagnoses instead of abstract advice.
- Route `context_compacted` to ProblemMap whenever continuity loss is plausible, and distinguish F3 continuity loss from F4 execution closure failure.
- Capture one case per concrete anchor event; do not collapse multiple interruptions or compactions into one decorative session summary.
- Only emit `experience_artifact` when `confidence >= medium` and `evidence_sufficiency != weak`.
- Prefer `problemmap-atlas-f*` event types over generic topic labels so downstream evolve routing stays family-first.

## Packaged Helpers
- `scripts/ensure_upstream_problemmap.py`
- `scripts/extract_failure_case.py`
- `scripts/diagnose_session.py`
- `scripts/emit_problemmap_event.py`

## Command examples
```bash
python3 ~/.agents/skills/custom/problemmap/scripts/extract_failure_case.py /path/to/session.jsonl --output /tmp/problemmap-case.json
python3 ~/.agents/skills/custom/problemmap/scripts/diagnose_session.py /tmp/problemmap-case.json --ensure-upstream --output /tmp/problemmap-diagnosis.json
python3 ~/.agents/skills/custom/problemmap/scripts/emit_problemmap_event.py /tmp/problemmap-diagnosis.json --output /tmp/problemmap-event.json
```

## Output Contract
Always aim to return a JSON-like structure with these fields:

```json
{
  "diagnostic_mode": "strict",
  "pm1_candidates": [
    {
      "number": 7,
      "label": "memory breaks across sessions",
      "confidence": "medium"
    }
  ],
  "atlas": {
    "primary_family": "...",
    "secondary_family": "...",
    "why_primary_not_secondary": "...",
    "broken_invariant": "...",
    "best_current_fit": "family-level | node-level | unresolved_subtype | no-fit",
    "fit_level": "...",
    "fix_surface_direction": "...",
    "misrepair_risk": "...",
    "confidence": "high | medium | low",
    "evidence_sufficiency": "sufficient | partial | weak"
  },
  "global_fix_route": {
    "family": "optional",
    "page": "optional",
    "minimal_fix": "optional"
  }
}
```

## Which references to read
- `references/pm1-taxonomy.md`
  - Read when you need the stable PM1 numbers or symptom-to-number mapping.
- `references/atlas-adapter-core.md`
  - Read for the minimum route-first schema and adapter contract.
- `references/atlas-runtime-modes.md`
  - Read when selecting `strict`, `teaching`, `repair_preview`, or `compact`.
- `references/atlas-family-core.md`
  - Read when you need the seven official Atlas families, broken invariants, or first-fix patterns.
- `references/atlas-failure-discipline.md`
  - Read before producing repair-facing guidance or when confidence is weak.
- `references/canonical-casebook.md`
  - Read only when boundary examples or teaching support are needed.
- `references/router-v1.txt`
  - Read for the compact operational contract.
- `references/global-fix-routing.md`
  - Read only after the route is stable and a downstream fix family is needed.
- `references/upstream-source.json`
  - Use for source resolution metadata, not for human reasoning.

## Scripts
- `scripts/ensure_upstream_problemmap.py`
  - Ensure the upstream ProblemMap corpus exists locally as a fallback source.
- `scripts/extract_failure_case.py`
  - Reduce raw session material into a failure-bearing case JSON.
- `scripts/diagnose_session.py`
  - Orchestrate reference loading and emit a first structured diagnosis.
- `scripts/emit_problemmap_event.py`
  - Convert a stable diagnosis into an evolve-ready experience artifact.

## Guardrails
- Route first, then repair.
- Never invent new PM1 numbers.
- Do not hide `why_primary_not_secondary`.
- Do not overstate confidence when evidence is weak.
- Do not let compact mode drop required fields.
- Do not treat `no-fit` as a lazy shortcut.
- Use `GlobalFixMap` as a downstream router, not as the primary diagnostic ontology.
- Treat the current `/home/paul_chen/prj_pri/problemmap/WFGY` clone as a development seed when present, but keep GitHub as the canonical upstream source.

## 自主維護知識（agent-managed）
<!-- self-evolve-managed-knowledge:start -->
<!-- self-evolve-managed-knowledge:end -->
