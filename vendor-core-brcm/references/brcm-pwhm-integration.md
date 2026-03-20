# Broadcom pWHM integration summary

## Vendor module and flow
- Vendor addon module: mod-whm-brcm.so with ODL in /etc/amx/wld/modules/mod-whm-brcm/.
- FTA override model: pWHM generic wifiGen_* handlers overridden by whm_brcm_* where needed.
- Mixed path: nl80211 baseline + wl iovar/TLV for BRCM-only features.

## Control paths
- TR-181 Device.WiFi.* -> FTA -> wifiGen_* or whm_brcm_* -> nl80211/hostapd/wpa_supplicant -> dhd.ko.
- Vendor ODL exposes BRCM-specific nodes under Device.WiFi.Radio.Vendor.Brcm.* (MLO/ACS/DFS).
- whm_brcm uses wl iovar and NVRAM updates for features that nl80211 cannot cover.

## Common override areas
- Radio sync/chanspec/regdomain/poschans/stats.
- DFS/ACS/BGDFS and channel management.
- MLO config (MLOStats, MLD role, link map).
- Sensing/CSI functions via whm_brcm_radcsi_*.

## Build and deploy notes
- Build mod-whm-brcm via Bcmbuild.mk in userspace/public/libs/prpl_brcm/mods/mod-whm-brcm.
- Deploy mod-whm-brcm.so and ODL directory, then restart wld_gen.
- Requires wld.so, libnl3, libamx*, and Broadcom dhd.ko on target.

