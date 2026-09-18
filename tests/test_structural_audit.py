import importlib.util
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("check_structural_audit", ROOT / "scripts/check_structural_audit.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class StructuralAuditTests(unittest.TestCase):
    def document(self, status="pass", counterfactual=False):
        required = set(MODULE.CORE)
        if counterfactual:
            required.add("counterfactual-invariance")
        return {
            "schema_version": "1",
            "model": "Dynamic discrete choice",
            "target": "Policy counterfactual",
            "estimator_or_solver": "Nested fixed point",
            "counterfactual_required": counterfactual,
            "diagnostics": [
                {"id": name, "status": status, "finding": "checked", "artifact": "research/check.json"}
                for name in sorted(required)
            ],
        }

    def test_complete_audit_passes(self):
        report = MODULE.validate(self.document())
        self.assertTrue(report["gate_passed"], report["errors"])

    def test_nonpassing_diagnostic_blocks_gate(self):
        document = self.document()
        document["diagnostics"][0]["status"] = "inconclusive"
        report = MODULE.validate(document)
        self.assertTrue(report["valid"], report["errors"])
        self.assertFalse(report["gate_passed"])

    def test_counterfactual_requires_invariance_check(self):
        document = self.document(counterfactual=True)
        document["diagnostics"] = [
            item for item in document["diagnostics"] if item["id"] != "counterfactual-invariance"
        ]
        report = MODULE.validate(document)
        self.assertTrue(any("counterfactual-invariance" in error for error in report["errors"]))

    def test_root_requires_real_artifacts(self):
        with tempfile.TemporaryDirectory() as directory:
            report = MODULE.validate(self.document(), Path(directory))
        self.assertTrue(any("artifact does not exist" in error for error in report["errors"]))


if __name__ == "__main__":
    unittest.main()
