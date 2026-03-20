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
3. Touch `.last_profile`.
4. Start the build in the Docker container and tee output to a timestamped log.
5. Monitor the log and confirm completion with both the final image message and `BUILD_DONE_MARKER`.
6. Validate that the expected `.itb` and `.pkgtb` files were generated under `targets/<PROFILE>/`.

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

## Validation checklist

- Confirm the intended PROFILE.
- Confirm `.last_profile` has been refreshed after any profile switch.
- Confirm the build log completed successfully.
- Confirm the expected image artifacts exist in `targets/<PROFILE>/`.
- For final verification, confirm the same branch builds successfully in a fresh clone.
