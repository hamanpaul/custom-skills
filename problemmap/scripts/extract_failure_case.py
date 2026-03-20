#!/usr/bin/env python3
"""Extract a failure-bearing case from a session JSONL file using rule-based anchors."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

FAILURE_KEYWORDS = {
    "error",
    "failed",
    "failure",
    "exception",
    "traceback",
    "not working",
    "broken",
    "abort",
    "aborted",
    "context compacted",
    "context_compacted",
    "wrong approach",
    "misunderstood",
    "bad result",
    "regression",
}

FAILURE_EVENTS = {
    "turn_aborted",
    "context_compacted",
    "wrong_approach",
    "misunderstood_request",
    "buggy_code",
    "excessive_changes",
}


def detect_failure_event_type(record: dict[str, Any]) -> str | None:
    top_level = record.get("event_type")
    if isinstance(top_level, str) and top_level in FAILURE_EVENTS:
        return top_level

    if record.get("type") != "event_msg":
        return None

    payload = record.get("payload")
    if not isinstance(payload, dict):
        return None

    payload_type = payload.get("type")
    if isinstance(payload_type, str) and payload_type in FAILURE_EVENTS:
        return payload_type
    return None


def collect_strings(value: Any) -> list[str]:
    out: list[str] = []
    if isinstance(value, str):
        out.append(value)
    elif isinstance(value, dict):
        for child in value.values():
            out.extend(collect_strings(child))
    elif isinstance(value, list):
        for child in value:
            out.extend(collect_strings(child))
    return out


def collect_nonzero_codes(value: Any) -> list[int]:
    codes: list[int] = []
    if isinstance(value, dict):
        for key, child in value.items():
            if key in {"exit_code", "returncode", "code"} and isinstance(child, int) and child != 0:
                codes.append(child)
            else:
                codes.extend(collect_nonzero_codes(child))
    elif isinstance(value, list):
        for child in value:
            codes.extend(collect_nonzero_codes(child))
    return codes


def normalize_text(strings: list[str]) -> str:
    text = " ".join(strings)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def score_record(record: dict[str, Any]) -> tuple[int, list[str]]:
    reasons: list[str] = []
    score = 0
    event_type = detect_failure_event_type(record)
    if event_type:
        score += 3
        reasons.append(f"event:{event_type}")

    strings = collect_strings(record)
    normalized = normalize_text(strings).lower()
    for keyword in FAILURE_KEYWORDS:
        if keyword in normalized:
            score += 1
            reasons.append(f"keyword:{keyword}")

    codes = collect_nonzero_codes(record)
    if codes:
        score += 2
        reasons.append("nonzero-exit-code")

    return score, reasons


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        records.append(json.loads(line))
    return records


def pick_anchor(records: list[dict[str, Any]]) -> tuple[int, list[str], int]:
    best_index = max(range(len(records)), key=lambda idx: score_record(records[idx])[0])
    best_score, reasons = score_record(records[best_index])
    return best_index, reasons, best_score


def extract_case_at_index(
    records: list[dict[str, Any]],
    source: Path,
    anchor_idx: int,
    anchor_event_type: str | None = None,
) -> dict[str, Any]:
    if not records:
        raise ValueError("session file is empty")
    if anchor_idx < 0 or anchor_idx >= len(records):
        raise ValueError(f"anchor index out of range: {anchor_idx}")

    start = max(0, anchor_idx - 5)
    end = min(len(records), anchor_idx + 3)
    window = records[start:end]

    expected = ""
    for record in reversed(records[:anchor_idx]):
        text = normalize_text(collect_strings(record))
        if text:
            expected = text
            break

    actual = normalize_text(collect_strings(records[anchor_idx]))
    evidence = [normalize_text(collect_strings(record)) for record in window]
    evidence = [item for item in evidence if item]
    anchor_record = records[anchor_idx]
    score, reasons = score_record(anchor_record)
    exit_codes = collect_nonzero_codes(anchor_record)
    anchor_event_type = anchor_event_type or detect_failure_event_type(anchor_record)
    if anchor_event_type and f"event:{anchor_event_type}" not in reasons:
        reasons = [f"event:{anchor_event_type}", *reasons]

    return {
        "status": "ok",
        "source_session": str(source),
        "anchor_index": anchor_idx,
        "anchor_score": score,
        "anchor_event_type": anchor_event_type,
        "anchor_reasons": reasons,
        "anchor_exit_codes": exit_codes,
        "expected": expected,
        "actual": actual,
        "candidate_failure_signals": reasons,
        "evidence": evidence,
        "recent_actions": evidence[-5:],
    }


def extract_case(records: list[dict[str, Any]], source: Path) -> dict[str, Any]:
    if not records:
        raise ValueError("session file is empty")
    anchor_idx, _, _ = pick_anchor(records)
    return extract_case_at_index(records, source, anchor_idx)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("session", type=Path, help="Path to a session JSONL file")
    parser.add_argument("--output", type=Path, help="Optional path to write the extracted case JSON")
    args = parser.parse_args()

    try:
        records = load_jsonl(args.session)
        case = extract_case(records, args.session)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "error", "error": str(exc)}, indent=2, ensure_ascii=False))
        return 1

    payload = json.dumps(case, indent=2, ensure_ascii=False)
    if args.output:
        args.output.write_text(payload + "\n", encoding="utf-8")
    print(payload)
    return 0


if __name__ == "__main__":
    sys.exit(main())
