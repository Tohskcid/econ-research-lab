import json
import unittest
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]


class JournalRegistryTests(unittest.TestCase):
    def test_registry_has_selected_finance_outlets(self):
        records = [json.loads(line) for line in (ROOT / "library/journals.jsonl").read_text(encoding="utf-8").splitlines()]
        by_id = {record["id"]: record for record in records}
        self.assertTrue({"jf", "jfe", "rfs", "jfqa", "rof"}.issubset(by_id))
        self.assertEqual(len(by_id), len(records))
        for record in records:
            self.assertEqual(record["profile_status"], "derive-from-corpus")
            self.assertEqual(urlparse(record["homepage"]).scheme, "https")


if __name__ == "__main__":
    unittest.main()
