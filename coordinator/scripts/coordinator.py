#!/usr/bin/env python3
"""Coordinator CLI skeleton for Topic 2 multi-agent job orchestration."""

from __future__ import annotations

import argparse
import json
import os
import re
import shlex
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from uuid import uuid4


TERMINAL_JOB_STATUS = {"done", "stopped", "killed", "failed"}
RELAY_INTENTS = {"ask", "answer", "propose", "review"}
WORKER_MODES = {"auto", "none", "template", "sdk"}
PROVIDER_DEFAULTS: dict[str, dict[str, str]] = {
    "codex": {"model": "gpt-5.3-codex", "reasoning": "xhigh"},
    "copilot": {"model": "gpt-5-mini", "reasoning": "high"},
    "gemini": {"model": "gemini-3-pro-preview", "reasoning": ""},
}


def _now_utc() -> datetime:
    return datetime.now(tz=UTC)


def _iso_now() -> str:
    return _now_utc().isoformat()


def _parse_iso(ts: str) -> datetime | None:
    try:
        return datetime.fromisoformat(ts.replace("Z", "+00:00")).astimezone(UTC)
    except ValueError:
        return None


def _parse_csv(value: str) -> list[str]:
    return [x.strip() for x in value.split(",") if x.strip()]


def _safe_int(value: Any, default: int = -1) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _slug(value: str) -> str:
    text = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return text or "topic"


def _normalize_scope_item(value: str) -> str:
    text = value.strip()
    if text.endswith("/**"):
        text = text[:-3]
    text = text.rstrip("/")
    return text or "."


def _scope_overlaps(a: str, b: str) -> bool:
    aa = _normalize_scope_item(a)
    bb = _normalize_scope_item(b)
    if aa == "." or bb == ".":
        return True
    if aa == bb:
        return True
    return aa.startswith(bb + "/") or bb.startswith(aa + "/")


def _read_json(path: Path, default: Any = None) -> Any:
    if default is None:
        default = {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return default


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _append_ndjson(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=False) + "\n")


def _print_json(payload: dict[str, Any]) -> None:
    print(json.dumps(payload, ensure_ascii=False))


def _layout(root: Path) -> dict[str, Path]:
    paths = {
        "root": root,
        "lock_dir": root / "lock",
        "jobs_dir": root / "jobs",
        "agents_dir": root / "agents",
        "mailbox_dir": root / "mailbox",
        "logs_dir": root / "logs",
    }
    for key in ("lock_dir", "jobs_dir", "agents_dir", "mailbox_dir", "logs_dir"):
        paths[key].mkdir(parents=True, exist_ok=True)
    return paths


def _lock_path(paths: dict[str, Path]) -> Path:
    return paths["lock_dir"] / "main.lock"


def _lock_is_stale(payload: dict[str, Any], ttl_sec: int) -> bool:
    ts = str(payload.get("started_at", "")).strip()
    parsed = _parse_iso(ts)
    if not parsed:
        return True
    age_sec = (_now_utc() - parsed).total_seconds()
    return age_sec > ttl_sec


def _acquire_lock(paths: dict[str, Path], mode: str, ttl_sec: int) -> tuple[bool, str | None, dict[str, Any] | None]:
    lock_file = _lock_path(paths)
    if lock_file.exists():
        current = _read_json(lock_file, {})
        if isinstance(current, dict) and not _lock_is_stale(current, ttl_sec):
            return False, None, current
        lock_file.unlink(missing_ok=True)

    token = str(uuid4())
    payload = {
        "token": token,
        "mode": mode,
        "pid": os.getpid(),
        "started_at": _iso_now(),
    }
    try:
        fd = os.open(str(lock_file), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError:
        current = _read_json(lock_file, {})
        return False, None, current if isinstance(current, dict) else {}

    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=False) + "\n")
    return True, token, None


def _release_lock(paths: dict[str, Path], token: str | None) -> None:
    if not token:
        return
    lock_file = _lock_path(paths)
    current = _read_json(lock_file, {})
    if isinstance(current, dict) and current.get("token") == token:
        lock_file.unlink(missing_ok=True)


def _new_job_id() -> str:
    return f"job-{_now_utc().strftime('%Y%m%d-%H%M%S')}-{str(uuid4())[:8]}"


def _new_trace_id(job_id: str) -> str:
    return f"{job_id}-trace-{str(uuid4())[:8]}"


