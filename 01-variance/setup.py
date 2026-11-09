"""Create a fresh project for exercise 1.

    python3 setup.py <folder>
"""
import argparse
import hashlib
import pathlib
import shutil
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
DATA = {
    "bikes-2025-09.csv": "502b831bda2bc5f1aceb1467ca5aebee5136b86c824d754557b17e42e502f246",
    "counters.csv": "c0a7a81ba996e67edd263a1a0b56b5bb8c4196d1e398fab5ce3b39f189df9a64",
}


def fail(message):
    print(f"setup: {message}", file=sys.stderr)
    sys.exit(2)


def check_target(target):
    if target.exists():
        fail(f"{target} already exists. Pick a new folder, or delete the old one first.")
    home = pathlib.Path.home().resolve()
    for parent in target.parents:
        if (parent / ".git").exists():
            fail(f"{parent} is a Git repository. Create the project outside your own projects, for example under /var/tmp.")
        found = [name for name in ("CLAUDE.md", "CLAUDE.local.md", "AGENTS.md") if (parent / name).is_file()]
        if parent != home and (parent / ".claude" / "CLAUDE.md").is_file():
            found.append(".claude/CLAUDE.md")
        if found:
            fail(f"{parent} holds {', '.join(found)}, and Claude Code could load it in this project too. Pick another place.")


def main():
    parser = argparse.ArgumentParser(description="Create a fresh project for exercise 1.")
    parser.add_argument("folder")
    args = parser.parse_args()

    target = pathlib.Path(args.folder).expanduser().resolve()
    check_target(target)

    source = HERE / "project"
    for name, digest in DATA.items():
        if hashlib.sha256((source / name).read_bytes()).hexdigest() != digest:
            fail(f"project/{name} isn't the original file (checksum differs). Download the exercise again.")
    (target / "results").mkdir(parents=True)
    (target / ".claude").mkdir()
    for name in DATA:
        shutil.copyfile(source / name, target / name)
    settings = (source / ".claude" / "settings.json").read_text(encoding="utf-8").replace("\r\n", "\n")
    with open(target / ".claude" / "settings.json", "w", encoding="utf-8", newline="\n") as handle:
        handle.write(settings)

    print(f"created {target}")


main()
