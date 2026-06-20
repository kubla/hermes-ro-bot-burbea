import json
import os
import shutil
import subprocess
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
HERMES = shutil.which("hermes")


def run_hermes(args, hermes_home, timeout=90, extra_env=None):
    env = {
        **os.environ,
        "HERMES_HOME": str(hermes_home),
        "PYTHONUNBUFFERED": "1",
    }
    if extra_env:
        env.update(extra_env)
    return subprocess.run(
        [HERMES, *args],
        cwd=REPO_ROOT,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=timeout,
    )


@unittest.skipUnless(HERMES, "Hermes CLI is not installed")
class HermesProfileAcceptanceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="ro-bot-hermes-acceptance."))

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def install_profile(self, name="acceptance-ro-bot"):
        result = run_hermes(
            ["profile", "install", str(REPO_ROOT), "--name", name, "-y"],
            hermes_home=self.tmp,
        )
        self.assertEqual(result.returncode, 0, result.stdout)
        return self.tmp / "profiles" / name, result.stdout

    def test_local_profile_install_copies_distribution_without_runtime_data(self):
        profile_path, output = self.install_profile()

        self.assertIn("Installed 'acceptance-ro-bot' v0.1.0", output)
        self.assertIn("Cron jobs were included but are NOT scheduled automatically", output)
        self.assertTrue((profile_path / "distribution.yaml").is_file())
        self.assertTrue((profile_path / "logo.png").is_file())
        self.assertTrue((profile_path / "SOUL.md").is_file())
        self.assertTrue((profile_path / "skills" / "first-run-setup" / "SKILL.md").is_file())
        self.assertFalse((profile_path / "knowledge" / "rob-burbea-garden").exists())
        self.assertFalse((profile_path / "data" / "practice-log.jsonl").exists())

    def test_installed_manifest_is_provider_silent_and_profile_info_reports_distribution(self):
        self.install_profile()

        info = run_hermes(["profile", "info", "acceptance-ro-bot"], hermes_home=self.tmp)
        self.assertEqual(info.returncode, 0, info.stdout)
        self.assertIn("Distribution: acceptance-ro-bot", info.stdout)
        self.assertIn("Version:      0.1.0", info.stdout)
        self.assertIn("Source:", info.stdout)

        manifest = (self.tmp / "profiles" / "acceptance-ro-bot" / "distribution.yaml").read_text()
        self.assertNotIn("env_requires:", manifest)
        self.assertNotIn("OPENAI_API_KEY", manifest)
        self.assertNotIn("ANTHROPIC_API_KEY", manifest)
        self.assertNotIn("HONCHO_API_KEY", manifest)

    def test_runtime_prompt_loads_ro_bot_identity_and_skill_index(self):
        self.install_profile()

        result = run_hermes(["-p", "acceptance-ro-bot", "prompt-size"], hermes_home=self.tmp)
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("Prompt-size breakdown", result.stdout)
        self.assertIn("skills index", result.stdout)
        self.assertIn("model=unset", result.stdout)

        soul = (self.tmp / "profiles" / "acceptance-ro-bot" / "SOUL.md").read_text()
        self.assertIn("You are not Rob Burbea", soul)
        self.assertIn("co-create a local name", soul)
        self.assertIn("Soulmaking Dharma", soul)

    def test_cron_templates_install_but_do_not_schedule_automatically(self):
        self.install_profile()

        cron_list = run_hermes(["-p", "acceptance-ro-bot", "cron", "list"], hermes_home=self.tmp)
        self.assertEqual(cron_list.returncode, 0, cron_list.stdout)
        self.assertIn("No scheduled jobs", cron_list.stdout)

        cron_templates = sorted((self.tmp / "profiles" / "acceptance-ro-bot" / "cron").glob("*.json"))
        self.assertEqual(len(cron_templates), 5)
        for path in cron_templates:
            with self.subTest(path=path.name):
                data = json.loads(path.read_text())
                self.assertTrue(data["paused"])

    def test_installed_scripts_run_locally_inside_profile(self):
        profile_path, _ = self.install_profile()
        fixture = self.tmp / "garden-fixture"
        (fixture / "Index").mkdir(parents=True)
        (fixture / "2019 Practising the Jhanas").mkdir()
        (fixture / "Guided meditations.md").write_text(
            "retreat | talk\n- | -\n[[2019 Practising the Jhanas]] | [[Whole-body breath]]\n"
        )
        (fixture / "Index" / "Energy body.md").write_text("# Energy body\n\nSee [[Whole-body breath]].\n")
        (fixture / "2019 Practising the Jhanas" / "Whole-body breath.md").write_text(
            "# Whole-body breath\n\nPractice with [[Energy body]].\n"
        )

        index_result = subprocess.run(
            [
                "/usr/bin/python3",
                str(profile_path / "scripts" / "build_garden_index.py"),
                "--garden",
                str(fixture),
                "--output",
                str(self.tmp / "acceptance.sqlite"),
            ],
            cwd=profile_path,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=30,
        )
        self.assertEqual(index_result.returncode, 0, index_result.stdout)
        self.assertIn("documents: 3", index_result.stdout)

        log_result = subprocess.run(
            [
                "/usr/bin/python3",
                str(profile_path / "scripts" / "log_practice_checkin.py"),
                "--log",
                str(self.tmp / "practice-log.jsonl"),
                "--duration-min",
                "15",
                "--practice-family",
                "metta",
                "--note",
                "acceptance test",
                "--source-ref",
                "Guided meditations.md",
            ],
            cwd=profile_path,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=30,
        )
        self.assertEqual(log_result.returncode, 0, log_result.stdout)
        logged = json.loads((self.tmp / "practice-log.jsonl").read_text().splitlines()[0])
        self.assertEqual(logged["practice_family"], "metta")
        self.assertEqual(logged["source_refs"], ["Guided meditations.md"])


