import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("check_topic_survey", ROOT / "scripts/check_topic_survey.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class TopicSurveyTests(unittest.TestCase):
    def survey(self):
        return {
            "schema_version": "1",
            "question": "Does a policy affect employment?",
            "scope": "Applied microeconomics through 2026-09-17",
            "cutoff": "2026-09-17",
            "searches": [
                {"axis": "question", "source": "EconLit", "query": "policy employment", "searched_at": "2026-09-17"},
                {"axis": "mechanism", "source": "NBER", "query": "policy labor demand", "searched_at": "2026-09-17"},
            ],
            "nearest_works": [{
                "title": "Closest paper",
                "locator": "https://example.org/paper",
                "source_evidence_artifact": "research/source.json",
                "source_evidence_sha256": "a" * 64,
                "verified_at": "2026-09-17",
                "question": "Related policy question",
                "estimand_or_theorem": "ATT",
                "method_or_proof": "DiD",
                "difference": "Different assignment mechanism",
                "relation": "extension",
                "nearest": True,
                "full_text_status": "checked",
                "backward_checked": True,
                "forward_checked": True,
            }],
            "contribution_class": "extension",
            "contribution_statement": "Tests a different assignment mechanism.",
            "decision": "proceed",
            "limitations": ["Coverage excludes inaccessible dissertations."],
        }

    def test_valid_bounded_extension(self):
        report = MODULE.validate(self.survey())
        self.assertTrue(report["valid"], report["errors"])

    def test_duplicate_cannot_proceed_unchanged(self):
        survey = self.survey()
        survey["nearest_works"][0]["relation"] = "duplicate"
        survey["contribution_class"] = "duplicate"
        report = MODULE.validate(survey)
        self.assertFalse(report["valid"])
        self.assertTrue(any("duplicate" in error for error in report["errors"]))

    def test_no_verified_work_cannot_be_called_novel(self):
        survey = self.survey()
        survey["nearest_works"] = []
        report = MODULE.validate(survey)
        self.assertFalse(report["valid"])
        self.assertTrue(any("blocked/unresolved" in error for error in report["errors"]))

    def test_locator_must_be_canonical_https_url(self):
        survey = self.survey()
        survey["nearest_works"][0]["locator"] = "Journal Name 1(2): 3-4"
        report = MODULE.validate(survey)
        self.assertFalse(report["valid"])
        self.assertTrue(any("canonical HTTPS URL" in error for error in report["errors"]))

    def test_source_evidence_requires_safe_path_and_sha256(self):
        survey = self.survey()
        survey["nearest_works"][0]["source_evidence_artifact"] = "../source.json"
        survey["nearest_works"][0]["source_evidence_sha256"] = "not-a-hash"
        report = MODULE.validate(survey)
        self.assertFalse(report["valid"])
        self.assertTrue(any("safe source_evidence_artifact" in error for error in report["errors"]))
        self.assertTrue(any("source_evidence_sha256" in error for error in report["errors"]))

    def test_source_evidence_checksum_is_verified(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            evidence = root / "research/source.json"
            evidence.parent.mkdir()
            survey = self.survey()
            work = survey["nearest_works"][0]
            evidence.write_text(json.dumps({"sources": [{
                "title": work["title"],
                "canonical_locator": work["locator"],
            }]}), encoding="utf-8")
            survey["nearest_works"][0]["source_evidence_sha256"] = hashlib.sha256(evidence.read_bytes()).hexdigest()
            self.assertTrue(MODULE.validate(survey, root)["valid"])
            evidence.write_text("changed", encoding="utf-8")
            report = MODULE.validate(survey, root)
        self.assertTrue(any("checksum mismatch" in error for error in report["errors"]))


if __name__ == "__main__":
    unittest.main()