def _job_file(paths: dict[str, Path], job_id: str) -> Path:
    return paths["jobs_dir"] / f"{job_id}.json"


def _mailbox_file(paths: dict[str, Path], job_id: str) -> Path:
    return paths["mailbox_dir"] / f"{job_id}.json"


def _agent_file(paths: dict[str, Path], job_id: str, agent_id: str) -> Path:
    return paths["agents_dir"] / job_id / f"{agent_id}.json"


def _log_file(paths: dict[str, Path], job_id: str) -> Path:
    return paths["logs_dir"] / f"{job_id}.ndjson"


def _build_branches(agent_ids: list[str], topic: str) -> dict[str, str]:
    topic_slug = _slug(topic)
    return {agent_id: f"agent/{agent_id}/{topic_slug}" for agent_id in agent_ids}


def _build_job_payload(
    job_id: str,
    topic: str,
    trigger: str,
    from_agent: str,
    to_agents: list[str],
    provider: str,
    model: str,
    reasoning: str,
    read_scope: list[str],
    write_scope: list[str],
) -> dict[str, Any]:
    now = _iso_now()
    return {
        "job_id": job_id,
        "status": "running",
        "topic": topic,
        "trigger": trigger,
        "from_agent": from_agent,
        "to_agents": to_agents,
        "provider": provider,
        "model": model,
        "reasoning": reasoning,
        "read_scope": read_scope,
        "write_scope": write_scope,
        "branches": _build_branches(to_agents, topic),
        "created_at": now,
        "started_at": now,
        "ended_at": None,
        "updated_at": now,
    }


def _build_mailbox_payload(
    job_id: str,
    from_agent: str,
    to_agents: list[str],
    topic: str,
    start_signal: str,
    trace_id: str,
) -> dict[str, Any]:
    return {
        "job_id": job_id,
        "from_agent": from_agent,
        "to_agents": to_agents,
        "topic": topic,
        "start_signal": start_signal,
        "trace_id": trace_id,
        "status": "opened",
        "result_summary_ref": "",
    }


def _write_agent_states(paths: dict[str, Path], job: dict[str, Any], status: str) -> list[str]:
    job_id = str(job["job_id"])
    agent_ids = [str(x) for x in job.get("to_agents", []) if str(x).strip()]
    out: list[str] = []
    for agent_id in agent_ids:
        payload = {
            "job_id": job_id,
            "agent_id": agent_id,
            "status": status,
            "branch": job.get("branches", {}).get(agent_id, ""),
            "read_scope": job.get("read_scope", []),
            "write_scope": job.get("write_scope", []),
            "updated_at": _iso_now(),
        }
        path = _agent_file(paths, job_id, agent_id)
        _write_json(path, payload)
        out.append(str(path))
    return out


def _load_agent_states(paths: dict[str, Path], job_id: str) -> list[dict[str, Any]]:
    root = paths["agents_dir"] / job_id
    if not root.exists():
        return []
    out: list[dict[str, Any]] = []
    for p in sorted(root.glob("*.json")):
        data = _read_json(p, {})
        if isinstance(data, dict):
            out.append(data)
    return out


def _complete_job(paths: dict[str, Path], job: dict[str, Any], mailbox: dict[str, Any], result: str) -> None:
    job["status"] = result
    job["ended_at"] = _iso_now()
    job["updated_at"] = job["ended_at"]
    mailbox["status"] = "closed"
    mailbox["result_summary_ref"] = str(_log_file(paths, str(job["job_id"])))
    _write_json(_job_file(paths, str(job["job_id"])), job)
    _write_json(_mailbox_file(paths, str(job["job_id"])), mailbox)
    _write_agent_states(paths, job, result)
    _append_ndjson(
        _log_file(paths, str(job["job_id"])),
        {
            "timestamp": _iso_now(),
            "event": f"job_{result}",
            "job_id": str(job["job_id"]),
        },
    )


def _trim_text(value: str, limit: int = 2000) -> str:
    text = value.strip()
    if len(text) <= limit:
        return text
    return text[:limit] + "...<trimmed>"


def _resolve_provider_runtime(provider: str, model: str, reasoning: str) -> tuple[str, str]:
    defaults = PROVIDER_DEFAULTS.get(provider, PROVIDER_DEFAULTS["codex"])
    resolved_model = model.strip() or defaults["model"]
    resolved_reasoning = reasoning.strip() or defaults["reasoning"]
    return resolved_model, resolved_reasoning


