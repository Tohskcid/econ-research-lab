import csv
import importlib.util
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("dgp_eval", ROOT / "scripts/run_dgp_evals.py")
dgp_eval = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(dgp_eval)


class DgpEvalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases = dgp_eval.rows(ROOT / "evals/dgp_cases.jsonl")

    def test_generation_is_deterministic_and_has_expected_rows(self):
        with tempfile.TemporaryDirectory() as first, tempfile.TemporaryDirectory() as second:
            dgp_eval.generate(self.cases, Path(first))
            dgp_eval.generate(self.cases, Path(second))
            for case in self.cases:
                name = f"{case['id']}.csv"
                left, right = Path(first, name), Path(second, name)
                self.assertEqual(left.read_bytes(), right.read_bytes())
                with left.open(newline="", encoding="utf-8") as handle:
                    self.assertEqual(sum(1 for _ in csv.reader(handle)) - 1, case["rows"])

    def test_grader_checks_decisions_findings_and_estimate(self):
        submissions = [
            {"case_id": "invalid-iv-direct-channel", "decision": "reject_identification", "findings": ["exclusion-violation"]},
            {"case_id": "did-differential-pretrend", "decision": "reject_identification", "findings": ["differential-pretrend"]},
            {"case_id": "randomized-mean-effect", "decision": "estimate", "findings": ["random-assignment", "uncertainty-reported"], "estimate": 1.5},
            {"case_id": "staggered-did-heterogeneous-effects", "decision": "use_heterogeneity_robust_design", "findings": ["heterogeneous-treatment-effects", "twfe-risk"]},
            {"case_id": "weak-iv-first-stage", "decision": "reject_conventional_inference", "findings": ["weak-first-stage", "weak-iv-robust-inference"]},
            {"case_id": "rdd-sorting-at-cutoff", "decision": "reject_identification", "findings": ["sorting-at-cutoff", "continuity-not-credible"]},
        ]
        self.assertTrue(dgp_eval.grade(self.cases, submissions)["all_passed"])
        submissions[0]["decision"] = "estimate"
        self.assertFalse(dgp_eval.grade(self.cases, submissions)["all_passed"])

    @patch.object(dgp_eval.subprocess, "run")
    def test_external_adapter_runs_end_to_end(self, run):
        answers = {
            "invalid-iv-direct-channel": {"decision": "reject_identification", "findings": ["exclusion-violation"]},
            "did-differential-pretrend": {"decision": "reject_identification", "findings": ["differential-pretrend"]},
            "randomized-mean-effect": {"decision": "estimate", "findings": ["random-assignment", "uncertainty-reported"], "estimate": 1.5},
            "staggered-did-heterogeneous-effects": {"decision": "use_heterogeneity_robust_design", "findings": ["heterogeneous-treatment-effects", "twfe-risk"]},
            "weak-iv-first-stage": {"decision": "reject_conventional_inference", "findings": ["weak-first-stage", "weak-iv-robust-inference"]},
            "rdd-sorting-at-cutoff": {"decision": "reject_identification", "findings": ["sorting-at-cutoff", "continuity-not-credible"]},
        }
        def response(*_args, **kwargs):
            request = __import__("json").loads(kwargs["input"])
            answer = {"case_id": request["case_id"], **answers[request["case_id"]]}
            return dgp_eval.subprocess.CompletedProcess(["adapter"], 0, __import__("json").dumps(answer), "")
        run.side_effect = response
        with tempfile.TemporaryDirectory() as directory:
            report = dgp_eval.run_adapter(self.cases, Path(directory), Path("adapter"), 30)
        self.assertEqual(report["adapter_failures"], [])
        self.assertTrue(report["grade"]["all_passed"])


if __name__ == "__main__":
    unittest.main()
