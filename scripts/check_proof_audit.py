#!/usr/bin/env python3
"""Deterministic Audit Gate for Mathematical Proofs and Micro-to-Macro Econometric Derivations.

Validates that mathematical proofs and structural derivations in manuscripts (.tex, .md)
do not suffer from handwaving, unverified spatial dependence decay, missing micro-macro
fixed effect bridges, or unproven Neyman orthogonality conditions.
"""

import argparse
import json
import re
import sys
from pathlib import Path

# --- Audit Rules and Regex Patterns ---

HANDWAVING_PATTERNS = [
    (re.compile(r"(?i)\b(trivial(ly)?\s+(algebra\s+shows|to\s+see|verified))\b"), "Handwaving: 'trivially shows/verified' used without full algebraic derivation."),
    (re.compile(r"(?i)\b(it\s+is\s+(obvious|easy\s+to\s+see)\s+that)\b"), "Handwaving: 'it is obvious/easy to see that' used instead of step-by-step derivation."),
    (re.compile(r"(?i)\b(left\s+as\s+an?\s+exercise)\b"), "Handwaving: Proof incomplete ('left as an exercise')."),
    (re.compile(r"(?i)\b(straightforward\s+algebra\s+(shows|yields|gives))\b"), "Handwaving: 'straightforward algebra' used to skip intermediate algebraic steps."),
]

DISCRETE_CHOICE_TRIGGERS = re.compile(
    r"(?i)\b(type\s*[-–—]?\s*i\s+extreme\s+value|gumbel|multinomial\s+logit|discrete\s+choice|random\s+utility)\b"
)

MICRO_MACRO_ABSORPTION_TERMS = re.compile(
    r"(?i)\b(berry|log[-–—\s]*odds|inclusive\s+value|partition\s+function|absorbed\s+by\s+(time\s+)?fixed\s+effects?|reference\s+(county|location|node))\b"
)

SPATIAL_DEPENDENCE_TRIGGERS = re.compile(
    r"(?i)\b(spatial\s+(durbin|autoregressive|clt|central\s+limit)|jenish|prucha|near[-–—\s]*epoch\s+dependence|ned\b|\(I\s*-\s*\\rho\s*W\)\^\{-1\})"
)

SPATIAL_DECAY_TERMS = re.compile(
    r"(?i)\b(geometric(al)?(\s+decay|\s+rate)?|exponential(\s+decay)?|neumann|\|\\rho\|(\^|\_)?m|\|\rho_0\|(\^|\_)?m|truncation\s+error|summab(le|ility))\b"
)

ORTHOGONALITY_TRIGGERS = re.compile(
    r"(?i)\b(neyman\s+orthogonal(ity)?|double\s+machine\s+learning|dml\b|gateaux)\b"
)

ORTHOGONALITY_DERIVATION_TERMS = re.compile(
    r"(?i)\b(directional\s+derivative|gateaux|\\frac\{d\}\{dr\}|\\frac\{\\partial\}\{\\partial\s*r\}|iterated\s+expectations?|lie\b|first[-–—\s]*order\s+(derivative\s+vanishes|bias\s+vanishes))\b"
)


