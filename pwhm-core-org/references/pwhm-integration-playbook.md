# pWHM Integration Playbook

## Mission
- Drive deterministic pWHM integration on prplOS with traceable HLAPI -> LLAPI paths.
- Keep changes minimal and evidence-driven.

## Core flow
1. Startup: `amxrt` loads `/etc/amx/wld/*.odl` and module constructors.
2. FTA dispatch: generic `wifiGen_*` with possible vendor function-table override.
3. Runtime: hostapd/wpa_supplicant/nl80211 interaction through pWHM handlers.

## HLAPI to LLAPI tracing contract
- Capture:
  - HLAPI read/write action path
  - `mfn_*` handler location
  - generic LLAPI path (`wifiGen_*`)
  - vendor path (if overridden)
- Output mapping with file and line evidence.

## FSM dependency checks
- Validate dependency bits and pending-state clear points.
- Verify sync order for radio, vap, endpoint, and post-check stages.

## ODL and model checkpoints
- Verify root ODL, defaults ODL, and mapping ODL consistency.
- Verify exposed objects match runtime behavior in CLI/ubus observations.

## Delivery checklist
- Trace mapping report
- Risk notes for unresolved branches
- Validation commands and observed outputs
