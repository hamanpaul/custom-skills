#!/usr/bin/env python3
"""Run one self-evolve cycle for this repository."""

from __future__ import annotations

import atexit
import argparse
from collections import Counter, defaultdict
import html
import importlib.util
import json
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


ALLOWED_COMMIT_PREFIXES = (".agents",)
MANAGED_RULES_SECTION_TITLE = "## 6. 自主維護規則（agent-managed）"
MANAGED_RULES_BEGIN = "<!-- self-evolve-managed-rules:start -->"
MANAGED_RULES_END = "<!-- self-evolve-managed-rules:end -->"
MANAGED_RULE_LINE = re.compile(r"^\s*-\s*\[(?P<event>[^\]]+)\]\s*(?P<text>.+?)\s*$")
SKILL_MANAGED_SECTION_TITLE = "## 自主維護知識（agent-managed）"
SKILL_MANAGED_BEGIN = "<!-- self-evolve-managed-knowledge:start -->"
SKILL_MANAGED_END = "<!-- self-evolve-managed-knowledge:end -->"
ROUTING_CONFIG_NAME = "session-topic-routing.json"
GLOBAL_EVENT_DEFAULTS = {
    "turn_aborted",
    "context_compacted",
    "agent_reasoning",
    "task_complete",
    "task_started",
    "token_count",
    "user_message",
    "wrong_approach",
    "misunderstood_request",
    "buggy_code",
    "excessive_changes",
}
PATH_TOKEN_RE = re.compile(r"(?:~|/)[A-Za-z0-9._/\-]+|(?:[A-Za-z0-9._-]+/)+[A-Za-z0-9._-]+")
WIKI_LINK_RE = re.compile(r"\[\[([A-Za-z0-9._/\-]+)\]\]")
SKILL_RELATION_FIELDS = ("related", "depends_on", "used_with", "anti_patterns")
SKILL_LINK_SCORES = {
    "depends_on": 0.92,
    "used_with": 0.80,
    "related": 0.70,
    "anti_patterns": 0.55,
    "wiki_link": 0.65,
}
DEFAULT_CARD_LINK_LIMIT = 2
DEFAULT_CARD_MIN_CONFIDENCE = 0.60
PROBLEMMAP_BRIDGE_DEFAULTS = {
    "enabled": False,
    "skill_id": "problemmap",
    "event_types": [],
    "max_cases_per_event": 50,
    "mode": "strict",
    "ensure_upstream": True,
}
SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_CONFIG_FILE = Path.home() / ".agents" / "config" / "self-evolve.json"


@dataclass
class CmdResult:
    returncode: int
    stdout: str
    stderr: str


def _run(
    cmd: list[str],
    cwd: Path,
    check: bool = False,
    timeout_sec: int | None = None,
) -> CmdResult:
    try:
        proc = subprocess.run(
            cmd,
            cwd=str(cwd),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
            timeout=timeout_sec,
        )
        result = CmdResult(proc.returncode, proc.stdout, proc.stderr)
    except FileNotFoundError:
        result = CmdResult(127, "", f"command not found: {cmd[0]}")
    except PermissionError:
        result = CmdResult(126, "", f"permission denied: {cmd[0]}")
    except subprocess.TimeoutExpired:
        result = CmdResult(124, "", f"command timeout after {timeout_sec} seconds")
    if check and result.returncode != 0:
        raise RuntimeError(f"command failed: {' '.join(cmd)}\n{result.stderr.strip()}")
    return result


def _load_config_payload(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"invalid config JSON at {path}: {exc}") from exc

    if not isinstance(payload, dict):
        raise RuntimeError(f"invalid config JSON at {path}: root must be an object")

    scoped = payload.get("self_evolve")
    if isinstance(scoped, dict):
        payload = scoped

    if not isinstance(payload, dict):
        raise RuntimeError(f"invalid config JSON at {path}: self_evolve must be an object")
    return payload


def _to_bool_value(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)
    if isinstance(value, str):
        text = value.strip().lower()
        if text in {"1", "true", "yes", "on"}:
            return True
        if text in {"0", "false", "no", "off"}:
            return False
    raise ValueError(f"invalid boolean value: {value!r}")


def _normalize_config_defaults(
    parser: argparse.ArgumentParser,
    raw: dict[str, Any],
) -> tuple[dict[str, Any], list[str]]:
    action_by_dest = {
        action.dest: action for action in parser._actions if action.dest not in {"help"}
    }
    defaults: dict[str, Any] = {}
    unknown_keys: list[str] = []

    for key, raw_value in raw.items():
        dest = key.replace("-", "_")
        action = action_by_dest.get(dest)
        if action is None:
            unknown_keys.append(key)
            continue

        value = raw_value
        try:
            if isinstance(action, argparse._StoreTrueAction) or isinstance(
                action, argparse._StoreFalseAction
            ):
                value = _to_bool_value(raw_value)
            elif action.type is not None and raw_value is not None:
                value = action.type(raw_value)
        except (TypeError, ValueError) as exc:
            raise RuntimeError(
                f"invalid config value for {key}: {raw_value!r}"
            ) from exc

        if action.choices and value not in action.choices:
            raise RuntimeError(
                f"invalid config value for {key}: {value!r} (choices: {list(action.choices)})"
            )
        defaults[dest] = value

    return defaults, unknown_keys


def _now_utc() -> datetime:
    return datetime.now(tz=UTC)


def _stamp(now: datetime) -> str:
    return now.strftime("%Y%m%d-%H%M%S")


def _has_git_repo(root: Path) -> bool:
    return (root / ".git").exists()


def _parse_iso(ts: str) -> datetime | None:
    try:
        return datetime.fromisoformat(ts.replace("Z", "+00:00")).astimezone(UTC)
    except ValueError:
        return None


def _within_allowed(path_str: str) -> bool:
    normalized = path_str.strip("/")
    return any(
        normalized == prefix or normalized.startswith(prefix + "/")
        for prefix in ALLOWED_COMMIT_PREFIXES
    )


def _git_status_paths(root: Path) -> set[str]:
    res = _run(["git", "status", "--porcelain"], cwd=root, check=True)
    changed: set[str] = set()
    for line in res.stdout.splitlines():
        if not line:
            continue
        payload = line[3:]
        if " -> " in payload:
            payload = payload.split(" -> ", 1)[1]
        if payload:
            changed.add(payload.strip())
    return changed


def _sync_repo(root: Path, topic: str) -> dict[str, Any]:
    if not _has_git_repo(root):
        return {"ok": True, "mode": "no_git", "maintenance_branch": None}

    pull = _run(["git", "pull", "--ff-only"], cwd=root)
    if pull.returncode == 0:
        return {"ok": True, "mode": "pull", "maintenance_branch": None}

    fetch = _run(["git", "fetch", "--all", "--prune"], cwd=root)
    if fetch.returncode == 0:
        return {"ok": True, "mode": "fetch", "maintenance_branch": None}

    branch = f"maintenance/{topic}-{_stamp(_now_utc())}"
    checkout = _run(["git", "checkout", "-b", branch], cwd=root)
    return {
        "ok": False,
        "mode": "failed",
        "maintenance_branch": branch if checkout.returncode == 0 else None,
        "pull_error": pull.stderr.strip(),
        "fetch_error": fetch.stderr.strip(),
        "checkout_error": checkout.stderr.strip(),
    }


def _run_project_insights(
    runtime_cwd: Path,
    sessions_root: Path,
    out_path: Path,
    short_days: int,
    long_days: int,
    half_life_days: int,
) -> None:
    script = SCRIPT_DIR / "project_insights.py"
    cmd = [
        sys.executable,
        str(script),
        "--sessions-root",
        str(sessions_root),
        "--short-days",
        str(short_days),
        "--long-days",
        str(long_days),
        "--half-life-days",
        str(half_life_days),
        "--out",
        str(out_path),
    ]
    _run(cmd, cwd=runtime_cwd, check=True)


def _run_lesson_report(runtime_cwd: Path, sessions_root: Path, out_path: Path) -> None:
    script = SCRIPT_DIR / "lesson_report.py"
    cmd = [
        sys.executable,
        str(script),
        "--sessions-root",
        str(sessions_root),
        "--out",
        str(out_path),
    ]
    _run(cmd, cwd=runtime_cwd, check=True)


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _load_state(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"updated_at": None, "rules": {}}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"updated_at": None, "rules": {}}
    if not isinstance(data, dict):
        return {"updated_at": None, "rules": {}}
    if "rules" not in data or not isinstance(data["rules"], dict):
        data["rules"] = {}
    return data


def _safe_rule_state(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "add_streak": int(row.get("add_streak", 0)),
        "remove_streak": int(row.get("remove_streak", 0)),
        "last_applied_at": row.get("last_applied_at"),
        "last_score": float(row.get("last_score", 0.0)),
    }


def _cooldown_ready(last_applied_at: str | None, now: datetime, cooldown_days: int) -> bool:
    if not last_applied_at:
        return True
    parsed = _parse_iso(last_applied_at)
    if not parsed:
        return True
    age_days = (now - parsed).total_seconds() / 86400.0
    return age_days >= cooldown_days


def _evaluate_thresholds(
    state: dict[str, Any],
    rows: list[dict[str, Any]],
    now: datetime,
    add_threshold: float,
    remove_threshold: float,
    add_required: int,
    remove_required: int,
    cooldown_days: int,
    max_changes: int,
) -> dict[str, Any]:
    proposals: list[dict[str, Any]] = []
    skipped_by_cooldown: list[dict[str, Any]] = []
    updated_rules = state.get("rules", {})

    for row in rows:
        event_type = str(row.get("event_type", "")).strip()
        if not event_type:
            continue
        score = float(row.get("score", 0.0))
        rule = _safe_rule_state(updated_rules.get(event_type, {}))

        if score >= add_threshold:
            rule["add_streak"] += 1
        else:
            rule["add_streak"] = 0

        if score <= remove_threshold:
            rule["remove_streak"] += 1
        else:
            rule["remove_streak"] = 0

        action: str | None = None
        reason = ""
        if rule["add_streak"] >= add_required:
            action = "add"
            reason = f"score >= {add_threshold} for {add_required} cycles"
        elif rule["remove_streak"] >= remove_required:
            action = "remove"
            reason = f"score <= {remove_threshold} for {remove_required} cycles"

        if action:
            if _cooldown_ready(rule["last_applied_at"], now, cooldown_days):
                if len(proposals) < max_changes:
                    proposal = {
                        "event_type": event_type,
                        "action": action,
                        "score": round(score, 4),
                        "reason": reason,
                        "cooldown_days": cooldown_days,
                    }
                    proposals.append(proposal)
                    rule["last_applied_at"] = now.isoformat()
                    if action == "add":
                        rule["add_streak"] = 0
                    else:
                        rule["remove_streak"] = 0
            else:
                skipped_by_cooldown.append(
                    {
                        "event_type": event_type,
                        "action": action,
                        "score": round(score, 4),
                        "reason": reason,
                    }
                )

        rule["last_score"] = round(score, 4)
        updated_rules[event_type] = rule

    state["rules"] = updated_rules
    state["updated_at"] = now.isoformat()
    return {"state": state, "proposals": proposals, "skipped_by_cooldown": skipped_by_cooldown}


