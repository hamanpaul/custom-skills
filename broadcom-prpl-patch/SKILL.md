---
name: broadcom-prpl-patch
description: Guide for applying Broadcom prplWare patch bundles into BGW720 worktrees. Use this when comparing a new Broadcom patch drop against its previous patch and the current codebase, deciding which files to copy directly, and determining from release notes how helper driver patch files should be integrated.
---

Use this skill when asked to apply or review a Broadcom prplWare patch bundle such as `CS00012439197_6.3.0_prplware4.0.3_YYYYMMDD.tgz` against a BGW720 worktree.

## Patch bundle structure

A Broadcom patch bundle may include:

- `altsdk/openwrt/patches/prpl/v23.05.3_prplware-v4.0.3/feeds/`
  - `feed_prplmesh/services/pwhm/files/etc/amx/wld/wld_defaults/`
  - `feed_prplmesh/services/pwhm/patches/`
  - `feed_prplos/.../prpl-webui-bcm/`
- `userspace/public/libs/prpl_brcm/mods/mod-whm-brcm/`
  - `Makefile.fullsrc`
  - `include_priv/`
  - `src/`
- `bcmdrivers/broadcom/net/wl/impl107/*.patch`
- `notes.txt`

Typical paths:

- Patch drops: `~/brcm-patchs/MMDD/`
- Original tarballs: `~/brcm-patchs/CS00012439197_6.3.0_prplware4.0.3_YYYYMMDD.tgz`
- Known-issues note: `~/brcm-patchs/patch-exp.md`
- Target worktree: the current BGW720 repo

## Proven comparison strategy

Always compare in two dimensions:

1. **New bundle vs previous bundle**
   - Purpose: identify what Broadcom newly added compared with the immediately previous patch release.
   - Do not hard-code this as a specific `0227` vs `0306` comparison; always compare the current patch against its own previous patch.
   - Example from one validated cycle: when bundle `0306` was compared with its previous patch bundle `0227`, the differences were only:
     - `bcmdrivers/.../impl107/0002-rb224211.patch`
     - `bcmdrivers/.../impl107/0003-rb223772_rb224292_rb225045.patch`
     - `bcmdrivers/.../impl107/0004-rb224802.patch`
     - extra `notes.txt` lines describing those three patches

2. **New bundle vs target repo**
   - Purpose: identify what the current codebase still lacks.
   - Do not assume bundle-to-bundle differences equal repo-to-bundle differences.
   - Example: `9025` and `9026` were already present in bundle `0227`, but a later repo baseline still lacked the correct `9025` content and still missed `9026`.

Useful commands:

```bash
diff -rq ~/brcm-patchs/0227 ~/brcm-patchs/0306

PATCH=~/brcm-patchs/0306
DST=~/BGW720-B0-403
cd "$PATCH"
find altsdk userspace bcmdrivers -type f | sort | while read -r rel; do
  if [ -e "$DST/$rel" ]; then
    cmp -s "$PATCH/$rel" "$DST/$rel" || echo "DIFF $rel"
  else
    echo "NEW  $rel"
  fi
done
```

## Provenance check

If you have both the original tarball and an unpacked directory, compare them once to confirm the unpacked tree is trustworthy.
This was verified for:

- `~/brcm-patchs/CS00012439197_6.3.0_prplware4.0.3_20260305.tgz`
- `~/brcm-patchs/0306`

## File handling rules

1. **OpenWrt feed patch files**
   - Files under `altsdk/.../feed_prplmesh/.../patches/*.patch` are OpenWrt patch-queue inputs.
   - Copy them verbatim when the repo differs.
   - Verify with `cmp -s`.

2. **userspace source files**
   - Treat `whm_brcm_api_ext.c` and `whm_brcm_api_ext_vndr.c` as high-risk files.
   - Preserve local fixes if the bundle would regress them.

3. **impl107 driver patch files**
   - Files under `bcmdrivers/broadcom/net/wl/impl107/*.patch` are not self-explanatory by path alone.
   - First read the patch bundle's release note (commonly `notes.txt`) to determine how they should be integrated into the repo.
   - Do not assume every impl107 patch bundle always uses `patch -p1`.
   - If the release note says they should be applied to source, dry-run the instructed command first, then apply it, then verify with reverse dry-run.
   - Do not commit the raw helper patch files unless the repo explicitly tracks them or the release note requires that.

Example:

```bash
# 0306 notes.txt said: ** impl107/# patch -p1 < xxx.patch
cd ~/BGW720-B0-403/bcmdrivers/broadcom/net/wl/impl107
patch --dry-run -p1 < ~/brcm-patchs/0306/bcmdrivers/broadcom/net/wl/impl107/0002-rb224211.patch
patch -p1 < ~/brcm-patchs/0306/bcmdrivers/broadcom/net/wl/impl107/0002-rb224211.patch
patch --dry-run -R -p1 < ~/brcm-patchs/0306/bcmdrivers/broadcom/net/wl/impl107/0002-rb224211.patch
```

4. **notes.txt**
   - Check `git ls-files -- notes.txt` before copying or committing it.
   - If the repo does not track `notes.txt`, treat it as reference only and do not commit it.

## Known recurring issues to check on every patch

1. `WL_STA_ANT_MAX` must not remain undefined.
   - In `whm_brcm_api_ext.c` and `whm_brcm_api_ext_vndr.c`, prefer `MAX_NR_ANTENNA` when needed.
2. eht/he band guards must be present.
   - eht logic should be protected for 6 GHz only.
   - he logic should be protected for non-2.4 GHz bands.
3. `Makefile.fullsrc` may miss a `cchk` fallback.
   - If the worktree already has the required `whm_brcm.c` handling, avoid regressing it.

Useful checks:

```bash
grep -n "WL_STA_ANT_MAX" <patch>/userspace/.../src/whm_brcm_api_ext*.c
grep -n "operatingFrequencyBand" <patch>/userspace/.../src/whm_brcm_api_ext.c | grep -c "eht\|he"
```

## Practical rules while editing

- Compare the current patch against its previous patch and against the repo separately.
- Preserve worktree-specific fixes over older patch content.
- Commit repo-tracked source changes and feed patch files, not raw helper artifacts.
- Exclude `notes.txt` if it is untracked.
- Let the release note decide how helper driver patches are applied; in the 0306 case, `notes.txt` explicitly required `patch -p1`.
- After patching, verify with targeted diffs or `cmp`, and verify applied driver patches with reverse dry-runs before building.
