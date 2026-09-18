import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("dream_replay_simulator", ROOT / "scripts/dream_replay_simulator.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class DreamRSITests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.tree_file = Path(self.temp_dir.name) / "discovery_tree.jsonl"
        self.sample_nodes = [
            {
                "node_id": "root",
                "parent_id": None,
                "metrics": {"direct_effect": -0.0030, "first_stage_f": 35.0},
                "referee_vulnerabilities": ["greg_correlation"]
            },
            {
                "node_id": "branch-1",
                "parent_id": "root",
                "metrics": {"direct_effect": -0.0035, "first_stage_f": 28.0},
                "referee_vulnerabilities": ["macro_shock"]
            },
            {
                "node_id": "branch-2",
                "parent_id": "root",
                "metrics": {"direct_effect": -0.0028, "first_stage_f": 8.0},  # weak IV
                "referee_vulnerabilities": []
            }
        ]
        with open(self.tree_file, "w", encoding="utf-8") as f:
            for n in self.sample_nodes:
                f.write(json.dumps(n) + "\n")

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_load_and_audit(self):
        nodes = MODULE.load_discovery_tree(self.tree_file)
        self.assertEqual(len(nodes), 3)
        audit = MODULE.audit_tree_structure(nodes)
        self.assertTrue(audit["valid"])
        self.assertEqual(audit["node_count"], 3)

    def test_dream_spec_curve_filters_weak_iv(self):
        nodes = MODULE.load_discovery_tree(self.tree_file)
        res = MODULE.dream_offline_spec_curve(nodes, min_f_stat=10.0)
        self.assertEqual(res["status"], "success")
        self.assertEqual(res["screened_candidates"], 3)
        self.assertEqual(res["retained_specifications"], 2)
        self.assertAlmostEqual(res["sign_stability"], 1.0)

    def test_evolve_adversarial_pool(self):
        nodes = MODULE.load_discovery_tree(self.tree_file)
        pool = MODULE.evolve_adversarial_pool(nodes)
        self.assertIn("greg_correlation", pool)
        self.assertIn("macro_shock", pool)


if __name__ == "__main__":
    unittest.main()
