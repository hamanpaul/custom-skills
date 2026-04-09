#!/bin/bash
# patch-inventory.sh — GATE 1: 清點 bundle 所有檔案並分類
# Usage: patch-inventory.sh <bundle_dir>
# Output: TSV (category \t path) to stdout
# Exit:   0 = success, 1 = error

set -euo pipefail

BUNDLE="${1:?Usage: patch-inventory.sh <bundle_dir>}"

if [ ! -d "$BUNDLE" ]; then
  echo "ERROR: Bundle directory not found: $BUNDLE" >&2
  exit 1
fi

TOTAL=0
IPATCH=0
COPY=0
REF=0
OTHER=0

while IFS= read -r fullpath; do
  rel="${fullpath#$BUNDLE/}"
  TOTAL=$((TOTAL + 1))

  case "$rel" in
    notes.txt)
      echo -e "REF\t$rel"
      REF=$((REF + 1))
      ;;
    bcmdrivers/*/impl107/*.patch)
      echo -e "IPATCH\t$rel"
      IPATCH=$((IPATCH + 1))
      ;;
    altsdk/*|userspace/*|build/*|bcmdrivers/*|kernel/*|targets/*|make.*|packages/*|rdp/*|bootloaders/*)
      echo -e "COPY\t$rel"
      COPY=$((COPY + 1))
      ;;
    *)
      echo -e "OTHER\t$rel"
      OTHER=$((OTHER + 1))
      ;;
  esac
done < <(find "$BUNDLE" -type f | sort)

echo "---" >&2
echo "TOTAL=$TOTAL  IPATCH=$IPATCH  COPY=$COPY  REF=$REF  OTHER=$OTHER" >&2
if [ "$OTHER" -gt 0 ]; then
  echo "WARNING: $OTHER file(s) classified as OTHER — review required" >&2
fi
