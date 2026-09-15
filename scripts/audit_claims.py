#!/usr/bin/env python3
"""Check Markdown claim markers against a research manifest."""

import argparse
import json
import re
import sys
from pathlib import Path


MARKER = re.compile(r"\[claim:([A-Za-z0-9_.:-]+)\]")
NUMBER = re.compile(r"(?<![\w/])(?:[$€£¥]\s*)?\d+(?:[.,]\d+)*(?:\s*%)?")
LINK_TARGET = re.compile(r"\]\([^)]+\)")


def claim_ids(path: Path) -> set[str]:
    ids: set[str] = set()
    for raw in path.read_text(encoding="utf-8").splitlines():
        if not raw.strip():
            continue
        record = json.loads(raw)
        if record.get("type") == "claim" and isinstance(record.get("id"), str):
            ids.add(record["id"])
    return ids


def prose_paragraphs(text: str):
    in_code, buffer, start = False, [], 0
    for line_no, line in enumerate(text.splitlines() + [""], 1):
        if line.lstrip().startswith("```"):
            in_code = not in_code
            continue
        ignored = in_code or line.lstrip().startswith(("#", "|", ">"))
        if not line.strip() or ignored:
            if buffer:
                yield start, " ".join(buffer)
                buffer = []
            continue
        if not buffer:
            start = line_no
        buffer.append(line.strip())


def audit(markdown: str, known: set[str], strict_numbers: bool) -> list[str]:
    errors: list[str] = []
    used = set(MARKER.findall(markdown))
    for marker in sorted(used - known):
        errors.append(f"unknown claim marker {marker!r}")
    if strict_numbers:
        for line, paragraph in prose_paragraphs(markdown):
            searchable = LINK_TARGET.sub("]", paragraph)
            if NUMBER.search(searchable) and not MARKER.search(paragraph):
                errors.append(f"line {line}: quantitative paragraph lacks [claim:ID]")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("markdown", type=Path)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--strict-numbers", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    if not args.markdown.is_file() or not args.manifest.is_file():
        print("[Error] Markdown and manifest files must exist", file=sys.stderr)
        return 2
    try:
        known = claim_ids(args.manifest)
    except (json.JSONDecodeError, OSError) as exc:
        print(f"[Error] Cannot read manifest: {exc}", file=sys.stderr)
        return 2
    errors = audit(args.markdown.read_text(encoding="utf-8"), known, args.strict_numbers)
    report = {"valid": not errors, "errors": errors}
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print("valid" if not errors else "invalid")
        for error in errors:
            print(f"- {error}")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
