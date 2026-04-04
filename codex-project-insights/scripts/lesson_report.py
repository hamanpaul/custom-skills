#!/usr/bin/env python3
"""Generate a lesson report from a single Codex session JSONL."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as f:
        for raw in f:
            raw = raw.strip()
            if not raw:
                continue
            try:
                rows.append(json.loads(raw))
            except json.JSONDecodeError:
                continue
    return rows


def _latest_session(root: Path) -> Path | None:
    files = sorted(root.rglob("*.jsonl"))
    return files[-1] if files else None


def _report(rows: list[dict[str, Any]]) -> dict[str, Any]:
    events: dict[str, int] = defaultdict(int)
    response_types: dict[str, int] = defaultdict(int)
    friction = {"turn_aborted": 0, "context_compacted": 0}

    for row in rows:
        row_type = row.get("type")
        if row_type == "event_msg":
            payload = row.get("payload") or {}
            ptype = payload.get("type")
            if isinstance(ptype, str):
                events[ptype] += 1
                if ptype in friction:
                    friction[ptype] += 1
        elif row_type == "response_item":
            payload = row.get("payload") or {}
            rtype = payload.get("type")
            if isinstance(rtype, str):
                response_types[rtype] += 1

    proposal = []
    if friction["turn_aborted"] > 0:
        proposal.append("縮短回覆前置規劃，明確指令優先直接執行。")
    if friction["context_compacted"] > 0:
        proposal.append("減少冗長輸出，將長流程拆成可檢核小步驟。")
    if not proposal:
        proposal.append("本 session 無明顯摩擦，維持現有規範。")

    return {
        "event_counts": dict(sorted(events.items(), key=lambda x: x[1], reverse=True)),
        "response_item_counts": dict(
            sorted(response_types.items(), key=lambda x: x[1], reverse=True)
        ),
        "friction_signals": friction,
        "patch_proposal": proposal,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--sessions-root",
        default=str(Path.home() / ".codex" / "sessions"),
        help="Root path of Codex sessions.",
    )
    parser.add_argument("--session", help="Specific session JSONL path.")
    parser.add_argument("--out", required=True, help="Output JSON path.")
    args = parser.parse_args()

    sessions_root = Path(args.sessions_root).expanduser()
    session_path = Path(args.session).expanduser() if args.session else _latest_session(sessions_root)
    if not session_path or not session_path.exists():
        raise SystemExit("No session file found.")

    rows = _load_jsonl(session_path)
    result = {
        "generated_at": datetime.now(tz=UTC).isoformat(),
        "session_path": str(session_path),
        "report": _report(rows),
    }

    out = Path(args.out).expanduser()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(str(out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
