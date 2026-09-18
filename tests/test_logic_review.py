import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("logic_review", ROOT / "scripts/check_logic_review.py")
logic_review = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(logic_review)


class LogicReviewTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.directory = Path(self.temp.name)
        self.manuscript = self.directory / "paper.md"
        self.manuscript.write_text("Result [claim:C1].\n", encoding="utf-8")
        self.manifest_path = self.directory / "manifest.jsonl"
        self.manifest = [{"id": "C1", "type": "claim", "central": True}]
        self.manifest_path.write_text(json.dumps(self.manifest[0]) + "\n", encoding="utf-8")

    def review(self):
        return {
            "reviewed_sha256": {
                "manuscript": hashlib.sha256(self.manuscript.read_bytes()).hexdigest(),
                "manifest": hashlib.sha256(self.manifest_path.read_bytes()).hexdigest(),
            },
            "overall_verdict": "pass",
            "global_gaps": [],
            "uncertainty": "No material gap found within the supplied artifacts.",
            "claim_reviews": [{
                "claim_id": "C1",
                "verdict": "coherent",
                "weakest_link": "External validity",
                "scope_or_number_mismatch": "",
                "competing_explanation": "",
                "required_revision": "",
            }],
        }

    def test_accepts_hash_bound_complete_review(self):
        self.assertEqual(
            logic_review.validate(self.review(), self.manuscript, self.manifest_path, self.manifest), []
        )

    def test_rejects_stale_hash(self):
        review = self.review()
        review["reviewed_sha256"]["manuscript"] = "stale"
        errors = logic_review.validate(review, self.manuscript, self.manifest_path, self.manifest)
        self.assertTrue(any("sha256" in error for error in errors))

    def test_delivery_requires_passing_verdict(self):
        review = self.review()
        review["overall_verdict"] = "revise"
        self.assertEqual(
            logic_review.validate(review, self.manuscript, self.manifest_path, self.manifest), []
        )
        errors = logic_review.validate(
            review, self.manuscript, self.manifest_path, self.manifest, require_pass=True
        )
        self.assertIn("overall_verdict must be pass for delivery", errors)

    def test_rejects_missing_central_claim(self):
        review = self.review()
        review["claim_reviews"] = []
        errors = logic_review.validate(review, self.manuscript, self.manifest_path, self.manifest)
        self.assertTrue(any("every central claim" in error for error in errors))

    def test_rejects_manifest_without_central_claims(self):
        self.manifest_path.write_text('{"id":"E1","type":"evidence"}\n', encoding="utf-8")
        review = self.review()
        review["reviewed_sha256"]["manifest"] = hashlib.sha256(self.manifest_path.read_bytes()).hexdigest()
        review["claim_reviews"] = []
        errors = logic_review.validate(review, self.manuscript, self.manifest_path, [],)
        self.assertTrue(any("no central claims" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
