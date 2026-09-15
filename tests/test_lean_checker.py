import importlib.util
import json
import tempfile
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

    def test_nested_comments_do_not_trigger_escape_scan(self):
        source = "/- outer /- sorry -/ axiom -/ theorem ok : True := by trivial"
        self.assertEqual(checker.proof_escapes(source), [])

    def test_locked_task_rejects_statement_or_policy_changes(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "proof-task.json"
            task = {
                "version": 1,
                "theorem_name": "identity",
                "source_statement": "Every natural number equals itself.",
                "formalization_status": "approved",
                "assumptions": [],
                "statement": "∀ n : Nat, n = n",
                "imports": [],
                "allowed_axioms": [],
                "timeout_seconds": 30,
            }
            path.write_text(json.dumps(task), encoding="utf-8")
            locked = checker.lock_task(path)
            checker.validate_task(locked)
            locked["statement"] = "True"
            with self.assertRaisesRegex(ValueError, "statement hash mismatch"):
                checker.validate_task(locked)

    def test_candidate_is_embedded_as_a_proof_term(self):
        task = {"imports": ["Mathlib"], "preamble": "", "statement": "True"}
        source = checker.build_source(task, "by trivial")
        self.assertIn("theorem target : (True) := (\nby trivial\n)", source)
        self.assertIn("#print axioms EconResearchHarness.target", source)

    def test_axiom_audit_is_transitive_and_fail_closed(self):
        output = "'EconResearchHarness.target' depends on axioms: [propext, Bad.hidden]"
        self.assertEqual(checker.parse_axioms(output), ["Bad.hidden", "propext"])
        self.assertEqual(checker.parse_axioms("'EconResearchHarness.target' does not depend on any axioms"), [])
        self.assertIsNone(checker.parse_axioms("unexpected compiler output"))

    def test_custom_axiom_cannot_be_allowlisted(self):
        task = {
            "version": 1,
            "theorem_name": "identity",
            "source_statement": "Every natural number equals itself.",
            "formalization_status": "approved",
            "assumptions": [],
            "statement": "∀ n : Nat, n = n",
            "imports": [],
            "allowed_axioms": ["sorryAx"],
            "timeout_seconds": 30,
        }
        task["statement_sha256"] = checker.digest(task["statement"])
        task["task_sha256"] = checker.task_digest(task)
        with self.assertRaisesRegex(ValueError, "nonstandard axioms"):
            checker.validate_task(task)

    @patch.object(checker, "compiler_command", return_value=["lean", "Candidate.lean"])
    @patch.object(checker.subprocess, "run")
    def test_locked_run_rejects_unapproved_transitive_axiom(self, run, _command):
        run.return_value = checker.subprocess.CompletedProcess(
            ["lean"], 0, "'EconResearchHarness.target' depends on axioms: [Bad.hidden]\n", ""
        )
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            task_path, proof_path = root / "proof-task.json", root / "candidate.lean"
            task_path.write_text(json.dumps({
                "version": 1,
                "theorem_name": "identity",
                "source_statement": "Every natural number equals itself.",
                "formalization_status": "approved",
                "assumptions": [],
                "statement": "∀ n : Nat, n = n",
                "imports": [],
                "allowed_axioms": [],
                "timeout_seconds": 30,
            }), encoding="utf-8")
            checker.lock_task(task_path)
            proof_path.write_text("by intro n; rfl", encoding="utf-8")
            result = checker.run_locked_task(task_path, proof_path)
        self.assertEqual(result["status"], "rejected")
        self.assertEqual(result["unexpected_axioms"], ["Bad.hidden"])

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
