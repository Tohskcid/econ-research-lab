import importlib.util
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("check_text_audit", ROOT / "scripts/check_text_audit.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class TextAuditTests(unittest.TestCase):
    def document(self, score=0.85, status="pass", temp=0.0, model="gpt-4o-2024-08-06"):
        return {
            "schema_version": "1",
            "task_description": "Classifying corporate climate risk transition commitments",
            "model_version": model,
            "temperature": temp,
            "prompt_template": "prompts/test_prompt.txt",
            "prompt_sha256": "a" * 64,
            "human_audit": {
                "sample_size": 150,
                "coder_count": 2,
                "metric": "cohen_kappa",
                "score": score,
                "artifact": "research/gold.json",
                "artifact_sha256": "b" * 64,
            },
            "diagnostics": [
                {
                    "id": name,
                    "status": status,
                    "finding": "checked",
                    "artifact": "research/check.json",
                    "artifact_sha256": "c" * 64,
                }
                for name in sorted(MODULE.REQUIRED_DIAGNOSTICS)
            ],
        }

    def test_valid_audit_passes(self):
        report = MODULE.validate(self.document())
        self.assertTrue(report["gate_passed"], report["errors"])

    def test_nonzero_temperature_fails(self):
        doc = self.document(temp=0.7)
        report = MODULE.validate(doc)
        self.assertFalse(report["gate_passed"])
        self.assertTrue(any("temperature" in error for error in report["errors"]))

    def test_unpinned_model_fails(self):
        doc = self.document(model="gpt-4")
        report = MODULE.validate(doc)
        self.assertFalse(report["gate_passed"])
        self.assertTrue(any("unpinned" in error for error in report["errors"]))

    def test_low_reliability_score_fails(self):
        doc = self.document(score=0.55)
        report = MODULE.validate(doc)
        self.assertFalse(report["gate_passed"])
        self.assertTrue(any("threshold" in error for error in report["errors"]))

    def test_small_sample_size_fails(self):
        doc = self.document()
        doc["human_audit"]["sample_size"] = 50
        report = MODULE.validate(doc)
        self.assertFalse(report["gate_passed"])
        self.assertTrue(any("sample_size" in error for error in report["errors"]))

    def test_nonpassing_diagnostic_blocks_gate(self):
        doc = self.document()
        doc["diagnostics"][0]["status"] = "inconclusive"
        report = MODULE.validate(doc)
        self.assertTrue(report["valid"])
        self.assertFalse(report["gate_passed"])

    def test_missing_diagnostic_fails(self):
        doc = self.document()
        doc["diagnostics"] = [d for d in doc["diagnostics"] if d["id"] != "prompt-drift-invariance"]
        report = MODULE.validate(doc)
        self.assertFalse(report["valid"])
        self.assertTrue(any("prompt-drift-invariance" in error for error in report["errors"]))

    def test_root_requires_real_artifacts(self):
        with tempfile.TemporaryDirectory() as directory:
            report = MODULE.validate(self.document(), Path(directory))
        self.assertTrue(any("does not exist" in error for error in report["errors"]))


if __name__ == "__main__":
    unittest.main()
