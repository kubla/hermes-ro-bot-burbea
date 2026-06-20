#!/usr/bin/env python3
"""Clone or update the Rob Burbea digital garden dependency."""

import argparse
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path


DEFAULT_REPO_URL = "https://github.com/fschuhi/digital-garden-rob-burbea-publish.git"
DEFAULT_GARDEN_PATH = Path("knowledge/rob-burbea-garden")
DEFAULT_MANIFEST_PATH = Path("knowledge/manifests/garden-source.json")


def run_command(command, cwd=None):
    return subprocess.check_output(command, cwd=cwd, text=True)


def count_markdown_files(path):
    return sum(1 for _ in path.rglob("*.md"))


def ensure_garden(garden_path, manifest_path, repo_url=DEFAULT_REPO_URL, runner=run_command):
    garden_path = Path(garden_path)
    manifest_path = Path(manifest_path)

    if (garden_path / ".git").is_dir():
        runner(["git", "pull", "--ff-only"], cwd=garden_path)
    else:
        garden_path.parent.mkdir(parents=True, exist_ok=True)
        runner(["git", "clone", repo_url, str(garden_path)])

    commit = runner(["git", "rev-parse", "HEAD"], cwd=garden_path).strip()
    manifest = {
        "repo_url": repo_url,
        "path": str(garden_path),
        "commit": commit,
        "markdown_files": count_markdown_files(garden_path) if garden_path.exists() else 0,
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--garden", default=str(DEFAULT_GARDEN_PATH), help="Local garden clone path.")
    parser.add_argument("--manifest", default=str(DEFAULT_MANIFEST_PATH), help="Manifest JSON output path.")
    parser.add_argument("--repo-url", default=DEFAULT_REPO_URL, help="Source git repository URL.")
    args = parser.parse_args()

    manifest = ensure_garden(
        garden_path=Path(args.garden),
        manifest_path=Path(args.manifest),
        repo_url=args.repo_url,
    )
    print(json.dumps(manifest, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
