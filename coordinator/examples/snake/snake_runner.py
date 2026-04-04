#!/usr/bin/env python3
"""Terminal auto-snake demo with optional coordinator relay integration."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys
import time
from typing import Any

from snake_agents import AgentMessage, MultiAgentPolicy
from snake_core import SnakeEngine


def _default_coordinator_script() -> Path:
    here = Path(__file__).resolve()
    candidates = [
        # Source template path:
        # .../.agents/skills/custom/coordinator/examples/snake/snake_runner.py
        # -> .../.agents/skills/custom/coordinator/scripts/coordinator.py
        here.parents[2] / "scripts" / "coordinator.py",
        # Generated repo path:
        # .../snake_demo/snake_runner.py
        # -> .../.agents/skills/custom/coordinator/scripts/coordinator.py
        here.parents[1] / ".agents" / "skills" / "custom" / "coordinator" / "scripts" / "coordinator.py",
        # Home deployed path.
        Path.home() / ".agents" / "skills" / "custom" / "coordinator" / "scripts" / "coordinator.py",
        Path.home() / ".agent" / "skills" / "custom" / "coordinator" / "scripts" / "coordinator.py",
        # Backward-compatible wrapper paths.
        Path.home() / ".agents" / "tools" / "coordinator" / "scripts" / "coordinator.py",
        Path.home() / ".agent" / "tools" / "coordinator" / "scripts" / "coordinator.py",
    ]
    for path in candidates:
        if path.exists():
            return path
    return candidates[0]


def _run_json(cmd: list[str], check: bool = True) -> dict[str, Any]:
    proc = subprocess.run(cmd, text=True, capture_output=True, check=False)
    if check and proc.returncode != 0:
        raise RuntimeError(f"command failed rc={proc.returncode}: {' '.join(cmd)}\nstdout={proc.stdout}\nstderr={proc.stderr}")
    text = proc.stdout.strip()
    if not text:
        raise RuntimeError(f"empty stdout: {' '.join(cmd)}")
    return json.loads(text)


class CoordinatorClient:
    def __init__(self, script_path: Path, state_root: Path) -> None:
        self.script_path = script_path
        self.state_root = state_root

    def start(self, topic: str, to_agents: list[str]) -> tuple[str, str]:
        payload = _run_json(
            [
                sys.executable,
                str(self.script_path),
                "--state-root",
                str(self.state_root),
                "run",
                "--topic",
                topic,
                "--from-agent",
                "coordinator",
                "--to-agents",
                ",".join(to_agents),
                "--hold-open",
                "--worker-mode",
                "none",
            ]
        )
        return str(payload["job_id"]), str(payload["trace_id"])

    def relay(self, job_id: str, trace_id: str, row: AgentMessage) -> None:
        _run_json(
            [
                sys.executable,
                str(self.script_path),
                "--state-root",
                str(self.state_root),
                "relay-send",
                job_id,
                "--from-agent",
                row.from_agent,
                "--to-agent",
                row.to_agent,
                "--intent",
                row.intent,
                "--payload-text",
                row.payload_text,
                "--trace-id",
                trace_id,
            ]
        )

    def stop(self, job_id: str) -> None:
        _run_json(
            [
                sys.executable,
                str(self.script_path),
                "--state-root",
                str(self.state_root),
                "stop",
                job_id,
            ],
            check=False,
        )


def _render_frame(engine: SnakeEngine) -> None:
    sys.stdout.write("\x1b[H\x1b[J")
    sys.stdout.write(engine.render() + "\n")
    sys.stdout.flush()


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Auto terminal snake with optional coordinator relay logging.")
    parser.add_argument("--width", type=int, default=20)
    parser.add_argument("--height", type=int, default=12)
    parser.add_argument("--steps", type=int, default=120)
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--tick-ms", type=int, default=40)
    parser.add_argument("--no-render", action="store_true")
    parser.add_argument("--use-coordinator", action="store_true")
    parser.add_argument("--state-root", default=str(Path.home() / ".agents" / "state" / "coordinator"))
    parser.add_argument("--topic", default="snake-auto")
    parser.add_argument("--summary-out", default="")
    parser.add_argument("--coordinator-script", default=str(_default_coordinator_script()))
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    engine = SnakeEngine(width=args.width, height=args.height, seed=args.seed)
    policy = MultiAgentPolicy()

    job_id = ""
    trace_id = ""
    client: CoordinatorClient | None = None

    if args.use_coordinator:
        client = CoordinatorClient(
            script_path=Path(args.coordinator_script).expanduser().resolve(),
            state_root=Path(args.state_root).expanduser().resolve(),
        )
        job_id, trace_id = client.start(topic=args.topic, to_agents=policy.agent_ids)

    alive = True
    try:
        if not args.no_render:
            _render_frame(engine)
        for _ in range(max(1, args.steps)):
            direction, messages = policy.decide(engine)
            if client is not None:
                for row in messages:
                    client.relay(job_id=job_id, trace_id=trace_id, row=row)
            alive = engine.apply(direction)
            if not args.no_render:
                _render_frame(engine)
                if args.tick_ms > 0:
                    time.sleep(args.tick_ms / 1000.0)
            if not alive:
                break
    finally:
        if client is not None and job_id:
            client.stop(job_id)

    result = "max_steps" if alive else "collision"
    summary = {
        "status": "ok",
        "result": result,
        "steps": engine.step,
        "score": engine.score,
        "length": len(engine.body),
        "head": list(engine.head),
        "food": list(engine.food),
        "job_id": job_id,
        "trace_id": trace_id,
        "state_root": str(Path(args.state_root).expanduser().resolve()) if args.use_coordinator else "",
    }

    if args.summary_out:
        out = Path(args.summary_out).expanduser().resolve()
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(json.dumps(summary, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
