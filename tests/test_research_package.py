import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("check_research_package", ROOT / "scripts/check_research_package.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class ResearchPackageTests(unittest.TestCase):
    def test_quantitative_results_require_data_provenance(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "research").mkdir()
            (root / "paper").mkdir()
            (root / "research/results.json").write_text("{}", encoding="utf-8")
            (root / "paper/main.tex").write_text("text", encoding="utf-8")
            config = root / "research/package.json"
            config.write_text(json.dumps({
                "results": "research/results.json",
                "manuscript": "paper/main.tex",
            }), encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "results requires data_provenance"):
                MODULE.check(root, config, ROOT / "scripts")

    def test_manuscript_requires_bibliography_archive(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "paper").mkdir()
            (root / "paper/main.tex").write_text("text", encoding="utf-8")
            config = root / "package.json"
            config.write_text(json.dumps({"manuscript": "paper/main.tex"}), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "requires bibliography and literature_archive"):
                MODULE.check(root, config, ROOT / "scripts")


if __name__ == "__main__":
    unittest.main()
