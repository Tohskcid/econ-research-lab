import importlib.util
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("check_design_audit", ROOT / "scripts/check_design_audit.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class DesignAuditTests(unittest.TestCase):
    def report(self, design="iv", status="pass"):
        required = MODULE.COMMON | MODULE.REQUIRED[design]
        return {
            "design": design,
            "estimand": "Instrument-specific LATE",
            "assignment_narrative": "Eligibility changes treatment take-up",
            "interpretation_boundary": "Compliers at the eligibility margin",
            "diagnostics": [
                {"id": key, "status": status, "finding": "Audited", "artifact": f"research/{key}.json"}
                for key in required
            ],
        }

    def test_iv_uses_iv_specific_obligations(self):
        report = MODULE.validate(self.report())
        self.assertTrue(report["gate_passed"], report["errors"])
        self.assertIn("complier-scope", report["required"])
        self.assertNotIn("parallel-trends", report["required"])

    def test_nonpassing_diagnostic_blocks_gate_without_invalidating_schema(self):
        document = self.report()
        document["diagnostics"][0]["status"] = "inconclusive"
        report = MODULE.validate(document)
        self.assertTrue(report["valid"])
        self.assertFalse(report["gate_passed"])

    def test_missing_design_specific_diagnostic_is_invalid(self):
        document = self.report("did")
        document["diagnostics"] = [item for item in document["diagnostics"] if item["id"] != "parallel-trends"]
        report = MODULE.validate(document)
        self.assertFalse(report["valid"])
        self.assertTrue(any("parallel-trends" in error for error in report["errors"]))

    def test_fuzzy_rdd_adds_local_iv_obligations(self):
        required = MODULE.COMMON | MODULE.REQUIRED["fuzzy-rdd"]
        self.assertTrue({"first-stage", "monotonicity", "complier-scope"}.issubset(required))

    def test_optional_root_requires_real_artifacts(self):
        with tempfile.TemporaryDirectory() as directory:
            report = MODULE.validate(self.report(), Path(directory))
        self.assertFalse(report["valid"])
        self.assertTrue(any("does not exist" in error for error in report["errors"]))


if __name__ == "__main__":
    unittest.main()
