# Atlas family core

## Source of truth
- Upstream repo: `WFGY/ProblemMap/Atlas/troubleshooting-atlas-router-v1.txt`

## Seven official families

### F1 — Grounding & Evidence Integrity
- broken invariant: `anchor_to_claim_coupling_broken`
- first failure: evidence, referent, target, world, or truth anchor mismatch
- first-fix pattern: re-grounding, evidence verification, target-reference audit
- common misrepair: rewriting tone or style before anchor restoration

### F2 — Reasoning & Progression Integrity
- broken invariant: `progression_continuity_broken`
- first failure: inferential path, decomposition path, recursion, or collapse-recovery path
- first-fix pattern: decomposition reset, interpretation checkpoint, recursive horizon fencing
- common misrepair: redesigning the carrier when the real failure is progression

### F3 — State & Continuity Integrity
- broken invariant: `state_continuity_broken`
- first failure: memory, role, ownership, continuity thread, or multi-agent interaction thread
- first-fix pattern: continuity restoration, role fencing, provenance tracing, interaction stabilization
- common misrepair: adding more instructions before restoring continuity infrastructure

### F4 — Execution & Contract Integrity
- broken invariant: `execution_skeleton_closure_broken`
- first failure: execution skeleton, ordering, readiness, bridge, liveness, closure path, or rule-to-action contract
- first-fix pattern: readiness audit, ordering validation, bridge check, closure-path trace
- common misrepair: improving reasoning before fixing the runtime skeleton

### F5 — Observability & Diagnosability Integrity
- broken invariant: `failure_path_visibility_broken`
- first failure: missing traceability, auditability, coherence visibility, or warning visibility
- first-fix pattern: observability insertion, trace exposure, audit-route uplift
- common misrepair: launching higher-order intervention before exposing the failure path

### F6 — Boundary & Safety Integrity
- broken invariant: `boundary_integrity_broken`
- first failure: drift, erosion, fragmentation, capture, overshoot, or unstable boundary crossing
- first-fix pattern: alignment guard, control-path audit, damping and stabilization
- common misrepair: improving observability only while the boundary itself is already drifting

### F7 — Representation & Localization Integrity
- broken invariant: `representation_container_fidelity_broken`
- first failure: carrier distortion, descriptor inadequacy, local anchor failure, or structural shell failure
- first-fix pattern: descriptor audit, structural preservation, local anchor repair
- common misrepair: repairing reasoning or grounding while the carrier remains untrustworthy

## Boundary pressure highlights
- `F1` vs `F7`: anchor mismatch vs carrier failure
- `F5` vs `F6`: observability deficit vs true boundary drift
- `F3` vs `F4`: continuity loss vs execution skeleton failure
- `F2` vs `F7`: usable carrier with broken reasoning vs broken carrier before reasoning
