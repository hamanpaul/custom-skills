#!/usr/bin/env bash
set -euo pipefail

AGENTS_ROOT="${AGENTS_ROOT:-$HOME/.agents}"
exec /usr/bin/python3 "$AGENTS_ROOT/tools/coordinator/scripts/coordinator.py" "$@"
