import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("journal_matcher", ROOT / "scripts/journal_matcher.py")
matcher = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(matcher)


class JournalMatcherTests(unittest.TestCase):
    def test_normalizes_and_and_ampersand(self):
        name, info, score = matcher.lookup_journal("Journal of Business & Economic Statistics")
        self.assertEqual(name, "journal of business and economic statistics")
        self.assertEqual(info["short"], "JBES")
        self.assertEqual(score, 1.0)

    def test_normalizes_unicode_dash(self):
        name, _, score = matcher.lookup_journal("American Economic Journal–Applied Economics")
        self.assertEqual(name, "american economic journal: applied economics")
        self.assertEqual(score, 1.0)

    def test_returns_multiple_candidates_for_broad_query(self):
        candidates = matcher.lookup_candidates("economic", limit=3)
        self.assertGreaterEqual(len(candidates), 2)
        self.assertLessEqual(len(candidates), 3)

    def test_empty_query_has_no_match(self):
        self.assertEqual(matcher.lookup_candidates("  "), [])

    def test_source_tiers_and_counts(self):
        self.assertEqual({tier: len(journals) for tier, journals in matcher.TIERS.items()}, {
            "Excellent": 6, "A+": 36, "A": 29, "TSSCI Core": 5,
        })
        self.assertEqual(matcher.lookup_journal("Journal of Finance")[1]["tier"], "Excellent")
        self.assertEqual(matcher.lookup_journal("Economic Theory")[1]["tier"], "A+")
        self.assertEqual(matcher.lookup_journal("Econometric Theory")[1]["tier"], "A")


if __name__ == "__main__":
    unittest.main()
