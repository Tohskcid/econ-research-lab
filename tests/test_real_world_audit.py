import importlib.util
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("check_real_world_audit", ROOT / "scripts/check_real_world_audit.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class RealWorldAuditTests(unittest.TestCase):
    def document(self, conclusion="applicable", status="pass"):
        return {
            "schema_version": "1",
            "decision_maker": "Municipal labor agency",
            "target_decision": "Whether to pilot the program",
            "deployment_context": "Urban offices in 2027",
            "target_population": "Eligible unemployed adults",
            "time_horizon": "Twelve months",
            "acceptable_failure": "No material employment gain in the pilot",
            "conclusion": conclusion,
            "diagnostics": [
                {
                    "id": name,
                    "status": status,
                    "finding": "checked",
                    "artifact": "research/check.json",
                    "artifact_sha256": "a" * 64,
                }
                for name in sorted(MODULE.REQUIRED)
            ],
        }

    def test_applicable_audit_passes(self):
        report = MODULE.validate(self.document())
        self.assertTrue(report["gate_passed"], report["errors"])

    def test_provisional_audit_is_valid_but_not_delivery_ready(self):
        report = MODULE.validate(self.document(conclusion="provisional"))
        self.assertTrue(report["valid"], report["errors"])
        self.assertFalse(report["gate_passed"])

    def test_nonpassing_diagnostic_blocks_applicability(self):
        document = self.document()
        document["diagnostics"][0]["status"] = "inconclusive"
        report = MODULE.validate(document)
        self.assertTrue(report["valid"], report["errors"])
        self.assertFalse(report["gate_passed"])

    def test_root_requires_real_artifacts(self):
        with tempfile.TemporaryDirectory() as directory:
            report = MODULE.validate(self.document(), Path(directory))
        self.assertTrue(any("artifact does not exist" in error for error in report["errors"]))

    def test_artifact_requires_sha256(self):
        document = self.document()
        document["diagnostics"][0]["artifact_sha256"] = "not-a-hash"
        report = MODULE.validate(document)
        self.assertTrue(any("artifact_sha256" in error for error in report["errors"]))


if __name__ == "__main__":
    unittest.main()