def _to_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _to_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _rows_by_event(rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for row in rows:
        if not isinstance(row, dict):
            continue
        event_type = str(row.get("event_type", "")).strip()
        if event_type:
            out[event_type] = row
    return out


def _time_weight_payload(row: dict[str, Any], half_life_days: int) -> dict[str, Any]:
    return {
        "half_life_days": int(half_life_days),
        "short_score": round(_to_float(row.get("short_weighted", 0.0), 0.0), 4),
        "long_score": round(_to_float(row.get("long_weighted", 0.0), 0.0), 4),
        "severity_score": round(_to_float(row.get("severity", 0.0), 0.0), 4),
        "weighted_score": round(_to_float(row.get("score", 0.0), 0.0), 4),
    }


def _extract_paths_from_text(text: str) -> set[str]:
    out: set[str] = set()
    for token in PATH_TOKEN_RE.findall(text):
        value = str(token).strip().strip(",.;:()[]{}<>\"'")
        if not value:
            continue
        if "/" not in value:
            continue
        if value.startswith("//"):
            continue
        out.add(value)
    return out


def _collect_commands_from_obj(obj: Any, out: set[str]) -> None:
    if isinstance(obj, dict):
        for key, value in obj.items():
            key_text = str(key).strip().lower()
            if isinstance(value, str) and key_text in {
                "cmd",
                "command",
                "shell_command",
                "bash",
                "script",
                "argv",
            }:
                cmd = " ".join(value.strip().split())
                if cmd:
                    out.add(cmd)
            else:
                _collect_commands_from_obj(value, out)
        return
    if isinstance(obj, list):
        for item in obj:
            _collect_commands_from_obj(item, out)


def _merge_sessions_roots(
    primary: Path,
    extras: list[Path],
    tmp_parent: Path,
) -> tuple[Path, Path | None]:
    """Merge multiple session roots into one directory via symlinks.

    Returns (effective_sessions_root, tmp_dir_or_None).
    If no extras are specified, returns (primary, None) with no temp dir.
    """
    if not extras:
        return primary, None
    merged = Path(tempfile.mkdtemp(prefix="evolve-merged-", dir=tmp_parent))
    seen: set[str] = set()
    for root in [primary] + extras:
        if not root.exists():
            continue
        for src in root.rglob("*.jsonl"):
            rel = src.relative_to(root)
            # prefix with root name to avoid collisions
            safe = f"{root.name}__{rel}"
            safe = safe.replace("/", "__")
            if safe in seen:
                continue
            seen.add(safe)
            dst = merged / safe
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.symlink_to(src)
    return merged, merged


def _collect_session_evidence(
    sessions_root: Path,
    tracked_events: set[str],
    max_sessions: int = 5,
    max_paths: int = 12,
    max_commands: int = 8,
) -> dict[str, dict[str, list[str]]]:
    evidence: dict[str, dict[str, set[str]]] = {}
    if not sessions_root.exists():
        return {}

    for path in sorted(sessions_root.rglob("*.jsonl")):
        session_id = path.stem
        session_events: set[str] = set()
        session_paths: set[str] = set()
        session_commands: set[str] = set()
        try:
            with path.open(encoding="utf-8", errors="replace") as f:
                for raw in f:
                    text = raw.strip()
                    if not text:
                        continue
                    row: dict[str, Any] | None = None
                    try:
                        loaded = json.loads(text)
                        if isinstance(loaded, dict):
                            row = loaded
                    except json.JSONDecodeError:
                        row = None

                    if row:
                        if row.get("type") == "event_msg":
                            payload = row.get("payload")
                            if isinstance(payload, dict):
                                event_type = str(payload.get("type", "")).strip()
                                if event_type and event_type in tracked_events:
                                    session_events.add(event_type)
                        _collect_commands_from_obj(row, session_commands)
                        json_text = json.dumps(row, ensure_ascii=False)
                        session_paths.update(_extract_paths_from_text(json_text))
                    else:
                        session_paths.update(_extract_paths_from_text(text))
        except OSError:
            continue

        for event_type in session_events:
            slot = evidence.setdefault(
                event_type,
                {"sample_sessions": set(), "related_paths": set(), "sample_commands": set()},
            )
            slot["sample_sessions"].add(session_id)
            slot["related_paths"].update(session_paths)
            slot["sample_commands"].update(session_commands)

    normalized: dict[str, dict[str, list[str]]] = {}
    for event_type, slot in evidence.items():
        samples = sorted(slot["sample_sessions"])[:max_sessions]
        paths = sorted(slot["related_paths"])[:max_paths]
        commands = sorted(slot["sample_commands"])[:max_commands]
        normalized[event_type] = {
            "sample_sessions": samples,
            "related_paths": paths,
            "sample_commands": commands,
        }
    return normalized


def _default_problemmap_bridge() -> dict[str, Any]:
    return {
        "enabled": bool(PROBLEMMAP_BRIDGE_DEFAULTS["enabled"]),
        "skill_id": str(PROBLEMMAP_BRIDGE_DEFAULTS["skill_id"]),
        "event_types": list(PROBLEMMAP_BRIDGE_DEFAULTS["event_types"]),
        "max_cases_per_event": int(PROBLEMMAP_BRIDGE_DEFAULTS["max_cases_per_event"]),
        "mode": str(PROBLEMMAP_BRIDGE_DEFAULTS["mode"]),
        "ensure_upstream": bool(PROBLEMMAP_BRIDGE_DEFAULTS["ensure_upstream"]),
    }


def _load_python_module(module_name: str, path: Path) -> Any:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"unable to load module spec from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _resolve_problemmap_bridge(
    routing: dict[str, Any],
    rows: list[dict[str, Any]],
) -> dict[str, Any]:
    base = _default_problemmap_bridge()
    raw = routing.get("problemmap_bridge", {})
    if isinstance(raw, dict):
        if "enabled" in raw:
            base["enabled"] = bool(raw.get("enabled", False))
        skill_id = _normalize_skill_id(str(raw.get("skill_id", base["skill_id"])).strip())
        if skill_id:
            base["skill_id"] = skill_id
        raw_events = raw.get("event_types")
        if isinstance(raw_events, list):
            cleaned = sorted(
                {
                    str(item).strip()
                    for item in raw_events
                    if isinstance(item, str) and str(item).strip()
                }
            )
            base["event_types"] = cleaned
        base["max_cases_per_event"] = max(0, _to_int(raw.get("max_cases_per_event"), base["max_cases_per_event"]))
        mode = str(raw.get("mode", base["mode"])).strip()
        if mode in {"strict", "teaching", "repair_preview", "compact"}:
            base["mode"] = mode
        base["ensure_upstream"] = bool(raw.get("ensure_upstream", base["ensure_upstream"]))

    if not base["enabled"]:
        return base

    if not base["event_types"]:
        derived: set[str] = set()
        for row in rows:
            if not isinstance(row, dict):
                continue
            event_type = str(row.get("event_type", "")).strip()
            if not event_type:
                continue
            target = _resolve_event_target(event_type, routing)
            if target["kind"] == "skill" and target["skill_id"] == base["skill_id"]:
                derived.add(event_type)
        base["event_types"] = sorted(derived)

    return base


def _run_problemmap_bridge(
    agents_root: Path,
    sessions_root: Path,
    routing: dict[str, Any],
    rows: list[dict[str, Any]],
    now: datetime,
    insights_dir: Path,
) -> dict[str, Any]:
    bridge = _resolve_problemmap_bridge(routing, rows)
    result: dict[str, Any] = {
        "enabled": bool(bridge.get("enabled", False)),
        "skill_id": str(bridge.get("skill_id", "")),
        "event_types": list(bridge.get("event_types", [])),
        "max_cases_per_event": int(bridge.get("max_cases_per_event", 0)),
        "mode": str(bridge.get("mode", "strict")),
        "ensure_upstream": bool(bridge.get("ensure_upstream", False)),
        "summary_report": None,
        "cases_report": None,
        "status": "disabled",
    }
    if not result["enabled"]:
        return result
    if not result["event_types"]:
        result["status"] = "no-target-events"
        return result
    if not sessions_root.exists():
        result["status"] = "sessions-root-missing"
        result["sessions_root"] = str(sessions_root)
        return result

    skill_root = agents_root / "skills" / "custom" / result["skill_id"]
    extract_path = skill_root / "scripts" / "extract_failure_case.py"
    diagnose_path = skill_root / "scripts" / "diagnose_session.py"
    emit_path = skill_root / "scripts" / "emit_problemmap_event.py"
    missing = [str(path) for path in [extract_path, diagnose_path, emit_path] if not path.exists()]
    if missing:
        result["status"] = "skill-missing"
        result["missing_paths"] = missing
        return result

    try:
        extract = _load_python_module(f"{result['skill_id']}_extract", extract_path)
        diagnose = _load_python_module(f"{result['skill_id']}_diagnose", diagnose_path)
        emit = _load_python_module(f"{result['skill_id']}_emit", emit_path)
        if result["ensure_upstream"]:
            diagnose.maybe_ensure_upstream(True)
    except Exception as exc:  # noqa: BLE001
        result["status"] = "bridge-load-error"
        result["error"] = str(exc)
        return result

    target_events = set(result["event_types"])
    per_event_counts: Counter[str] = Counter()
    per_session_counts: Counter[str] = Counter()
    cases: list[dict[str, Any]] = []

    max_cases_per_event = int(result["max_cases_per_event"])
    for path in sorted(sessions_root.rglob("*.jsonl")):
        try:
            records = extract.load_jsonl(path)
        except Exception:  # noqa: BLE001
            continue

        for idx, record in enumerate(records):
            event_type = extract.detect_failure_event_type(record)
            if event_type not in target_events:
                continue
            if max_cases_per_event > 0 and per_event_counts[event_type] >= max_cases_per_event:
                continue

            try:
                case = extract.extract_case_at_index(records, path, idx, event_type)
                diagnosis = diagnose.build_diagnosis(case, result["mode"])
                artifact = emit.build_artifact(diagnosis)
            except Exception as exc:  # noqa: BLE001
                cases.append(
                    {
                        "status": "error",
                        "source_session": str(path),
                        "source_session_name": path.name,
                        "anchor_index": idx,
                        "anchor_event_type": event_type,
                        "error": str(exc),
                    }
                )
                per_event_counts[event_type] += 1
                per_session_counts[path.name] += 1
                continue

            per_event_counts[event_type] += 1
            per_session_counts[path.name] += 1
            cases.append(
                {
                    "status": "ok",
                    "case": case,
                    "diagnosis": diagnosis,
                    "artifact": artifact,
                }
            )

        if max_cases_per_event > 0 and all(per_event_counts[event] >= max_cases_per_event for event in target_events):
            break

    primary_family_counts: Counter[str] = Counter()
    primary_family_by_event: dict[str, Counter[str]] = defaultdict(Counter)
    confidence_counts: Counter[str] = Counter()
    gate_counts: Counter[str] = Counter()
    gate_by_event: dict[str, Counter[str]] = defaultdict(Counter)
    pm1_top_counts: Counter[str] = Counter()
    pm1_by_event: dict[str, Counter[str]] = defaultdict(Counter)
    sample_cases: list[dict[str, Any]] = []
    error_cases: list[dict[str, Any]] = []

    for item in cases:
        if item.get("status") != "ok":
            error_cases.append(
                {
                    "source_session": item.get("source_session"),
                    "source_session_name": item.get("source_session_name"),
                    "anchor_index": item.get("anchor_index"),
                    "anchor_event_type": item.get("anchor_event_type"),
                    "error": item.get("error"),
                }
            )
            continue

        case = item["case"]
        diagnosis = item["diagnosis"]
        artifact = item["artifact"]
        event_type = str(case.get("anchor_event_type", "")).strip()
        primary_family = str(diagnosis.get("atlas", {}).get("primary_family", "")).strip() or "unresolved"
        primary_family_counts[primary_family] += 1
        primary_family_by_event[event_type][primary_family] += 1
        confidence = str(diagnosis.get("atlas", {}).get("confidence", "low")).strip() or "low"
        confidence_counts[confidence] += 1
        gate_allow = str(artifact.get("writeback_gate", {}).get("allow", False))
        gate_counts[gate_allow] += 1
        gate_by_event[event_type][gate_allow] += 1

        pm1_candidates = diagnosis.get("pm1_candidates", [])
        if isinstance(pm1_candidates, list) and pm1_candidates:
            top = pm1_candidates[0]
            label = str(top.get("label", "")).strip()
            try:
                number = int(top.get("number", 0))
            except (TypeError, ValueError):
                number = 0
            pm1_key = f"PM1-{number:02d} {label}".strip() if number else (label or "none")
        else:
            pm1_key = "none"
        pm1_top_counts[pm1_key] += 1
        pm1_by_event[event_type][pm1_key] += 1

        if len(sample_cases) < 12:
            sample_cases.append(
                {
                    "session": Path(str(case.get("source_session", ""))).name,
                    "anchor_index": case.get("anchor_index"),
                    "anchor_event_type": event_type,
                    "primary_family": primary_family,
                    "broken_invariant": diagnosis.get("atlas", {}).get("broken_invariant"),
                    "confidence": confidence,
                    "event_type": artifact.get("event_type"),
                    "writeback_allow": artifact.get("writeback_gate", {}).get("allow"),
                }
            )

    ts = _stamp(now)
    summary_report = insights_dir / f"problemmap-bridge-{ts}.json"
    cases_report = insights_dir / f"problemmap-bridge-cases-{ts}.json"
    summary_payload = {
        "generated_at": now.isoformat(),
        "status": "ok",
        "skill_id": result["skill_id"],
        "sessions_root": str(sessions_root),
        "event_types": sorted(target_events),
        "mode": result["mode"],
        "ensure_upstream": result["ensure_upstream"],
        "max_cases_per_event": max_cases_per_event,
        "cases_total": sum(1 for item in cases if item.get("status") == "ok"),
        "error_cases_total": len(error_cases),
        "sessions_with_cases": len(per_session_counts),
        "per_event_counts": dict(per_event_counts),
        "per_session_case_counts": dict(per_session_counts.most_common()),
        "primary_family_counts": dict(primary_family_counts.most_common()),
        "primary_family_by_event": {key: dict(value.most_common()) for key, value in primary_family_by_event.items()},
        "confidence_counts": dict(confidence_counts.most_common()),
        "writeback_gate_counts": dict(gate_counts.most_common()),
        "writeback_gate_by_event": {key: dict(value.most_common()) for key, value in gate_by_event.items()},
        "pm1_top_counts": dict(pm1_top_counts.most_common()),
        "pm1_by_event": {key: dict(value.most_common()) for key, value in pm1_by_event.items()},
        "sample_cases": sample_cases,
        "error_cases": error_cases[:10],
        "cases_report": str(cases_report),
    }
    summary_report.write_text(json.dumps(summary_payload, ensure_ascii=False, indent=2), encoding="utf-8")
    cases_report.write_text(json.dumps(cases, ensure_ascii=False, indent=2), encoding="utf-8")

    result.update(
        {
            "status": "ok",
            "summary_report": str(summary_report),
            "cases_report": str(cases_report),
            "cases_total": summary_payload["cases_total"],
            "error_cases_total": summary_payload["error_cases_total"],
            "sessions_with_cases": summary_payload["sessions_with_cases"],
            "per_event_counts": summary_payload["per_event_counts"],
            "primary_family_counts": summary_payload["primary_family_counts"],
            "writeback_gate_counts": summary_payload["writeback_gate_counts"],
        }
    )
    return result


