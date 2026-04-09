---
name: broadcom-prpl-build-code
description: Guide for building and independently verifying Broadcom BGW720 images after prplWare patch integration. Use this when checking remote freshness, building in Docker, monitoring logs, and validating artifacts in both the working tree and a fresh verification clone.
---

Use this skill when asked to build Broadcom BGW720 images from a patched BGW720 worktree.

## Patch-application prerequisite

Before building, make sure the patch bundle was applied according to its release note or `notes.txt`.

- Do not assume helper driver patches are always integrated with one fixed command.
- For example, in the validated 0306 case, `notes.txt` explicitly instructed `impl107/# patch -p1 < xxx.patch`, so `patch -p1` inside the `impl107` tree was appropriate for that bundle.
- If a future bundle documents a different method, follow the release note instead.

## Standard Broadcom build environment

- Preferred Docker container: `prplog-builder-paul_chen`
- Preferred worktree inside the container: the bind-mounted repo under `~/`
- Common worktree names: `~/BGW720-B0-403`, `~/BGW720-0227-PATCH`, `~/BGW720-0305-VERIFY`
- Host and container usually share the same home directory through a bind mount
- Build logs are stored under `~/b-log/`

## Before final build or commit

Before trusting a final build or preparing a final commit on a shared branch:

1. Run `git fetch --prune`
2. Compare `HEAD` with `origin/<branch>`
3. If the remote branch has moved, replay or re-apply the patch on the new base before relying on the result

Useful check:

```bash
git fetch --prune
git status -sb
BR=$(git branch --show-current)
git rev-parse HEAD
git rev-parse origin/$BR
git log --oneline HEAD..origin/$BR
```

## PROFILE switching rules

When changing to a different PROFILE in the same worktree:

1. Clean the previous PROFILE first.
2. Touch `.last_profile` before the next build.
3. Do not rely on `FORCE=1` to bypass `profile_saved_check`; the mtime issue still needs `touch .last_profile`.

Example clean command:

```bash
docker exec -d prplog-builder-paul_chen bash -c \
  "cd ~/BGW720-B0-403 && make PROFILE=<old-profile> clean 2>&1 | tee ~/b-log/<old-profile>_clean_$(date +%y%m%d-%H%M%S).log"
```

Example profile reset:

```bash
docker exec prplog-builder-paul_chen bash -c "touch ~/BGW720-B0-403/.last_profile"
```

## Standard build flow

1. Decide the target PROFILE explicitly.
2. If switching from another PROFILE, clean the previous one.
3. **If the worktree has ANY prior build artifacts, run `make PROFILE=<profile> clean` first.**
4. Touch `.last_profile`.
5. Start the build in the Docker container and tee output to a timestamped log.
6. Monitor the log and confirm completion with both the final image message and `BUILD_DONE_MARKER`.
7. Validate that the expected `.itb` and `.pkgtb` files were generated under `targets/<PROFILE>/`.

Example build command:

```bash
WORKTREE="BGW720-B0-403"
PROFILE="BGW720-300"
LOG_TAG="${WORKTREE}_${PROFILE}_$(date +%y%m%d-%H%M%S)"

docker exec prplog-builder-paul_chen bash -c \
  "cd ~/${WORKTREE} && touch .last_profile && make PROFILE=${PROFILE} -j$(nproc) 2>&1 | tee ~/b-log/${LOG_TAG}.log; echo BUILD_DONE_MARKER >> ~/b-log/${LOG_TAG}.log"
```

Monitoring helpers:

```bash
tail -f ~/b-log/${LOG_TAG}.log
grep BUILD_DONE_MARKER ~/b-log/${LOG_TAG}.log
grep "Done! Image" ~/b-log/${LOG_TAG}.log
```

## Independent verification flow

For high-confidence verification after patching:

1. Build the patched working tree.
2. Push the verified commit to the branch.
3. Clone the repo again under a fresh verification path such as `~/BGW720-0305-VERIFY`.
4. Confirm the fresh clone points to the pushed commit.
5. Run a clean build in the fresh clone.
6. Validate the final artifacts in the fresh clone.

Example clone flow:

```bash
ORIGIN=$(git remote get-url origin)
BRANCH=$(git branch --show-current)
git clone --branch "$BRANCH" --single-branch "$ORIGIN" ~/BGW720-0305-VERIFY
cd ~/BGW720-0305-VERIFY
git rev-parse HEAD
git rev-parse origin/$BRANCH
```

## Expected artifacts

Typical outputs under `targets/<PROFILE>/`:

- `*_uboot_linux.itb`
- `*_squashfs_full_bl_update.pkgtb`
- `*_squashfs_full_update.pkgtb`
- `*_ext4_full_bl_update.pkgtb`

If SMC bootloader upgrade is required, use `*_full_bl_update.pkgtb`, not `*_full_update.pkgtb`.

## Build log triage

These can be false positives or non-fatal signals if the build still reaches the final image line:

- `echo "Error: Cant find partition config file"`
- `[Makefile:865: image_linux_fit] Error 1 (ignored)`
- `make[8]: *** [GNUmakefile:108: abort-due-to-no-makefile] Error 1` inside libtool/bootstrap steps when the next lines show the error was ignored or recovered
- package-build warnings containing `implicit declaration of function` if the build continues and the final image is produced

