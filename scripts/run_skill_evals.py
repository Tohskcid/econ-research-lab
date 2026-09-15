#!/usr/bin/env python3
"""Aggregate independently observed gates for versioned skill eval cases."""

import argparse
import json
import sys
from pathlib import Path


def rows(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def evaluate(cases: list[dict], results: list[dict]) -> dict:
    by_case: dict[str, dict] = {}
    duplicates: set[str] = set()
    for result in results:
        case_id = result.get("case_id")
        if case_id in by_case:
            duplicates.add(case_id)
        by_case[case_id] = result
    details, passed = [], 0
    for case in cases:
        case_id = case["id"]
        result = by_case.get(case_id)
        errors: list[str] = []
        if result is None:
            errors.append("missing result")
            observed: set[str] = set()
        else:
            gates = result.get("gates", [])
            if not isinstance(gates, list) or not all(isinstance(gate, str) for gate in gates):
                errors.append("gates must be a list of strings")
                gates = []
            if case_id in duplicates:
                errors.append("duplicate result")
            observed = set(gates)
            errors.extend(f"missing gate: {gate}" for gate in case.get("required_gates", []) if gate not in observed)
            errors.extend(f"forbidden gate: {gate}" for gate in case.get("forbidden_gates", []) if gate in observed)
        ok = not errors
        passed += int(ok)
        details.append({"case_id": case_id, "passed": ok, "errors": errors})
    tokens = sum(result.get("token_count", 0) for result in results if isinstance(result.get("token_count", 0), int))
    return {"passed": passed, "total": len(cases), "all_passed": passed == len(cases), "token_count": tokens, "cases": details}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cases", type=Path, default=Path("evals/cases.jsonl"))
    parser.add_argument("--results", type=Path, required=True, help="JSONL produced by an independent evaluator")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        report = evaluate(rows(args.cases), rows(args.results))
    except (OSError, json.JSONDecodeError, KeyError) as exc:
        print(f"[Error] Invalid eval input: {exc}", file=sys.stderr)
        return 2
    rendered = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0 if report["all_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
