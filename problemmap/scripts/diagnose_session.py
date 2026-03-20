#!/usr/bin/env python3
"""Emit a first structured ProblemMap diagnosis from a failure-bearing case JSON."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

PM1_HEURISTICS = [
    (1, "hallucination & chunk drift", ["hallucination", "chunk drift", "anchor mismatch", "wrong source", "referent drift"]),
    (2, "interpretation collapse", ["misunderstood", "misread", "interpretation", "instruction collapse"]),
    (3, "long reasoning chains", ["long reasoning", "chain of thought", "recursive chain", "reasoning chain"]),
    (4, "bluffing / overconfidence", ["overconfident", "confident but wrong", "bluff", "fake certainty"]),
    (5, "semantic != embedding", ["embedding", "semantic mismatch", "retrieval mismatch", "vector drift"]),
    (6, "logic collapse & recovery", ["logic collapse", "contradiction", "inference failure", "recovery scaffold"]),
    (7, "memory breaks across sessions", ["memory", "forgot", "context_compacted", "lost context", "session drift", "persistence"]),
    (8, "debugging black box", ["black box", "no trace", "missing logs", "uninspectable", "no visibility"]),
    (9, "entropy collapse", ["entropy collapse", "fragmentation", "drift", "incoherent"]),
    (10, "creative freeze", ["creative freeze", "stuck", "blank", "freeze"]),
    (11, "symbolic collapse", ["symbolic collapse", "json", "schema", "representation", "carrier distortion"]),
    (12, "philosophical recursion", ["philosophical recursion", "self-reference", "meta loop", "recursion"]),
    (13, "multi-agent chaos", ["multi-agent", "parallel", "race", "conflict", "coordinator"]),
    (14, "bootstrap ordering", ["bootstrap", "startup", "init order", "ordering"]),
    (15, "deployment deadlock", ["deploy", "deadlock", "rollout blocked"]),
    (16, "pre-deploy collapse", ["pre-deploy", "predeploy", "ci gate", "before deploy"]),
]

ATLAS_FAMILIES = [
    {
        "id": "F1",
        "name": "Grounding & Evidence Integrity",
        "broken_invariant": "anchor_to_claim_coupling_broken",
        "keywords": [
            "hallucination",
            "anchor mismatch",
            "evidence mismatch",
            "referent drift",
            "wrong source",
            "target mismatch",
            "grounding",
        ],
        "pm1_support": [1, 5],
        "first_fix": "re-grounding -> evidence verification -> target-reference audit",
        "misrepair": "rewriting tone or style before anchor restoration",
    },
    {
        "id": "F2",
        "name": "Reasoning & Progression Integrity",
        "broken_invariant": "progression_continuity_broken",
        "keywords": [
            "reasoning",
            "inference",
            "logic collapse",
            "recursive",
            "decomposition",
            "contradiction",
            "progression break",
            "loop",
        ],
        "pm1_support": [2, 3, 4, 6, 10, 12],
        "first_fix": "decomposition reset -> interpretation checkpoint -> recovery scaffold",
        "misrepair": "redesigning the carrier when the real failure is progression",
    },
    {
        "id": "F3",
        "name": "State & Continuity Integrity",
        "broken_invariant": "state_continuity_broken",
        "keywords": [
            "memory",
            "ownership",
            "role",
            "continuity",
            "persistence",
            "session drift",
            "multi-agent",
            "interaction thread",
        ],
        "pm1_support": [7, 13],
        "first_fix": "continuity restoration -> role fencing -> provenance tracing",
        "misrepair": "adding more instructions before continuity infrastructure is restored",
    },
    {
        "id": "F4",
        "name": "Execution & Contract Integrity",
        "broken_invariant": "execution_skeleton_closure_broken",
        "keywords": [
            "bootstrap",
            "ordering",
            "readiness",
            "bridge",
            "liveness",
            "deadlock",
            "deployment",
            "contract",
            "protocol",
            "execution",
            "closure",
        ],
        "pm1_support": [14, 15, 16],
        "first_fix": "readiness audit -> ordering validation -> bridge and closure-path trace",
        "misrepair": "improving reasoning before fixing the runtime skeleton",
    },
    {
        "id": "F5",
        "name": "Observability & Diagnosability Integrity",
        "broken_invariant": "failure_path_visibility_broken",
        "keywords": [
            "traceability",
            "audit",
            "visibility",
            "black box",
            "uninspectable",
            "no logs",
            "observability",
            "diagnosability",
            "warning blindness",
        ],
        "pm1_support": [8],
        "first_fix": "observability insertion -> trace exposure -> audit-route uplift",
        "misrepair": "launching higher-order intervention before exposing the failure path",
    },
    {
        "id": "F6",
        "name": "Boundary & Safety Integrity",
        "broken_invariant": "boundary_integrity_broken",
        "keywords": [
            "boundary",
            "safety",
            "erosion",
            "capture",
            "overshoot",
            "drift",
            "fragmentation",
            "unstable boundary",
            "alignment",
            "control path",
        ],
        "pm1_support": [9],
        "first_fix": "alignment guard -> control-path audit -> damping and stabilization",
        "misrepair": "improving observability only while the boundary itself is already drifting",
    },
    {
        "id": "F7",
        "name": "Representation & Localization Integrity",
        "broken_invariant": "representation_container_fidelity_broken",
        "keywords": [
            "representation",
            "carrier",
            "descriptor",
            "layout",
            "schema",
            "json",
            "symbolic",
            "structural shell",
            "local anchor",
            "ocr",
        ],
        "pm1_support": [11],
        "first_fix": "descriptor audit -> structural preservation -> local anchor repair",
        "misrepair": "repairing reasoning or grounding while the carrier remains untrustworthy",
    },
]

FAILURE_SIGNAL_FAMILY_HINTS = {
    "event:context_compacted": ["F3"],
    "event:turn_aborted": ["F4"],
    "event:wrong_approach": ["F2"],
    "event:misunderstood_request": ["F2"],
    "event:buggy_code": ["F4"],
    "event:excessive_changes": ["F2", "F4"],
    "nonzero-exit-code": ["F4"],
}


def load_case(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def maybe_ensure_upstream(ensure_upstream: bool) -> None:
    if not ensure_upstream:
        return
    script = Path(__file__).resolve().parent / "ensure_upstream_problemmap.py"
    subprocess.run([sys.executable, str(script)], check=True)


def match_pm1(text: str) -> list[dict[str, Any]]:
    lowered = text.lower()
    matches: list[dict[str, Any]] = []
    for number, label, keywords in PM1_HEURISTICS:
        hit_count = sum(1 for keyword in keywords if keyword in lowered)
        if hit_count:
            confidence = "high" if hit_count >= 2 else "medium"
            matches.append({"number": number, "label": label, "confidence": confidence, "score": hit_count})
    matches.sort(key=lambda item: (-int(item["score"]), int(item["number"])))
    for item in matches:
        item.pop("score", None)
    return matches[:3]


def select_references(mode: str, text: str) -> list[str]:
    refs = [
        "references/pm1-taxonomy.md",
        "references/atlas-adapter-core.md",
        "references/atlas-family-core.md",
        "references/atlas-runtime-modes.md",
        "references/atlas-failure-discipline.md",
    ]
    lowered = text.lower()
    if mode == "teaching":
        refs.append("references/canonical-casebook.md")
    if any(token in lowered for token in ["deploy", "deadlock", "bootstrap", "bridge", "liveness", "observability", "trace"]):
        refs.append("references/router-v1.txt")
    if any(token in lowered for token in ["vendor", "provider", "tool-specific", "page", "fix"]):
        refs.append("references/global-fix-routing.md")
    return refs


def score_families(text: str, signals: list[str], pm1_candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    lowered = text.lower()
    scored: list[dict[str, Any]] = []
    for family in ATLAS_FAMILIES:
        score = 0
        matched: list[str] = []
        for keyword in family["keywords"]:
            if keyword in lowered:
                score += 2 if " " in keyword else 1
                matched.append(keyword)
        supported_pm1 = []
        for candidate in pm1_candidates:
            if int(candidate["number"]) in family["pm1_support"]:
                score += 2
                supported_pm1.append(int(candidate["number"]))
                matched.append(f"pm1:{candidate['number']}")
        for signal in signals:
            if family["id"] in FAILURE_SIGNAL_FAMILY_HINTS.get(signal, []):
                score += 1
                matched.append(signal)
        scored.append(
            {
                "family": family,
                "score": score,
                "matched_keywords": matched,
                "supported_pm1": supported_pm1,
            }
        )
    scored.sort(key=lambda item: item["score"], reverse=True)
    return scored


def describe_primary_vs_secondary(primary: dict[str, Any], secondary: dict[str, Any] | None) -> str:
    primary_family = primary["family"]
    primary_matches = primary["matched_keywords"][:4]
    if secondary is None or secondary["score"] <= 0:
        joined = ", ".join(primary_matches) if primary_matches else "coarse structural evidence"
        return (
            f"{primary_family['id']} is primary because the current evidence points first to "
            f"{primary_family['broken_invariant']} ({joined}), and neighboring family pressure is weak."
        )

    secondary_family = secondary["family"]
    primary_joined = ", ".join(primary_matches) if primary_matches else primary_family["broken_invariant"]
    secondary_joined = ", ".join(secondary["matched_keywords"][:3]) if secondary["matched_keywords"] else secondary_family["broken_invariant"]
    return (
        f"{primary_family['id']} beats {secondary_family['id']} because the earliest decisive signals "
        f"fit {primary_family['broken_invariant']} ({primary_joined}) more directly than the neighboring "
        f"pressure for {secondary_family['broken_invariant']} ({secondary_joined})."
    )


def calibrate_confidence(primary_score: int, secondary_score: int, evidence_count: int) -> tuple[str, str]:
    gap = primary_score - secondary_score
    if primary_score >= 6 and gap >= 2 and evidence_count >= 2:
        return "high", "sufficient"
    if primary_score >= 3:
        return "medium", "partial"
    return "low", "weak"


def build_global_fix_route(primary_family: dict[str, Any], confidence: str) -> dict[str, Any]:
    if confidence == "low":
        return {"family": None, "page": None, "minimal_fix": None}

    family_id = primary_family["id"]
    if family_id == "F4":
        return {
            "family": "Agents & Orchestration",
            "page": "choose after runtime evidence review",
            "minimal_fix": "audit readiness, ordering, and closure path before changing prompts",
        }
    if family_id == "F5":
        return {
            "family": "Eval / Observability",
            "page": "choose after traceability review",
            "minimal_fix": "expose the failure path before deeper intervention",
        }
    if family_id == "F3":
        return {
            "family": "Agents & Orchestration",
            "page": "choose after continuity review",
            "minimal_fix": "restore role, persistence, and interaction continuity first",
        }
    return {"family": None, "page": None, "minimal_fix": None}


def build_diagnosis(case: dict[str, Any], mode: str) -> dict[str, Any]:
    evidence = case.get("evidence", [])
    signals = case.get("candidate_failure_signals", [])
    text = " ".join([case.get("expected", ""), case.get("actual", ""), *evidence, *signals])
    pm1_candidates = match_pm1(text)
    ranked_families = score_families(text, signals, pm1_candidates)

    primary = ranked_families[0]
    secondary = ranked_families[1] if len(ranked_families) > 1 and ranked_families[1]["score"] > 0 else None
    primary_score = int(primary["score"])
    secondary_score = int(secondary["score"]) if secondary else 0
    confidence, evidence_sufficiency = calibrate_confidence(primary_score, secondary_score, len(evidence))

    if primary_score <= 0:
        primary_family_name = "unresolved"
        broken_invariant = "undetermined"
        best_current_fit = "no-fit"
        fit_level = "coarse"
        why_primary = (
            "No Atlas family has enough structural evidence yet. Prefer need_more_evidence over decorative precision."
        )
        fix_surface_direction = "collect better structural evidence before routing"
        misrepair_risk = "forcing a decorative family choice under thin evidence"
        need_more_evidence = True
        global_fix_route = {"family": None, "page": None, "minimal_fix": None}
    else:
        family = primary["family"]
        primary_family_name = f"{family['id']} {family['name']}"
        broken_invariant = family["broken_invariant"]
        best_current_fit = "family-level"
        fit_level = "family"
        why_primary = describe_primary_vs_secondary(primary, secondary)
        fix_surface_direction = family["first_fix"]
        misrepair_risk = family["misrepair"]
        need_more_evidence = evidence_sufficiency == "weak"
        global_fix_route = build_global_fix_route(family, confidence)

    result = {
        "status": "ok",
        "diagnostic_mode": mode,
        "implementation_state": "development-heuristic-router",
        "pm1_candidates": pm1_candidates,
        "atlas": {
            "primary_family": primary_family_name,
            "secondary_family": f"{secondary['family']['id']} {secondary['family']['name']}" if secondary else "none",
            "why_primary_not_secondary": why_primary,
            "broken_invariant": broken_invariant,
            "best_current_fit": best_current_fit,
            "fit_level": fit_level,
            "fix_surface_direction": fix_surface_direction,
            "misrepair_risk": misrepair_risk,
            "confidence": confidence,
            "evidence_sufficiency": evidence_sufficiency,
        },
        "global_fix_route": global_fix_route,
        "source_case": case.get("source_session") or case.get("source_case"),
        "references_used": select_references(mode, text),
    }
    if need_more_evidence:
        result["need_more_evidence"] = True
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("case_json", type=Path, help="Path to a failure-bearing case JSON file")
    parser.add_argument("--mode", choices=["strict", "teaching", "repair_preview", "compact"], default="strict")
    parser.add_argument("--ensure-upstream", action="store_true", help="Ensure upstream references before diagnosing")
    parser.add_argument("--output", type=Path, help="Optional path to write the diagnosis JSON")
    args = parser.parse_args()

    try:
        maybe_ensure_upstream(args.ensure_upstream)
        case = load_case(args.case_json)
        diagnosis = build_diagnosis(case, args.mode)
    except (OSError, json.JSONDecodeError, subprocess.CalledProcessError, ValueError) as exc:
        print(json.dumps({"status": "error", "error": str(exc)}, indent=2, ensure_ascii=False))
        return 1

    payload = json.dumps(diagnosis, indent=2, ensure_ascii=False)
    if args.output:
        args.output.write_text(payload + "\n", encoding="utf-8")
    print(payload)
    return 0


if __name__ == "__main__":
    sys.exit(main())
