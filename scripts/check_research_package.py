#!/usr/bin/env python3
"""Run applicable deterministic gates declared by a research package config."""

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path, PurePosixPath


ALLOWED = {"manifest", "manuscript", "results", "design_audit", "latex_main"}


def resolve(root: Path, value: object, field: str) -> Path:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{field} must be a non-empty relative path")
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts:
        raise ValueError(f"{field} must stay below the package root")
    target = root.joinpath(*path.parts)
    if not target.is_file():
        raise ValueError(f"{field} file does not exist: {value}")
    return target


def run(command: list[str]) -> dict:
    completed = subprocess.run(command, capture_output=True, text=True, check=False)
    return {
        "command": command,
        "passed": completed.returncode == 0,
        "exit_code": completed.returncode,
        "stdout": completed.stdout[-4000:],
        "stderr": completed.stderr[-4000:],
    }


def check(root: Path, config_path: Path, scripts: Path) -> dict:
    config = json.loads(config_path.read_text(encoding="utf-8"))
    if not isinstance(config, dict):
        raise ValueError("package config must be a JSON object")
    unknown = sorted(set(config) - ALLOWED)
    if unknown:
        raise ValueError(f"unknown package fields: {unknown}")
    paths = {field: resolve(root, value, field) for field, value in config.items()}
    checks: list[dict] = []
    python = sys.executable

    if "manifest" in paths:
        checks.append(run([python, str(scripts / "validate_research_manifest.py"), str(paths["manifest"]), "--require-argument-graph", "--json"]))
    if "manuscript" in paths and "manifest" in paths:
        checks.append(run([
            python, str(scripts / "audit_claims.py"), str(paths["manuscript"]), str(paths["manifest"]),
            "--strict-numbers", "--require-central-claims", "--json",
        ]))
    if ("results" in paths) != ("manuscript" in paths):
        raise ValueError("results and manuscript must be declared together")
    if "results" in paths:
        checks.append(run([
            python, str(scripts / "check_result_bindings.py"), "--results", str(paths["results"]),
            "--manuscript", str(paths["manuscript"]), "--root", str(root), "--json",
        ]))
    if "design_audit" in paths:
        checks.append(run([
            python, str(scripts / "check_design_audit.py"), str(paths["design_audit"]),
            "--root", str(root), "--require-pass", "--json",
        ]))
    if "latex_main" in paths:
        with tempfile.TemporaryDirectory(prefix="research-latex-") as directory:
            build = Path(directory) / "build"
            checks.append(run([
                python, str(scripts / "check_latex.py"), "check", "--main", str(paths["latex_main"]),
                "--build-dir", str(build), "--report", str(build / "report.json"),
            ]))
    if not checks:
        raise ValueError("package config selects no checks")
    return {"valid": all(item["passed"] for item in checks), "checks": checks}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--config", type=Path, default=Path("research/package.json"))
    parser.add_argument("--allow-missing", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    config = args.config if args.config.is_absolute() else root / args.config
    if not config.is_file():
        if args.allow_missing:
            print(json.dumps({"valid": True, "skipped": True, "reason": f"{config} not found"}, indent=2))
            return 0
        print(f"[Error] File not found: {config}", file=sys.stderr)
        return 2
    try:
        report = check(root, config, Path(__file__).resolve().parent)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"[Error] Cannot check research package: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