class FakeOpenAIHandler(BaseHTTPRequestHandler):
    requests = []

    def do_GET(self):
        if self.path.endswith("/models"):
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(
                json.dumps({"object": "list", "data": [{"id": "acceptance-fake", "object": "model"}]}).encode()
            )
            return
        self.send_response(404)
        self.end_headers()

    def do_POST(self):
        length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(length).decode()
        self.requests.append((self.path, body))
        if self.path == "/api/show":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"model": "acceptance-fake"}).encode())
            return

        payload = json.loads(body or "{}")
        if payload.get("stream"):
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream")
            self.end_headers()
            first = {
                "id": "chatcmpl-acceptance",
                "object": "chat.completion.chunk",
                "choices": [
                    {
                        "index": 0,
                        "delta": {"content": "I can help you co-create a name and begin gently."},
                        "finish_reason": None,
                    }
                ],
            }
            done = {
                "id": "chatcmpl-acceptance",
                "object": "chat.completion.chunk",
                "choices": [{"index": 0, "delta": {}, "finish_reason": "stop"}],
            }
            for chunk in (first, done):
                self.wfile.write(f"data: {json.dumps(chunk)}\n\n".encode())
                self.wfile.flush()
            self.wfile.write(b"data: [DONE]\n\n")
            return

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(
            json.dumps(
                {
                    "id": "chatcmpl-acceptance",
                    "object": "chat.completion",
                    "choices": [
                        {
                            "index": 0,
                            "message": {
                                "role": "assistant",
                                "content": "I can help you co-create a name and begin gently.",
                            },
                            "finish_reason": "stop",
                        }
                    ],
                    "usage": {"prompt_tokens": 1, "completion_tokens": 1, "total_tokens": 2},
                }
            ).encode()
        )

    def log_message(self, fmt, *args):
        return


@unittest.skipUnless(HERMES, "Hermes CLI is not installed")
@unittest.skipUnless(
    os.environ.get("RUN_HERMES_RUNTIME_ACCEPTANCE") == "1",
    "Set RUN_HERMES_RUNTIME_ACCEPTANCE=1 to run fake-provider chat acceptance",
)
class HermesRuntimeInteractionAcceptanceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="ro-bot-hermes-runtime."))
        FakeOpenAIHandler.requests = []
        self.server = HTTPServer(("127.0.0.1", 0), FakeOpenAIHandler)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=5)
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_chat_query_uses_installed_profile_against_local_fake_provider(self):
        install = run_hermes(
            ["profile", "install", str(REPO_ROOT), "--name", "acceptance-ro-bot", "-y"],
            hermes_home=self.tmp,
        )
        self.assertEqual(install.returncode, 0, install.stdout)

        profile_config = self.tmp / "profiles" / "acceptance-ro-bot" / "config.yaml"
        base_url = f"http://127.0.0.1:{self.server.server_address[1]}/v1"
        profile_config.write_text(
            profile_config.read_text()
            + f"""

model:
  provider: openai-api
  default: acceptance-fake
  base_url: {base_url}
providers:
  openai-api:
    api_key: test-key
    base_url: {base_url}
"""
        )

        chat = run_hermes(
            [
                "-p",
                "acceptance-ro-bot",
                "chat",
                "-q",
                "Use the first-run-setup skill. Start by asking about the coach name.",
                "--provider",
                "openai-api",
                "--model",
                "acceptance-fake",
                "--quiet",
            ],
            hermes_home=self.tmp,
            timeout=90,
            extra_env={"OPENAI_API_KEY": "test-key"},
        )

        self.assertEqual(chat.returncode, 0, chat.stdout)
        self.assertIn("co-create a name", chat.stdout)
        request_text = "\n".join(body for _, body in FakeOpenAIHandler.requests)
        self.assertIn("RoBot Burbea", request_text)
        self.assertIn("first-run-setup", request_text)
        self.assertIn("You are not Rob Burbea", request_text)


if __name__ == "__main__":
    unittest.main()
