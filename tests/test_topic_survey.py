import importlib.util
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


if __name__ == "__main__":
    unittest.main()
