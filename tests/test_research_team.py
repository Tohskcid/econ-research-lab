import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("research_team", ROOT / "scripts/run_research_team.py")
team = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(team)


def task(task_id, dependencies=None, write_scope=None):
    return {
        "id": task_id,
        "role": "specialist",
        "objective": f"complete {task_id}",
        "depends_on": dependencies or [],
        "inputs": ["research/state.md"],
        "write_scope": write_scope or [f"research/{task_id}"],
        "validation": ["artifact exists"],
        "budget": {"max_seconds": 30},
    }


class ResearchTeamTests(unittest.TestCase):
    def test_malformed_lists_return_errors_instead_of_crashing(self):
        malformed = {"contract_id": "c", "pi": "pi", "tasks": [task("a")]}
        malformed["tasks"][0]["depends_on"] = [{}]
        malformed["tasks"][0]["write_scope"] = [7, "."]
        errors = team.validate_plan(malformed)
        self.assertTrue(any("depends_on" in error for error in errors))
        self.assertTrue(any("unsafe write_scope" in error for error in errors))

    def test_plan_rejects_cycles_and_parallel_write_conflicts(self):
        cyclic = {"contract_id": "c", "pi": "pi", "tasks": [task("a", ["b"]), task("b", ["a"])]}
        self.assertTrue(any("cycle" in error for error in team.validate_plan(cyclic)))
        conflict = {"contract_id": "c", "pi": "pi", "tasks": [task("a", write_scope=["research/shared"]), task("b", write_scope=["research/shared/table.md"])]}
        self.assertTrue(any("overlapping" in error for error in team.validate_plan(conflict)))

    def test_handoff_rejects_artifact_outside_declared_scope(self):
        item = task("search")
        handoff = {
            "task_id": "search",
            "status": "complete",
            "summary": "done",
            "evidence_ids": [],
            "artifacts": ["manuscript.md"],
            "uncertainty": "",
            "blockers": [],
            "recommended_next": "PI review",
        }
        self.assertTrue(any("outside" in error for error in team.validate_handoff(handoff, item)))

    @patch.object(team.subprocess, "run")
    def test_dependency_handoffs_flow_to_downstream_task(self, run):
        seen = []

        def response(*_args, **kwargs):
            request = json.loads(kwargs["input"])
            seen.append(request)
            task_id = request["task"]["id"]
            handoff = {
                "task_id": task_id,
                "status": "complete",
                "summary": f"done {task_id}",
                "evidence_ids": [],
                "artifacts": [f"research/{task_id}/result.md"],
                "uncertainty": "",
                "blockers": [],
                "recommended_next": "PI review",
            }
            return team.subprocess.CompletedProcess(["adapter"], 0, json.dumps(handoff), "")

        run.side_effect = response
        plan = {"contract_id": "c", "pi": "pi", "tasks": [task("search"), task("review", ["search"])]}
        with tempfile.TemporaryDirectory() as directory:
            report = team.run_plan(plan, Path("adapter"), Path(directory), 1)
            self.assertTrue(Path(directory, "events.jsonl").is_file())
            self.assertTrue(Path(directory, "report.json").is_file())
        self.assertTrue(report["all_complete"])
        review = next(request for request in seen if request["task"]["id"] == "review")
        self.assertEqual(review["dependency_handoffs"][0]["task_id"], "search")

    @patch.object(team.subprocess, "run")
    def test_failed_dependency_blocks_downstream_task(self, run):
        run.return_value = team.subprocess.CompletedProcess(["adapter"], 1, "", "boom")
        plan = {"contract_id": "c", "pi": "pi", "tasks": [task("search"), task("review", ["search"])]}
        with tempfile.TemporaryDirectory() as directory:
            report = team.run_plan(plan, Path("adapter"), Path(directory), 1)
        by_id = {item["task_id"]: item for item in report["handoffs"]}
        self.assertEqual(by_id["search"]["status"], "failed")
        self.assertEqual(by_id["review"]["status"], "blocked")


if __name__ == "__main__":
    unittest.main()
