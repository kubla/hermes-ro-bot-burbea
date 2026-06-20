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


class BootstrapGardenTests(unittest.TestCase):
    def test_clone_creates_manifest_with_source_url_and_commit(self):
        module = load_script("clone_or_update_garden.py")
        commands = []

        def runner(command, cwd=None):
            commands.append((command, cwd))
            if command[:2] == ["git", "rev-parse"]:
                return "abc123\n"
            return ""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            garden = root / "garden"
            manifest = root / "manifest.json"

            module.ensure_garden(
                garden_path=garden,
                manifest_path=manifest,
                repo_url="https://example.test/garden.git",
                runner=runner,
            )

            self.assertEqual(commands[0][0], ["git", "clone", "https://example.test/garden.git", str(garden)])
            self.assertEqual(commands[1][0], ["git", "rev-parse", "HEAD"])
            self.assertEqual(commands[1][1], garden)

            data = json.loads(manifest.read_text())
            self.assertEqual(data["repo_url"], "https://example.test/garden.git")
            self.assertEqual(data["commit"], "abc123")
            self.assertEqual(data["path"], str(garden))

    def test_existing_clone_runs_git_pull_before_manifest(self):
        module = load_script("clone_or_update_garden.py")
        commands = []

        def runner(command, cwd=None):
            commands.append((command, cwd))
            if command[:2] == ["git", "rev-parse"]:
                return "def456\n"
            return ""

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            garden = root / "garden"
            (garden / ".git").mkdir(parents=True)
            manifest = root / "manifest.json"

            module.ensure_garden(
                garden_path=garden,
                manifest_path=manifest,
                repo_url="https://example.test/garden.git",
                runner=runner,
            )

            self.assertEqual(commands[0][0], ["git", "pull", "--ff-only"])
            self.assertEqual(commands[0][1], garden)
            data = json.loads(manifest.read_text())
            self.assertEqual(data["commit"], "def456")


if __name__ == "__main__":
    unittest.main()
