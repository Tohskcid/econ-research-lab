import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("econ_data_profiler", ROOT / "scripts/econ_data_profiler.py")
profiler = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(profiler)


class ProfilerTests(unittest.TestCase):
    def test_cli_smoke_on_bundled_fixture(self):
        with tempfile.TemporaryDirectory() as directory:
            result = subprocess.run([
                sys.executable, str(ROOT / "scripts/econ_data_profiler.py"),
                "--data", str(ROOT / "tests/fixtures/minimal_panel.csv"),
                "--id", "unit_id", "--time", "year", "--x", "treatment", "--y", "outcome",
                "--bins", "2", "--latex", "--out-dir", directory,
            ], check=False, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("Balanced Panel", result.stdout)
            self.assertTrue((Path(directory) / "table1_summary_stats.tex").is_file())
            self.assertTrue((Path(directory) / "descriptive_binned_means_outcome_vs_treatment.svg").is_file())

    def test_unknown_column_fails_with_suggestion(self):
        frame = pd.DataFrame({"County_FIPS": [1], "Year": [2020]})
        with self.assertRaisesRegex(ValueError, "County_FIPS"):
            profiler.validate_columns(frame, {"id": "county_fips"})

    def test_panel_reports_duplicate_and_missing_keys(self):
        frame = pd.DataFrame({"id": [1, 1, 1, 2, None], "year": [1, 1, 2, 1, 2]})
        result = profiler.check_panel_structure(frame, "id", "year")
        self.assertFalse(result["is_balanced"])
        self.assertEqual(result["duplicate_key_rows"], 2)
        self.assertEqual(result["missing_key_rows"], 1)
        self.assertEqual((result["min_periods_per_unit"], result["max_periods_per_unit"]), (1, 2))

    def test_constant_x_returns_no_bins(self):
        frame = pd.DataFrame({"x": [1] * 10, "y": range(10)})
        self.assertTrue(profiler.compute_binned_means(frame, "x", "y", 5).empty)

    def test_latex_and_svg_escape_special_characters(self):
        summary = profiler.compute_summary_table(pd.DataFrame({"R&D_%": [1, 2]}))
        latex = profiler.generate_latex_table(summary)
        self.assertIn(r"R\&D\_\%", latex)
        self.assertIn(r"0.0\%", latex)
        self.assertIn(r"\begin{tabular}{lrrrrrrr}", latex)

        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "plot.svg"
            profiler.generate_svg_binscatter([1, 2], [2, 3], "price & tax", "profit < 1", str(target))
            svg = target.read_text(encoding="utf-8")
            self.assertIn("price &amp; tax", svg)
            self.assertIn("profit &lt; 1", svg)


if __name__ == "__main__":
    unittest.main()