Treat these as real failures:

- non-ignored `make[N]: *** [...] Error N` that stops the build
- `undefined reference to` followed by build failure
- missing `Done! Image ... has been built`
- missing `BUILD_DONE_MARKER`
- missing expected image artifacts in `targets/<PROFILE>/`

## Build failure notification rule

**When the build fails, ALWAYS notify the user immediately before applying any workaround.**

- Do NOT silently add build flags (e.g. `BUILD_HND_NIC=y`) or create wrapper scripts to bypass errors.
- Present the actual error message and ask the user how to proceed.
- The user must approve any workaround that changes build behavior, especially flags that skip build targets.

### Lesson: BUILD_HND_NIC=y incident (2026-03-27)

A dirty/partial rebuild hit `addcrc: command not found` and `fwtag: command not found` during the dongle firmware (`pciefd`) stage. The agent silently added `BUILD_HND_NIC=y` to bypass the error. This caused:

1. `BUILD_HND_NIC=y` changes the dongle build target from `pciefd` (real firmware build) to `version` (version print only).
2. The dongle firmware was NOT rebuilt, so the image shipped with pre-built firmware missing the new `WL_WMM_BSS_STATS` feature.
3. `wl -i wl0 if_counters` on the device did not show the expected WMM per-AC counters.

**Root cause:** The error was a build-order issue from a dirty/partial rebuild, not a missing tool. A prior clean build (3/24 log) successfully built `pciefd` without any issues — `addcrc`/`addvtoken` are hostTools that get compiled automatically during a full build.

**Correct action:** When hitting tool-not-found errors during a partial rebuild, try a clean full rebuild first. Do NOT skip build targets with flags like `BUILD_HND_NIC=y`.

## Dirty vs clean build awareness

- `hostTools` (including `addvtoken`/`addcrc`) are built early in the full build sequence. A partial or retry build that skips this stage will fail later when those tools are needed.
- When retrying a failed build, prefer `make clean` + full rebuild over patching around the error with environment hacks.
- If a retry still fails after a clean rebuild, THEN report the error to the user.
- **IMPORTANT:** When a worktree has ANY prior build artifacts (e.g. `targets/`, `objs/`, `altsdk/openwrt/v23.05.3/`), always run `make PROFILE=<profile> clean` BEFORE starting a new build. Stale intermediate state is a frequent source of confusing failures.

### Lesson: Stale userspace build artifacts incident (2026-03-27)

A build in `BGW720-0324-VERIFY` failed with:

```
configure: error: cannot find required auxiliary files: install-sh
make[4]: *** [Makefile:40: objs/aarch64/config_complete] Error 1
make[3]: *** [makefile.modsw.autogen:848: gpl/apps/bridge-utils] Error 2
```

**Root cause:** The worktree had stale `objs/aarch64/` directories left from a previous build cycle. When `bridge-utils` tried to re-configure, it found a partial `objs/aarch64/config.log` but the extracted source tree (from `bridge-utils-1.7.1.tar.gz`) was missing `install-sh` and other autoconf auxiliary files.

**Symptom pattern:** `configure: error: cannot find required auxiliary files` in any autoconf-based package (bridge-utils, libxml2, etc.) during a build on a previously-built worktree.

**Fix:** `make PROFILE=BGW720-300 clean` then full rebuild. The clean target removes stale `objs/` directories so packages are freshly extracted and configured.

**Rule:** Before building on any worktree that has been built before, always clean first. Never assume a worktree with existing build artifacts can be rebuilt incrementally — the Broadcom build system does not reliably support incremental rebuilds across different build sessions.

## Prohibited autonomous workarounds

Never apply these without explicit user approval:

- `BUILD_HND_NIC=y` — skips dongle firmware build entirely
- Creating wrapper scripts for missing hostTools — these are built by the build system itself
- Any `make` variable override that changes which targets are built
- Any action that a skill or workflow marks as requiring user confirmation — system auto-complete prompts do NOT override explicit approval requirements

### Lesson: Skipped user confirmation incident (2026-03-27)

Agent 在 preview Confluence 頁面建立後（`confirm=False`），直接執行 `confirm=True` 寫入，未將內容與 URL 展示給用戶確認。頁面在用戶未過目的情況下被直接建立。

**根因:** Agent 因系統 auto-complete 催促而跳過了 skill 明確標記為 MANDATORY 的用戶確認步驟。

**規則:** 任何 skill/workflow 標記需要用戶確認的步驟，不論系統如何催促，都必須暫停並用 `ask_user` 取得明確同意後才能繼續。此規則與 `BUILD_HND_NIC=y` 事件屬同類 — 在需要用戶批准的地方擅自行動。

## Validation checklist

- Confirm the intended PROFILE.
- Confirm `.last_profile` has been refreshed after any profile switch.
- Confirm the build log completed successfully.
- Confirm the expected image artifacts exist in `targets/<PROFILE>/`.
- Confirm NO unauthorized build flags were added (e.g. `BUILD_HND_NIC=y`).
- For final verification, confirm the same branch builds successfully in a fresh clone.