def _build_topic_candidates(
    rows: list[dict[str, Any]],
    half_life_days: int,
    evidence_map: dict[str, dict[str, list[str]]],
) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        event_type = str(row.get("event_type", "")).strip()
        if not event_type:
            continue
        ev = evidence_map.get(event_type, {})
        out.append(
            {
                "topic_id": event_type,
                "signals": [event_type],
                "related_paths": list(ev.get("related_paths", [])),
                "evidence_count": _to_int(row.get("raw_count", 0), 0),
                "sample_sessions": list(ev.get("sample_sessions", [])),
                "sample_commands": list(ev.get("sample_commands", [])),
                "short_score": round(_to_float(row.get("short_weighted", 0.0), 0.0), 4),
                "long_score": round(_to_float(row.get("long_weighted", 0.0), 0.0), 4),
                "severity_score": round(_to_float(row.get("severity", 0.0), 0.0), 4),
                "weighted_score": round(_to_float(row.get("score", 0.0), 0.0), 4),
                "time_weight_used": _time_weight_payload(row, half_life_days),
            }
        )
    return out


def _build_skill_actions(
    decisions: list[dict[str, Any]],
    candidate_proposals: list[dict[str, Any]],
    rows: list[dict[str, Any]],
    routing: dict[str, Any],
    half_life_days: int,
) -> list[dict[str, Any]]:
    by_event = _rows_by_event(rows)
    proposal_map: dict[tuple[str, str], dict[str, Any]] = {}
    for item in candidate_proposals:
        event_type = str(item.get("event_type", "")).strip()
        action = str(item.get("action", "")).strip()
        if event_type and action:
            proposal_map[(event_type, action)] = item

    out: list[dict[str, Any]] = []
    for row in decisions:
        if not isinstance(row, dict):
            continue
        event_type = str(row.get("event_type", "")).strip()
        action = str(row.get("action", "")).strip()
        decision = str(row.get("decision", "")).strip().lower()
        reason = str(row.get("reason", "")).strip() or "no reason provided"
        if not event_type or action not in {"add", "remove"}:
            continue

        target = _resolve_event_target(event_type, routing)
        target_skill = "AGENTS.md#self-evolve-managed-rules"
        if target["kind"] == "skill":
            target_skill = f"skills/custom/{target['skill_id']}/SKILL.md"

        normalized_action = "skip"
        if decision == "accept":
            normalized_action = "update" if action == "add" else "remove"

        proposal = proposal_map.get((event_type, action), {})
        row_score = by_event.get(event_type, {})
        out.append(
            {
                "topic_id": event_type,
                "target_skill": target_skill,
                "action": normalized_action,
                "reason": reason,
                "confidence": round(_to_float(proposal.get("score", 0.0), 0.0), 4),
                "time_weight_used": _time_weight_payload(row_score, half_life_days),
            }
        )
    return out


def _skill_id_from_target_skill(target_skill: str) -> str:
    text = target_skill.strip()
    if not text:
        return ""
    parts = [x for x in text.split("/") if x]
    if len(parts) >= 4 and parts[0] == "skills" and parts[1] == "custom":
        return _normalize_skill_id(parts[2])
    return ""


def _card_id(skill_id: str, topic_id: str) -> str:
    return f"{skill_id}--{_slug(topic_id)}"


def _normalize_relation_token(raw: str) -> str:
    token = raw.strip().strip("`\"'")
    if not token:
        return ""
    if token.startswith("[[") and token.endswith("]]"):
        token = token[2:-2].strip()
    low = token.lower()
    if low.startswith("skill:"):
        token = token.split(":", 1)[1].strip()
    token = token.replace("\\", "/").strip()
    if token.endswith("/SKILL.md"):
        token = token[: -len("/SKILL.md")]
    if token.endswith(".md"):
        token = token[:-3]
    token = token.rstrip("/")
    if "/" in token:
        token = token.split("/")[-1]
    return _normalize_skill_id(token)


def _dedupe_sorted(values: list[str]) -> list[str]:
    return sorted({x for x in values if x})


def _parse_frontmatter_relations(text: str) -> dict[str, list[str]]:
    result: dict[str, list[str]] = {key: [] for key in SKILL_RELATION_FIELDS}
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return result

    end_idx = None
    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            end_idx = idx
            break
    if end_idx is None:
        return result

    current_key = ""
    for line in lines[1:end_idx]:
        stripped = line.strip()
        if not stripped:
            continue
        m = re.match(r"^(related|depends_on|used_with|anti_patterns)\s*:\s*(.*)$", stripped)
        if m:
            current_key = m.group(1)
            raw_value = m.group(2).strip()
            if raw_value.startswith("[") and raw_value.endswith("]"):
                inner = raw_value[1:-1].strip()
                if inner:
                    for item in inner.split(","):
                        token = _normalize_relation_token(item)
                        if token:
                            result[current_key].append(token)
            elif raw_value:
                token = _normalize_relation_token(raw_value)
                if token:
                    result[current_key].append(token)
            continue

        if current_key and stripped.startswith("-"):
            token = _normalize_relation_token(stripped[1:])
            if token:
                result[current_key].append(token)

    for key in SKILL_RELATION_FIELDS:
        result[key] = _dedupe_sorted(result[key])
    return result


def _extract_wiki_links(text: str) -> list[str]:
    links: list[str] = []
    for raw in WIKI_LINK_RE.findall(text):
        token = _normalize_relation_token(raw)
        if token:
            links.append(token)
    return _dedupe_sorted(links)


def _load_skill_relations(skill_path: Path) -> dict[str, list[str]]:
    result: dict[str, list[str]] = {key: [] for key in SKILL_RELATION_FIELDS}
    result["wiki_links"] = []
    if not skill_path.exists():
        return result
    try:
        text = skill_path.read_text(encoding="utf-8")
    except OSError:
        return result

    frontmatter = _parse_frontmatter_relations(text)
    for key in SKILL_RELATION_FIELDS:
        result[key] = frontmatter.get(key, [])
    result["wiki_links"] = _extract_wiki_links(text)
    return result


def _build_skill_cards(
    skill_actions_rows: list[dict[str, Any]],
    evidence_map: dict[str, dict[str, list[str]]],
    agents_root: Path,
    now: datetime,
) -> dict[str, Any]:
    cards: list[dict[str, Any]] = []
    action_card_map: dict[tuple[str, str], str] = {}
    cards_by_skill: dict[str, list[str]] = {}

    for item in skill_actions_rows:
        if not isinstance(item, dict):
            continue
        target_skill = str(item.get("target_skill", "")).strip()
        skill_id = _skill_id_from_target_skill(target_skill)
        topic_id = str(item.get("topic_id", "")).strip()
        if not skill_id or not topic_id:
            continue

        card_id = _card_id(skill_id, topic_id)
        skill_path = agents_root / target_skill
        existed_before = skill_path.exists()
        action = str(item.get("action", "skip")).strip() or "skip"
        if action == "update" and not existed_before:
            action = "create"

        evidence = evidence_map.get(topic_id, {})
        relations = _load_skill_relations(skill_path)
        card = {
            "card_id": card_id,
            "skill_id": skill_id,
            "topic_id": topic_id,
            "target_skill": target_skill,
            "skill_file": str(skill_path),
            "action": action,
            "confidence": round(_to_float(item.get("confidence", 0.0), 0.0), 4),
            "time_weight_used": item.get("time_weight_used", {}),
            "sample_sessions": list(evidence.get("sample_sessions", [])),
            "related_paths": list(evidence.get("related_paths", [])),
            "sample_commands": list(evidence.get("sample_commands", [])),
            "trigger": f"當任務涉及 `{topic_id}` 主題時使用。",
            "input": ["session_evidence", "related_paths", "sample_commands"],
            "flow": ["baseline", "capture", "verify"],
            "output": ["commands_run", "artifacts", "key_findings", "next_actions"],
            "relation_hints": relations,
            "generated_at": now.isoformat(),
            "existed_before": existed_before,
        }
        cards.append(card)
        action_card_map[(topic_id, target_skill)] = card_id
        cards_by_skill.setdefault(skill_id, []).append(card_id)

    for key in list(cards_by_skill):
        cards_by_skill[key] = sorted(set(cards_by_skill[key]))

    return {
        "rows": cards,
        "action_card_map": action_card_map,
        "cards_by_skill": cards_by_skill,
    }


def _build_skill_links(skill_cards: list[dict[str, Any]], cards_by_skill: dict[str, list[str]]) -> list[dict[str, Any]]:
    primary_card_by_skill: dict[str, str] = {}
    for skill_id, card_ids in cards_by_skill.items():
        if card_ids:
            primary_card_by_skill[skill_id] = sorted(card_ids)[0]

    links: list[dict[str, Any]] = []
    seen: set[tuple[str, str, str, str]] = set()
    for card in skill_cards:
        from_card = str(card.get("card_id", "")).strip()
        from_skill_id = str(card.get("skill_id", "")).strip()
        relation_hints = card.get("relation_hints", {})
        if not from_card or not from_skill_id or not isinstance(relation_hints, dict):
            continue

        for relation_type in (*SKILL_RELATION_FIELDS, "wiki_links"):
            raw_targets = relation_hints.get(relation_type, [])
            if not isinstance(raw_targets, list):
                continue
            mapped_relation = "wiki_link" if relation_type == "wiki_links" else relation_type
            score = SKILL_LINK_SCORES.get(mapped_relation, 0.6)
            for raw_target in raw_targets:
                target_skill_id = _normalize_skill_id(str(raw_target))
                if not target_skill_id or target_skill_id == from_skill_id:
                    continue
                target_card = primary_card_by_skill.get(target_skill_id, "")
                dedupe_key = (from_card, target_skill_id, mapped_relation, target_card)
                if dedupe_key in seen:
                    continue
                seen.add(dedupe_key)
                links.append(
                    {
                        "from_card": from_card,
                        "from_skill_id": from_skill_id,
                        "to_skill_id": target_skill_id,
                        "to_card": target_card,
                        "target_exists": bool(target_card),
                        "relation_type": mapped_relation,
                        "score": round(score, 4),
                        "evidence": [f"{mapped_relation}:{target_skill_id}"],
                    }
                )

    links.sort(
        key=lambda row: (
            str(row.get("from_card", "")),
            -_to_float(row.get("score", 0.0), 0.0),
            str(row.get("relation_type", "")),
            str(row.get("to_skill_id", "")),
        )
    )
    return links


def _attach_linked_cards(
    skill_actions_rows: list[dict[str, Any]],
    action_card_map: dict[tuple[str, str], str],
    skill_links: list[dict[str, Any]],
    card_link_limit: int,
    card_min_confidence: float,
) -> list[dict[str, Any]]:
    card_links: dict[str, list[dict[str, Any]]] = {}
    for row in skill_links:
        from_card = str(row.get("from_card", "")).strip()
        to_card = str(row.get("to_card", "")).strip()
        score = _to_float(row.get("score", 0.0), 0.0)
        if not from_card or not to_card:
            continue
        if score < card_min_confidence:
            continue
        card_links.setdefault(from_card, []).append(row)

    for from_card, rows in card_links.items():
        rows.sort(
            key=lambda row: (
                -_to_float(row.get("score", 0.0), 0.0),
                str(row.get("relation_type", "")),
                str(row.get("to_card", "")),
            )
        )

    enriched_rows: list[dict[str, Any]] = []
    max_links = max(0, int(card_link_limit))
    for row in skill_actions_rows:
        if not isinstance(row, dict):
            continue
        topic_id = str(row.get("topic_id", "")).strip()
        target_skill = str(row.get("target_skill", "")).strip()
        primary_card = action_card_map.get((topic_id, target_skill), "")

        enriched = dict(row)
        enriched["primary_card"] = primary_card
        linked_cards: list[dict[str, Any]] = []
        if primary_card and max_links > 0:
            for link in card_links.get(primary_card, [])[:max_links]:
                linked_cards.append(
                    {
                        "card_id": str(link.get("to_card", "")),
                        "skill_id": str(link.get("to_skill_id", "")),
                        "relation_type": str(link.get("relation_type", "")),
                        "score": round(_to_float(link.get("score", 0.0), 0.0), 4),
                    }
                )
        enriched["linked_cards"] = linked_cards
        enriched_rows.append(enriched)
    return enriched_rows


