"""Create a fresh project for exercise 6: a Git repository with one commit, "baseline".

    python3 setup.py <folder>            # the local project (steps 1 to 7)
    python3 setup.py <folder> --fabric   # the same project with a real deploy (optional step 8)
"""
import argparse
import pathlib
import shutil
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent

NOTES = """# Notes

## Prediction (write it before you open /rewind)

After "Restore code", which files are back as in the baseline, and does your own line stay?

## What happened

## My rule for undoing Claude's changes

"""


FABRIC_SETTINGS = """{
  "env": {
    "CLAUDE_CODE_USE_POWERSHELL_TOOL": "0"
  },
  "permissions": {
    "allow": [
      "Bash(./deploy.sh dev)"
    ]
  }
}
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


def git(target, *args):
    run = subprocess.run(["git", "-C", str(target), *args], capture_output=True, text=True)
    if run.returncode != 0:
        fail(f"git {' '.join(args)} failed: {run.stderr.strip()}")
    return run.stdout


def main():
    parser = argparse.ArgumentParser(description="Create a fresh project for exercise 6.")
    parser.add_argument("folder")
    parser.add_argument("--fabric", action="store_true", help="add the real deploy for step 8")
    args = parser.parse_args()

    if not shutil.which("git"):
        fail("git not found. This exercise is about Git; install it first (on Windows: Git for Windows).")

    target = pathlib.Path(args.folder).expanduser().resolve()
    check_target(target)

    source = HERE / "project"
    for path in sorted(source.rglob("*")):
        if path.is_file() and "__pycache__" not in path.parts:
            copy_text(path, target / path.relative_to(source))
    if args.fabric:
        for name in ("deploy.sh", "show.sh"):
            copy_text(HERE / "fabric" / name, target / name)
            (target / name).chmod(0o755)
        settings = target / ".claude" / "settings.json"
        settings.write_text(FABRIC_SETTINGS, encoding="utf-8")

    git(target, "init", "-q")
    git(target, "symbolic-ref", "HEAD", "refs/heads/main")
    git(target, "add", "-A")
    git(target, "-c", "user.name=Exercise 6", "-c", "user.email=exercise6@example.invalid",
        "-c", "commit.gpgsign=false",
        "commit", "-q", "--no-verify", "-m", "baseline")

    with open(target / "notes.md", "w", encoding="utf-8", newline="\n") as handle:
        handle.write(NOTES)

    print(f"created {target}: Git repository on main with one commit, baseline")
    print("notes.md is your own note; it stays untracked")


main()
