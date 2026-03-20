# ATT prplOS source and build notes

## Source layout
- att-prpl is the workspace root.
- prplos is the OpenWrt main tree.
- prplos_patch is the overlay layer with feeds, include, scripts, and profiles.
- extern/broadcom-bsp-6.3.0 is Broadcom BSP source and build system.

## Overlay flow
- Use prplos_patch/rsync_to_openwrt.sh for init/patch/regen.
- Overlay avoids direct edits to upstream OpenWrt tree.

## Build flow
- OpenWrt world: tools -> toolchain -> target -> package.
- Outputs: staging_dir/ and bin/targets/.
- Broadcom BSP build in extern/broadcom-bsp-6.3.0/build/Makefile.

## Notes
- prplos_patch/feeds includes prplMesh and pwhm packages.
- If CONFIG_USE_PRPLMESH_WHM is enabled, build libswlc, libswla, and pwhm backend.
- Bear and grpc sync server can exhaust resources; align make -j with ulimit.