def _build_multi_agent_skill_pipeline(
    routed_skill_rules: list[dict[str, Any]],
    evidence_map: dict[str, dict[str, list[str]]],
    now: datetime,
) -> dict[str, Any]:
    planner_tasks: list[dict[str, Any]] = []
    for row in routed_skill_rules:
        skill_id = str(row.get("target_skill_id", "")).strip()
        event_type = str(row.get("event_type", "")).strip()
        if skill_id and event_type:
            planner_tasks.append({"skill_id": skill_id, "event_type": event_type})

    extractor_rows: list[dict[str, Any]] = []
    for task in planner_tasks:
        event_type = task["event_type"]
        evidence = evidence_map.get(event_type, {})
        extractor_rows.append(
            {
                "skill_id": task["skill_id"],
                "event_type": event_type,
                "sample_sessions": list(evidence.get("sample_sessions", [])),
                "related_paths": list(evidence.get("related_paths", [])),
                "sample_commands": list(evidence.get("sample_commands", [])),
            }
        )

    reviewed = [
        {
            "skill_id": row["skill_id"],
            "event_type": row["event_type"],
            "status": "approved",
        }
        for row in extractor_rows
    ]

    return {
        "mode": "multi-agent",
        "generated_at": now.isoformat(),
        "agents": [
            {"id": "skill-planner", "role": "plan skill tasks from routed accepts"},
            {"id": "evidence-extractor", "role": "extract session evidence by topic"},
            {"id": "skill-author", "role": "prepare skill updates from evidence"},
            {"id": "skill-reviewer", "role": "validate managed skill updates"},
        ],
        "steps": [
            {"agent": "skill-planner", "status": "done", "tasks": planner_tasks},
            {"agent": "evidence-extractor", "status": "done", "rows": extractor_rows},
            {"agent": "skill-author", "status": "done", "count": len(extractor_rows)},
            {"agent": "skill-reviewer", "status": "done", "rows": reviewed},
        ],
    }


def _slug(text: str) -> str:
    normalized = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return normalized or "general"


def _normalize_skill_id(raw: str) -> str:
    text = raw.strip()
    if not text:
        return ""
    return _slug(text.replace("_", "-"))


def _routing_config_path(agents_root: Path) -> Path:
    return agents_root / "routing" / ROUTING_CONFIG_NAME


def _load_routing_config(agents_root: Path) -> dict[str, Any]:
    path = _routing_config_path(agents_root)
    result: dict[str, Any] = {
        "path": str(path),
        "source": "default",
        "global_events": sorted(GLOBAL_EVENT_DEFAULTS),
        "topic_overrides": {},
        "card_link_limit": DEFAULT_CARD_LINK_LIMIT,
        "card_min_confidence": DEFAULT_CARD_MIN_CONFIDENCE,
        "problemmap_bridge": _default_problemmap_bridge(),
    }
    if not path.exists():
        return result

    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        result["source"] = "invalid"
        return result

    if not isinstance(payload, dict):
        result["source"] = "invalid"
        return result

    global_events = payload.get("global_events")
    if isinstance(global_events, list):
        cleaned = sorted(
            {
                str(x).strip()
                for x in global_events
                if isinstance(x, str) and str(x).strip()
            }
        )
        if cleaned:
            result["global_events"] = cleaned

    overrides = payload.get("topic_overrides")
    if isinstance(overrides, dict):
        cleaned_overrides: dict[str, str] = {}
        for key, value in overrides.items():
            event_type = str(key).strip()
            target = str(value).strip()
            if event_type and target:
                cleaned_overrides[event_type] = target
        result["topic_overrides"] = cleaned_overrides

    if "card_link_limit" in payload:
        value = _to_int(payload.get("card_link_limit"), DEFAULT_CARD_LINK_LIMIT)
        result["card_link_limit"] = max(0, value)

    if "card_min_confidence" in payload:
        value = _to_float(payload.get("card_min_confidence"), DEFAULT_CARD_MIN_CONFIDENCE)
        result["card_min_confidence"] = max(0.0, min(1.0, value))

    problemmap_bridge = payload.get("problemmap_bridge")
    if isinstance(problemmap_bridge, dict):
        cleaned = _default_problemmap_bridge()
        try:
            if "enabled" in problemmap_bridge:
                cleaned["enabled"] = _to_bool_value(problemmap_bridge.get("enabled"))
        except ValueError:
            cleaned["enabled"] = bool(PROBLEMMAP_BRIDGE_DEFAULTS["enabled"])
        skill_id = _normalize_skill_id(str(problemmap_bridge.get("skill_id", cleaned["skill_id"])).strip())
        if skill_id:
            cleaned["skill_id"] = skill_id
        event_types = problemmap_bridge.get("event_types")
        if isinstance(event_types, list):
            cleaned["event_types"] = sorted(
                {
                    str(item).strip()
                    for item in event_types
                    if isinstance(item, str) and str(item).strip()
                }
            )
        cleaned["max_cases_per_event"] = max(
            0,
            _to_int(problemmap_bridge.get("max_cases_per_event"), cleaned["max_cases_per_event"]),
        )
        mode = str(problemmap_bridge.get("mode", cleaned["mode"])).strip()
        if mode in {"strict", "teaching", "repair_preview", "compact"}:
            cleaned["mode"] = mode
        try:
            if "ensure_upstream" in problemmap_bridge:
                cleaned["ensure_upstream"] = _to_bool_value(problemmap_bridge.get("ensure_upstream"))
        except ValueError:
            cleaned["ensure_upstream"] = bool(PROBLEMMAP_BRIDGE_DEFAULTS["ensure_upstream"])
        result["problemmap_bridge"] = cleaned

    result["source"] = "file"
    return result


def _resolve_event_target(event_type: str, routing: dict[str, Any]) -> dict[str, str]:
    topic_overrides = routing.get("topic_overrides", {})
    if not isinstance(topic_overrides, dict):
        topic_overrides = {}

    global_events = routing.get("global_events", [])
    if not isinstance(global_events, list):
        global_events = []
    global_event_set = {
        str(x).strip()
        for x in global_events
        if isinstance(x, str) and str(x).strip()
    }

    override = str(topic_overrides.get(event_type, "")).strip()
    if override:
        low = override.lower()
        if low in {"global", "agents", "agents.md", "agents-rule", "agents-rules"}:
            return {"kind": "agents", "skill_id": "", "route_source": "override"}
        if low.startswith("skill:"):
            skill_id = _normalize_skill_id(low.split(":", 1)[1])
            return {"kind": "skill", "skill_id": skill_id, "route_source": "override"}
        skill_id = _normalize_skill_id(override)
        return {"kind": "skill", "skill_id": skill_id, "route_source": "override"}

    if event_type in global_event_set or event_type.startswith("global_"):
        return {"kind": "agents", "skill_id": "", "route_source": "default"}

    return {
        "kind": "skill",
        "skill_id": _normalize_skill_id(event_type),
        "route_source": "default",
    }


def _split_accepted_rules_by_target(
    accepted_rules: list[dict[str, Any]],
    routing: dict[str, Any],
) -> dict[str, list[dict[str, Any]]]:
    agents_rules: list[dict[str, Any]] = []
    skill_rules: list[dict[str, Any]] = []
    routed_rules: list[dict[str, Any]] = []

    for row in accepted_rules:
        event_type = str(row.get("event_type", "")).strip()
        if not event_type:
            continue
        target = _resolve_event_target(event_type, routing)
        enriched = dict(row)
        enriched["target_kind"] = target["kind"]
        enriched["target_skill_id"] = target["skill_id"]
        enriched["route_source"] = target["route_source"]
        if target["kind"] == "skill":
            enriched["target_skill"] = f"skills/custom/{target['skill_id']}/SKILL.md"
            skill_rules.append(enriched)
        else:
            enriched["target_skill"] = "AGENTS.md#self-evolve-managed-rules"
            agents_rules.append(enriched)
        routed_rules.append(enriched)

    return {
        "agents": agents_rules,
        "skills": skill_rules,
        "all": routed_rules,
    }


def _lesson_friction(lesson_payload: dict[str, Any] | None) -> dict[str, int]:
    if not lesson_payload or not isinstance(lesson_payload, dict):
        return {}
    report = lesson_payload.get("report")
    if not isinstance(report, dict):
        return {}
    friction = report.get("friction_signals")
    if not isinstance(friction, dict):
        return {}
    out: dict[str, int] = {}
    for key, value in friction.items():
        name = str(key).strip()
        if name:
            out[name] = _to_int(value, 0)
    return out


def _heuristic_decision(
    candidate_proposals: list[dict[str, Any]],
    rows: list[dict[str, Any]],
    lesson_payload: dict[str, Any] | None,
) -> dict[str, Any]:
    by_event = _rows_by_event(rows)
    friction = _lesson_friction(lesson_payload)
    accepted: list[dict[str, Any]] = []
    rejected: list[dict[str, Any]] = []
    decisions: list[dict[str, Any]] = []

    for proposal in candidate_proposals:
        event_type = str(proposal.get("event_type", "")).strip()
        action = str(proposal.get("action", "")).strip()
        row = by_event.get(event_type, {})
        raw_count = _to_int(row.get("raw_count", 0), 0)
        severity = _to_float(row.get("severity", 0.0), 0.0)
        score = _to_float(proposal.get("score", 0.0), 0.0)
        friction_count = _to_int(friction.get(event_type, 0), 0)

        accept = False
        reason = ""
        if action == "add":
            accept = (
                friction_count > 0
                or raw_count >= 2
                or severity >= 0.6
                or score >= 0.85
            )
            reason = (
                f"add gate: friction={friction_count}, raw_count={raw_count}, "
                f"severity={severity:.2f}, score={score:.2f}"
            )
        elif action == "remove":
            accept = raw_count == 0 and friction_count == 0 and score <= 0.15
            reason = (
                f"remove gate: friction={friction_count}, raw_count={raw_count}, "
                f"score={score:.2f}"
            )
        else:
            reason = f"unsupported action={action}"

        decision = "accept" if accept else "reject"
        enriched = dict(proposal)
        enriched["decision_reason"] = reason
        decisions.append(
            {
                "event_type": event_type,
                "action": action,
                "decision": decision,
                "reason": reason,
            }
        )
        if accept:
            accepted.append(enriched)
        else:
            rejected.append(enriched)

    return {
        "accepted_proposals": accepted,
        "rejected_proposals": rejected,
        "decisions": decisions,
    }


def _normalize_agent_decisions(payload: dict[str, Any]) -> dict[tuple[str, str], dict[str, str]]:
    if not isinstance(payload, dict):
        raise RuntimeError("agent output is not a JSON object")
    decisions = payload.get("decisions")
    if not isinstance(decisions, list):
        raise RuntimeError("agent output missing decisions list")

    normalized: dict[tuple[str, str], dict[str, str]] = {}
    for item in decisions:
        if not isinstance(item, dict):
            continue
        event_type = str(item.get("event_type", "")).strip()
        action = str(item.get("action", "")).strip()
        decision = str(item.get("decision", "")).strip().lower()
        reason = str(item.get("reason", "")).strip() or "no reason provided"
        if not event_type or not action:
            continue
        if decision not in {"accept", "reject", "defer"}:
            continue
        normalized[(event_type, action)] = {"decision": decision, "reason": reason}

    return normalized


def _build_decision_prompt(decision_input: dict[str, Any]) -> str:
    payload = json.dumps(decision_input, ensure_ascii=False, indent=2)
    return (
        "You are a strict rule-change reviewer for a self-evolve system.\n"
        "Decide each candidate rule change as accept/reject/defer.\n"
        "Return ONLY valid JSON with this exact schema:\n"
        '{"decisions":[{"event_type":"<string>","action":"add|remove","decision":"accept|reject|defer","reason":"<short reason>"}]}\n'
        "Rules:\n"
        "1) Keep event_type/action unchanged from candidates.\n"
        "2) Use reject when evidence is weak or stale.\n"
        "3) Use defer when uncertain but potentially useful.\n"
        "4) No markdown, no prose, no extra keys.\n"
        "Input data:\n"
        f"{payload}\n"
    )


