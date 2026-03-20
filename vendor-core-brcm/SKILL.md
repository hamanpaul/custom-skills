---
name: vendor-core-brcm
description: Broadcom vendor-specific pWHM integration, mod-whm-brcm behavior, wl/nl80211/hostapd interactions, dhd.ko driver flow, NVRAM and bring-up, and MLO configuration. Use when questions involve Broadcom-specific overrides, vendor ODL, BRCM driver behavior, or MLO/ACS/DFS handling in prpl projects. Exclude generic pWHM core content.
---

# Vendor Core - Broadcom

## Scope

Use for Broadcom-specific implementation details: mod-whm-brcm overrides, wl ioctl/iovar paths, dhd.ko behaviors, NVRAM handling, and MLO bring-up.

## Workflow

1. Identify vendor-specific paths (whm_brcm_*, wl ioctl/iovar, dhd.ko/NVRAM, MLO).
2. Load references as needed:
   - `references/brcm-pwhm-integration.md` for mod-whm-brcm flow, FTA overrides, ODL layout, and build/deploy notes.
   - `references/brcm-driver-bringup.md` for driver build, bring-up, NVRAM, and MLO behavior.
   - `references/brcm-bdk-playbook.md` for bring-up checklist, performance baselines, and rollback-oriented validation.
3. Provide minimal-change guidance; defer generic pWHM architecture to pwhm-core-org.

## Outputs

- Vendor override map (FTA functions and impact).
- BRCM-specific control path explanation (wl/nl80211/hostapd/dhd).
- MLO and bring-up validation checklist.
