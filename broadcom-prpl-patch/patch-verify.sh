#!/bin/bash
# patch-verify.sh — GATE 3: 驗證 bundle 每個檔案都已正確反映在 worktree 中
# Usage: patch-verify.sh <bundle_dir> <worktree_dir>
# Output: per-file OK/FAIL lines to stdout, summary to stderr
# Exit:   0 = ALL PASSED, 1 = HAS FAILURES (blocked)

set -uo pipefail

BUNDLE="${1:?Usage: patch-verify.sh <bundle_dir> <worktree_dir>}"
DST="${2:?Usage: patch-verify.sh <bundle_dir> <worktree_dir>}"

if [ ! -d "$BUNDLE" ]; then
  echo "ERROR: Bundle directory not found: $BUNDLE" >&2
  exit 1
fi
if [ ! -d "$DST" ]; then
  echo "ERROR: Worktree directory not found: $DST" >&2
  exit 1
fi

PASS=0
FAIL=0
SKIP=0
DIFF_COUNT=0

while IFS= read -r fullpath; do
  rel="${fullpath#$BUNDLE/}"

  case "$rel" in
    notes.txt)
      # REF — skip
      SKIP=$((SKIP + 1))
      continue
      ;;

    bcmdrivers/*/impl107/*.patch)
      # IPATCH — verify patch was applied by checking target files exist in worktree
      # Support multiple patch formats:
      #   git diff:    "diff --git a/X b/Y"
      #   unified:     "--- a/X" or "--- impl107.svn/X" or "--- X.orig"
      #   diff -urN:   "+++ impl107/path/to/file"
      patch_targets=$(grep '^+++ ' "$fullpath" 2>/dev/null \
        | sed 's|^+++ ||; s|\t.*||' \
        | sed 's|^b/||; s|^impl107/||; s|^impl107\.svn/||' \
        | grep -v '^/dev/null' \
        | sort -u | head -20)

      if [ -z "$patch_targets" ]; then
        echo "FAIL  $rel  (cannot parse patch targets)"
        FAIL=$((FAIL + 1))
        continue
      fi

      # impl107 patches target files under impl107/main/... or impl107/sys/...
      # The worktree path is bcmdrivers/broadcom/net/wl/impl107/<target>
      impl107_base="bcmdrivers/broadcom/net/wl/impl107"
      patch_ok=1
      checked=0
      for pf in $patch_targets; do
        wt_path="$impl107_base/$pf"
        checked=$((checked + 1))
        if [ -f "$DST/$wt_path" ]; then
          : # file exists in worktree
        else
          echo "FAIL  $rel  -> $wt_path not found in worktree"
          patch_ok=0
          FAIL=$((FAIL + 1))
        fi
      done
      if [ "$patch_ok" = "1" ]; then
        echo "OK    $rel  (IPATCH, $checked target files verified)"
        PASS=$((PASS + 1))
      fi
      ;;

    *)
      # COPY — direct file comparison
      if [ ! -e "$DST/$rel" ]; then
        echo "FAIL  $rel  (MISSING in worktree)"
        FAIL=$((FAIL + 1))
      elif cmp -s "$fullpath" "$DST/$rel"; then
        echo "OK    $rel"
        PASS=$((PASS + 1))
      else
        # Show first few diff lines to help human review
        echo "DIFF  $rel  (DIFFERS from bundle — review required)"
        diff --brief "$fullpath" "$DST/$rel" 2>/dev/null || true
        DIFF_COUNT=$((${DIFF_COUNT:-0} + 1))
        # DIFF is not auto-FAIL: it requires human decision
        # (worktree may have intentional local modifications)
      fi
      ;;
  esac
done < <(find "$BUNDLE" -type f | sort)

echo "---" >&2
echo "PASS=$PASS  FAIL=$FAIL  DIFF=$DIFF_COUNT  SKIP=$SKIP" >&2

if [ "$FAIL" -gt 0 ]; then
  echo "🔴 VERIFICATION FAILED — $FAIL file(s) missing or unparseable" >&2
  echo "BLOCKED: Do NOT proceed to build or commit." >&2
  exit 1
elif [ "$DIFF_COUNT" -gt 0 ]; then
  echo "🟡 $DIFF_COUNT file(s) DIFFER from bundle — human review required" >&2
  echo "Each DIFF must be explained: intentional local mod or missed update?" >&2
  exit 2
else
  echo "✅ ALL PASSED — $PASS file(s) verified, $SKIP skipped" >&2
  exit 0
fi
