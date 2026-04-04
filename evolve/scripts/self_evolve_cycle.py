#!/usr/bin/env python3
from __future__ import annotations

import os
import sys
from pathlib import Path


def main() -> int:
    target = (
        Path(__file__).resolve().parents[2]
        / "codex-project-insights"
        / "scripts"
        / "self_evolve_cycle.py"
    )
    if not target.exists():
        raise SystemExit(f"missing codex-project-insights self_evolve_cycle script: {target}")
    os.execv(sys.executable, [sys.executable, str(target), *sys.argv[1:]])


if __name__ == "__main__":
    raise SystemExit(main())
