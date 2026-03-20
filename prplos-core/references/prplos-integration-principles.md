# prplOS Integration Principles

## Scope and mission
- Focus on prplOS 4.x CPE/gateway integration with TR-181/USP service lifecycle.
- Keep platform integration deterministic with minimal-change rollout.

## Platform stack view
1. Management plane: Ambiorix ODL -> TR-181 objects -> USP/ubus/CWMP exposure.
2. Runtime layer: service startup, object publication, backend registration.
3. Build/overlay layer: OpenWrt base + overlay synchronization.

## Responsibility boundaries
- In scope:
  - platform-level TR-181/USP exposure behavior
  - startup/registration ordering
  - ubus-cli/amx-cli validation flow
  - OpenWrt overlay/build integration
- Out of scope:
  - vendor-specific wl/dhd/NVRAM bring-up
  - vendor override internals

## Validation contract
- Verify object exposure and query path consistency in ubus and CLI backends.
- Verify startup dependency ordering before feature-level debugging.
- Keep guidance tied to concrete files and service scripts.

## KPI-oriented checks
- Interop target: stable model exposure with no missing critical objects.
- Upgrade target: rollback-ready integration path.
- Telemetry path: TR-181 visibility remains consistent across restarts.
