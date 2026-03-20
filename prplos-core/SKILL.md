---
name: prplos-core
description: prplOS and OpenWrt core integration for Ambiorix/TR-181/ubus/CLI, startup and registration flow, overlay/build system, and validation/debug on prpl projects. Use when questions are about prplOS platform architecture, data model registration, ubus-cli behavior, init ordering, or build/overlay mechanics. Exclude pWHM and vendor-specific implementation details.
---

# prplOS Core

## Scope

Use for prplOS platform architecture and integration tasks that are not vendor-specific and not pWHM-specific. Focus on Ambiorix/TR-181 runtime, ubus exposure, CLI usage, init order, and OpenWrt overlay/build flow.

## Workflow

1. Identify whether the question is platform-level (Ambiorix/TR-181/ubus/CLI/init/build).
2. Load references as needed:
   - Use `references/prplos-core-summary.md` for Ambiorix/ubus/CLI/init/registration details.
   - Use `references/att-prpl-build.md` for ATT source tree and overlay/build flow.
   - Use `references/prplos-integration-principles.md` for TR-181/USP scope boundaries, integration KPI, and platform-level validation contracts.
3. Provide minimal-change guidance tied to actual files and init order.
4. If the question is pWHM or vendor-specific, defer to the corresponding skill.

## Outputs

- Architecture explanation linked to concrete files and services.
- Debug/validation steps tied to ubus-cli and init scripts.
- Build/overlay guidance using the existing ATT flow.
