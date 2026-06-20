import importlib.util
import sqlite3
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


class GardenIndexTests(unittest.TestCase):
    def test_build_index_extracts_documents_links_topics_and_guided_meditations(self):
        module = load_script("build_garden_index.py")

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            garden = root / "garden"
            (garden / "Index").mkdir(parents=True)
            (garden / "2019 Practising the Jhanas").mkdir()

            (garden / "Guided meditations.md").write_text(
                "retreat | talk\n"
                "- | -\n"
                "[[2019 Practising the Jhanas]] | [[Whole-body breath]]\n"
            )
            (garden / "Index" / "Energy body.md").write_text(
                "# Energy body\n\nMentioned in [[Whole-body breath]].\n"
            )
            (garden / "2019 Practising the Jhanas" / "Whole-body breath.md").write_text(
                "# Whole-body breath\n\n"
                "Practice with [[Energy body]].\n\n"
                "## Guided meditation\n\n"
                "Feel the breath in the whole body.\n"
            )

            db_path = root / "index.sqlite"
            stats = module.build_index(garden_path=garden, db_path=db_path)

            self.assertEqual(stats["documents"], 3)
            self.assertGreaterEqual(stats["links"], 2)
            self.assertEqual(stats["guided_meditations"], 1)

            conn = sqlite3.connect(db_path)
            try:
                titles = {row[0] for row in conn.execute("select title from documents")}
                self.assertIn("Whole-body breath", titles)
                topics = {row[0] for row in conn.execute("select name from topics")}
                self.assertIn("Energy body", topics)
                chunks = list(conn.execute("select heading, text from chunks where document_path like ?", ("%Whole-body breath.md",)))
                self.assertTrue(any(row[0] == "Guided meditation" for row in chunks))
            finally:
                conn.close()


if __name__ == "__main__":
    unittest.main()