def _default_sdk_script_path() -> Path:
    # coordinator.py: .../.agents/skills/custom/coordinator/scripts/coordinator.py
    # bundled sdk orchestrator: .../.agents/skills/custom/coordinator/scripts/copilot_sdk_orchestrator.mjs
    return Path(__file__).resolve().parent / "copilot_sdk_orchestrator.mjs"


def _run_worker_command(
    *,
    command: list[str],
    command_text: str,
    worker_cwd: Path,
    timeout_sec: int,
    agent_id: str,
) -> dict[str, Any]:
    try:
        proc = subprocess.run(
            command,
            text=True,
            capture_output=True,
            check=False,
            timeout=max(1, timeout_sec),
            cwd=str(worker_cwd),
        )
        rc = int(proc.returncode)
        ok = rc == 0
        return {
            "agent_id": agent_id,
            "ok": ok,
            "returncode": rc,
            "reason": "ok" if ok else "command_failed",
            "command": command_text,
            "stdout": _trim_text(proc.stdout),
            "stderr": _trim_text(proc.stderr),
        }
    except subprocess.TimeoutExpired as exc:
        return {
            "agent_id": agent_id,
            "ok": False,
            "returncode": 124,
            "reason": "timeout",
            "command": command_text,
            "stdout": _trim_text(str(exc.stdout or "")),
            "stderr": _trim_text(str(exc.stderr or "")),
        }


def _run_worker_commands(
    paths: dict[str, Path],
    job: dict[str, Any],
    trace_id: str,
    worker_mode: str,
    worker_cmd_template: str,
    worker_timeout_sec: int,
    worker_cwd: Path,
    sdk_script: Path,
    sdk_config_dir: Path,
    sdk_delegate_template: str,
) -> dict[str, Any]:
    mode = worker_mode.strip().lower()
    if mode not in WORKER_MODES:
        return {
            "executed": True,
            "all_ok": False,
            "workers": [],
            "mode": mode,
            "reason": "invalid_worker_mode",
        }

    template = worker_cmd_template.strip()
    if mode == "auto":
        mode = "template" if template else "none"
    if mode == "none":
        return {"executed": False, "all_ok": True, "workers": []}

    job_id = str(job.get("job_id", "")).strip()
    provider = str(job.get("provider", "")).strip()
    model = str(job.get("model", "")).strip()
    reasoning = str(job.get("reasoning", "")).strip()
    topic = str(job.get("topic", "")).strip()
    from_agent = str(job.get("from_agent", "")).strip()
    read_scope = ",".join([str(x) for x in job.get("read_scope", []) if str(x).strip()])
    write_scope = ",".join([str(x) for x in job.get("write_scope", []) if str(x).strip()])

    rows: list[dict[str, Any]] = []
    for agent_id in [str(x) for x in job.get("to_agents", []) if str(x).strip()]:
        prompt = (
            f"topic={topic}\n"
            f"job_id={job_id}\n"
            f"trace_id={trace_id}\n"
            f"from_agent={from_agent}\n"
            f"agent_id={agent_id}\n"
            f"read_scope={read_scope}\n"
            f"write_scope={write_scope}\n"
        )

        cmd: list[str] = []
        cmd_text = ""
        if mode == "template":
            try:
                cmd_text = template.format(
                    provider=provider,
                    model=model,
                    reasoning=reasoning,
                    topic=topic,
                    job_id=job_id,
                    trace_id=trace_id,
                    agent_id=agent_id,
                    from_agent=from_agent,
                    read_scope=read_scope,
                    write_scope=write_scope,
                    state_root=str(paths["root"]),
                )
            except KeyError as exc:
                err = f"invalid template placeholder: {exc}"
                _append_ndjson(
                    _log_file(paths, job_id),
                    {
                        "timestamp": _iso_now(),
                        "event": "worker_error",
                        "job_id": job_id,
                        "agent_id": agent_id,
                        "reason": err,
                    },
                )
                rows.append(
                    {
                        "agent_id": agent_id,
                        "ok": False,
                        "returncode": 2,
                        "reason": err,
                        "command": "",
                        "stdout": "",
                        "stderr": "",
                    }
                )
                continue

            cmd = shlex.split(cmd_text)
            if not cmd:
                err = "empty command after template expansion"
                rows.append(
                    {
                        "agent_id": agent_id,
                        "ok": False,
                        "returncode": 2,
                        "reason": err,
                        "command": cmd_text,
                        "stdout": "",
                        "stderr": "",
                    }
                )
                continue
        elif mode == "sdk":
            out_path = paths["logs_dir"] / f"{job_id}-{agent_id}-sdk.json"
            cmd = [
                "node",
                str(sdk_script),
                "--provider",
                provider,
                "--cwd",
                str(worker_cwd),
                "--prompt",
                prompt,
                "--json-out",
                str(out_path),
            ]
            if model:
                cmd.extend(["--model", model])
            if reasoning:
                cmd.extend(["--reasoning", reasoning])
            if provider == "copilot" and sdk_config_dir:
                cmd.extend(["--config-dir", str(sdk_config_dir)])
            if provider != "copilot":
                delegate_tpl = sdk_delegate_template.strip()
                if not delegate_tpl:
                    rows.append(
                        {
                            "agent_id": agent_id,
                            "ok": False,
                            "returncode": 2,
                            "reason": "sdk_delegate_template_required",
                            "command": "node ... --delegate-cmd-template <required>",
                            "stdout": "",
                            "stderr": "",
                        }
                    )
                    continue
                cmd.extend(["--delegate-cmd-template", delegate_tpl])
            cmd_text = " ".join(shlex.quote(x) for x in cmd)
        else:
            rows.append(
                {
                    "agent_id": agent_id,
                    "ok": False,
                    "returncode": 2,
                    "reason": f"unsupported_worker_mode:{mode}",
                    "command": "",
                    "stdout": "",
                    "stderr": "",
                }
            )
            continue

        _append_ndjson(
            _log_file(paths, job_id),
            {
                "timestamp": _iso_now(),
                "event": "worker_started",
                "job_id": job_id,
                "trace_id": trace_id,
                "agent_id": agent_id,
                "command": cmd,
            },
        )
        row = _run_worker_command(
            command=cmd,
            command_text=cmd_text,
            worker_cwd=worker_cwd,
            timeout_sec=worker_timeout_sec,
            agent_id=agent_id,
        )
        rows.append(row)
        _append_ndjson(
            _log_file(paths, job_id),
            {
                "timestamp": _iso_now(),
                "event": "worker_finished",
                "job_id": job_id,
                "trace_id": trace_id,
                "agent_id": agent_id,
                "ok": row["ok"],
                "returncode": row["returncode"],
                "reason": row["reason"],
            },
        )

    return {
        "executed": True,
        "all_ok": all(bool(x.get("ok")) for x in rows),
        "workers": rows,
        "mode": mode,
    }


