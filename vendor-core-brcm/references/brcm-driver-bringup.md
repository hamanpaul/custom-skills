# Broadcom driver bring-up and MLO notes

## Driver build issues (Wi-Fi8 EA1 example)
- Build requires bash shell; use SHELL=/bin/bash CONFIG_SHELL=/bin/bash.
- Missing ThreadX .prebuilt objects causes tx_block_allocate.o errors; verify dongle/.prebuilt.
- Follow sdkdeps + src merge order and apply patch scripts.

## DHD and interface bring-up
- If no wlan interfaces appear, check regulatory.db, PCIe enumeration, dhd.ko load, firmware path.
- Validate with dmesg for PCIe and DHD errors.

## NVRAM handling
- Prepare per-band NVRAM, apply prefix and devpath, merge and convert via nvserial.
- Ensure NVRAM path matches rootfs defaults and wlFeature settings.

## MLO configuration
- Use wl_mlo_config and wl_mlo_map aligned with NVRAM prefix.
- MAP/AAP selection: prefer FD as MAP for mixed NIC/FD.
- Avoid forcing MAP off; use wlX_mlo_forced_inactive for per-link control.
- Consider MAXSCB count per link; MLO uses per-link slots.

## Tools
- wl, envram, nvserial, CLM tools for power table.

