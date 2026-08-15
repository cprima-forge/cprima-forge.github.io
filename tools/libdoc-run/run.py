"""Run `henri uips libdoc` against every open-edition cpmf-uipsl-* repo.

henri (cprima-forge/cpmf-uips-cli) is a dotnet global tool that statically
parses a UiPath Library's src/open project and emits docs/<Name>.doc.json.
This centralizes what was previously an ad-hoc, one-off run against
lib-appintegration-sap.

Requires: `dotnet tool install -g henri` (or `--tool` pointing at the exe).

Usage:
    uv run run.py [--root D:/github.com/cprima-forge] [--tool henri]
"""

import argparse
import subprocess
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
DATA_DIR = HERE.parent.parent / "data"


def load_libraries():
    with open(DATA_DIR / "libraries.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f)["libraries"]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--root",
        type=Path,
        default=HERE.parent.parent.parent,
        help="Directory containing the repo clones",
    )
    parser.add_argument("--tool", default="henri", help="henri executable name or path")
    args = parser.parse_args()

    for lib in load_libraries():
        if not lib.get("open"):
            continue
        name = lib["name"]
        project_json = args.root / name / "src" / "open" / "project.json"
        if not project_json.is_file():
            print(f"{name}: SKIP (no {project_json})")
            continue

        print(f"{name}: running libdoc...")
        result = subprocess.run(
            [args.tool, "uips", "libdoc", "-p", str(project_json)],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            print(f"{name}: FAILED\n{result.stderr}")
        else:
            print(f"{name}: OK")


if __name__ == "__main__":
    main()