def _run_job(
    paths: dict[str, Path],
    topic: str,
    trigger: str,
    from_agent: str,
    to_agents: list[str],
    provider: str,
    model: str,
    reasoning: str,
    read_scope: list[str],
    write_scope: list[str],
    hold_open: bool,
    worker_mode: str,
    worker_cmd_template: str,
    worker_timeout_sec: int,
    worker_cwd: Path,
    sdk_script: Path,
    sdk_config_dir: Path,
    sdk_delegate_template: str,
) -> dict[str, Any]:
    conflicts = _active_scope_conflicts(paths, write_scope)
    if conflicts:
        return {
            "status": "blocked_by_scope_conflict",
            "reason": "active job write_scope overlap",
            "conflicts": conflicts,
        }

    job_id = _new_job_id()
    trace_id = _new_trace_id(job_id)
    job = _build_job_payload(
        job_id=job_id,
        topic=topic,
        trigger=trigger,
        from_agent=from_agent,
        to_agents=to_agents,
        provider=provider,
        model=model,
        reasoning=reasoning,
        read_scope=read_scope,
        write_scope=write_scope,
    )
    mailbox = _build_mailbox_payload(
        job_id=job_id,
        from_agent=from_agent,
        to_agents=to_agents,
        topic=topic,
        start_signal=trigger,
        trace_id=trace_id,
    )

    _write_json(_job_file(paths, job_id), job)
    _write_json(_mailbox_file(paths, job_id), mailbox)
    _write_agent_states(paths, job, "running")
    _append_ndjson(
        _log_file(paths, job_id),
        {
            "timestamp": _iso_now(),
            "event": "job_started",
            "job_id": job_id,
            "trigger": trigger,
            "topic": topic,
        },
    )

    worker_execution = {"executed": False, "all_ok": True, "workers": []}
    if not hold_open:
        worker_execution = _run_worker_commands(
            paths=paths,
            job=job,
            trace_id=trace_id,
            worker_mode=worker_mode,
            worker_cmd_template=worker_cmd_template,
            worker_timeout_sec=worker_timeout_sec,
            worker_cwd=worker_cwd,
            sdk_script=sdk_script,
            sdk_config_dir=sdk_config_dir,
            sdk_delegate_template=sdk_delegate_template,
        )
        final_status = "done" if worker_execution.get("all_ok", True) else "failed"
        _complete_job(paths, job, mailbox, final_status)

    return {
        "status": job["status"] if hold_open else ("done" if worker_execution.get("all_ok", True) else "failed"),
        "job_id": job_id,
        "trace_id": trace_id,
        "job_file": str(_job_file(paths, job_id)),
        "mailbox_file": str(_mailbox_file(paths, job_id)),
        "log_file": str(_log_file(paths, job_id)),
        "worker_execution": worker_execution,
    }


