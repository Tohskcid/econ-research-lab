#!/usr/bin/env python3
"""Validate and run a small, provider-neutral research-team task graph."""

import argparse
import concurrent.futures
import json
import re
import subprocess
import sys
from pathlib import Path, PurePosixPath


TASK_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]*$")
HANDOFF_STATUSES = {"complete", "blocked", "failed"}


def load_plan(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("plan must be a JSON object")
    return value


def scope_path(value: object) -> PurePosixPath | None:
    if not isinstance(value, str):
        return None
    path = PurePosixPath(value)
    if not value or not path.parts or path.is_absolute() or ".." in path.parts:
        return None
    return path


def overlaps(left: str, right: str) -> bool:
    a, b = PurePosixPath(left).parts, PurePosixPath(right).parts
    return a[: len(b)] == b or b[: len(a)] == a


def inside_scope(path: str, scopes: list[str]) -> bool:
    target = scope_path(path)
    if target is None:
        return False
    parts = target.parts
    return any(parts[: len(PurePosixPath(scope).parts)] == PurePosixPath(scope).parts for scope in scopes)


def validate_plan(plan: dict) -> list[str]:
    errors: list[str] = []
    if not isinstance(plan.get("contract_id"), str) or not plan["contract_id"].strip():
        errors.append("contract_id must be a non-empty string")
    if not isinstance(plan.get("pi"), str) or not plan["pi"].strip():
        errors.append("pi must be a non-empty string")
    tasks = plan.get("tasks")
    if not isinstance(tasks, list) or not tasks:
        return errors + ["tasks must be a non-empty list"]

    by_id: dict[str, dict] = {}
    for index, task in enumerate(tasks):
        prefix = f"task {index + 1}"
        if not isinstance(task, dict):
            errors.append(f"{prefix} must be an object")
            continue
        task_id = task.get("id")
        if not isinstance(task_id, str) or not TASK_ID.fullmatch(task_id):
            errors.append(f"{prefix} id must match {TASK_ID.pattern}")
            continue
        if task_id in by_id:
            errors.append(f"duplicate task id {task_id!r}")
        else:
            by_id[task_id] = task
        for field in ("role", "objective"):
            if not isinstance(task.get(field), str) or not task[field].strip():
                errors.append(f"task {task_id!r} requires non-empty {field}")
        for field in ("depends_on", "inputs", "write_scope", "validation"):
            values = task.get(field)
            if not isinstance(values, list) or not all(isinstance(item, str) and item for item in values):
                errors.append(f"task {task_id!r} requires {field} as a list of non-empty strings")
        for value in task.get("write_scope", []) if isinstance(task.get("write_scope"), list) else []:
            if scope_path(value) is None:
                errors.append(f"task {task_id!r} has unsafe write_scope {value!r}")
        budget = task.get("budget")
        if not isinstance(budget, dict) or isinstance(budget.get("max_seconds"), bool) or not isinstance(budget.get("max_seconds"), int) or budget["max_seconds"] <= 0:
            errors.append(f"task {task_id!r} requires a positive integer budget.max_seconds")

    dependencies = {task_id: task.get("depends_on", []) for task_id, task in by_id.items()}
    for task_id, values in dependencies.items():
        if not isinstance(values, list):
            continue
        for value in values:
            if not isinstance(value, str):
                continue
            if value == task_id:
                errors.append(f"task {task_id!r} cannot depend on itself")
            elif value not in by_id:
                errors.append(f"task {task_id!r} has unknown dependency {value!r}")

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(task_id: str) -> None:
        if task_id in visiting:
            errors.append(f"dependency cycle reaches task {task_id!r}")
            return
        if task_id in visited:
            return
        visiting.add(task_id)
        for dependency in dependencies.get(task_id, []):
            if isinstance(dependency, str) and dependency in by_id:
                visit(dependency)
        visiting.remove(task_id)
        visited.add(task_id)

    for task_id in by_id:
        visit(task_id)

    def ancestors(task_id: str) -> set[str]:
        result: set[str] = set()
        stack = list(dependencies.get(task_id, []))
        while stack:
            current = stack.pop()
            if not isinstance(current, str) or current in result or current not in by_id:
                continue
            result.add(current)
            stack.extend(dependencies.get(current, []))
        return result

    task_ids = list(by_id)
    ancestry = {task_id: ancestors(task_id) for task_id in task_ids}
    for index, left_id in enumerate(task_ids):
        for right_id in task_ids[index + 1 :]:
            if left_id in ancestry[right_id] or right_id in ancestry[left_id]:
                continue
            left_scope = [value for value in by_id[left_id].get("write_scope", []) if isinstance(value, str)]
            right_scope = [value for value in by_id[right_id].get("write_scope", []) if isinstance(value, str)]
            if isinstance(left_scope, list) and isinstance(right_scope, list):
                conflict = next((a for a in left_scope for b in right_scope if overlaps(a, b)), None)
                if conflict:
                    errors.append(f"parallel tasks {left_id!r} and {right_id!r} have overlapping write_scope")
    return errors


def validate_handoff(value: object, task: dict) -> list[str]:
    if not isinstance(value, dict):
        return ["handoff must be a JSON object"]
    errors = []
    if value.get("task_id") != task["id"]:
        errors.append("handoff task_id does not match request")
    if value.get("status") not in HANDOFF_STATUSES:
        errors.append(f"status must be one of {sorted(HANDOFF_STATUSES)}")
    for field in ("summary", "uncertainty", "recommended_next"):
        if not isinstance(value.get(field), str):
            errors.append(f"{field} must be a string")
    for field in ("evidence_ids", "artifacts", "blockers"):
        values = value.get(field)
        if not isinstance(values, list) or not all(isinstance(item, str) for item in values):
            errors.append(f"{field} must be a list of strings")
    artifacts = value.get("artifacts", [])
    if isinstance(artifacts, list):
        for artifact in artifacts:
            if isinstance(artifact, str) and not inside_scope(artifact, task["write_scope"]):
                errors.append(f"artifact {artifact!r} is outside the task write_scope")
    return errors


def failed_handoff(task_id: str, status: str, message: str) -> dict:
    return {
        "task_id": task_id,
        "status": status,
        "summary": "",
        "evidence_ids": [],
        "artifacts": [],
        "uncertainty": "",
        "blockers": [message],
        "recommended_next": "PI review required",
    }


def call_adapter(adapter: Path, contract_id: str, task: dict, dependencies: list[dict]) -> dict:
    request = {
        "contract_id": contract_id,
        "task": task,
        "dependency_handoffs": dependencies,
        "handoff_schema": {
            "task_id": "string",
            "status": "complete|blocked|failed",
            "summary": "string",
            "evidence_ids": ["string"],
            "artifacts": ["string"],
            "uncertainty": "string",
            "blockers": ["string"],
            "recommended_next": "string",
        },
    }
    try:
        completed = subprocess.run(
            [str(adapter)],
            input=json.dumps(request),
            capture_output=True,
            text=True,
            timeout=task["budget"]["max_seconds"],
            check=False,
        )
        if completed.returncode:
            return failed_handoff(task["id"], "failed", f"adapter exit {completed.returncode}: {completed.stderr.strip()}")
        handoff = json.loads(completed.stdout)
        errors = validate_handoff(handoff, task)
        return failed_handoff(task["id"], "failed", "; ".join(errors)) if errors else handoff
    except subprocess.TimeoutExpired:
        return failed_handoff(task["id"], "failed", "task exceeded budget.max_seconds")
    except (OSError, json.JSONDecodeError) as exc:
        return failed_handoff(task["id"], "failed", str(exc))


def run_plan(plan: dict, adapter: Path, output_dir: Path, max_workers: int) -> dict:
    errors = validate_plan(plan)
    if max_workers <= 0:
        errors.append("max_workers must be positive")
    if errors:
        return {"valid": False, "errors": errors, "all_complete": False, "handoffs": []}
    output_dir.mkdir(parents=True, exist_ok=True)
    handoff_dir = output_dir / "handoffs"
    handoff_dir.mkdir(exist_ok=True)
    tasks = {task["id"]: task for task in plan["tasks"]}
    pending = set(tasks)
    handoffs: dict[str, dict] = {}
    events: list[dict] = []

    def save(task_id: str, handoff: dict) -> None:
        handoffs[task_id] = handoff
        events.append({"task_id": task_id, "status": handoff["status"]})
        (handoff_dir / f"{task_id}.json").write_text(json.dumps(handoff, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (output_dir / "events.jsonl").write_text("".join(json.dumps(event) + "\n" for event in events), encoding="utf-8")

    while pending:
        blocked = [
            task_id
            for task_id in pending
            if any(dependency in handoffs and handoffs[dependency]["status"] != "complete" for dependency in tasks[task_id]["depends_on"])
        ]
        for task_id in sorted(blocked):
            save(task_id, failed_handoff(task_id, "blocked", "a dependency did not complete"))
            pending.remove(task_id)
        ready = [
            task_id
            for task_id in pending
            if all(dependency in handoffs and handoffs[dependency]["status"] == "complete" for dependency in tasks[task_id]["depends_on"])
        ]
        if not ready:
            if pending:
                for task_id in sorted(pending):
                    save(task_id, failed_handoff(task_id, "blocked", "no runnable dependency path"))
                pending.clear()
            break
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as pool:
            futures = {
                pool.submit(
                    call_adapter,
                    adapter,
                    plan["contract_id"],
                    tasks[task_id],
                    [handoffs[dependency] for dependency in tasks[task_id]["depends_on"]],
                ): task_id
                for task_id in ready
            }
            for future in concurrent.futures.as_completed(futures):
                task_id = futures[future]
                save(task_id, future.result())
                pending.remove(task_id)

    ordered = [handoffs[task["id"]] for task in plan["tasks"]]
    report = {
        "valid": True,
        "contract_id": plan["contract_id"],
        "pi": plan["pi"],
        "all_complete": all(item["status"] == "complete" for item in ordered),
        "handoffs": ordered,
    }
    (output_dir / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    validate_parser = subparsers.add_parser("validate")
    validate_parser.add_argument("plan", type=Path)
    run_parser = subparsers.add_parser("run")
    run_parser.add_argument("plan", type=Path)
    run_parser.add_argument("--adapter", type=Path, required=True)
    run_parser.add_argument("--work-dir", type=Path, required=True)
    run_parser.add_argument("--max-workers", type=int, default=4)
    args = parser.parse_args()
    try:
        plan = load_plan(args.plan)
        if args.command == "validate":
            errors = validate_plan(plan)
            print(json.dumps({"valid": not errors, "errors": errors}, ensure_ascii=False, indent=2))
            return 0 if not errors else 1
        if args.max_workers <= 0:
            raise ValueError("max-workers must be positive")
        report = run_plan(plan, args.adapter, args.work_dir, args.max_workers)
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0 if report["all_complete"] else 1
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"[Error] Invalid research-team input: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
