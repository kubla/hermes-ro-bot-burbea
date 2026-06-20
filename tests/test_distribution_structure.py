import json
import re
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


class DistributionStructureTests(unittest.TestCase):
    def test_required_profile_distribution_files_exist(self):
        required = [
            "distribution.yaml",
            "SOUL.md",
            "config.yaml",
            "mcp.json",
            ".env.EXAMPLE",
            "README.md",
            "SPEC.md",
            "docs/coaching-contract.md",
            "docs/knowledge-base-rights.md",
            "docs/supported-practices.md",
            "knowledge/README.md",
        ]
        for relative in required:
            with self.subTest(relative=relative):
                self.assertTrue((REPO_ROOT / relative).is_file())

    def test_required_skills_exist(self):
        skills = [
            "first-run-setup",
            "practice-intake",
            "meditation-session",
            "post-sit-reflection",
            "burbea-garden-retrieval",
            "practice-plan-review",
            "safety-and-grounding",
            "teacherly-style-guardrails",
        ]
        for skill in skills:
            with self.subTest(skill=skill):
                path = REPO_ROOT / "skills" / skill / "SKILL.md"
                self.assertTrue(path.is_file())
                text = path.read_text()
                self.assertIn("description:", text)
                self.assertIn("#", text)

    def test_cron_templates_are_json_and_paused_by_default(self):
        cron_dir = REPO_ROOT / "cron"
        expected = {
            "morning-practice-invitation.json",
            "evening-reflection.json",
            "weekly-practice-review.json",
            "monthly-curriculum-refresh.json",
            "quarterly-safety-and-direction-review.json",
        }
        found = {path.name for path in cron_dir.glob("*.json")}
        self.assertEqual(found, expected)
        for path in cron_dir.glob("*.json"):
            with self.subTest(path=path.name):
                data = json.loads(path.read_text())
                self.assertTrue(data["paused"])
                self.assertIn("schedule", data)
                self.assertIn("prompt", data)

    def test_distribution_manifest_is_provider_silent_and_public_ready(self):
        text = (REPO_ROOT / "distribution.yaml").read_text()
        self.assertIn("name: ro-bot-burbea", text)
        self.assertIn("logo: logo.png", text)
        self.assertIn("  - logo.png", text)
        self.assertIn("env_requires: []", text)
        self.assertNotRegex(text, re.compile(r"(OPENAI|ANTHROPIC|HONCHO)_API_KEY"))
        self.assertIn("distribution_owned:", text)

    def test_readme_displays_committed_logo_for_github_landing_page(self):
        readme = (REPO_ROOT / "README.md").read_text()
        self.assertIn("![RoBot Burbea logo](logo.png)", readme)
        self.assertTrue((REPO_ROOT / "logo.png").is_file())

    def test_runtime_paths_are_ignored(self):
        ignore = (REPO_ROOT / ".gitignore").read_text()
        self.assertIn("knowledge/rob-burbea-garden/", ignore)
        self.assertIn("knowledge/indexes/", ignore)
        self.assertIn("data/", ignore)


if __name__ == "__main__":
    unittest.main()
