#!/usr/bin/env python3
"""Compile one Lean file and reject local proof escapes."""

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path


ESCAPE_PATTERN = re.compile(r"\b(sorry|admit|sorryAx|axiom)\b")


def proof_escapes(source: str) -> list[str]:
    """Find proof escapes after removing ordinary comments and strings."""
    stripped = re.sub(r'"(?:\\.|[^"\\])*"|--.*?$|/-.*?-/', "", source, flags=re.MULTILINE | re.DOTALL)
    return sorted(set(ESCAPE_PATTERN.findall(stripped)))


def compiler_command(path: Path) -> list[str]:
    if shutil.which("lake"):
        return ["lake", "env", "lean", str(path)]
    if shutil.which("lean"):
        return ["lean", str(path)]
    raise FileNotFoundError("Lean 4 is unavailable; install Lean 4 + Mathlib before claiming a formal proof")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=Path, help="Lean source file to verify")
    args = parser.parse_args()

    if not args.file.is_file():
        print(f"[Error] File not found: {args.file}", file=sys.stderr)
        return 2
    escapes = proof_escapes(args.file.read_text(encoding="utf-8"))
    if escapes:
        print(f"[Error] Proof escape(s) found: {', '.join(escapes)}", file=sys.stderr)
        return 2
    try:
        command = compiler_command(args.file)
    except FileNotFoundError as exc:
        print(f"[Blocked] {exc}", file=sys.stderr)
        return 3
    return subprocess.run(command, check=False).returncode


if __name__ == "__main__":
    raise SystemExit(main())
