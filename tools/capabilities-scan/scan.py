"""Scan cpmf-uipsl-* repos for capability doc sources.

Reads the repo list from data/libraries.yaml, checks each local clone for
the doc source required by data/capabilities.yaml's convention (doc.json
for open, XML doc comments for plus), and prints a report.

Usage:
    uv run scan.py [--root D:/github.com/cprima-forge]
"""

import argparse
import re
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
DATA_DIR = HERE.parent.parent / "data"


def load_libraries():
    with open(DATA_DIR / "libraries.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f)["libraries"]


def check_open(repo_path: Path) -> bool:
    # henri libdoc default output: src/open/docs/*.doc.json
    docs = repo_path / "src" / "open" / "docs"
    if docs.is_dir() and any(docs.glob("*.doc.json")):
        return True
    # legacy manual location
    docs = repo_path / "docs"
    return docs.is_dir() and any(docs.glob("*.doc.json"))


def check_plus(repo_path: Path) -> bool:
    activities_dirs = list(repo_path.glob("src/plus/**/Activities"))
    if not activities_dirs:
        return False
    pattern = re.compile(r"///\s*<summary>")
    for d in activities_dirs:
        for cs in d.glob("*.cs"):
            if pattern.search(cs.read_text(encoding="utf-8", errors="ignore")):
                return True
    return False


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--root",
        type=Path,
        default=HERE.parent.parent.parent,
        help="Directory containing the repo clones (default: parent of this repo's checkout)",
    )
    args = parser.parse_args()

    for lib in load_libraries():
        name = lib["name"]
        repo_path = args.root / name
        if not repo_path.is_dir():
            print(f"{name}: NOT CLONED ({repo_path})")
            continue

        results = []
        if lib.get("open"):
            results.append(("open", check_open(repo_path)))
        if lib.get("plus"):
            results.append(("plus", check_plus(repo_path)))

        status = ", ".join(f"{ed}={'ok' if ok else 'missing'}" for ed, ok in results) or "no editions"
        print(f"{name}: {status}")


if __name__ == "__main__":
    main()
