---
name: pwhm-core-org
description: prplOS pWHM core knowledge for HLAPI to LLAPI tracing, FTA override flow, FSM dependencies, and integration/debug workflows. Use when questions involve pWHM architecture, trace mapping, FSM behavior, or pWHM integration in prpl projects. Exclude vendor-specific implementation details.
---

# pWHM Core (Org)

## Scope

Use for pWHM core architecture, trace methodology, FSM flow, and non-vendor-specific integration logic.

## Workflow

1. Identify if the request is pWHM core (trace, FSM, FTA flow, HLAPI/LLAPI mapping).
2. Load references as needed:
   - `references/pwhm-core-summary.md` for startup/FTA/FSM/trace principles.
   - `references/pwhm-trace-guides.md` for trace formats, mapping files, and failed-case analysis.
   - `references/pwhm-integration-playbook.md` for HLAPI->LLAPI tracing contract, FSM checks, and delivery checklist.
3. Provide minimal-change guidance; defer vendor-specific parts to vendor-core skills.

## Outputs

- Trace plan with expected HLAPI/FTA/LLAPI layers and call points.
- FSM dependency explanation and validation steps.
- Mapping guidance using existing tables and trace lists.
