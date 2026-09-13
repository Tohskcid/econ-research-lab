import importlib.util
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("check_lean_proof", ROOT / "scripts/check_lean_proof.py")
checker = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(checker)


class LeanCheckerTests(unittest.TestCase):
    def test_detects_proof_escapes_but_ignores_comments_and_strings(self):
        source = 'theorem bad : True := by sorry\n-- admit\ndef label := "axiom"\n'
        self.assertEqual(checker.proof_escapes(source), ["sorry"])

    @patch.object(checker.shutil, "which")
    def test_prefers_lake(self, which):
        which.side_effect = lambda command: "/usr/bin/lake" if command == "lake" else None
        self.assertEqual(checker.compiler_command(Path("Proof.lean")), ["lake", "env", "lean", "Proof.lean"])

    @patch.object(checker.shutil, "which", return_value=None)
    def test_missing_lean_is_blocked(self, _):
        with self.assertRaisesRegex(FileNotFoundError, "Lean 4 is unavailable"):
            checker.compiler_command(Path("Proof.lean"))


if __name__ == "__main__":
    unittest.main()
