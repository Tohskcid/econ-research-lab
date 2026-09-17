import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("check_result_bindings", ROOT / "scripts/check_result_bindings.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class ResultBindingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.directory = Path(self.temp.name)
        self.results = self.directory / "results.json"
        self.results.write_text(json.dumps({
            "schema_version": "1",
            "run_id": "run-1",
            "source_sha256": {"analysis": "a" * 64, "data": "b" * 64},
            "required_bindings": ["main.estimate", "main.n"],
            "results": {"main": {"estimate": 5.4764, "std_error": 1.2, "n": 321}},
        }, sort_keys=True), encoding="utf-8")

    def tearDown(self):
        self.temp.cleanup()

    def test_accepts_rounded_markdown_and_latex_bindings(self):
        digest = hashlib.sha256(self.results.read_bytes()).hexdigest()
        manuscript = self.directory / "paper.tex"
        manuscript.write_text(
            f"Effect: \\result{{main.estimate}}{{5.48}} and N=321 [result:main.n].\n[results-sha256:{digest}]\n",
            encoding="utf-8",
        )
        report = MODULE.audit(self.results, manuscript)
        self.assertTrue(report["valid"], report["errors"])

    def test_rejects_changed_number_and_stale_hash(self):
        manuscript = self.directory / "paper.md"
        manuscript.write_text(
            "Effect: 4.20 [result:main.estimate]; N=321 [result:main.n].\n"
            f"[results-sha256:{'c' * 64}]\n",
            encoding="utf-8",
        )
        report = MODULE.audit(self.results, manuscript)
        self.assertFalse(report["valid"])
        self.assertTrue(any("displays 4.20" in error for error in report["errors"]))
        self.assertTrue(any("stale results" in error for error in report["errors"]))

    def test_root_verifies_hashed_sources(self):
        source = self.directory / "analysis"
        source.write_text("version one", encoding="utf-8")
        document = json.loads(self.results.read_text(encoding="utf-8"))
        document["source_sha256"] = {"analysis": hashlib.sha256(source.read_bytes()).hexdigest()}
        self.results.write_text(json.dumps(document, sort_keys=True), encoding="utf-8")
        digest = hashlib.sha256(self.results.read_bytes()).hexdigest()
        manuscript = self.directory / "paper.md"
        manuscript.write_text(
            f"5.48 [result:main.estimate] 321 [result:main.n]\n[results-sha256:{digest}]\n",
            encoding="utf-8",
        )
        self.assertTrue(MODULE.audit(self.results, manuscript, root=self.directory)["valid"])
        source.write_text("changed", encoding="utf-8")
        report = MODULE.audit(self.results, manuscript, root=self.directory)
        self.assertTrue(any("hashed source changed" in error for error in report["errors"]))


if __name__ == "__main__":
    unittest.main()
