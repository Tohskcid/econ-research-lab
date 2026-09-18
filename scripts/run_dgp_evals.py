#!/usr/bin/env python3
"""Generate public econometric DGP fixtures and grade standardized submissions."""

import argparse
import csv
import json
import random
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def rows(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def invalid_iv(case: dict) -> tuple[list[str], list[list[object]]]:
    rng = random.Random(case["seed"])
    data = []
    for index in range(case["rows"]):
        confounder = rng.gauss(0, 1)
        instrument = rng.randrange(2)
        treatment = 0.8 * instrument + 0.8 * confounder + rng.gauss(0, 1)
        outcome = 2 * treatment + 1.5 * instrument + confounder + rng.gauss(0, 1)
        data.append([index, instrument, treatment, outcome])
    return ["unit", "instrument", "treatment", "outcome"], data


def panel_pretrend(case: dict) -> tuple[list[str], list[list[object]]]:
    rng = random.Random(case["seed"])
    data = []
    periods = 8
    units = case["rows"] // periods
    for unit in range(units):
        treated = int(unit < units // 2)
        unit_effect = rng.gauss(0, 1)
        for period in range(periods):
            post = int(period >= 5)
            outcome = unit_effect + 0.2 * period + treated * 0.35 * period + rng.gauss(0, 0.35)
            data.append([unit, period, treated, post, treated * post, outcome])
    return ["unit", "time", "treated_group", "post", "treatment", "outcome"], data


def randomized(case: dict) -> tuple[list[str], list[list[object]]]:
    rng = random.Random(case["seed"])
    data = []
    for index in range(case["rows"]):
        treatment = rng.randrange(2)
        outcome = 1.5 * treatment + rng.gauss(0, 1)
        data.append([index, treatment, outcome])
    return ["unit", "treatment", "outcome"], data


def staggered_heterogeneous(case: dict) -> tuple[list[str], list[list[object]]]:
    rng = random.Random(case["seed"])
    periods = 9
    units = case["rows"] // periods
    data = []
    for unit in range(units):
        cohort = 3 if unit < units // 3 else 6 if unit < 2 * units // 3 else 0
        unit_effect = rng.gauss(0, 1)
        for period in range(periods):
            treated = int(cohort > 0 and period >= cohort)
            effect = (1.0 + 0.4 * (period - cohort)) if cohort == 3 and treated else 3.0 * treated
            outcome = unit_effect + 0.15 * period + effect + rng.gauss(0, 0.35)
            data.append([unit, period, cohort, treated, outcome])
    return ["unit", "time", "first_treat_time", "treatment", "outcome"], data


def weak_iv(case: dict) -> tuple[list[str], list[list[object]]]:
    rng = random.Random(case["seed"])
    data = []
    for index in range(case["rows"]):
        confounder = rng.gauss(0, 1)
        instrument = rng.randrange(2)
        treatment = 0.04 * instrument + confounder + rng.gauss(0, 1)
        outcome = 2 * treatment + confounder + rng.gauss(0, 1)
        data.append([index, instrument, treatment, outcome])
    return ["unit", "instrument", "treatment", "outcome"], data


def rdd_manipulation(case: dict) -> tuple[list[str], list[list[object]]]:
    rng = random.Random(case["seed"])
    data = []
    for index in range(case["rows"]):
        running = rng.uniform(-1, 1)
        if -0.12 < running < 0:
            running = abs(running)
        treatment = int(running >= 0)
        outcome = 0.5 * running + 2 * treatment + rng.gauss(0, 0.5)
        data.append([index, running, treatment, outcome])
    return ["unit", "running_variable", "treatment", "outcome"], data


GENERATORS = {
    "invalid_iv": invalid_iv,
    "panel_pretrend": panel_pretrend,
    "randomized": randomized,
    "staggered_heterogeneous": staggered_heterogeneous,
    "weak_iv": weak_iv,
    "rdd_manipulation": rdd_manipulation,
}


def generate(cases: list[dict], output_dir: Path) -> list[dict]:
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest = []
    for case in cases:
        header, data = GENERATORS[case["generator"]](case)
        target = output_dir / f"{case['id']}.csv"
        with target.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.writer(handle)
            writer.writerow(header)
            writer.writerows(data)
        manifest.append({"case_id": case["id"], "prompt": case["prompt"], "data": str(target)})
    return manifest


def grade(cases: list[dict], submissions: list[dict]) -> dict:
    by_id, duplicates = {}, set()
    for submission in submissions:
        case_id = submission.get("case_id")
        if case_id in by_id:
            duplicates.add(case_id)
        by_id[case_id] = submission
    details, passed = [], 0
    for case in cases:
        submission = by_id.get(case["id"])
        errors = []
        if not submission:
            errors.append("missing submission")
        else:
            findings = submission.get("findings", [])
            if not isinstance(findings, list) or not all(isinstance(item, str) for item in findings):
                findings = []
                errors.append("findings must be a list of strings")
            if case["id"] in duplicates:
                errors.append("duplicate submission")
            if submission.get("decision") != case["expected_decision"]:
                errors.append(f"expected decision: {case['expected_decision']}")
            errors.extend(f"missing finding: {item}" for item in case.get("required_findings", []) if item not in findings)
            errors.extend(f"forbidden finding: {item}" for item in case.get("forbidden_findings", []) if item in findings)
            if "expected_estimate" in case:
                estimate = submission.get("estimate")
                if isinstance(estimate, bool) or not isinstance(estimate, (int, float)):
                    errors.append("estimate must be numeric")
                elif abs(estimate - case["expected_estimate"]) > case["tolerance"]:
                    errors.append("estimate outside tolerance")
        ok = not errors
        passed += int(ok)
        details.append({"case_id": case["id"], "passed": ok, "errors": errors})
    return {"passed": passed, "total": len(cases), "all_passed": passed == len(cases), "cases": details}


def run_adapter(cases: list[dict], output_dir: Path, adapter: Path, timeout: int) -> dict:
    manifest = generate(cases, output_dir)
    submissions, failures = [], []
    for item in manifest:
        request = {**item, "submission_schema": {"case_id": "string", "decision": "string", "findings": ["string"], "estimate": "optional number"}}
        try:
            completed = subprocess.run(
                [str(adapter)], input=json.dumps(request), capture_output=True, text=True, timeout=timeout, check=False
            )
            if completed.returncode:
                raise ValueError(f"adapter exit {completed.returncode}: {completed.stderr.strip()}")
            submission = json.loads(completed.stdout)
            if not isinstance(submission, dict) or submission.get("case_id") != item["case_id"]:
                raise ValueError("adapter returned the wrong case_id")
            submissions.append(submission)
        except (OSError, subprocess.TimeoutExpired, json.JSONDecodeError, ValueError) as exc:
            failures.append({"case_id": item["case_id"], "error": str(exc)})
    submission_path = output_dir / "submissions.jsonl"
    submission_path.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in submissions), encoding="utf-8")
    return {"adapter_failures": failures, "submissions": str(submission_path), "grade": grade(cases, submissions)}


