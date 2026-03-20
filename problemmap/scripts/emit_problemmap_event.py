#!/usr/bin/env python3
"""Convert a ProblemMap diagnosis into an evolve-ready experience artifact."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

CONFIDENCE_ORDER = {"low": 0, "medium": 1, "high": 2}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def gate_diagnosis(diagnosis: dict[str, Any]) -> tuple[bool, str]:
    atlas = diagnosis.get("atlas", {})
    confidence = str(atlas.get("confidence", "low"))
    evidence = str(atlas.get("evidence_sufficiency", "weak"))
    if CONFIDENCE_ORDER.get(confidence, 0) < CONFIDENCE_ORDER["medium"]:
        return False, "confidence below medium"
    if evidence == "weak":
        return False, "evidence_sufficiency is weak"
    return True, "gate passed"


def build_event_type(diagnosis: dict[str, Any]) -> str:
    primary_family = str(diagnosis.get("atlas", {}).get("primary_family", "unresolved")).strip()
    if primary_family and primary_family != "unresolved":
        family_token = primary_family.split()[0].lower()
        if family_token.startswith("f") and family_token[1:].isdigit():
            return f"problemmap-atlas-{family_token}"

    candidates = diagnosis.get("pm1_candidates", [])
    if candidates:
        number = int(candidates[0]["number"])
        return f"problemmap-pm1-{number:02d}"
    return "problemmap-unresolved"


def build_artifact(diagnosis: dict[str, Any]) -> dict[str, Any]:
    allow, reason = gate_diagnosis(diagnosis)
    atlas = diagnosis.get("atlas", {})
    return {
        "status": "ok",
        "event_type": build_event_type(diagnosis),
        "target_skill_id": "problemmap",
        "decision_reason": "; ".join(
            item
            for item in [
                reason,
                f"broken_invariant={atlas.get('broken_invariant', 'undetermined')}",
                f"why_primary_not_secondary={atlas.get('why_primary_not_secondary', 'n/a')}",
                f"misrepair_risk={atlas.get('misrepair_risk', 'n/a')}",
            ]
            if item
        ),
        "writeback_gate": {
            "allow": allow,
            "confidence": atlas.get("confidence", "low"),
            "evidence_sufficiency": atlas.get("evidence_sufficiency", "weak"),
        },
        "pm1_candidates": diagnosis.get("pm1_candidates", []),
        "atlas": atlas,
        "global_fix_route": diagnosis.get("global_fix_route", {}),
        "source_case": diagnosis.get("source_case"),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("diagnosis_json", type=Path, help="Path to a ProblemMap diagnosis JSON file")
    parser.add_argument("--output", type=Path, help="Optional path to write the experience artifact JSON")
    args = parser.parse_args()

    try:
        diagnosis = load_json(args.diagnosis_json)
        artifact = build_artifact(diagnosis)
    except (OSError, json.JSONDecodeError, ValueError, KeyError) as exc:
        print(json.dumps({"status": "error", "error": str(exc)}, indent=2, ensure_ascii=False))
        return 1

    payload = json.dumps(artifact, indent=2, ensure_ascii=False)
    if args.output:
        args.output.write_text(payload + "\n", encoding="utf-8")
    print(payload)
    return 0


if __name__ == "__main__":
    sys.exit(main())
