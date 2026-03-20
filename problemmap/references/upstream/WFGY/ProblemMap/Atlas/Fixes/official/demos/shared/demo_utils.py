from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable, Mapping
from urllib.request import urlopen


REQUIRED_DEMO_FILES = (
    "input_case.json",
    "replay_outputs.json",
    "expected_output.json",
)

ROUTE_TARGET_FIELDS = (
    "primary_family",
    "secondary_family",
    "best_current_fit",
    "broken_invariant",
)

MODE_LABELS = {
    "replay": "Replay-only MVP",
    "live": "Live reproduction",
}


def is_url(value: str) -> bool:
    return value.startswith("http://") or value.startswith("https://")


def _read_text(path_or_url: str | Path, encoding: str = "utf-8") -> str:
    value = str(path_or_url)

    if is_url(value):
        with urlopen(value) as response:
            return response.read().decode(encoding)

    return Path(value).read_text(encoding=encoding)


def load_json(path_or_url: str | Path) -> dict[str, Any]:
    text = _read_text(path_or_url)
    data = json.loads(text)

    if not isinstance(data, dict):
        raise TypeError(f"Expected a JSON object from {path_or_url}, got {type(data).__name__}")

    return data


def dump_json(data: Mapping[str, Any], indent: int = 2) -> str:
    return json.dumps(data, indent=indent, ensure_ascii=False)


def resolve_path(base_dir: str | Path, filename: str) -> Path:
    return Path(base_dir).expanduser().resolve() / filename


def load_input_case(base_dir: str | Path = ".") -> dict[str, Any]:
    return load_json(resolve_path(base_dir, "input_case.json"))


def load_replay_outputs(base_dir: str | Path = ".") -> dict[str, Any]:
    return load_json(resolve_path(base_dir, "replay_outputs.json"))


def load_expected_output(base_dir: str | Path = ".") -> dict[str, Any]:
    return load_json(resolve_path(base_dir, "expected_output.json"))


def load_demo_bundle(base_dir: str | Path = ".") -> dict[str, dict[str, Any]]:
    return {
        "input_case": load_input_case(base_dir),
        "replay_outputs": load_replay_outputs(base_dir),
        "expected_output": load_expected_output(base_dir),
    }


def validate_required_keys(
    data: Mapping[str, Any],
    required_keys: Iterable[str],
    label: str = "data",
) -> None:
    missing = [key for key in required_keys if key not in data]
    if missing:
        raise KeyError(f"Missing required keys in {label}: {', '.join(missing)}")


def validate_family_target(input_case: Mapping[str, Any]) -> None:
    if "family_target" not in input_case:
        raise KeyError("Missing required key in input_case: family_target")

    family_target = input_case["family_target"]
    if not isinstance(family_target, dict):
        raise TypeError("input_case['family_target'] must be a JSON object")

    validate_required_keys(
        family_target,
        ROUTE_TARGET_FIELDS,
        label="input_case.family_target",
    )


def validate_demo_bundle(base_dir: str | Path = ".") -> dict[str, Any]:
    base = Path(base_dir).expanduser().resolve()
    status: dict[str, Any] = {
        "base_dir": str(base),
        "required_files": {},
        "is_complete": True,
    }

    for filename in REQUIRED_DEMO_FILES:
        path = resolve_path(base, filename)
        exists = path.exists()
        status["required_files"][filename] = exists
        if not exists:
            status["is_complete"] = False

    if status["is_complete"]:
        bundle = load_demo_bundle(base)
        validate_required_keys(bundle["input_case"], ("title", "user_question", "family_target"), "input_case")
        validate_family_target(bundle["input_case"])

    return status


def get_mode_label(mode: str) -> str:
    return MODE_LABELS.get(mode.strip().lower(), f"Unknown mode: {mode}")


def is_replay_mode(mode: str) -> bool:
    return mode.strip().lower() == "replay"


def is_live_mode(mode: str) -> bool:
    return mode.strip().lower() == "live"


