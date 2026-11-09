"""Create a fresh project for exercise 7.

    python3 setup.py <folder>
"""
import argparse
import pathlib
import shutil
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent


def fail(message):
    print(f"setup: {message}", file=sys.stderr)
    sys.exit(2)


def check_target(target):
    if target.exists():
        fail(f"{target} already exists. Pick a new folder.")
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


def git(target, *args):
    return subprocess.run(["git", "-C", str(target), *args], capture_output=True, text=True)


def main():
    parser = argparse.ArgumentParser(description="Create a fresh project for exercise 7.")
    parser.add_argument("folder")
    args = parser.parse_args()

    target = pathlib.Path(args.folder).expanduser().resolve()
    check_target(target)

    source = HERE / "project"
    for path in sorted(source.rglob("*")):
        if path.is_file() and "__pycache__" not in path.parts:
            copy_text(path, target / path.relative_to(source))

    if shutil.which("git"):
        git(target.parent, "init", "-q", str(target))
        git(target, "add", "-A")
        run = git(target, "-c", "user.name=Exercise 7", "-c", "user.email=exercise7@example.invalid",
                  "commit", "-q", "-m", "Migration state on 2026-11-04")
        if run.returncode != 0:
            print("setup: the first commit failed; the files are there, but not committed.", file=sys.stderr)
    else:
        print("setup: git not found; the project is not a Git repository.", file=sys.stderr)

    print(f"created {target}")


main()
