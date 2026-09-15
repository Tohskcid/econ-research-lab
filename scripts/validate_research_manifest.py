#!/usr/bin/env python3
"""Validate a JSONL research provenance graph."""

import argparse
import json
import sys
from pathlib import Path


LINKS = {
    "experiment": ("hypothesis_id", "hypothesis"),
    "run": ("experiment_id", "experiment"),
}
LIST_LINKS = {
    "finding": ("run_ids", "run"),
    "claim": ("evidence_ids", "evidence"),
}
REQUIRED = {
    "hypothesis": ("statement", "falsifier"),
    "experiment": ("hypothesis_id", "validation"),
    "run": ("experiment_id", "harness_version", "status", "artifact"),
    "evidence": ("source", "locator", "verified_at"),
    "finding": ("statement", "run_ids", "status"),
    "claim": ("statement",),
}


def load_jsonl(path: Path) -> tuple[list[dict], list[str]]:
    records, errors = [], []
    for line_no, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        try:
            value = json.loads(raw)
        except json.JSONDecodeError as exc:
            errors.append(f"line {line_no}: invalid JSON ({exc.msg})")
            continue
        if not isinstance(value, dict):
            errors.append(f"line {line_no}: record must be an object")
            continue
        value["_line"] = line_no
        records.append(value)
    return records, errors


def validate(records: list[dict]) -> list[str]:
    errors: list[str] = []
    by_id: dict[str, dict] = {}
    for record in records:
        line = record["_line"]
        record_id = record.get("id")
        kind = record.get("type")
        if not isinstance(record_id, str) or not record_id.strip():
            errors.append(f"line {line}: missing non-empty id")
        elif record_id in by_id:
            errors.append(f"line {line}: duplicate id {record_id!r}")
        else:
            by_id[record_id] = record
        if kind not in REQUIRED:
            errors.append(f"line {line}: unknown type {kind!r}")
            continue
        for field in REQUIRED[kind]:
            if record.get(field) in (None, "", []):
                errors.append(f"line {line}: {kind} requires {field}")

    for record in records:
        kind, line = record.get("type"), record["_line"]
        if kind in LINKS:
            field, target_type = LINKS[kind]
            target = by_id.get(record.get(field))
            if target is None or target.get("type") != target_type:
                errors.append(f"line {line}: {field} must reference a {target_type}")
        if kind in LIST_LINKS:
            field, target_type = LIST_LINKS[kind]
            values = record.get(field, [])
            if isinstance(values, list):
                for value in values:
                    target = by_id.get(value)
                    if target is None or target.get("type") != target_type:
                        errors.append(f"line {line}: {field} entry {value!r} must reference a {target_type}")
            elif values not in (None, ""):
                errors.append(f"line {line}: {field} must be a list")
        if kind == "claim":
            finding_ids = record.get("finding_ids", [])
            evidence_ids = record.get("evidence_ids", [])
            if not isinstance(finding_ids, list):
                errors.append(f"line {line}: finding_ids must be a list")
            if not isinstance(evidence_ids, list):
                errors.append(f"line {line}: evidence_ids must be a list")
            if not evidence_ids and not finding_ids:
                errors.append(f"line {line}: claim requires evidence_ids or finding_ids")
            for value in finding_ids if isinstance(finding_ids, list) else []:
                target = by_id.get(value)
                if target is None or target.get("type") != "finding":
                    errors.append(f"line {line}: finding_ids entry {value!r} must reference a finding")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--json", action="store_true", help="emit a machine-readable report")
    args = parser.parse_args()
    if not args.manifest.is_file():
        print(f"[Error] File not found: {args.manifest}", file=sys.stderr)
        return 2
    records, errors = load_jsonl(args.manifest)
    errors.extend(validate(records))
    report = {"valid": not errors, "records": len(records), "errors": errors}
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print("valid" if not errors else "invalid")
        for error in errors:
            print(f"- {error}")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
