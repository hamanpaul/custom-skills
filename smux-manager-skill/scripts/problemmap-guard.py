#!/usr/bin/env python3
"""Build a ProblemMap drift diagnosis from smux context events."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

STOPWORDS = {
    "the",
    "and",
    "for",
    "with",
    "that",
    "this",
    "into",
    "from",
    "under",
    "over",
    "about",
    "your",
    "their",
    "then",
    "than",
    "have",
    "has",
    "been",
    "were",
    "will",
    "would",
    "should",
    "could",
    "task",
    "note",
}

SIGNAL_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    (
        re.compile(r"\b(context compacted|context_compacted|lost context|forgot|forget|memory break|session drift)\b", re.I),
        "event:context_compacted",
    ),
    (
        re.compile(r"\b(misunderstood|misread|wrong task|wrong target|wrong repo|off[- ]track|drift|wrong approach)\b", re.I),
        "event:misunderstood_request",
    ),
    (
        re.compile(r"\b(stuck|looping|circling|not progressing|blocked|unclear|unsure|not sure|guessing|confused)\b", re.I),
        "event:wrong_approach",
    ),
    (
        re.compile(r"\b(abort|aborted|cancelled|timed out|timeout|gave up|stopped responding)\b", re.I),
        "event:turn_aborted",
    ),
    (
        re.compile(r"\b(traceback|exception|syntax error|build failed|test failed|compile error|runtime error)\b", re.I),
        "event:buggy_code",
    ),
    (
        re.compile(r"\b(too broad|overshoot|changed too much|excessive changes|touched unrelated)\b", re.I),
        "event:excessive_changes",
    ),
]


class CommandError(RuntimeError):
    pass


def load_context(path: Path) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line:
            continue
        payload = json.loads(line)
        if isinstance(payload, dict):
            events.append(payload)
    return events


def filter_events(
    events: list[dict[str, Any]],
    task_id: str,
    worker_id: str,
    manager_id: str,
    window: int,
) -> list[dict[str, Any]]:
    manager_aliases = {manager_id, "manager", "mgr"}
    selected = [
        event
        for event in events
        if event.get("task_id") == task_id
        and (
            event.get("from") in manager_aliases
            or event.get("to") in manager_aliases
            or event.get("from") == worker_id
            or event.get("to") == worker_id
        )
    ]
    if not selected:
        raise ValueError(f"no context events found for task={task_id} worker={worker_id}")
    if window > 0:
        return selected[-window:]
    return selected


def event_line(event: dict[str, Any]) -> str:
    seq = event.get("seq", "?")
    src = event.get("from", "?")
    dst = event.get("to", "?")
    event_type = event.get("type", "?")
    summary = str(event.get("summary", "")).strip()
    return f"seq={seq} {src}->{dst} type={event_type}: {summary}"


def tokenize(text: str) -> set[str]:
    return {
        token
        for token in re.findall(r"[a-zA-Z0-9_./:-]{3,}", text.lower())
        if token not in STOPWORDS
    }


def lexical_overlap(expected: str, actual: str) -> float:
    expected_tokens = tokenize(expected)
    if not expected_tokens:
        return 1.0
    actual_tokens = tokenize(actual)
    return len(expected_tokens & actual_tokens) / len(expected_tokens)


def pick_expected(events: list[dict[str, Any]], worker_id: str, manager_id: str, override: str | None) -> str:
    if override:
        return override
    manager_aliases = {manager_id, "manager", "mgr"}
    for event in reversed(events):
        if event.get("from") in manager_aliases and event.get("to") == worker_id:
            summary = str(event.get("summary", "")).strip()
            if summary:
                return summary
    for event in events:
        summary = str(event.get("summary", "")).strip()
        if summary:
            return summary
    return ""


def pick_actual(events: list[dict[str, Any]], worker_id: str) -> str:
    for event in reversed(events):
        if event.get("from") == worker_id:
            summary = str(event.get("summary", "")).strip()
            if summary:
                return summary
    return str(events[-1].get("summary", "")).strip()


def dedupe_keep_order(items: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        if item and item not in seen:
            seen.add(item)
            result.append(item)
    return result


def infer_signals(events: list[dict[str, Any]], worker_id: str, expected: str, actual: str) -> list[str]:
    signals: list[str] = []
    worker_events = [event for event in events if event.get("from") == worker_id]
    ask_count = sum(1 for event in worker_events if event.get("type") == "ASK")
    status_count = sum(1 for event in worker_events if event.get("type") == "STATUS")

    if ask_count >= 2:
        signals.append("event:misunderstood_request")
    if status_count >= 3:
        signals.append("event:wrong_approach")

    terminal_types = {str(event.get("type")) for event in worker_events}
    if "FAIL" in terminal_types:
        signals.append("event:turn_aborted")

    full_text = " ".join(str(event.get("summary", "")) for event in worker_events)
    for pattern, signal in SIGNAL_PATTERNS:
        if pattern.search(full_text):
            signals.append(signal)

    if re.search(r"\b(exit code|returncode|non-zero|rc=|code [1-9][0-9]*)\b", full_text, re.I):
        signals.append("nonzero-exit-code")

    if expected and actual and lexical_overlap(expected, actual) < 0.2:
        signals.append("event:wrong_approach")

    return dedupe_keep_order(signals)


def build_case(
    events: list[dict[str, Any]],
    context_path: Path,
    task_id: str,
    worker_id: str,
    expected: str,
    actual: str,
    signals: list[str],
) -> dict[str, Any]:
    last_event = events[-1]
    evidence = [event_line(event) for event in events]
    return {
        "status": "ok",
        "source_case": str(context_path),
        "source_session": str(context_path),
        "task_id": task_id,
        "worker_id": worker_id,
        "anchor_index": int(last_event.get("seq", 0) or 0),
        "anchor_event_type": str(last_event.get("type", "")) or None,
        "anchor_reasons": signals,
        "expected": expected,
        "actual": actual,
        "candidate_failure_signals": signals,
        "evidence": evidence,
        "recent_actions": evidence[-5:],
    }


def run_json_command(cmd: list[str]) -> dict[str, Any]:
    proc = subprocess.run(cmd, text=True, capture_output=True)
    if proc.returncode != 0:
        raise CommandError(
            f"command failed: {' '.join(cmd)}\nstdout:\n{proc.stdout}\nstderr:\n{proc.stderr}"
        )
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        raise CommandError(
            f"command did not return JSON: {' '.join(cmd)}\nstdout:\n{proc.stdout}\nstderr:\n{proc.stderr}"
        ) from exc


def resolve_problemmap_root(override: str | None) -> Path:
    if override:
        return Path(override).expanduser().resolve()
    return Path(__file__).resolve().parents[2] / "problemmap"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("runtime_dir", type=Path, help="smux runtime directory")
    parser.add_argument("task_id", help="Task identifier to inspect")
    parser.add_argument("worker_id", help="Worker identifier to inspect")
    parser.add_argument("--expected", help="Override the manager-side expected goal/summary")
    parser.add_argument("--manager-id", default="manager", help="Logical manager identifier")
    parser.add_argument("--window", type=int, default=12, help="How many recent matching context events to inspect")
    parser.add_argument("--mode", choices=["strict", "teaching", "repair_preview", "compact"], default="strict")
    parser.add_argument("--ensure-upstream", action="store_true", help="Ensure upstream ProblemMap references before diagnosing")
    parser.add_argument("--problemmap-root", help="Override the sibling problemmap skill path")
    parser.add_argument("--output-dir", type=Path, help="Optional explicit output directory")
    args = parser.parse_args()

    runtime_dir = args.runtime_dir.expanduser().resolve()
    context_path = runtime_dir / "context" / "context.jsonl"
    if not context_path.exists():
        print(json.dumps({"status": "error", "error": f"context file not found: {context_path}"}, indent=2, ensure_ascii=False))
        return 1

    problemmap_root = resolve_problemmap_root(args.problemmap_root)
    diagnose_script = problemmap_root / "scripts" / "diagnose_session.py"
    emit_script = problemmap_root / "scripts" / "emit_problemmap_event.py"
    if not diagnose_script.exists() or not emit_script.exists():
        print(
            json.dumps(
                {
                    "status": "error",
                    "error": f"problemmap scripts not found under {problemmap_root}",
                },
                indent=2,
                ensure_ascii=False,
            )
        )
        return 1

    output_dir = (
        args.output_dir.expanduser().resolve()
        if args.output_dir
        else runtime_dir / "artifacts" / "problemmap" / args.task_id / args.worker_id
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    case_path = output_dir / "case.json"
    diagnosis_path = output_dir / "diagnosis.json"
    event_path = output_dir / "event.json"

    try:
        events = load_context(context_path)
        selected = filter_events(events, args.task_id, args.worker_id, args.manager_id, args.window)
        expected = pick_expected(selected, args.worker_id, args.manager_id, args.expected)
        actual = pick_actual(selected, args.worker_id)
        signals = infer_signals(selected, args.worker_id, expected, actual)
        case = build_case(selected, context_path, args.task_id, args.worker_id, expected, actual, signals)
        case_path.write_text(json.dumps(case, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

        diagnose_cmd = [
            sys.executable,
            str(diagnose_script),
            str(case_path),
            "--mode",
            args.mode,
            "--output",
            str(diagnosis_path),
        ]
        if args.ensure_upstream:
            diagnose_cmd.insert(-2, "--ensure-upstream")
        diagnosis = run_json_command(diagnose_cmd)

        event = run_json_command(
            [
                sys.executable,
                str(emit_script),
                str(diagnosis_path),
                "--output",
                str(event_path),
            ]
        )
    except (CommandError, OSError, ValueError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "error", "error": str(exc)}, indent=2, ensure_ascii=False))
        return 1

    summary = {
        "status": "ok",
        "task_id": args.task_id,
        "worker_id": args.worker_id,
        "signals": signals,
        "diagnosis": {
            "primary_family": diagnosis.get("atlas", {}).get("primary_family"),
            "confidence": diagnosis.get("atlas", {}).get("confidence"),
            "fix_surface_direction": diagnosis.get("atlas", {}).get("fix_surface_direction"),
            "misrepair_risk": diagnosis.get("atlas", {}).get("misrepair_risk"),
        },
        "writeback_gate": event.get("writeback_gate"),
        "paths": {
            "case": str(case_path),
            "diagnosis": str(diagnosis_path),
            "event": str(event_path),
        },
    }
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