def normalize_mode(mode: str) -> str:
    value = mode.strip().lower()
    if value not in MODE_LABELS:
        raise ValueError(f"Unsupported mode: {mode}")
    return value


def pretty_json(data: Mapping[str, Any], indent: int = 2) -> str:
    return json.dumps(data, indent=indent, ensure_ascii=False, sort_keys=False)


def print_section(title: str, width: int = 88) -> None:
    line = "=" * width
    print()
    print(line)
    print(title)
    print(line)


def format_bullets(items: Iterable[Any], prefix: str = "- ") -> str:
    return "\n".join(f"{prefix}{item}" for item in items)


def summarize_family_target(input_case: Mapping[str, Any]) -> dict[str, Any]:
    validate_family_target(input_case)
    family_target = input_case["family_target"]

    return {
        "primary_family": family_target["primary_family"],
        "secondary_family": family_target["secondary_family"],
        "best_current_fit": family_target["best_current_fit"],
        "broken_invariant": family_target["broken_invariant"],
    }


def format_route_summary(input_case: Mapping[str, Any]) -> str:
    route = summarize_family_target(input_case)

    lines = [
        "Route summary",
        f"Primary family   : {route['primary_family']}",
        f"Secondary family : {route['secondary_family']}",
        f"Best current fit : {route['best_current_fit']}",
        f"Broken invariant : {route['broken_invariant']}",
    ]
    return "\n".join(lines)


def format_case_overview(input_case: Mapping[str, Any]) -> str:
    title = input_case.get("title", "Untitled case")
    question = input_case.get("user_question", "No user question provided.")
    return "\n".join(
        [
            f"Title    : {title}",
            f"Question : {question}",
        ]
    )


def format_before_after(
    before: Any,
    after: Any,
    before_label: str = "Before",
    after_label: str = "After",
    width: int = 88,
) -> str:
    line = "-" * width
    return "\n".join(
        [
            line,
            before_label,
            line,
            str(before),
            "",
            line,
            after_label,
            line,
            str(after),
        ]
    )


def format_checklist(items: Iterable[str], ordered: bool = True) -> str:
    lines = []
    for index, item in enumerate(items, start=1):
        prefix = f"{index}. " if ordered else "- "
        lines.append(f"{prefix}{item}")
    return "\n".join(lines)


def get_before_after_from_replay_outputs(
    replay_outputs: Mapping[str, Any],
    before_key: str,
    after_key: str,
) -> tuple[Any, Any]:
    if before_key not in replay_outputs:
        raise KeyError(f"Missing key in replay_outputs: {before_key}")
    if after_key not in replay_outputs:
        raise KeyError(f"Missing key in replay_outputs: {after_key}")

    return replay_outputs[before_key], replay_outputs[after_key]


def get_default_bundle_summary(base_dir: str | Path = ".") -> str:
    bundle = load_demo_bundle(base_dir)
    input_case = bundle["input_case"]
    replay_outputs = bundle["replay_outputs"]
    expected_output = bundle["expected_output"]

    parts = [
        format_case_overview(input_case),
        "",
        format_route_summary(input_case),
        "",
        "Replay output keys",
        format_bullets(replay_outputs.keys()),
        "",
        "Expected output keys",
        format_bullets(expected_output.keys()),
    ]
    return "\n".join(parts)


__all__ = [
    "REQUIRED_DEMO_FILES",
    "ROUTE_TARGET_FIELDS",
    "MODE_LABELS",
    "is_url",
    "load_json",
    "dump_json",
    "resolve_path",
    "load_input_case",
    "load_replay_outputs",
    "load_expected_output",
    "load_demo_bundle",
    "validate_required_keys",
    "validate_family_target",
    "validate_demo_bundle",
    "get_mode_label",
    "is_replay_mode",
    "is_live_mode",
    "normalize_mode",
    "pretty_json",
    "print_section",
    "format_bullets",
    "summarize_family_target",
    "format_route_summary",
    "format_case_overview",
    "format_before_after",
    "format_checklist",
    "get_before_after_from_replay_outputs",
    "get_default_bundle_summary",
]
