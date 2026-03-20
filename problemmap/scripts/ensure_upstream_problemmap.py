#!/usr/bin/env python3
"""Ensure the upstream WFGY ProblemMap corpus exists locally as a fallback reference source."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path


class CommandError(RuntimeError):
    pass


def run(cmd: list[str], cwd: Path | None = None) -> None:
    proc = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True)
    if proc.returncode != 0:
        raise CommandError(
            f"command failed: {' '.join(cmd)}\nstdout:\n{proc.stdout}\nstderr:\n{proc.stderr}"
        )


def run_capture(cmd: list[str], cwd: Path | None = None) -> str:
    proc = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True)
    if proc.returncode != 0:
        raise CommandError(
            f"command failed: {' '.join(cmd)}\nstdout:\n{proc.stdout}\nstderr:\n{proc.stderr}"
        )
    return proc.stdout.strip()


def load_manifest(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"manifest not found: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def resolve_target(skill_root: Path, clone_target: str) -> Path:
    path = Path(clone_target)
    return path if path.is_absolute() else skill_root / path


def configure_sparse_checkout(target: Path, sparse_paths: list[str]) -> None:
    run(["git", "sparse-checkout", "init", "--cone"], cwd=target)
    run(["git", "sparse-checkout", "set", *sparse_paths], cwd=target)


def try_run(cmd: list[str], cwd: Path | None = None) -> bool:
    proc = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True)
    return proc.returncode == 0


def ref_exists(target: Path, ref: str) -> bool:
    return try_run(["git", "rev-parse", "--verify", f"{ref}^{{commit}}"], cwd=target)


def checkout_existing_head(target: Path) -> None:
    run(["git", "checkout", "-f", "HEAD"], cwd=target)


def checkout_ref(target: Path, ref: str, update: bool) -> str:
    if update:
        try:
            run(["git", "fetch", "origin", ref], cwd=target)
        except CommandError:
            pass

    if ref_exists(target, ref):
        run(["git", "checkout", ref], cwd=target)
        if update:
            try:
                run(["git", "pull", "--ff-only", "origin", ref], cwd=target)
            except CommandError:
                pass
        return ref

    remote_ref = f"origin/{ref}"
    if ref_exists(target, remote_ref):
        run(["git", "checkout", "-B", ref, remote_ref], cwd=target)
        return ref

    checkout_existing_head(target)
    return run_capture(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=target)


def resolve_seed_candidates(skill_root: Path, candidates: list[str]) -> list[Path]:
    resolved: list[Path] = []
    for item in candidates:
        path = Path(item)
        resolved.append(path if path.is_absolute() else skill_root / path)
    return resolved


def seed_has_sparse_paths(seed: Path, sparse_paths: list[str]) -> bool:
    return all((seed / rel).exists() for rel in sparse_paths)


def clone_from_seed(seed: Path, target: Path) -> None:
    run(["git", "clone", "--no-checkout", str(seed), str(target)])


def clone_from_remote(repo_url: str, target: Path) -> None:
    run(["git", "clone", "--filter=blob:none", "--no-checkout", repo_url, str(target)])


def copy_from_seed(seed: Path, target: Path, sparse_paths: list[str]) -> None:
    if target.exists():
        shutil.rmtree(target)
    target.mkdir(parents=True, exist_ok=True)
    for rel in sparse_paths:
        src = seed / rel
        dst = target / rel
        if src.is_dir():
            shutil.copytree(src, dst, dirs_exist_ok=True)
        elif src.is_file():
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)


def refresh_snapshot_from_seed(seed: Path, target: Path, sparse_paths: list[str]) -> None:
    copy_from_seed(seed, target, sparse_paths)


def verify_required_files(target: Path, required_files: list[str]) -> list[str]:
    missing = []
    for rel in required_files:
        if not (target / rel).exists():
            missing.append(rel)
    return missing


def ensure_upstream(manifest_path: Path, update: bool) -> dict:
    skill_root = manifest_path.parent.parent
    manifest = load_manifest(manifest_path)
    repo_url = manifest["repo_url"]
    ref = manifest.get("default_ref", "main")
    seed_candidates = resolve_seed_candidates(skill_root, manifest.get("local_seed_candidates", []))
    sparse_paths = manifest.get("sparse_paths", ["ProblemMap"])
    target = resolve_target(skill_root, manifest.get("clone_target", "references/upstream/WFGY"))
    target.parent.mkdir(parents=True, exist_ok=True)

    action = "existing"
    selected_ref = ref
    source = repo_url
    if not target.exists():
        seed = next((candidate for candidate in seed_candidates if seed_has_sparse_paths(candidate, sparse_paths)), None)
        if seed is not None:
            source = str(seed)
            if (seed / ".git").exists():
                try:
                    clone_from_seed(seed, target)
                    action = "seed-cloned"
                    configure_sparse_checkout(target, sparse_paths)
                    checkout_existing_head(target)
                    selected_ref = run_capture(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=target)
                except CommandError:
                    copy_from_seed(seed, target, sparse_paths)
                    action = "seed-copied"
                    selected_ref = "seed-snapshot"
            else:
                copy_from_seed(seed, target, sparse_paths)
                action = "seed-copied"
                selected_ref = "seed-snapshot"
        else:
            clone_from_remote(repo_url, target)
            action = "cloned"
            configure_sparse_checkout(target, sparse_paths)
            selected_ref = checkout_ref(target, ref, update=update)
    else:
        if not (target / ".git").exists():
            seed = next((candidate for candidate in seed_candidates if seed_has_sparse_paths(candidate, sparse_paths)), None)
            if update and seed is not None:
                refresh_snapshot_from_seed(seed, target, sparse_paths)
                action = "seed-refreshed"
            else:
                action = "existing-snapshot"
            selected_ref = "seed-snapshot"
        else:
            configure_sparse_checkout(target, sparse_paths)
            selected_ref = checkout_ref(target, ref, update=update)
            if update:
                action = "updated"

    missing = verify_required_files(target, manifest.get("required_files", []))
    if missing:
        raise RuntimeError(f"missing required upstream files after ensure: {missing}")

    return {
        "status": "ok",
        "action": action,
        "source": source,
        "target": str(target),
        "ref": selected_ref,
        "required_files": [str(target / rel) for rel in manifest.get("required_files", [])],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--manifest",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "references" / "upstream-source.json",
        help="Path to upstream-source.json",
    )
    parser.add_argument("--update", action="store_true", help="Fetch and fast-forward the existing clone")
    args = parser.parse_args()

    try:
        result = ensure_upstream(args.manifest, update=args.update)
    except (CommandError, FileNotFoundError, RuntimeError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "error", "error": str(exc)}, indent=2, ensure_ascii=False))
        return 1

    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
