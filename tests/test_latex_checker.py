import importlib.util
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("latex_checker", ROOT / "scripts/check_latex.py")
checker = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(checker)


class LatexCheckerTests(unittest.TestCase):
    def test_log_rejects_undefined_references_and_overfull_boxes(self):
        errors, _warnings = checker.analyze_log(
            "LaTeX Warning: Reference `x' on page 1 undefined.\nOverfull \\hbox (4.2pt too wide)", 0
        )
        self.assertTrue(any("undefined" in error.lower() for error in errors))
        self.assertTrue(any("4.2pt" in error for error in errors))

    def test_magic_comment_selects_available_engine(self):
        with tempfile.TemporaryDirectory() as directory:
            main = Path(directory, "main.tex")
            main.write_text("% !TeX program = xelatex\n\\documentclass{article}", encoding="utf-8")
            with patch.object(checker.shutil, "which", side_effect=lambda name: f"/bin/{name}" if name == "xelatex" else None):
                self.assertEqual(checker.select_engine(main, "auto"), "xelatex")

    def test_render_requires_all_reported_pages(self):
        with tempfile.TemporaryDirectory() as directory, patch.object(checker.shutil, "which", side_effect=lambda name: f"/bin/{name}" if name in {"pdfinfo", "pdftoppm"} else None), patch.object(checker.subprocess, "run") as run:
            Path(directory, "paper.pdf").write_bytes(b"pdf")
            run.side_effect = [
                checker.subprocess.CompletedProcess(["pdfinfo"], 0, "Pages: 2\n", ""),
                checker.subprocess.CompletedProcess(["pdftoppm"], 0, "", ""),
                checker.subprocess.CompletedProcess(["pdftoppm"], 0, "", ""),
            ]
            result = checker.render_pdf(Path(directory, "paper.pdf"), Path(directory, "pages"), 10)
        self.assertTrue(any("rendered 0 pages" in error for error in result["errors"]))

    def test_commands_disable_shell_escape_and_network_fetch(self):
        main, build = Path("main.tex"), Path("build")
        self.assertIn("--only-cached", checker.engine_commands("tectonic", main, build)[0])
        self.assertIn("--untrusted", checker.engine_commands("tectonic", main, build)[0])
        self.assertIn("-no-shell-escape", checker.engine_commands("pdflatex", main, build)[0])

    def test_finalize_requires_matching_hash_and_all_pages(self):
        report = {"automated_passed": True, "rendering": {"pdf_sha256": "abc", "page_count": 2}}
        review = {
            "pdf_sha256": "abc",
            "status": "pass",
            "reviewer": "layout-agent",
            "pages_reviewed": [1, 2],
            "issues": [],
        }
        self.assertTrue(checker.finalize(report, review)["delivery_ready"])
        review["pages_reviewed"] = [1]
        self.assertFalse(checker.finalize(report, review)["delivery_ready"])


if __name__ == "__main__":
    unittest.main()