def _list_jobs(paths: dict[str, Path], limit: int) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    for p in sorted(paths["jobs_dir"].glob("*.json"), key=lambda x: x.stat().st_mtime, reverse=True):
        data = _read_json(p, {})
        if not isinstance(data, dict):
            continue
        rows.append(
            {
                "job_id": data.get("job_id"),
                "status": data.get("status"),
                "topic": data.get("topic"),
                "trigger": data.get("trigger"),
                "created_at": data.get("created_at"),
                "ended_at": data.get("ended_at"),
            }
        )
        if len(rows) >= max(1, limit):
            break
    return {"status": "ok", "jobs": rows}


def _active_scope_conflicts(paths: dict[str, Path], write_scope: list[str]) -> list[dict[str, Any]]:
    conflicts: list[dict[str, Any]] = []
    for p in sorted(paths["jobs_dir"].glob("*.json")):
        job = _read_json(p, {})
        if not isinstance(job, dict):
            continue
        status = str(job.get("status", "")).strip()
        if status != "running":
            continue

        existing_scope = [str(x) for x in job.get("write_scope", []) if str(x).strip()]
        overlap_pairs: list[list[str]] = []
        for current in write_scope:
            for existing in existing_scope:
                if _scope_overlaps(current, existing):
                    overlap_pairs.append([current, existing])
        if overlap_pairs:
            conflicts.append(
                {
                    "job_id": str(job.get("job_id", "")),
                    "status": status,
                    "write_scope": existing_scope,
                    "overlap_pairs": overlap_pairs,
                }
            )
    return conflicts


def _stat_job(paths: dict[str, Path], job_id: str) -> tuple[int, dict[str, Any]]:
    job_path = _job_file(paths, job_id)
    if not job_path.exists():
        return 2, {"status": "error", "reason": "job_not_found", "job_id": job_id}
    job = _read_json(job_path, {})
    mailbox = _read_json(_mailbox_file(paths, job_id), {})
    agents = _load_agent_states(paths, job_id)
    return (
        0,
        {
            "status": "ok",
            "job": job,
            "mailbox": mailbox,
            "agents": agents,
            "log_file": str(_log_file(paths, job_id)),
        },
    )


def _transition_job(paths: dict[str, Path], job_id: str, target_status: str) -> tuple[int, dict[str, Any]]:
    job_path = _job_file(paths, job_id)
    if not job_path.exists():
        return 2, {"status": "error", "reason": "job_not_found", "job_id": job_id}

    job = _read_json(job_path, {})
    if not isinstance(job, dict):
        return 2, {"status": "error", "reason": "invalid_job_payload", "job_id": job_id}

    current = str(job.get("status", "")).strip()
    changed = current not in TERMINAL_JOB_STATUS and current != target_status
    if changed:
        job["status"] = target_status
        job["ended_at"] = _iso_now()
        job["updated_at"] = job["ended_at"]
        _write_json(job_path, job)

        mailbox_path = _mailbox_file(paths, job_id)
        mailbox = _read_json(mailbox_path, {})
        if isinstance(mailbox, dict):
            mailbox["status"] = "closed"
            mailbox["result_summary_ref"] = str(_log_file(paths, job_id))
            _write_json(mailbox_path, mailbox)
        _write_agent_states(paths, job, target_status)
        _append_ndjson(
            _log_file(paths, job_id),
            {
                "timestamp": _iso_now(),
                "event": f"job_{target_status}",
                "job_id": job_id,
            },
        )

    payload = {"status": "ok", "job_id": job_id, "target_status": target_status, "changed": changed}
    return 0, payload


