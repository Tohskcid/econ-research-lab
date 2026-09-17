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

    def test_version_is_consistent(self):
        pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
        self.assertIn('version = "2.11.0"', pyproject)
        self.assertIn('version: "2.11.0"', self.text)

    def test_theory_requires_auditable_complete_proofs(self):
        theory = (ROOT / "references/theory.md").read_text(encoding="utf-8")
        for phrase in ["Complete paper-proof gate", "obligation table", "complete paper proof", "no obligation is unresolved"]:
            self.assertIn(phrase, theory)

    def test_latex_gate_requires_semantic_equation_breaks(self):
        latex = (ROOT / "references/latex_validation.md").read_text(encoding="utf-8")
        for phrase in ["No mathematical ink", "align", "multline", "zero-overfull gate", "inside the margins"]:
            self.assertIn(phrase, latex)

    def test_readme_documents_architecture(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("# Invisible Hands for Economists", readme)
        self.assertIn("```mermaid", readme)
        self.assertIn("provenance graph", readme)

    def test_readme_documents_supported_install_locations(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        for phrase in [
            "### Codex",
            '"$HOME/.agents/skills/econ-research-lab"',
            "### Claude Code",
            '"$HOME/.claude/skills/econ-research-lab"',
            "### Google Antigravity",
            '"$HOME/.gemini/config/skills/econ-research-lab"',
        ]:
            self.assertIn(phrase, readme)

    def test_core_contract_invariants_are_present(self):
        for phrase in [
            "Without an explicit autonomy budget",
            "Do not optimize p-values",
            "Lean 4 + Mathlib",
            "locked Lean 4 + Mathlib harness",
            "claim-centered literature map",
            "mathematical obligations",
            "never rewrite skill instructions during an ordinary research run",
            "confidential",
            "proxy data",
            "auditing an article",
            "validated task DAG",
            "actually dispatch",
            "do not merely name roles",
            "Retain agent identifiers",
            "wait for every required handoff",
            "compile and render the full document",
            "inspect every page",
        ]:
            self.assertIn(phrase, self.body)

    def test_core_is_not_bound_to_a_specific_research_topic(self):
        lowered = self.text.casefold()
        for phrase in ["data center", "time-to-power", "master thesis"]:
            self.assertNotIn(phrase, lowered)

    def test_core_uses_target_journal_without_rankings(self):
        self.assertIn("target journal/audience", self.text)
        self.assertNotIn("ranking", self.text.casefold())

    def test_journal_style_is_progressively_loaded(self):
        reference = (ROOT / "references/journal_style.md").read_text(encoding="utf-8")
        self.assertIn("extracting or applying target-outlet conventions", self.body)
        for phrase in ["observations", "confidence", "do not reproduce distinctive sentences", "research validity"]:
            self.assertIn(phrase, reference.casefold())

    def test_manuscript_has_research_merit_gates(self):
        manuscript = (ROOT / "references/manuscript.md").read_text(encoding="utf-8")
        for phrase in ["Identification", "Economic mechanism", "Data and econometrics", "Contribution and relevance"]:
            self.assertIn(phrase, manuscript)

    def test_method_router_prioritizes_identification_over_data_shape(self):
        router = (ROOT / "references/method_router.md").read_text(encoding="utf-8")
        for phrase in [
            "estimand and assignment mechanism",
            "natural experiment",
            "DiD / causal event study",
            "IV / LATE",
            "complier population",
            "never silently rename LATE as ATE",
            "do not choose by p-value",
        ]:
            self.assertIn(phrase, router)


if __name__ == "__main__":
    unittest.main()
