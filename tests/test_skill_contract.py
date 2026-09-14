import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class SkillContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        cls.body = cls.text.split("---", 2)[2]

    def test_entrypoint_is_small(self):
        self.assertLessEqual(len(self.body.split()), 1000)

    def test_mode_references_exist(self):
        links = re.findall(r"\((references/[^)]+\.md)\)", self.body)
        for link in links:
            self.assertTrue((ROOT / link).is_file(), link)

    def test_core_contract_invariants_are_present(self):
        for phrase in [
            "Without an explicit autonomy budget",
            "Do not optimize p-values",
            "Lean 4 + Mathlib",
            "claim-centered literature map",
            "mathematical obligations",
            "never rewrite skill instructions during an ordinary research run",
        ]:
            self.assertIn(phrase, self.body)

    def test_core_is_not_bound_to_a_specific_research_topic(self):
        lowered = self.text.casefold()
        for phrase in ["data center", "time-to-power", "master thesis"]:
            self.assertNotIn(phrase, lowered)


if __name__ == "__main__":
    unittest.main()