def _load_job(paths: dict[str, Path], job_id: str) -> tuple[Path, dict[str, Any] | None]:
    job_path = _job_file(paths, job_id)
    if not job_path.exists():
        return job_path, None
    job = _read_json(job_path, {})
    return job_path, job if isinstance(job, dict) else None


def _resolve_trace_id(paths: dict[str, Path], job_id: str, trace_id: str) -> str:
    tid = trace_id.strip()
    if tid:
        return tid
    mailbox = _read_json(_mailbox_file(paths, job_id), {})
    if isinstance(mailbox, dict):
        fallback = str(mailbox.get("trace_id", "")).strip()
        if fallback:
            return fallback
    return _new_trace_id(job_id)


def _allowed_agents(job: dict[str, Any]) -> set[str]:
    out = {"coordinator"}
    out.add(str(job.get("from_agent", "")).strip())
    for agent in job.get("to_agents", []):
        text = str(agent).strip()
        if text:
            out.add(text)
    return {x for x in out if x}


def _read_relay_events(log_path: Path, trace_id: str) -> list[dict[str, Any]]:
    if not log_path.exists():
        return []
    rows: list[dict[str, Any]] = []
    with log_path.open("r", encoding="utf-8") as f:
        for line in f:
            text = line.strip()
            if not text:
                continue
            try:
                row = json.loads(text)
            except json.JSONDecodeError:
                continue
            if not isinstance(row, dict):
                continue
            if str(row.get("event", "")).strip() != "relay":
                continue
            if str(row.get("trace_id", "")).strip() != trace_id:
                continue
            rows.append(row)
    return rows


def _next_relay_seq(log_path: Path, trace_id: str) -> int:
    max_seq = -1
    for row in _read_relay_events(log_path, trace_id):
        seq = _safe_int(row.get("seq", -1), -1)
        if seq < 0:
            continue
        max_seq = max(max_seq, seq)
    return max_seq + 1


def _relay_send(
    paths: dict[str, Path],
    job_id: str,
    from_agent: str,
    to_agent: str,
    intent: str,
    payload_text: str,
    trace_id: str,
) -> tuple[int, dict[str, Any]]:
    _, job = _load_job(paths, job_id)
    if job is None:
        return 2, {"status": "error", "reason": "job_not_found", "job_id": job_id}

    status = str(job.get("status", "")).strip()
    if status != "running":
        return 2, {
            "status": "error",
            "reason": "job_not_running",
            "job_id": job_id,
            "job_status": status,
        }

    if intent not in RELAY_INTENTS:
        return 2, {"status": "error", "reason": "invalid_intent", "intent": intent}

    allowed = _allowed_agents(job)
    from_text = from_agent.strip()
    to_text = to_agent.strip()
    if from_text not in allowed or to_text not in allowed:
        return 2, {
            "status": "error",
            "reason": "scope_violation",
            "job_id": job_id,
            "allowed_agents": sorted(allowed),
            "from_agent": from_text,
            "to_agent": to_text,
        }

    resolved_trace_id = _resolve_trace_id(paths, job_id, trace_id)
    log_path = _log_file(paths, job_id)
    seq = _next_relay_seq(log_path, resolved_trace_id)
    relay = {
        "timestamp": _iso_now(),
        "event": "relay",
        "job_id": job_id,
        "trace_id": resolved_trace_id,
        "seq": seq,
        "from_agent": from_text,
        "to_agent": to_text,
        "intent": intent,
        "payload_text": payload_text,
    }
    _append_ndjson(log_path, relay)
    return 0, {
        "status": "ok",
        "job_id": job_id,
        "trace_id": resolved_trace_id,
        "seq": seq,
        "log_file": str(log_path),
    }


