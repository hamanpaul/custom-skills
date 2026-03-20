#!/usr/bin/env bash
set -euo pipefail

# Git sync gate:
# 1) pull --ff-only
# 2) fallback fetch --all --prune
# 3) on fail, create maintenance branch and exit non-zero

topic="${1:-sync-fail}"
ts="$(date +%Y%m%d-%H%M%S)"

if git pull --ff-only; then
  echo "sync: pull ok"
  exit 0
fi

if git fetch --all --prune; then
  echo "sync: fetch only (pull failed)"
  exit 0
fi

branch="maintenance/${topic}-${ts}"
git checkout -b "${branch}"
echo "sync failed -> switched to ${branch}"
exit 1
