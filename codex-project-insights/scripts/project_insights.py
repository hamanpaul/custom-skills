#!/usr/bin/env python3
"""Summarize Codex sessions with time-weighted scoring."""

from __future__ import annotations

import argparse
import json
import math
from collections import defaultdict
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


SEVERITY_DEFAULTS = {
    "turn_aborted": 1.0,
    "context_compacted": 0.6,
    "agent_reasoning": 0.2,
    "task_complete": 0.1,
    "task_started": 0.1,
    "token_count": 0.1,
    "user_message": 0.2,
}


@dataclass
class SessionStats:
    timestamp: datetime
    event_counts: dict[str, int]


def _parse_iso(ts: str) -> datetime | None:
    try:
        return datetime.fromisoformat(ts.replace("Z", "+00:00")).astimezone(UTC)
    except ValueError:
        return None


def _find_session_timestamp(lines: list[dict[str, Any]], fallback: datetime) -> datetime:
    for row in lines:
        if row.get("type") == "session_meta":
            payload = row.get("payload") or {}
            ts = payload.get("timestamp")
            if isinstance(ts, str):
                parsed = _parse_iso(ts)
                if parsed:
                    return parsed
    return fallback


def _read_session(path: Path) -> SessionStats | None:
    lines: list[dict[str, Any]] = []
    try:
        with path.open(encoding="utf-8", errors="replace") as f:
            for raw in f:
                raw = raw.strip()
                if not raw:
                    continue
                try:
                    lines.append(json.loads(raw))
                except json.JSONDecodeError:
                    continue
    except OSError:
        return None

    if not lines:
        return None

    event_counts: dict[str, int] = defaultdict(int)
    for row in lines:
        if row.get("type") != "event_msg":
            continue
        payload = row.get("payload") or {}
        event_type = payload.get("type")
        if isinstance(event_type, str):
            event_counts[event_type] += 1

    fallback = datetime.fromtimestamp(path.stat().st_mtime, tz=UTC)
    ts = _find_session_timestamp(lines, fallback)
    return SessionStats(timestamp=ts, event_counts=dict(event_counts))


def _collect_sessions(root: Path) -> list[SessionStats]:
    sessions: list[SessionStats] = []
    for p in sorted(root.rglob("*.jsonl")):
        st = _read_session(p)
        if st:
            sessions.append(st)
    return sessions


def _time_weight(age_days: float, half_life_days: int) -> float:
    return math.pow(0.5, age_days / float(half_life_days))


def _severity(event_type: str) -> float:
    return SEVERITY_DEFAULTS.get(event_type, 0.2)


def _score(
    now: datetime,
    sessions: list[SessionStats],
    short_days: int,
    long_days: int,
    half_life_days: int,
) -> dict[str, Any]:
    short_weighted: dict[str, float] = defaultdict(float)
    long_weighted: dict[str, float] = defaultdict(float)
    raw_counts: dict[str, int] = defaultdict(int)

    for st in sessions:
        age_days = max(0.0, (now - st.timestamp).total_seconds() / 86400.0)
        w = _time_weight(age_days, half_life_days)
        for event_type, count in st.event_counts.items():
            raw_counts[event_type] += count
            if age_days <= short_days:
                short_weighted[event_type] += count * w
            if age_days <= long_days:
                long_weighted[event_type] += count * w

    max_short = max(short_weighted.values(), default=1.0)
    max_long = max(long_weighted.values(), default=1.0)

    rows = []
    for event_type in sorted(set(raw_counts) | set(short_weighted) | set(long_weighted)):
        short_norm = short_weighted.get(event_type, 0.0) / max_short
        long_norm = long_weighted.get(event_type, 0.0) / max_long
        sev = _severity(event_type)
        score = 0.55 * short_norm + 0.30 * long_norm + 0.15 * sev
        rows.append(
            {
                "event_type": event_type,
                "raw_count": raw_counts.get(event_type, 0),
                "short_weighted": round(short_weighted.get(event_type, 0.0), 4),
                "long_weighted": round(long_weighted.get(event_type, 0.0), 4),
                "severity": sev,
                "score": round(score, 4),
            }
        )
    rows.sort(key=lambda x: x["score"], reverse=True)
    return {
        "scoring_formula": "score = 0.55*short_window + 0.30*long_window + 0.15*severity",
        "half_life_days": half_life_days,
        "short_window_days": short_days,
        "long_window_days": long_days,
        "rows": rows,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--sessions-root",
        default=str(Path.home() / ".codex" / "sessions"),
        help="Root path of Codex sessions.",
    )
    parser.add_argument("--short-days", type=int, default=14)
    parser.add_argument("--long-days", type=int, default=90)
    parser.add_argument("--half-life-days", type=int, default=21)
    parser.add_argument("--out", required=True, help="Output JSON file path.")
    args = parser.parse_args()

    root = Path(args.sessions_root).expanduser()
    out = Path(args.out).expanduser()
    out.parent.mkdir(parents=True, exist_ok=True)

    sessions = _collect_sessions(root)
    now = datetime.now(tz=UTC)
    result = {
        "generated_at": now.isoformat(),
        "sessions_root": str(root),
        "session_count": len(sessions),
        "scoring": _score(
            now=now,
            sessions=sessions,
            short_days=args.short_days,
            long_days=args.long_days,
            half_life_days=args.half_life_days,
        ),
    }
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(str(out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
