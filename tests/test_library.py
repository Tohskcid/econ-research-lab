import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_module(name, relative_path):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


search_tool = load_module("search_library", "scripts/search_library.py")
validate_tool = load_module("validate_library", "scripts/validate_library.py")


class LibraryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog, catalog_errors = validate_tool.load_jsonl(ROOT / "library/catalog.jsonl")
        cls.cards, card_errors = validate_tool.load_jsonl(ROOT / "library/index.jsonl")
        cls.relations, relation_errors = validate_tool.load_jsonl(ROOT / "library/relations.jsonl")
        cls.load_errors = catalog_errors + card_errors + relation_errors

    def test_bundled_library_is_valid_and_balanced(self):
        self.assertEqual(self.load_errors, [])
        self.assertEqual(validate_tool.validate(self.catalog, self.cards, self.relations), [])
        self.assertGreaterEqual(len(self.cards), 10)
        self.assertLessEqual(len(self.cards), 20)
        self.assertEqual({card["mode"] for card in self.cards}, {"theory", "empirical", "structural"})

    def test_problem_search_finds_expected_cards(self):
        theory = search_tool.search(self.cards, "single crossing monotone choice", "theory", None, 3, False)
        empirical = search_tool.search(self.cards, "staggered adoption heterogeneous effects", "empirical", None, 3, False)
        self.assertEqual(theory[0]["id"], "milgrom-shannon-monotone-comparative-statics")
        self.assertIn("callaway-santanna-group-time-att", {card["id"] for card in empirical})

    def test_blind_mode_hides_solution_fields(self):
        result = search_tool.search(self.cards, "Nash equilibrium fixed point", "theory", "theorem", 1, True)[0]
        self.assertNotIn("proof_strategy", result)
        self.assertIn("path", result)

        markdown = (ROOT / result["path"]).read_text(encoding="utf-8")
        hidden = search_tool.hide_solution_sections(markdown)
        self.assertNotIn("## Proof strategy", hidden)
        self.assertIn("## Assumptions", hidden)
        self.assertIn("## Conclusion", hidden)

    def test_search_results_are_compact_and_point_to_markdown(self):
        result = search_tool.search(self.cards, "dynamic discrete choice", "structural", None, 3, False)[0]
        self.assertNotIn("assumptions", result)
        self.assertNotIn("conclusion", result)
        self.assertTrue((ROOT / result["path"]).is_file())

    def test_dangling_relation_is_rejected(self):
        bad = [{"from": "missing", "to": "also-missing", "type": "alternative", "note": "x", "_line": 1}]
        errors = validate_tool.validate(self.catalog, self.cards, bad)
        self.assertTrue(any("endpoints" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
