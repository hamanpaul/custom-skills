#!/usr/bin/env python3
"""Simple Liu (boshiamy) decode helper packaged inside repo."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


DEFAULT_TABLE_CANDIDATES = [
    Path(__file__).resolve().parent / "liu_mcp_table.tsv",
    Path.home() / ".paul_tools" / "mcp_server" / "liu-mcp" / "data" / "liu_mcp_table.tsv",
]


def load_table(explicit: str | None) -> dict[str, list[str]]:
    table_path = Path(explicit).expanduser() if explicit else None
    candidates = [table_path] if table_path else DEFAULT_TABLE_CANDIDATES
    chosen = next((p for p in candidates if p and p.exists()), None)
    if not chosen:
        raise FileNotFoundError("liu_mcp_table.tsv not found.")

    exact: dict[str, list[str]] = {}
    with chosen.open(encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            code = row.get("code")
            char = row.get("char")
            if not code or not char:
                continue
            exact.setdefault(code, []).append(char)
    return exact


def decode(exact: dict[str, list[str]], line: str) -> dict:
    tokens = [t for t in line.strip().split() if t]
    segments = []
    for tok in tokens:
        if tok in exact:
            segments.append({"type": "decoded", "code": tok, "text": exact[tok][0]})
        else:
            segments.append({"type": "raw", "code": tok, "text": tok})
    text = "".join(seg["text"] for seg in segments)
    return {"text": text, "segments": segments}


def lookup(exact: dict[str, list[str]], code: str) -> dict:
    if code in exact:
        return {"status": "ok", "code": code, "candidates": exact[code]}
    suggest = sorted([c for c in exact if c.startswith(code)])[:20]
    if suggest:
        return {"status": "partial", "code": code, "suggest_codes": suggest}
    return {"status": "not_found", "code": code}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["health", "lookup", "decode"])
    parser.add_argument("--code")
    parser.add_argument("--line")
    parser.add_argument("--table")
    args = parser.parse_args()

    exact = load_table(args.table)
    if args.mode == "health":
        print(json.dumps({"status": "ok", "codes": len(exact)}, ensure_ascii=False))
        return 0
    if args.mode == "lookup":
        if not args.code:
            raise SystemExit("--code is required in lookup mode")
        print(json.dumps(lookup(exact, args.code), ensure_ascii=False))
        return 0
    if not args.line:
        raise SystemExit("--line is required in decode mode")
    print(json.dumps(decode(exact, args.line), ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
