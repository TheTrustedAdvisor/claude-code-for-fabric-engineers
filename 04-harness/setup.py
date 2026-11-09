"""Create a fresh project for exercise 4.

    python3 setup.py <folder> --notes <notes folder>
"""
import argparse
import pathlib
import shutil
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent

HARNESS = """# Harness

## When did notebooks/CLAUDE.md load?

In each cell write `yes` or `no`. A dash means: nothing to check at this point.

| When | Under "Memory files"? | Claude names the time zone rule? |
|---|---|---|
| before the first prompt (step 2) |  | - |
| after step 3 |  |  |
| after reading the notebook (step 4) |  |  |
| after /clear (step 4) |  |  |
| after the import (step 5) |  |  |

What brought the rule into the context, and which line showed it?



## The parts besides the model

For each part: where it comes from (Claude Code, the project, your profile, you) and where you saw it (a command, a file, a prompt).

| Part | Comes from | Where I saw it |
|---|---|---|
| System prompt |  |  |
| Tools |  |  |
| CLAUDE.md |  |  |
| notebooks/CLAUDE.md |  |  |
| Agent definition |  |  |
| Permissions |  |  |
| Approval |  |  |

## What I check before the first prompt, and why



"""


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
        found = [name for name in ("CLAUDE.md", "CLAUDE.local.md") if (parent / name).is_file()]
        if parent != home and (parent / ".claude" / "CLAUDE.md").is_file():
            found.append(".claude/CLAUDE.md")
        if found:
            fail(f"{parent} holds {', '.join(found)}, and Claude Code would load it in this project too. Pick another place.")


def copy_text(source, destination):
    destination.parent.mkdir(parents=True, exist_ok=True)
    text = source.read_text(encoding="utf-8").replace("\r\n", "\n")
    with open(destination, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)


def main():
    parser = argparse.ArgumentParser(description="Create a fresh project for exercise 4.")
    parser.add_argument("folder")
    parser.add_argument("--notes", required=True, help="folder for your notes")
    args = parser.parse_args()

    target = pathlib.Path(args.folder).expanduser().resolve()
    notes = pathlib.Path(args.notes).expanduser().resolve()
    check_target(target)

    source = HERE / "project"
    for path in sorted(source.rglob("*")):
        if path.is_file() and "__pycache__" not in path.parts:
            copy_text(path, target / path.relative_to(source))
    copy_text(HERE / "stages" / "project-settings.json", target / ".claude" / "settings.json")

    if shutil.which("git"):
        subprocess.run(["git", "init", "-q", str(target)], check=False)
    else:
        print("setup: git not found; the project is not a Git repository.", file=sys.stderr)

    notes.mkdir(parents=True, exist_ok=True)
    if not (notes / "harness.md").exists():
        with open(notes / "harness.md", "w", encoding="utf-8", newline="\n") as handle:
            handle.write(HARNESS)

    print(f"created {target}")
    print(f"notes in {notes / 'harness.md'}")


main()