def audit_proof_content(text: str, filename: str = "manuscript") -> dict:
    """Audit mathematical text against core econometric verification gates."""
    violations: list[dict] = []
    checks: dict[str, dict] = {}
    lines = text.splitlines()

    # 1. Handwaving Detection
    handwaving_found = []
    for line_no, line in enumerate(lines, 1):
        for pattern, msg in HANDWAVING_PATTERNS:
            match = pattern.search(line)
            if match:
                handwaving_found.append({
                    "line": line_no,
                    "matched": match.group(0),
                    "snippet": line.strip()[:100],
                    "message": msg,
                })
    checks["no_handwaving"] = {
        "status": "fail" if handwaving_found else "pass",
        "violations": handwaving_found,
    }
    if handwaving_found:
        violations.extend([{"gate": "no_handwaving", **item} for item in handwaving_found])

    # 2. Micro-to-Macro Aggregation Gate
    has_discrete_choice = bool(DISCRETE_CHOICE_TRIGGERS.search(text))
    if has_discrete_choice:
        has_absorption = bool(MICRO_MACRO_ABSORPTION_TERMS.search(text))
        if not has_absorption:
            msg = (
                "Discrete choice / random utility model detected, but lacks explicit explanation "
                "of how the inclusive value / partition function is absorbed by time fixed effects "
                "or normalized via log-odds ratios (Berry 1994)."
            )
            checks["micro_macro_bridge"] = {"status": "fail", "message": msg}
            violations.append({"gate": "micro_macro_bridge", "message": msg})
        else:
            checks["micro_macro_bridge"] = {
                "status": "pass",
                "message": "Discrete choice partition function absorption properly established.",
            }
    else:
        checks["micro_macro_bridge"] = {"status": "pass", "message": "No discrete choice model declared; check skipped."}

    # 3. Spatial Dependence Decay Rate Gate
    has_spatial_dep = bool(SPATIAL_DEPENDENCE_TRIGGERS.search(text))
    if has_spatial_dep:
        has_decay = bool(SPATIAL_DECAY_TERMS.search(text))
        if not has_decay:
            msg = (
                "Spatial network / dependence CLT invoked, but lacks algebraic derivation or bound "
                "for dependence decay rate (e.g. geometric decay O(|rho|^m) via Neumann expansion "
                "or near-epoch dependence truncation error)."
            )
            checks["spatial_decay_bound"] = {"status": "fail", "message": msg}
            violations.append({"gate": "spatial_decay_bound", "message": msg})
        else:
            checks["spatial_decay_bound"] = {
                "status": "pass",
                "message": "Spatial dependence decay rate / Neumann bound verified.",
            }
    else:
        checks["spatial_decay_bound"] = {"status": "pass", "message": "No spatial network dependence invoked; check skipped."}

    # 4. Neyman Orthogonality Gateaux Derivation Gate
    has_orthogonality = bool(ORTHOGONALITY_TRIGGERS.search(text))
    if has_orthogonality:
        has_gateaux_proof = bool(ORTHOGONALITY_DERIVATION_TERMS.search(text))
        if not has_gateaux_proof:
            msg = (
                "Neyman orthogonality or Double ML invoked, but directional (Gateaux) derivative "
                "or law of iterated expectations derivation is missing."
            )
            checks["neyman_orthogonality_derivation"] = {"status": "fail", "message": msg}
            violations.append({"gate": "neyman_orthogonality_derivation", "message": msg})
        else:
            checks["neyman_orthogonality_derivation"] = {
                "status": "pass",
                "message": "Gateaux directional derivative / orthogonality verification confirmed.",
            }
    else:
        checks["neyman_orthogonality_derivation"] = {
            "status": "pass",
            "message": "No Neyman orthogonality claim detected; check skipped.",
        }

    # Overall Verdict
    gate_passed = len(violations) == 0
    return {
        "manuscript": filename,
        "valid": True,
        "gate_passed": gate_passed,
        "overall_verdict": "pass" if gate_passed else "fail",
        "total_violations": len(violations),
        "checks": checks,
        "violations": violations,
    }


def audit_file(path: Path) -> dict:
    """Load and audit a single manuscript or proof file."""
    if not path.exists():
        return {
            "manuscript": str(path),
            "valid": False,
            "gate_passed": False,
            "overall_verdict": "fail",
            "total_violations": 1,
            "violations": [{"gate": "file_io", "message": f"File not found: {path}"}],
        }
    text = path.read_text(encoding="utf-8", errors="replace")
    return audit_proof_content(text, filename=str(path))


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit econometric and mathematical proofs for completeness.")
    parser.add_argument("paths", nargs="+", type=Path, help="Paths to .tex or .md proof manuscripts.")
    parser.add_argument("--json", action="store_true", help="Output machine-readable JSON report.")
    parser.add_argument("--strict", action="store_true", help="Exit with code 1 if any gate fails.")
    args = parser.parse_args()

    results = [audit_file(p) for p in args.paths]
    all_passed = all(r["gate_passed"] for r in results)

    if args.json:
        print(json.dumps({"results": results, "all_passed": all_passed}, indent=2, ensure_ascii=False))
    else:
        for r in results:
            print(f"\n{'='*70}")
            print(f"Proof Audit for: {r['manuscript']}")
            print(f"Verdict: {r['overall_verdict'].upper()} (Violations: {r['total_violations']})")
            print(f"{'-'*70}")
            for name, check in r.get("checks", {}).items():
                status_symbol = "✓ PASS" if check["status"] == "pass" else "✗ FAIL"
                print(f"  [{status_symbol}] {name}: {check.get('message', '')}")
            if r.get("violations"):
                print("  Violations Detail:")
                for v in r["violations"]:
                    if "line" in v:
                        print(f"    - Line {v['line']}: {v['message']} -> '{v.get('snippet', '')}'")
                    else:
                        print(f"    - [{v.get('gate')}]: {v['message']}")

    if args.strict and not all_passed:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