def write_json(value, output: Path | None) -> None:
    rendered = json.dumps(value, ensure_ascii=False, indent=2) + "\n"
    if output:
        output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cases", type=Path, default=ROOT / "evals/dgp_cases.jsonl")
    subparsers = parser.add_subparsers(dest="command", required=True)
    generate_parser = subparsers.add_parser("generate")
    generate_parser.add_argument("--out-dir", type=Path, required=True)
    grade_parser = subparsers.add_parser("grade")
    grade_parser.add_argument("--results", type=Path, required=True)
    grade_parser.add_argument("--output", type=Path)
    run_parser = subparsers.add_parser("run")
    run_parser.add_argument("--adapter", type=Path, required=True, help="executable that reads one JSON request from stdin")
    run_parser.add_argument("--work-dir", type=Path, required=True)
    run_parser.add_argument("--timeout", type=int, default=300)
    run_parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        cases = rows(args.cases)
        if args.command == "generate":
            write_json(generate(cases, args.out_dir), None)
            return 0
        if args.command == "run":
            report = run_adapter(cases, args.work_dir, args.adapter, args.timeout)
            write_json(report, args.output)
            return 0 if not report["adapter_failures"] and report["grade"]["all_passed"] else 1
        report = grade(cases, rows(args.results))
        write_json(report, args.output)
        return 0 if report["all_passed"] else 1
    except (OSError, KeyError, ValueError, json.JSONDecodeError) as exc:
        print(f"[Error] Invalid DGP evaluation input: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
