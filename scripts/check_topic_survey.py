#!/usr/bin/env python3
"""Validate the pre-design survey and bounded contribution decision for a new question."""

import argparse
import json
import re
import sys
from pathlib import Path


AXES = {"question", "mechanism", "method", "setting"}
RELATIONS = {"duplicate", "replication", "extension", "external-validity", "adjacent", "contradiction"}
DECISIONS = {"proceed", "reframe", "replicate", "stop", "blocked"}
CONTRIBUTIONS = {"distinct-under-search", "extension", "external-validity", "replication", "synthesis", "duplicate", "unresolved"}
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def nonempty(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate(document: object) -> dict:
    errors: list[str] = []
    if not isinstance(document, dict):
        return {"valid": False, "errors": ["survey must be a JSON object"]}
    if document.get("schema_version") != "1":
        errors.append("schema_version must be '1'")
    for field in ("question", "scope", "contribution_statement"):
        if not nonempty(document.get(field)):
            errors.append(f"{field} must be a non-empty string")
    cutoff = document.get("cutoff")
    if not isinstance(cutoff, str) or not DATE.fullmatch(cutoff):
        errors.append("cutoff must use YYYY-MM-DD")

    searches = document.get("searches")
    observed_axes: set[str] = set()
    if not isinstance(searches, list) or not searches:
        errors.append("searches must be a non-empty list")
        searches = []
    for index, search in enumerate(searches, 1):
        if not isinstance(search, dict):
            errors.append(f"search {index} must be an object")
            continue
        axis = search.get("axis")
        if axis not in AXES:
            errors.append(f"search {index} axis must be one of {sorted(AXES)}")
        else:
            observed_axes.add(axis)
        for field in ("source", "query", "searched_at"):
            if not nonempty(search.get(field)):
                errors.append(f"search {index} requires {field}")
        if nonempty(search.get("searched_at")) and not DATE.fullmatch(search["searched_at"]):
            errors.append(f"search {index} searched_at must use YYYY-MM-DD")
    if "question" not in observed_axes:
        errors.append("survey requires a question-axis search")
    if not observed_axes.intersection({"mechanism", "method", "setting"}):
        errors.append("survey requires at least one mechanism, method, or setting search")

    works = document.get("nearest_works")
    if not isinstance(works, list):
        errors.append("nearest_works must be a list")
        works = []
    nearest_count = 0
    relations: set[str] = set()
    for index, work in enumerate(works, 1):
        if not isinstance(work, dict):
            errors.append(f"nearest work {index} must be an object")
            continue
        if work.get("nearest") is True:
            nearest_count += 1
        relation = work.get("relation")
        if relation not in RELATIONS:
            errors.append(f"nearest work {index} relation must be one of {sorted(RELATIONS)}")
        else:
            relations.add(relation)
        for field in ("title", "locator", "verified_at", "question", "estimand_or_theorem", "method_or_proof", "difference"):
            if not nonempty(work.get(field)):
                errors.append(f"nearest work {index} requires {field}")
        if nonempty(work.get("verified_at")) and not DATE.fullmatch(work["verified_at"]):
            errors.append(f"nearest work {index} verified_at must use YYYY-MM-DD")
        if work.get("full_text_status") not in {"checked", "abstract-only", "inaccessible"}:
            errors.append(f"nearest work {index} requires valid full_text_status")
        for field in ("backward_checked", "forward_checked"):
            if not isinstance(work.get(field), bool):
                errors.append(f"nearest work {index} requires boolean {field}")

    decision = document.get("decision")
    contribution = document.get("contribution_class")
    if decision not in DECISIONS:
        errors.append(f"decision must be one of {sorted(DECISIONS)}")
    if contribution not in CONTRIBUTIONS:
        errors.append(f"contribution_class must be one of {sorted(CONTRIBUTIONS)}")
    limitations = document.get("limitations")
    if not isinstance(limitations, list) or not limitations or not all(nonempty(item) for item in limitations):
        errors.append("limitations must be a non-empty list of strings")

    if works and nearest_count == 0:
        errors.append("at least one work must be marked nearest")
    if not works and (decision != "blocked" or contribution != "unresolved"):
        errors.append("no verified nearest work requires blocked/unresolved rather than a novelty claim")
    if "duplicate" in relations and decision == "proceed":
        errors.append("a duplicate nearest work forbids proceeding without reframe, replication, or stop")
    if contribution == "duplicate" and decision not in {"reframe", "replicate", "stop"}:
        errors.append("duplicate contribution requires reframe, replicate, or stop")
    return {"valid": not errors, "decision": decision, "contribution_class": contribution, "errors": errors}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("survey", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    if not args.survey.is_file():
        print(f"[Error] File not found: {args.survey}", file=sys.stderr)
        return 2
    try:
        report = validate(json.loads(args.survey.read_text(encoding="utf-8")))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"[Error] Cannot read topic survey: {exc}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print("valid" if report["valid"] else "invalid")
        for error in report["errors"]:
            print(f"- {error}")
    return 0 if report["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
