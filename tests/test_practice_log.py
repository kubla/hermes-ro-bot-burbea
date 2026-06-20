import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def load_script(name):
    path = REPO_ROOT / "scripts" / name
    spec = importlib.util.spec_from_file_location(name.replace(".py", ""), path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class PracticeLogTests(unittest.TestCase):
    def test_append_entry_writes_jsonl_with_source_refs(self):
        module = load_script("log_practice_checkin.py")

        with tempfile.TemporaryDirectory() as tmp:
            log_path = Path(tmp) / "practice-log.jsonl"
            entry = module.append_entry(
                log_path=log_path,
                duration_min=25,
                practice_family="metta",
                note="softened effort",
                source_refs=["Guided meditations.md"],
            )

            self.assertEqual(entry["duration_min"], 25)
            self.assertEqual(entry["practice_family"], "metta")
            self.assertIn("ts", entry)

            rows = [json.loads(line) for line in log_path.read_text().splitlines()]
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]["note"], "softened effort")
            self.assertEqual(rows[0]["source_refs"], ["Guided meditations.md"])


if __name__ == "__main__":
    unittest.main()