def _relay_replay(
    paths: dict[str, Path],
    job_id: str,
    trace_id: str,
    from_seq: int,
    limit: int,
) -> tuple[int, dict[str, Any]]:
    _, job = _load_job(paths, job_id)
    if job is None:
        return 2, {"status": "error", "reason": "job_not_found", "job_id": job_id}

    resolved_trace_id = _resolve_trace_id(paths, job_id, trace_id)
    rows = _read_relay_events(_log_file(paths, job_id), resolved_trace_id)
    seq_base = max(0, from_seq)
    rows = [x for x in rows if _safe_int(x.get("seq", -1), -1) >= seq_base]
    rows.sort(key=lambda x: _safe_int(x.get("seq", 0), 0))
    capped = rows[: max(1, limit)]
    events = [
        {
            "trace_id": str(x.get("trace_id", "")),
            "seq": _safe_int(x.get("seq", 0), 0),
            "from_agent": str(x.get("from_agent", "")),
            "to_agent": str(x.get("to_agent", "")),
            "intent": str(x.get("intent", "")),
            "payload_text": str(x.get("payload_text", "")),
            "timestamp": str(x.get("timestamp", "")),
        }
        for x in capped
    ]
    return 0, {
        "status": "ok",
        "job_id": job_id,
        "trace_id": resolved_trace_id,
        "count": len(events),
        "events": events,
    }