def _extract_json_payload(raw_text: str) -> dict[str, Any]:
    text = html.unescape(raw_text or "").strip()
    if not text:
        raise RuntimeError("empty model output")

    text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s*```$", "", text, flags=re.IGNORECASE)
    text = re.sub(r"</?p[^>]*>", "", text, flags=re.IGNORECASE).strip()

    candidates = [text]
    decoder = json.JSONDecoder()
    for idx, ch in enumerate(text):
        if ch != "{":
            continue
        try:
            obj, end = decoder.raw_decode(text[idx:])
        except json.JSONDecodeError:
            continue
        if isinstance(obj, dict):
            candidates.append(text[idx : idx + end])
            break

    for candidate in candidates:
        try:
            payload = json.loads(candidate)
        except json.JSONDecodeError:
            continue
        if isinstance(payload, dict):
            return payload

    raise RuntimeError("cannot parse JSON from model output")


def _resolve_acp_command(
    provider: str,
    acp_copilot_bin: str,
    acp_copilot_config_dir: Path,
    acp_copilot_model: str,
    acp_codex_adapter_cmd: str,
    acp_gemini_bin: str,
    acp_gemini_model: str,
) -> list[str]:
    if provider == "copilot":
        resolved = acp_copilot_bin or shutil.which("copilot")
        if not resolved:
            raise RuntimeError("copilot binary not found for ACP")
        cmd = [resolved, "--acp", "--stdio"]
        if acp_copilot_config_dir:
            cmd.extend(["--config-dir", str(acp_copilot_config_dir)])
        if acp_copilot_model:
            cmd.extend(["--model", acp_copilot_model])
        return cmd

    if provider == "gemini":
        resolved = acp_gemini_bin or shutil.which("gemini")
        if not resolved:
            raise RuntimeError("gemini binary not found for ACP")
        cmd = [resolved, "--experimental-acp"]
        if acp_gemini_model:
            cmd.extend(["-m", acp_gemini_model])
        return cmd

    cmd = shlex.split(acp_codex_adapter_cmd)
    if not cmd:
        raise RuntimeError("codex ACP adapter command is empty")
    return cmd


def _resolve_acp_runtime(
    provider: str,
    acp_model: str | None,
    acp_reasoning: str | None,
    acp_copilot_model: str,
    acp_copilot_reasoning: str,
    acp_codex_model: str,
    acp_codex_reasoning: str,
    acp_gemini_model: str,
    acp_gemini_reasoning: str,
) -> tuple[str, str]:
    if provider == "copilot":
        model = acp_model or acp_copilot_model
        reasoning = acp_reasoning or acp_copilot_reasoning
        return model, reasoning
    if provider == "gemini":
        model = acp_model or acp_gemini_model
        reasoning = acp_reasoning or acp_gemini_reasoning
        return model, reasoning
    model = acp_model or acp_codex_model
    reasoning = acp_reasoning or acp_codex_reasoning
    return model, reasoning


def _run_acp_decision(
    runtime_cwd: Path,
    decision_input: dict[str, Any],
    provider: str,
    acp_node_bin: str,
    acp_timeout_sec: int,
    acp_model: str | None,
    acp_reasoning: str | None,
    acp_copilot_bin: str,
    acp_copilot_model: str,
    acp_copilot_reasoning: str,
    acp_copilot_config_dir: Path,
    acp_codex_adapter_cmd: str,
    acp_codex_model: str,
    acp_codex_reasoning: str,
    acp_gemini_bin: str,
    acp_gemini_model: str,
    acp_gemini_reasoning: str,
) -> dict[str, Any]:
    if acp_node_bin:
        if "/" in acp_node_bin:
            node_bin = acp_node_bin
        else:
            node_bin = shutil.which(acp_node_bin)
    else:
        node_bin = shutil.which("node")
    if not node_bin:
        raise RuntimeError("node binary not found for ACP router")

    script = SCRIPT_DIR / "acp_router_decision.mjs"
    if not script.exists():
        raise RuntimeError(f"ACP router script not found: {script}")

    command = _resolve_acp_command(
        provider=provider,
        acp_copilot_bin=acp_copilot_bin,
        acp_copilot_config_dir=acp_copilot_config_dir,
        acp_copilot_model=acp_copilot_model,
        acp_codex_adapter_cmd=acp_codex_adapter_cmd,
        acp_gemini_bin=acp_gemini_bin,
        acp_gemini_model=acp_gemini_model,
    )
    model, reasoning = _resolve_acp_runtime(
        provider=provider,
        acp_model=acp_model,
        acp_reasoning=acp_reasoning,
        acp_copilot_model=acp_copilot_model,
        acp_copilot_reasoning=acp_copilot_reasoning,
        acp_codex_model=acp_codex_model,
        acp_codex_reasoning=acp_codex_reasoning,
        acp_gemini_model=acp_gemini_model,
        acp_gemini_reasoning=acp_gemini_reasoning,
    )
    prompt = _build_decision_prompt(decision_input)

    with tempfile.TemporaryDirectory(prefix="self-evolve-acp-") as tds:
        td = Path(tds)
        request_path = td / "request.json"
        output_path = td / "output.json"
        request_path.write_text(
            json.dumps(
                {
                    "provider": provider,
                    "cwd": str(runtime_cwd),
                    "prompt": prompt,
                    "timeoutSec": max(1, acp_timeout_sec),
                    "command": command,
                    "model": model,
                    "reasoning": reasoning,
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        cmd = [
            node_bin,
            str(script),
            "--request",
            str(request_path),
            "--output",
            str(output_path),
        ]
        result = _run(cmd, cwd=runtime_cwd, timeout_sec=max(5, acp_timeout_sec + 30))
        if result.returncode != 0:
            err = result.stderr.strip() or result.stdout.strip() or "unknown ACP router error"
            raise RuntimeError(f"acp decision failed: {err}")

        if not output_path.exists():
            raise RuntimeError("acp router output file not found")
        payload = json.loads(output_path.read_text(encoding="utf-8"))
        if isinstance(payload, dict) and payload.get("error"):
            raise RuntimeError(str(payload.get("error")))
        raw = str(payload.get("assistant_output", ""))
        decision_payload = _extract_json_payload(raw)
        return {
            "backend": f"acp-{provider}",
            "raw": {"router_output": payload, "parsed": decision_payload},
            "decision_map": _normalize_agent_decisions(decision_payload),
            "command": command,
        }


def _run_agent_decision(
    runtime_cwd: Path,
    cmd_template: str,
    timeout_sec: int,
    decision_input: dict[str, Any],
) -> dict[str, Any]:
    if not cmd_template.strip():
        raise RuntimeError("agent command is empty")

    with tempfile.TemporaryDirectory(prefix="self-evolve-agent-") as tds:
        td = Path(tds)
        input_path = td / "decision-input.json"
        output_path = td / "decision-output.json"
        input_path.write_text(json.dumps(decision_input, ensure_ascii=False, indent=2), encoding="utf-8")

        cmd_text = cmd_template.format(
            input_json=str(input_path),
            output_json=str(output_path),
        )
        cmd = shlex.split(cmd_text)
        if not cmd:
            raise RuntimeError("agent command parsing produced empty argv")

        result = _run(cmd, cwd=runtime_cwd, timeout_sec=timeout_sec)
        if result.returncode != 0:
            err = result.stderr.strip() or result.stdout.strip() or "unknown error"
            raise RuntimeError(f"agent command failed: {err}")

        if not output_path.exists():
            raise RuntimeError("agent output file not found")

        try:
            payload = json.loads(output_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise RuntimeError("agent output is not valid JSON") from exc

        return {
            "raw": payload,
            "decision_map": _normalize_agent_decisions(payload),
            "command": cmd,
        }


def _apply_agent_decisions(
    candidate_proposals: list[dict[str, Any]],
    decision_map: dict[tuple[str, str], dict[str, str]],
) -> dict[str, Any]:
    accepted: list[dict[str, Any]] = []
    rejected: list[dict[str, Any]] = []
    decisions: list[dict[str, Any]] = []

    for proposal in candidate_proposals:
        event_type = str(proposal.get("event_type", "")).strip()
        action = str(proposal.get("action", "")).strip()
        key = (event_type, action)
        item = decision_map.get(key)

        if item is None:
            decision = "reject"
            reason = "missing decision from agent"
        else:
            decision = item.get("decision", "reject")
            reason = item.get("reason", "no reason provided")

        accepted_flag = decision == "accept"
        enriched = dict(proposal)
        enriched["decision_reason"] = reason
        decisions.append(
            {
                "event_type": event_type,
                "action": action,
                "decision": decision,
                "reason": reason,
            }
        )
        if accepted_flag:
            accepted.append(enriched)
        else:
            rejected.append(enriched)

    return {
        "accepted_proposals": accepted,
        "rejected_proposals": rejected,
        "decisions": decisions,
    }


def _decide_proposals(
    mode: str,
    runtime_cwd: Path,
    agent_cmd: str | None,
    agent_timeout_sec: int,
    acp_provider: str,
    acp_node_bin: str,
    acp_timeout_sec: int,
    acp_model: str | None,
    acp_reasoning: str | None,
    acp_copilot_bin: str,
    acp_copilot_model: str,
    acp_copilot_reasoning: str,
    acp_copilot_config_dir: Path,
    acp_codex_adapter_cmd: str,
    acp_codex_model: str,
    acp_codex_reasoning: str,
    acp_gemini_bin: str,
    acp_gemini_model: str,
    acp_gemini_reasoning: str,
    decision_input: dict[str, Any],
    candidate_proposals: list[dict[str, Any]],
    rows: list[dict[str, Any]],
    lesson_payload: dict[str, Any] | None,
) -> dict[str, Any]:
    resolved = mode
    if resolved == "copilot":
        resolved = "acp"
    if resolved == "auto":
        node_ready = bool(shutil.which(acp_node_bin or "node"))
        if not node_ready:
            resolved = "heuristic"
        else:
            try:
                _resolve_acp_command(
                    provider=acp_provider,
                    acp_copilot_bin=acp_copilot_bin,
                    acp_copilot_config_dir=acp_copilot_config_dir,
                    acp_copilot_model=acp_copilot_model,
                    acp_codex_adapter_cmd=acp_codex_adapter_cmd,
                    acp_gemini_bin=acp_gemini_bin,
                    acp_gemini_model=acp_gemini_model,
                )
                resolved = "acp"
            except RuntimeError:
                resolved = "heuristic"

    if resolved == "acp":
        try:
            acp = _run_acp_decision(
                runtime_cwd=runtime_cwd,
                decision_input=decision_input,
                provider=acp_provider,
                acp_node_bin=acp_node_bin,
                acp_timeout_sec=max(1, acp_timeout_sec),
                acp_model=acp_model,
                acp_reasoning=acp_reasoning,
                acp_copilot_bin=acp_copilot_bin,
                acp_copilot_model=acp_copilot_model,
                acp_copilot_reasoning=acp_copilot_reasoning,
                acp_copilot_config_dir=acp_copilot_config_dir,
                acp_codex_adapter_cmd=acp_codex_adapter_cmd,
                acp_codex_model=acp_codex_model,
                acp_codex_reasoning=acp_codex_reasoning,
                acp_gemini_bin=acp_gemini_bin,
                acp_gemini_model=acp_gemini_model,
                acp_gemini_reasoning=acp_gemini_reasoning,
            )
            applied = _apply_agent_decisions(
                candidate_proposals=candidate_proposals,
                decision_map=acp["decision_map"],
            )
            applied["mode"] = "acp"
            applied["error"] = None
            applied["agent"] = {
                "backend": acp["backend"],
                "command": " ".join(acp["command"]),
                "raw": acp["raw"],
            }
            return applied
        except RuntimeError as exc:
            heuristic = _heuristic_decision(
                candidate_proposals=candidate_proposals,
                rows=rows,
                lesson_payload=lesson_payload,
            )
            heuristic["mode"] = "heuristic_fallback"
            heuristic["error"] = str(exc)
            heuristic["agent"] = {"backend": "heuristic", "command": None, "raw": None}
            return heuristic

    if resolved == "agent":
        if not agent_cmd:
            resolved = "heuristic"
        else:
            try:
                agent = _run_agent_decision(
                    runtime_cwd=runtime_cwd,
                    cmd_template=agent_cmd,
                    timeout_sec=agent_timeout_sec,
                    decision_input=decision_input,
                )
                applied = _apply_agent_decisions(
                    candidate_proposals=candidate_proposals,
                    decision_map=agent["decision_map"],
                )
                applied["mode"] = "agent"
                applied["error"] = None
                applied["agent"] = {
                    "backend": "external-agent",
                    "command": " ".join(agent["command"]),
                    "raw": agent["raw"],
                }
                return applied
            except RuntimeError as exc:
                heuristic = _heuristic_decision(
                    candidate_proposals=candidate_proposals,
                    rows=rows,
                    lesson_payload=lesson_payload,
                )
                heuristic["mode"] = "heuristic_fallback"
                heuristic["error"] = str(exc)
                heuristic["agent"] = {
                    "backend": "heuristic",
                    "command": agent_cmd,
                    "raw": None,
                }
                return heuristic

    heuristic = _heuristic_decision(
        candidate_proposals=candidate_proposals,
        rows=rows,
        lesson_payload=lesson_payload,
    )
    heuristic["mode"] = "heuristic"
    heuristic["error"] = None
    heuristic["agent"] = {"backend": "heuristic", "command": None, "raw": None}
    return heuristic


def _rule_sentence(event_type: str, decision_reason: str) -> str:
    templates = {
        "turn_aborted": "收到可直接執行的明確需求時，優先實作並回報驗證結果，避免先輸出冗長規劃。",
        "context_compacted": "跨檔案或長流程任務先摘要既有結論，再進入下一步，降低上下文流失風險。",
        "agent_reasoning": "保持輸出可驗證且精簡，只保留會影響決策的證據與結論。",
        "task_complete": "任務完成後同步更新對應規範，避免同類型問題重複發生。",
    }
    base = templates.get(
        event_type,
        f"針對 `{event_type}` 類事件，採最小可驗證修改並同步更新規範。",
    )
    reason = decision_reason.strip()
    if reason and reason != "no reason provided":
        return f"{base} 依據：{reason}。"
    return base


def _render_managed_rules(order: list[str], rules: dict[str, str]) -> list[str]:
    lines = [MANAGED_RULES_SECTION_TITLE, MANAGED_RULES_BEGIN]
    for event_type in order:
        text = rules.get(event_type)
        if text:
            lines.append(f"- [{event_type}] {text}")
    lines.append(MANAGED_RULES_END)
    return lines


def _extract_managed_rules(block_lines: list[str]) -> tuple[list[str], dict[str, str]]:
    order: list[str] = []
    rules: dict[str, str] = {}
    for line in block_lines:
        m = MANAGED_RULE_LINE.match(line)
        if not m:
            continue
        event_type = m.group("event").strip()
        text = m.group("text").strip()
        if not event_type:
            continue
        if event_type not in rules:
            order.append(event_type)
        rules[event_type] = text
    return order, rules


def _skill_sentence(event_type: str, decision_reason: str) -> str:
    base = f"整理 `{event_type}` 主題的專業流程、關鍵指令與驗證步驟。"
    reason = decision_reason.strip()
    if reason and reason != "no reason provided":
        return f"{base} 依據：{reason}。"
    return base


def _render_managed_skill_rows(order: list[str], rows: dict[str, str]) -> list[str]:
    lines = [SKILL_MANAGED_SECTION_TITLE, SKILL_MANAGED_BEGIN]
    for event_type in order:
        text = rows.get(event_type)
        if text:
            lines.append(f"- [{event_type}] {text}")
    lines.append(SKILL_MANAGED_END)
    return lines


def _initial_skill_text(skill_id: str) -> str:
    return (
        "---\n"
        f"name: {skill_id}\n"
        "description: Auto-generated skill from self-evolve session analysis.\n"
        "---\n\n"
        f"# {skill_id}\n\n"
        "## Trigger\n"
        f"- 當任務涉及 `{skill_id}` 主題時使用。\n\n"
        "## Scope\n"
        "- 聚焦該領域的專業知識、命令與驗證流程。\n"
    )


def _integrate_rules_into_skill_file(
    skill_path: Path,
    skill_id: str,
    accepted_rules: list[dict[str, Any]],
    now: datetime,
) -> dict[str, Any]:
    skill_path.parent.mkdir(parents=True, exist_ok=True)
    if skill_path.exists():
        original = skill_path.read_text(encoding="utf-8")
    else:
        original = _initial_skill_text(skill_id)

    normalized = original.replace("\r\n", "\n")
    lines = normalized.split("\n")
    if lines and lines[-1] == "":
        lines = lines[:-1]

    start_idx: int | None = None
    end_idx: int | None = None
    for idx, line in enumerate(lines):
        s = line.strip()
        if s == SKILL_MANAGED_BEGIN and start_idx is None:
            start_idx = idx
        if s == SKILL_MANAGED_END:
            end_idx = idx
            break

    order: list[str] = []
    rows: dict[str, str] = {}
    if start_idx is not None and end_idx is not None and start_idx < end_idx:
        order, rows = _extract_managed_rules(lines[start_idx + 1 : end_idx])

    applied: list[dict[str, Any]] = []
    skipped: list[dict[str, Any]] = []
    for item in accepted_rules:
        event_type = str(item.get("event_type", "")).strip()
        action = str(item.get("action", "")).strip()
        if not event_type or action not in {"add", "remove"}:
            continue
        score = round(_to_float(item.get("score", 0.0), 0.0), 4)
        reason = str(item.get("decision_reason", "")).strip()
        if action == "add":
            existed = event_type in rows
            rows[event_type] = _skill_sentence(event_type, reason)
            if event_type not in order:
                order.append(event_type)
            applied.append(
                {
                    "event_type": event_type,
                    "action": action,
                    "status": "updated" if existed else "added",
                    "score": score,
                }
            )
            continue

        if event_type in rows:
            rows.pop(event_type, None)
            applied.append(
                {
                    "event_type": event_type,
                    "action": action,
                    "status": "removed",
                    "score": score,
                }
            )
        else:
            skipped.append(
                {
                    "event_type": event_type,
                    "action": action,
                    "status": "not_found",
                    "score": score,
                }
            )

    if not applied:
        return {
            "skill_id": skill_id,
            "skill_file": str(skill_path),
            "managed_rule_count": len(rows),
            "applied_count": 0,
            "skipped_count": len(skipped),
            "applied": [],
            "skipped": skipped,
            "updated": False,
            "updated_at": now.isoformat(),
        }

    managed_lines = _render_managed_skill_rows(order, rows)
    if start_idx is not None and end_idx is not None and start_idx < end_idx:
        block_start = start_idx
        if block_start > 0 and lines[block_start - 1].strip() == SKILL_MANAGED_SECTION_TITLE:
            block_start -= 1
        rebuilt = lines[:block_start]
        if rebuilt and rebuilt[-1].strip():
            rebuilt.append("")
        rebuilt.extend(managed_lines)
        tail = lines[end_idx + 1 :]
        if tail and tail[0].strip():
            rebuilt.append("")
        rebuilt.extend(tail)
    else:
        rebuilt = lines[:]
        if rebuilt and rebuilt[-1].strip():
            rebuilt.append("")
        rebuilt.extend(managed_lines)

    updated_text = ("\n".join(rebuilt).rstrip() + "\n") if rebuilt else ""
    changed = updated_text != normalized
    if changed:
        skill_path.write_text(updated_text, encoding="utf-8")

    return {
        "skill_id": skill_id,
        "skill_file": str(skill_path),
        "managed_rule_count": len(rows),
        "applied_count": len(applied),
        "skipped_count": len(skipped),
        "applied": applied,
        "skipped": skipped,
        "updated": changed,
        "updated_at": now.isoformat(),
    }


def _integrate_rules_into_skills(
    agents_root: Path,
    accepted_rules: list[dict[str, Any]],
    now: datetime,
) -> dict[str, Any]:
    by_skill: dict[str, list[dict[str, Any]]] = {}
    for item in accepted_rules:
        skill_id = _normalize_skill_id(str(item.get("target_skill_id", "")).strip())
        if not skill_id:
            continue
        by_skill.setdefault(skill_id, []).append(item)

    results: list[dict[str, Any]] = []
    for skill_id in sorted(by_skill):
        skill_path = agents_root / "skills" / "custom" / skill_id / "SKILL.md"
        result = _integrate_rules_into_skill_file(
            skill_path=skill_path,
            skill_id=skill_id,
            accepted_rules=by_skill[skill_id],
            now=now,
        )
        results.append(result)

    return {
        "skills_total": len(results),
        "skills_updated": sum(1 for x in results if x.get("updated")),
        "applied_count": sum(_to_int(x.get("applied_count", 0), 0) for x in results),
        "skipped_count": sum(_to_int(x.get("skipped_count", 0), 0) for x in results),
        "skills": results,
    }


def _integrate_rules_into_agents(
    agents_path: Path,
    accepted_rules: list[dict[str, Any]],
    now: datetime,
) -> dict[str, Any]:
    agents_path.parent.mkdir(parents=True, exist_ok=True)
    if agents_path.exists():
        original = agents_path.read_text(encoding="utf-8")
    else:
        original = "# AGENTS\n"

    normalized = original.replace("\r\n", "\n")
    lines = normalized.split("\n")
    if lines and lines[-1] == "":
        lines = lines[:-1]

    start_idx: int | None = None
    end_idx: int | None = None
    for idx, line in enumerate(lines):
        s = line.strip()
        if s == MANAGED_RULES_BEGIN and start_idx is None:
            start_idx = idx
        if s == MANAGED_RULES_END:
            end_idx = idx
            break

    order: list[str] = []
    rules: dict[str, str] = {}
    if start_idx is not None and end_idx is not None and start_idx < end_idx:
        order, rules = _extract_managed_rules(lines[start_idx + 1 : end_idx])

    applied: list[dict[str, Any]] = []
    skipped: list[dict[str, Any]] = []
    for item in accepted_rules:
        event_type = str(item.get("event_type", "")).strip()
        action = str(item.get("action", "")).strip()
        if not event_type or action not in {"add", "remove"}:
            continue

        score = round(_to_float(item.get("score", 0.0), 0.0), 4)
        reason = str(item.get("decision_reason", "")).strip()

        if action == "add":
            existed = event_type in rules
            rules[event_type] = _rule_sentence(event_type, reason)
            if event_type not in order:
                order.append(event_type)
            applied.append(
                {
                    "event_type": event_type,
                    "action": action,
                    "status": "updated" if existed else "added",
                    "score": score,
                }
            )
            continue

        if event_type in rules:
            rules.pop(event_type, None)
            applied.append(
                {
                    "event_type": event_type,
                    "action": action,
                    "status": "removed",
                    "score": score,
                }
            )
        else:
            skipped.append(
                {
                    "event_type": event_type,
                    "action": action,
                    "status": "not_found",
                    "score": score,
                }
            )

    if not applied:
        return {
            "agents_file": str(agents_path),
            "managed_rule_count": len(rules),
            "applied_count": 0,
            "skipped_count": len(skipped),
            "applied": [],
            "skipped": skipped,
            "updated": False,
            "updated_at": now.isoformat(),
        }

    managed_lines = _render_managed_rules(order, rules)
    if start_idx is not None and end_idx is not None and start_idx < end_idx:
        block_start = start_idx
        if block_start > 0 and lines[block_start - 1].strip() == MANAGED_RULES_SECTION_TITLE:
            block_start -= 1
        rebuilt = lines[:block_start]
        if rebuilt and rebuilt[-1].strip():
            rebuilt.append("")
        rebuilt.extend(managed_lines)
        tail = lines[end_idx + 1 :]
        if tail and tail[0].strip():
            rebuilt.append("")
        rebuilt.extend(tail)
    else:
        rebuilt = lines[:]
        if rebuilt and rebuilt[-1].strip():
            rebuilt.append("")
        rebuilt.extend(managed_lines)

    updated_text = ("\n".join(rebuilt).rstrip() + "\n") if rebuilt else ""
    changed = updated_text != normalized
    if changed:
        agents_path.write_text(updated_text, encoding="utf-8")

    return {
        "agents_file": str(agents_path),
        "managed_rule_count": len(rules),
        "applied_count": len(applied),
        "skipped_count": len(skipped),
        "applied": applied,
        "skipped": skipped,
        "updated": changed,
        "updated_at": now.isoformat(),
    }


def _append_changes_log(path: Path, lines: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        for line in lines:
            f.write(line.rstrip() + "\n")


def _disallowed_changes(paths: set[str]) -> list[str]:
    return sorted([p for p in paths if not _within_allowed(p)])


def _is_subpath(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def _auto_commit(
    repo_root: Path,
    preexisting_changes: set[str],
    commit_header: str,
    body_lines: list[str],
) -> dict[str, Any]:
    if not _has_git_repo(repo_root):
        return {"performed": False, "reason": "no_git"}

    current_changes = _git_status_paths(repo_root)
    disallowed = _disallowed_changes(current_changes)
    if disallowed:
        return {"performed": False, "reason": "disallowed_changes", "paths": disallowed}

    if preexisting_changes:
        return {
            "performed": False,
            "reason": "preexisting_changes",
            "paths": sorted(preexisting_changes),
        }

    _run(["git", "add", ".agents"], cwd=repo_root, check=True)
    staged = _run(["git", "diff", "--cached", "--name-only"], cwd=repo_root, check=True)
    staged_paths = [p.strip() for p in staged.stdout.splitlines() if p.strip()]
    if not staged_paths:
        return {"performed": False, "reason": "no_staged_changes"}

    commit_cmd = ["git", "commit", "-m", commit_header]
    if body_lines:
        commit_cmd.extend(["-m", "\n".join(body_lines)])
    result = _run(commit_cmd, cwd=repo_root)
    if result.returncode != 0:
        return {"performed": False, "reason": "commit_failed", "stderr": result.stderr.strip()}
    return {"performed": True, "paths": staged_paths}


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)

    pre_parser = argparse.ArgumentParser(add_help=False)
    pre_parser.add_argument("--config-file", default=str(DEFAULT_CONFIG_FILE))
    pre_parser.add_argument("--no-config", action="store_true")
    pre_args, _ = pre_parser.parse_known_args(argv)

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config-file",
        default=str(DEFAULT_CONFIG_FILE),
        help="Optional self-evolve config JSON path. Supports top-level keys or self_evolve.* keys.",
    )
    parser.add_argument(
        "--no-config",
        action="store_true",
        help="Ignore config file and use parser defaults + CLI arguments only.",
    )
    parser.add_argument("--repo-root", default=".", help="Repository root path.")
    parser.add_argument(
        "--agents-root",
        default=str(Path.home() / ".agents"),
        help="Root path of deployed .agents directory. Reports/registry/AGENTS are written here.",
    )
    parser.add_argument(
        "--sessions-root",
        default=str(Path.home() / ".codex" / "sessions"),
        help="Codex sessions root.",
    )
    parser.add_argument("--topic", default="self-evolve")
    parser.add_argument("--short-days", type=int, default=14)
    parser.add_argument("--long-days", type=int, default=90)
    parser.add_argument("--half-life-days", type=int, default=21)
    parser.add_argument("--add-threshold", type=float, default=0.65)
    parser.add_argument("--remove-threshold", type=float, default=0.25)
    parser.add_argument("--add-required", type=int, default=2)
    parser.add_argument("--remove-required", type=int, default=4)
    parser.add_argument("--cooldown-days", type=int, default=7)
    parser.add_argument("--max-rule-changes", type=int, default=5)
    parser.add_argument(
        "--agents-file",
        default="AGENTS.md",
        help="Target AGENTS file path for direct rule integration. Relative paths resolve under --agents-root.",
    )
    parser.add_argument(
        "--decision-mode",
        choices=["auto", "heuristic", "acp", "copilot", "agent"],
        default="auto",
        help="Rule decision mode. auto=ACP provider if available, otherwise heuristic. copilot is legacy alias of acp.",
    )
    parser.add_argument(
        "--agent-cmd",
        help="Agent command template with {input_json} and {output_json} placeholders.",
    )
    parser.add_argument(
        "--agent-timeout-sec",
        type=int,
        default=180,
        help="Timeout (seconds) for agent decision command.",
    )
    parser.add_argument(
        "--acp-provider",
        choices=["codex", "copilot", "gemini"],
        default="codex",
        help="ACP provider used in decision-mode=acp/auto. Default: codex.",
    )
    parser.add_argument(
        "--acp-node-bin",
        default="node",
        help="Node.js binary path for ACP router helper.",
    )
    parser.add_argument(
        "--acp-timeout-sec",
        type=int,
        default=240,
        help="Timeout (seconds) for ACP provider decision execution.",
    )
    parser.add_argument(
        "--acp-model",
        help="Optional model override for the selected ACP provider.",
    )
    parser.add_argument(
        "--acp-reasoning",
        help="Optional reasoning override for the selected ACP provider.",
    )
    parser.add_argument(
        "--acp-copilot-bin",
        default="copilot",
        help="Copilot CLI binary for ACP mode.",
    )
    parser.add_argument(
        "--acp-copilot-model",
        default="gpt-5-mini",
        help="Default model for copilot ACP provider.",
    )
    parser.add_argument(
        "--acp-copilot-reasoning",
        default="high",
        help="Default reasoning level for copilot ACP provider.",
    )
    parser.add_argument(
        "--acp-copilot-config-dir",
        default=str(Path.home() / ".copilot"),
        help="Copilot config directory for ACP mode.",
    )
    parser.add_argument(
        "--acp-codex-adapter-cmd",
        default=f"{sys.executable} {SCRIPT_DIR / 'codex_exec_acp_adapter.py'}",
        help="Command used as codex ACP adapter.",
    )
    parser.add_argument(
        "--acp-codex-model",
        default="gpt-5.3-codex",
        help="Default model for codex ACP provider.",
    )
    parser.add_argument(
        "--acp-codex-reasoning",
        default="xhigh",
        help="Default reasoning level for codex ACP provider.",
    )
    parser.add_argument(
        "--acp-gemini-bin",
        default="gemini",
        help="Gemini CLI binary for ACP mode.",
    )
    parser.add_argument(
        "--acp-gemini-model",
        default="gemini-3-pro-preview",
        help="Default model for gemini ACP provider.",
    )
    parser.add_argument(
        "--acp-gemini-reasoning",
        default="",
        help="Default reasoning level for gemini ACP provider (if supported).",
    )
    parser.add_argument("--skip-lesson", action="store_true")
    parser.add_argument("--auto-commit", action="store_true")
    parser.add_argument(
        "--commit-header",
        default="chore(self-evolve): update insights and rule state",
    )
    parser.add_argument(
        "--summary-out",
        help="Optional summary JSON output path. Default: .agents/reports/insights/cycle-<ts>.json",
    )
    parser.add_argument(
        "--extra-sessions-root",
        action="append",
        default=[],
        help="Additional session directory to scan (e.g. ~/.copilot/session-state). Can be repeated.",
    )
    config_file: Path | None = None
    config_loaded = False
    config_unknown_keys: list[str] = []
    try:
        if not pre_args.no_config:
            config_file = Path(pre_args.config_file).expanduser().resolve()
            if config_file.exists():
                raw_config = _load_config_payload(config_file)
                config_defaults, config_unknown_keys = _normalize_config_defaults(parser, raw_config)
                if config_defaults:
                    parser.set_defaults(**config_defaults)
                    config_loaded = True
    except RuntimeError as exc:
        print(f"config_error: {exc}", file=sys.stderr)
        return 2

    args = parser.parse_args(argv)

    repo_root = Path(args.repo_root).expanduser().resolve()
    agents_root = Path(args.agents_root).expanduser().resolve()
    primary_sessions_root = Path(args.sessions_root).expanduser().resolve()
    extra_sessions_roots = [Path(p).expanduser().resolve() for p in args.extra_sessions_root]
    acp_copilot_config_dir = Path(args.acp_copilot_config_dir).expanduser().resolve()
    agents_root.mkdir(parents=True, exist_ok=True)
    runtime_cwd = agents_root.parent if agents_root.parent.exists() else Path.home().resolve()

    tmp_merged: Path | None = None
    sessions_root, tmp_merged = _merge_sessions_roots(
        primary_sessions_root, extra_sessions_roots, agents_root,
    )
    if tmp_merged is not None:
        atexit.register(shutil.rmtree, tmp_merged, ignore_errors=True)
    agents_file = Path(args.agents_file).expanduser()
    if not agents_file.is_absolute():
        agents_file = (agents_root / agents_file).resolve()
    now = _now_utc()
    ts = _stamp(now)

    insights_dir = agents_root / "reports" / "insights"
    lesson_dir = agents_root / "reports" / "lesson"
    registry_dir = agents_root / "registry"
    insights_dir.mkdir(parents=True, exist_ok=True)
    lesson_dir.mkdir(parents=True, exist_ok=True)
    registry_dir.mkdir(parents=True, exist_ok=True)

    if not _is_subpath(agents_file, agents_root):
        summary = {
            "generated_at": now.isoformat(),
            "status": "blocked",
            "reason": "blocked_by_scope",
            "agents_root": str(agents_root),
            "agents_file": str(agents_file),
            "config": {
                "file": str(config_file) if config_file else None,
                "loaded": config_loaded,
                "unknown_keys": config_unknown_keys,
            },
        }
        out = (
            Path(args.summary_out).expanduser()
            if args.summary_out
            else insights_dir / f"cycle-{ts}.json"
        )
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
        print(str(out))
        if tmp_merged is not None:
            shutil.rmtree(tmp_merged, ignore_errors=True)
        return 2

    preexisting_changes: set[str] = set()
    if _has_git_repo(repo_root):
        preexisting_changes = _git_status_paths(repo_root)

    sync = _sync_repo(repo_root, args.topic)
    if not sync.get("ok", False):
        summary = {
            "generated_at": now.isoformat(),
            "status": "sync_failed",
            "sync": sync,
            "config": {
                "file": str(config_file) if config_file else None,
                "loaded": config_loaded,
                "unknown_keys": config_unknown_keys,
            },
        }
        out = (
            Path(args.summary_out).expanduser()
            if args.summary_out
            else insights_dir / f"cycle-{ts}.json"
        )
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
        print(str(out))
        if tmp_merged is not None:
            shutil.rmtree(tmp_merged, ignore_errors=True)
        return 2

    insights_report = insights_dir / f"insights-{ts}.json"
    _run_project_insights(
        runtime_cwd=runtime_cwd,
        sessions_root=sessions_root,
        out_path=insights_report,
        short_days=args.short_days,
        long_days=args.long_days,
        half_life_days=args.half_life_days,
    )

    lesson_report: Path | None = None
    lesson_payload: dict[str, Any] | None = None
    if not args.skip_lesson:
        lesson_report = lesson_dir / f"lesson-{ts}.json"
        try:
            _run_lesson_report(runtime_cwd=runtime_cwd, sessions_root=sessions_root, out_path=lesson_report)
            lesson_payload = _load_json(lesson_report)
        except RuntimeError:
            lesson_report = None
            lesson_payload = None

    insights_payload = _load_json(insights_report)
    rows = insights_payload.get("scoring", {}).get("rows", [])
    if not isinstance(rows, list):
        rows = []

    state_path = registry_dir / "rule-state.json"
    state = _load_state(state_path)
    evaluated = _evaluate_thresholds(
        state=state,
        rows=rows,
        now=now,
        add_threshold=args.add_threshold,
        remove_threshold=args.remove_threshold,
        add_required=args.add_required,
        remove_required=args.remove_required,
        cooldown_days=args.cooldown_days,
        max_changes=args.max_rule_changes,
    )
    state_path.write_text(
        json.dumps(evaluated["state"], ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    policy = {
        "add_threshold": args.add_threshold,
        "remove_threshold": args.remove_threshold,
        "add_required": args.add_required,
        "remove_required": args.remove_required,
        "cooldown_days": args.cooldown_days,
        "max_rule_changes": args.max_rule_changes,
    }
    routing = _load_routing_config(agents_root)
    tracked_events = {
        str(item.get("event_type", "")).strip()
        for item in rows
        if isinstance(item, dict) and str(item.get("event_type", "")).strip()
    }
    tracked_events.update(
        str(item.get("event_type", "")).strip()
        for item in evaluated["proposals"]
        if isinstance(item, dict) and str(item.get("event_type", "")).strip()
    )
    evidence_map = _collect_session_evidence(
        sessions_root=sessions_root,
        tracked_events=tracked_events,
    )
    topic_candidates_rows = _build_topic_candidates(
        rows=rows,
        half_life_days=args.half_life_days,
        evidence_map=evidence_map,
    )
    topic_candidates_report = insights_dir / f"topic-candidates-{ts}.json"
    topic_candidates_report.write_text(
        json.dumps(
            {
                "generated_at": now.isoformat(),
                "sessions_root": str(sessions_root),
                "rows": topic_candidates_rows,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    decision_input = {
        "generated_at": now.isoformat(),
        "sessions_root": str(sessions_root),
        "insights_summary": {
            "session_count": insights_payload.get("session_count"),
            "top_rows": rows[:20],
        },
        "topic_candidates": {
            "count": len(topic_candidates_rows),
            "top_rows": topic_candidates_rows[:20],
        },
        "sessions_evidence": {
            "tracked_event_count": len(tracked_events),
            "evidence_event_count": len(evidence_map),
            "evidence_events": sorted(evidence_map.keys())[:50],
        },
        "lesson_summary": lesson_payload,
        "candidate_proposals": evaluated["proposals"],
        "skipped_by_cooldown": evaluated["skipped_by_cooldown"],
        "policy": policy,
        "routing_policy": {
            "source": routing.get("source"),
            "global_events": routing.get("global_events", []),
            "topic_overrides": routing.get("topic_overrides", {}),
            "card_link_limit": routing.get("card_link_limit", DEFAULT_CARD_LINK_LIMIT),
            "card_min_confidence": routing.get(
                "card_min_confidence", DEFAULT_CARD_MIN_CONFIDENCE
            ),
        },
    }
    decision = _decide_proposals(
        mode=args.decision_mode,
        runtime_cwd=runtime_cwd,
        agent_cmd=args.agent_cmd,
        agent_timeout_sec=max(1, args.agent_timeout_sec),
        acp_provider=args.acp_provider,
        acp_node_bin=args.acp_node_bin,
        acp_timeout_sec=max(1, args.acp_timeout_sec),
        acp_model=args.acp_model,
        acp_reasoning=args.acp_reasoning,
        acp_copilot_bin=args.acp_copilot_bin,
        acp_copilot_model=args.acp_copilot_model,
        acp_copilot_reasoning=args.acp_copilot_reasoning,
        acp_copilot_config_dir=acp_copilot_config_dir,
        acp_codex_adapter_cmd=args.acp_codex_adapter_cmd,
        acp_codex_model=args.acp_codex_model,
        acp_codex_reasoning=args.acp_codex_reasoning,
        acp_gemini_bin=args.acp_gemini_bin,
        acp_gemini_model=args.acp_gemini_model,
        acp_gemini_reasoning=args.acp_gemini_reasoning,
        decision_input=decision_input,
        candidate_proposals=evaluated["proposals"],
        rows=rows,
        lesson_payload=lesson_payload,
    )
    accepted_rules = decision["accepted_proposals"]
    routed_accepts = _split_accepted_rules_by_target(accepted_rules, routing)
    accepted_rules_agents = routed_accepts["agents"]
    accepted_rules_skills = routed_accepts["skills"]
    accepted_rules_all = routed_accepts["all"]
    skill_actions_rows = _build_skill_actions(
        decisions=decision["decisions"],
        candidate_proposals=evaluated["proposals"],
        rows=rows,
        routing=routing,
        half_life_days=args.half_life_days,
    )
    card_link_limit = max(0, _to_int(routing.get("card_link_limit"), DEFAULT_CARD_LINK_LIMIT))
    card_min_confidence = max(
        0.0,
        min(1.0, _to_float(routing.get("card_min_confidence"), DEFAULT_CARD_MIN_CONFIDENCE)),
    )
    skill_cards_payload = _build_skill_cards(
        skill_actions_rows=skill_actions_rows,
        evidence_map=evidence_map,
        agents_root=agents_root,
        now=now,
    )
    skill_links_rows = _build_skill_links(
        skill_cards=skill_cards_payload["rows"],
        cards_by_skill=skill_cards_payload["cards_by_skill"],
    )
    skill_actions_rows = _attach_linked_cards(
        skill_actions_rows=skill_actions_rows,
        action_card_map=skill_cards_payload["action_card_map"],
        skill_links=skill_links_rows,
        card_link_limit=card_link_limit,
        card_min_confidence=card_min_confidence,
    )
    skill_pipeline = _build_multi_agent_skill_pipeline(
        routed_skill_rules=accepted_rules_skills,
        evidence_map=evidence_map,
        now=now,
    )
    skill_cards_report = insights_dir / f"skill-cards-{ts}.json"
    skill_cards_report.write_text(
        json.dumps(
            {
                "generated_at": now.isoformat(),
                "routing_strategy": {
                    "mode": "card-then-graph",
                    "card_link_limit": card_link_limit,
                    "card_min_confidence": card_min_confidence,
                },
                "cards": skill_cards_payload["rows"],
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    skill_links_report = insights_dir / f"skill-links-{ts}.json"
    skill_links_report.write_text(
        json.dumps(
            {
                "generated_at": now.isoformat(),
                "routing_strategy": {
                    "mode": "card-then-graph",
                    "card_link_limit": card_link_limit,
                    "card_min_confidence": card_min_confidence,
                },
                "links": skill_links_rows,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    skill_actions_report = insights_dir / f"skill-actions-{ts}.json"
    skill_actions_report.write_text(
        json.dumps(
            {
                "generated_at": now.isoformat(),
                "routing_strategy": {
                    "mode": "card-then-graph",
                    "card_link_limit": card_link_limit,
                    "card_min_confidence": card_min_confidence,
                },
                "decisions": skill_actions_rows,
                "skill_cards_report": str(skill_cards_report),
                "skill_links_report": str(skill_links_report),
                "skill_pipeline": skill_pipeline,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    problemmap_bridge = _run_problemmap_bridge(
        agents_root=agents_root,
        sessions_root=sessions_root,
        routing=routing,
        rows=rows,
        now=now,
        insights_dir=insights_dir,
    )

    decision_report = insights_dir / f"decision-{ts}.json"
    decision_report_payload = {
        "generated_at": now.isoformat(),
        "decision_mode": decision["mode"],
        "decision_error": decision["error"],
        "candidate_count": len(evaluated["proposals"]),
        "accepted_count": len(accepted_rules),
        "rejected_count": len(decision["rejected_proposals"]),
        "accepted_agents_count": len(accepted_rules_agents),
        "accepted_skills_count": len(accepted_rules_skills),
        "decisions": decision["decisions"],
        "agent": decision["agent"],
        "routing": routing,
        "topic_candidates_report": str(topic_candidates_report),
        "topic_candidates_count": len(topic_candidates_rows),
        "skill_actions_report": str(skill_actions_report),
        "skill_actions_count": len(skill_actions_rows),
        "skill_cards_report": str(skill_cards_report),
        "skill_cards_count": len(skill_cards_payload["rows"]),
        "skill_links_report": str(skill_links_report),
        "skill_links_count": len(skill_links_rows),
        "skill_pipeline_mode": skill_pipeline.get("mode"),
        "problemmap_bridge": problemmap_bridge,
    }
    decision_report.write_text(
        json.dumps(decision_report_payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    integration_agents = _integrate_rules_into_agents(
        agents_path=agents_file,
        accepted_rules=accepted_rules_agents,
        now=now,
    )
    integration_skills = _integrate_rules_into_skills(
        agents_root=agents_root,
        accepted_rules=accepted_rules_skills,
        now=now,
    )

    integration_report = insights_dir / f"integration-{ts}.json"
    integration_payload = {
        "generated_at": now.isoformat(),
        "insights_report": str(insights_report),
        "decision_report": str(decision_report),
        "accepted_rules": accepted_rules_all,
        "accepted_rules_agents": accepted_rules_agents,
        "accepted_rules_skills": accepted_rules_skills,
        "candidate_rules": evaluated["proposals"],
        "rejected_rules": decision["rejected_proposals"],
        "skipped_by_cooldown": evaluated["skipped_by_cooldown"],
        "policy": policy,
        "routing": routing,
        "topic_candidates_report": str(topic_candidates_report),
        "skill_actions_report": str(skill_actions_report),
        "skill_cards_report": str(skill_cards_report),
        "skill_links_report": str(skill_links_report),
        "skill_pipeline": skill_pipeline,
        "problemmap_bridge": problemmap_bridge,
        "integration": integration_agents,
        "integration_agents": integration_agents,
        "integration_skills": integration_skills,
        "integration_cards": {
            "cards_total": len(skill_cards_payload["rows"]),
            "cards_actionable": sum(
                1
                for row in skill_cards_payload["rows"]
                if str(row.get("action", "")).strip() in {"create", "update", "remove"}
            ),
            "cards_with_links": sum(
                1 for row in skill_actions_rows if isinstance(row.get("linked_cards"), list) and row.get("linked_cards")
            ),
            "card_link_limit": card_link_limit,
        },
        "integration_links": {
            "links_total": len(skill_links_rows),
            "links_with_existing_target": sum(
                1 for row in skill_links_rows if bool(row.get("target_exists", False))
            ),
            "card_min_confidence": card_min_confidence,
        },
        "decision": {
            "mode": decision["mode"],
            "error": decision["error"],
        },
    }
    integration_report.write_text(
        json.dumps(integration_payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    log_path = registry_dir / "changes.log"
    log_lines = [
        f"{now.isoformat()} cycle sync_mode={sync['mode']} insights={insights_report.name}",
        (
            f"{now.isoformat()} rule_candidates={len(evaluated['proposals'])} "
            f"accepted={len(accepted_rules_all)} accepted_agents={len(accepted_rules_agents)} "
            f"accepted_skills={len(accepted_rules_skills)} "
            f"cooldown_skip={len(evaluated['skipped_by_cooldown'])} decision_mode={decision['mode']}"
        ),
        (
            f"{now.isoformat()} agents_file={integration_agents['agents_file']} "
            f"updated={integration_agents['updated']} applied={integration_agents['applied_count']} "
            f"skipped={integration_agents['skipped_count']}"
        ),
        (
            f"{now.isoformat()} skills_total={integration_skills['skills_total']} "
            f"skills_updated={integration_skills['skills_updated']} "
            f"applied={integration_skills['applied_count']} skipped={integration_skills['skipped_count']}"
        ),
        (
            f"{now.isoformat()} skill_cards={len(skill_cards_payload['rows'])} "
            f"skill_links={len(skill_links_rows)} card_link_limit={card_link_limit} "
            f"card_min_confidence={card_min_confidence:.2f}"
        ),
        (
            f"{now.isoformat()} problemmap_bridge status={problemmap_bridge.get('status', 'disabled')} "
            f"cases={problemmap_bridge.get('cases_total', 0)} "
            f"events={','.join(problemmap_bridge.get('event_types', []))}"
        ),
    ]
    for p in accepted_rules_all:
        log_lines.append(
            (
                f"{now.isoformat()} rule {p['action']} event={p['event_type']} "
                f"target={p.get('target_kind', 'agents')} skill={p.get('target_skill_id', '')} "
                f"score={p['score']} reason={p.get('decision_reason', '')}"
            )
        )
    _append_changes_log(log_path, log_lines)

    commit_result = {"performed": False, "reason": "auto_commit_disabled"}
    if args.auto_commit:
        if _is_subpath(agents_root, repo_root):
            body = [
                f"sync_mode: {sync['mode']}",
                f"insights_report: {insights_report.name}",
                f"topic_candidates_report: {topic_candidates_report.name}",
                f"decision_report: {decision_report.name}",
                f"skill_actions_report: {skill_actions_report.name}",
                f"skill_cards_report: {skill_cards_report.name}",
                f"skill_links_report: {skill_links_report.name}",
                f"integration_report: {integration_report.name}",
                f"rule_candidates: {len(evaluated['proposals'])}",
                f"rule_accepted: {len(accepted_rules_all)}",
                f"rule_accepted_agents: {len(accepted_rules_agents)}",
                f"rule_accepted_skills: {len(accepted_rules_skills)}",
                f"skill_cards: {len(skill_cards_payload['rows'])}",
                f"skill_links: {len(skill_links_rows)}",
                f"agents_file: {integration_agents['agents_file']}",
                f"agents_updated: {integration_agents['updated']}",
                f"skills_updated: {integration_skills['skills_updated']}",
                f"decision_mode: {decision['mode']}",
            ]
            if lesson_report:
                body.append(f"lesson_report: {lesson_report.name}")
            commit_result = _auto_commit(
                repo_root=repo_root,
                preexisting_changes=preexisting_changes,
                commit_header=args.commit_header,
                body_lines=body,
            )
        else:
            commit_result = {
                "performed": False,
                "reason": "agents_root_outside_repo",
                "agents_root": str(agents_root),
                "repo_root": str(repo_root),
            }

    summary = {
        "generated_at": now.isoformat(),
        "status": "ok",
        "sync": sync,
        "agents_root": str(agents_root),
        "insights_report": str(insights_report),
        "topic_candidates_report": str(topic_candidates_report),
        "lesson_report": str(lesson_report) if lesson_report else None,
        "decision_report": str(decision_report),
        "skill_actions_report": str(skill_actions_report),
        "skill_cards_report": str(skill_cards_report),
        "skill_links_report": str(skill_links_report),
        "integration_report": str(integration_report),
        "proposal_report": str(integration_report),
        "problemmap_bridge_report": problemmap_bridge.get("summary_report"),
        "problemmap_bridge_cases_report": problemmap_bridge.get("cases_report"),
        "agents_file": str(agents_file),
        "routing_config": str(_routing_config_path(agents_root)),
        "state_file": str(state_path),
        "config": {
            "file": str(config_file) if config_file else None,
            "loaded": config_loaded,
            "unknown_keys": config_unknown_keys,
        },
        "commit": commit_result,
    }
    summary_path = (
        Path(args.summary_out).expanduser()
        if args.summary_out
        else insights_dir / f"cycle-{ts}.json"
    )
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(str(summary_path))
    if tmp_merged is not None:
        shutil.rmtree(tmp_merged, ignore_errors=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
