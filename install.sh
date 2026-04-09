#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

# Default destination for skill links
DEST="$HOME/.agents/skills"
FORCE=0
DRY_RUN=0
ALL=0

usage() {
  cat <<'EOF'
Usage: $(basename "$0") [options]
Options:
  -d DIR, --dest DIR   Destination (default: ~/.agents/skills)
  -f, --force          Overwrite existing links/directories
  -n, --dry-run        Print actions but don't perform them
  -a, --all            Link all top-level directories (not only those with SKILL.md)
  -h, --help           Show this help
EOF
}

# Parse arguments
while [[ $# -gt 0 ]]; do
  case "$1" in
    -d|--dest)
      DEST="$2"; shift 2;;
    -f|--force)
      FORCE=1; shift;;
    -n|--dry-run)
      DRY_RUN=1; shift;;
    -a|--all)
      ALL=1; shift;;
    -h|--help)
      usage; exit 0;;
    *)
      echo "Unknown arg: $1"; usage; exit 1;;
  esac
done

# Expand ~ in DEST
DEST="${DEST/#\~/$HOME}"

# Determine repository root as the directory containing this script
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [[ $DRY_RUN -eq 1 ]]; then
  echo "[DRY-RUN] Would create destination: $DEST"
else
  mkdir -p "$DEST"
fi

for d in "$REPO_ROOT"/*; do
  [[ -d "$d" ]] || continue
  name="$(basename "$d")"
  # skip hidden directories
  [[ "$name" == .* ]] && continue

  if [[ $ALL -ne 1 ]]; then
    # detect skill directories by presence of SKILL.md (case-insensitive-ish)
    if [[ ! -f "$d/SKILL.md" && ! -f "$d/SKILL.MD" && ! -f "$d/skill.md" ]]; then
      continue
    fi
  fi

  dest_link="$DEST/$name"

  if [[ -L "$dest_link" ]]; then
    target="$(readlink "$dest_link")"
    if [[ "$target" == "$d" ]]; then
      echo "Skipped: $name already linked"
      continue
    else
      if [[ $FORCE -eq 1 ]]; then
        echo "Removing existing symlink $dest_link"
        [[ $DRY_RUN -eq 0 ]] && rm -f "$dest_link"
      else
        echo "Warning: $dest_link is a symlink to $target (use --force to replace); skipping"
        continue
      fi
    fi
  elif [[ -e "$dest_link" ]]; then
    if [[ $FORCE -eq 1 ]]; then
      echo "Removing existing path $dest_link"
      [[ $DRY_RUN -eq 0 ]] && rm -rf "$dest_link"
    else
      echo "Warning: $dest_link exists and is not a symlink (use --force to replace); skipping"
      continue
    fi
  fi

  echo "Linking $dest_link -> $d"
  if [[ $DRY_RUN -eq 0 ]]; then
    ln -s "$d" "$dest_link"
  fi
done

echo "Done."