def _add_common_run_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--topic", default="general")
    parser.add_argument("--from-agent", default="coordinator")
    parser.add_argument("--to-agents", default="agent-a")
    parser.add_argument("--provider", choices=["codex", "copilot", "gemini"], default="codex")
    parser.add_argument(
        "--model",
        default="",
        help="Optional model override. Empty => provider default model.",
    )
    parser.add_argument(
        "--reasoning",
        default="",
        help="Optional reasoning override. Empty => provider default reasoning.",
    )
    parser.add_argument("--read-scope", default=".")
    parser.add_argument("--write-scope", default=".agents/**")
    parser.add_argument("--worker-mode", choices=sorted(WORKER_MODES), default="auto")
    parser.add_argument(
        "--worker-cmd-template",
        default="",
        help=(
            "Optional per-agent command template. Placeholders: "
            "{provider},{model},{reasoning},{topic},{job_id},{trace_id},{agent_id},"
            "{from_agent},{read_scope},{write_scope},{state_root}"
        ),
    )
    parser.add_argument("--worker-timeout-sec", type=int, default=120)
    parser.add_argument(
        "--worker-cwd",
        default=str(Path.cwd()),
        help="Working directory used by worker command execution.",
    )
    parser.add_argument(
        "--sdk-script",
        default=str(_default_sdk_script_path()),
        help="Path to copilot_sdk_orchestrator.mjs used when worker-mode=sdk.",
    )
    parser.add_argument(
        "--sdk-config-dir",
        default=str(Path.home() / ".copilot"),
        help="Copilot config directory passed to SDK orchestrator when provider=copilot.",
    )
    parser.add_argument(
        "--sdk-delegate-template",
        default="",
        help=(
            "Delegate command template used by SDK orchestrator for non-copilot providers. "
            "Placeholders: {provider},{model},{reasoning},{cwd},{prompt}; "
            "shell-safe variants: {provider_q},{model_q},{reasoning_q},{cwd_q},{prompt_q}."
        ),
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--state-root",
        default=str(Path.home() / ".agents" / "state" / "coordinator"),
        help="Coordinator state root directory.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    run_parser = sub.add_parser("run")
    _add_common_run_args(run_parser)
    run_parser.add_argument("--hold-open", action="store_true")

    jobs_parser = sub.add_parser("jobs")
    jobs_parser.add_argument("--limit", type=int, default=50)

    stat_parser = sub.add_parser("stat")
    stat_parser.add_argument("job_id")

    stop_parser = sub.add_parser("stop")
    stop_parser.add_argument("job_id")

    kill_parser = sub.add_parser("kill")
    kill_parser.add_argument("job_id")

    relay_send_parser = sub.add_parser("relay-send")
    relay_send_parser.add_argument("job_id")
    relay_send_parser.add_argument("--from-agent", required=True)
    relay_send_parser.add_argument("--to-agent", required=True)
    relay_send_parser.add_argument("--intent", choices=sorted(RELAY_INTENTS), required=True)
    relay_send_parser.add_argument("--payload-text", required=True)
    relay_send_parser.add_argument("--trace-id", default="")

    relay_replay_parser = sub.add_parser("relay-replay")
    relay_replay_parser.add_argument("job_id")
    relay_replay_parser.add_argument("--trace-id", default="")
    relay_replay_parser.add_argument("--from-seq", type=int, default=0)
    relay_replay_parser.add_argument("--limit", type=int, default=200)

    cron_parser = sub.add_parser("cron-run")
    _add_common_run_args(cron_parser)
    cron_parser.add_argument("--lock-ttl-sec", type=int, default=7200)

    args = parser.parse_args()
    paths = _layout(Path(args.state_root).expanduser().resolve())

    if args.command == "run":
        worker_cwd = Path(args.worker_cwd).expanduser().resolve()
        sdk_script = Path(args.sdk_script).expanduser().resolve()
        sdk_config_dir = Path(args.sdk_config_dir).expanduser().resolve()
        model, reasoning = _resolve_provider_runtime(args.provider, args.model, args.reasoning)
        result = _run_job(
            paths=paths,
            topic=args.topic,
            trigger="manual",
            from_agent=args.from_agent,
            to_agents=_parse_csv(args.to_agents),
            provider=args.provider,
            model=model,
            reasoning=reasoning,
            read_scope=_parse_csv(args.read_scope),
            write_scope=_parse_csv(args.write_scope),
            hold_open=bool(args.hold_open),
            worker_mode=args.worker_mode,
            worker_cmd_template=args.worker_cmd_template,
            worker_timeout_sec=max(1, args.worker_timeout_sec),
            worker_cwd=worker_cwd,
            sdk_script=sdk_script,
            sdk_config_dir=sdk_config_dir,
            sdk_delegate_template=args.sdk_delegate_template,
        )
        _print_json(result)
        return 0 if result.get("status") == "done" or result.get("status") == "running" else 2

    if args.command == "jobs":
        _print_json(_list_jobs(paths, args.limit))
        return 0

    if args.command == "stat":
        code, payload = _stat_job(paths, args.job_id)
        _print_json(payload)
        return code

    if args.command == "stop":
        code, payload = _transition_job(paths, args.job_id, "stopped")
        _print_json(payload)
        return code

    if args.command == "kill":
        code, payload = _transition_job(paths, args.job_id, "killed")
        _print_json(payload)
        return code

    if args.command == "relay-send":
        code, payload = _relay_send(
            paths=paths,
            job_id=args.job_id,
            from_agent=args.from_agent,
            to_agent=args.to_agent,
            intent=args.intent,
            payload_text=args.payload_text,
            trace_id=args.trace_id,
        )
        _print_json(payload)
        return code

    if args.command == "relay-replay":
        code, payload = _relay_replay(
            paths=paths,
            job_id=args.job_id,
            trace_id=args.trace_id,
            from_seq=args.from_seq,
            limit=args.limit,
        )
        _print_json(payload)
        return code

    if args.command == "cron-run":
        worker_cwd = Path(args.worker_cwd).expanduser().resolve()
        sdk_script = Path(args.sdk_script).expanduser().resolve()
        sdk_config_dir = Path(args.sdk_config_dir).expanduser().resolve()
        model, reasoning = _resolve_provider_runtime(args.provider, args.model, args.reasoning)
        ok, token, current = _acquire_lock(paths, mode="cron-run", ttl_sec=max(1, args.lock_ttl_sec))
        if not ok:
            _print_json(
                {
                    "status": "skipped_due_to_lock",
                    "reason": "lock_exists",
                    "lock": current or {},
                }
            )
            return 0
        try:
            result = _run_job(
                paths=paths,
                topic=args.topic,
                trigger="cron",
                from_agent=args.from_agent,
                to_agents=_parse_csv(args.to_agents),
                provider=args.provider,
                model=model,
                reasoning=reasoning,
                read_scope=_parse_csv(args.read_scope),
                write_scope=_parse_csv(args.write_scope),
                hold_open=False,
                worker_mode=args.worker_mode,
                worker_cmd_template=args.worker_cmd_template,
                worker_timeout_sec=max(1, args.worker_timeout_sec),
                worker_cwd=worker_cwd,
                sdk_script=sdk_script,
                sdk_config_dir=sdk_config_dir,
                sdk_delegate_template=args.sdk_delegate_template,
            )
            if result.get("status") == "blocked_by_scope_conflict":
                result["trigger"] = "cron"
                _print_json(result)
                return 2
            result["trigger"] = "cron"
            _print_json(result)
            return 0 if result.get("status") == "done" else 2
        finally:
            _release_lock(paths, token)

    _print_json({"status": "error", "reason": "unsupported_command"})
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
