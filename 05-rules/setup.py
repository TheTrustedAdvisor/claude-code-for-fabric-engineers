"""Create a fresh project for exercise 5.

    python3 setup.py <folder> rule-only|deny|hook|fabric --notes <notes folder>
"""
import argparse
import pathlib
import shutil
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
STAGES = ("rule-only", "deny", "hook", "fabric")

RULES_CHECKED = """# Rules checked

One row per rule in your `CLAUDE.md`. In each step column write `kept`, `broken` or `not checkable`.

| Rule | Step 3 | Step 4, session 1 | Step 4, session 2 |
|---|---|---|---|
|  |  |  |  |
|  |  |  |  |

## Step 4: what Claude did

- Session 1:
- Session 2:

## Step 5: who stopped the call, and why an allow rule wouldn't help

"""

GAPS = """# Gaps

In "Stopped it?" write `yes`, `no` or `partly`. Leave the Fabric row empty if you skip step 9.

| Layer | Stopped it? | What got through, and why |
|---|---|---|
| deny rule |  |  |
| hook |  |  |
| Fabric role |  |  |
"""


def fail(message):
    print(f"setup: {message}", file=sys.stderr)
    sys.exit(2)


def python3_works():
    exe = shutil.which("python3")
    if not exe:
        return False
    try:
        run = subprocess.run([exe, "--version"], capture_output=True, text=True, timeout=20)
    except (OSError, subprocess.SubprocessError):
        return False
    return run.returncode == 0 and "Python 3" in (run.stdout + run.stderr)


def check_target(target):
    if target.exists():
        fail(f"{target} already exists. Pick a new folder for each stage.")
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
    parser = argparse.ArgumentParser(description="Create a fresh project for exercise 5.")
    parser.add_argument("folder")
    parser.add_argument("stage", choices=STAGES)
    parser.add_argument("--notes", required=True, help="notes folder shared by all stages")
    args = parser.parse_args()

    if not python3_works():
        fail("`python3 --version` doesn't run here. The allow rules and the hook call python3; "
             "install Python 3 so that `python3` works (on Windows: the Python Install Manager from python.org).")

    target = pathlib.Path(args.folder).expanduser().resolve()
    notes = pathlib.Path(args.notes).expanduser().resolve()
    check_target(target)

    source = HERE / "project"
    for path in sorted(source.rglob("*")):
        if path.is_file() and "__pycache__" not in path.parts:
            copy_text(path, target / path.relative_to(source))
    if args.stage == "fabric":
        for name in ("deploy.sh", "deploy.py", "fab.sh", "parameter.yml"):
            copy_text(HERE / "fabric" / name, target / name)
        (target / "fab.sh").chmod(0o755)
    (target / "deploy.sh").chmod(0o755)

    stage = "rule-only" if args.stage == "fabric" else args.stage
    copy_text(HERE / "stages" / f"{stage}.json", target / ".claude" / "settings.json")
    if args.stage == "hook":
        copy_text(HERE / "hooks" / "block-prod.py", target / ".claude" / "hooks" / "block-prod.py")

    if shutil.which("git"):
        subprocess.run(["git", "init", "-q", str(target)], check=False)
    else:
        print("setup: git not found; the project is not a Git repository.", file=sys.stderr)

    notes.mkdir(parents=True, exist_ok=True)
    for name, text in (("rules-checked.md", RULES_CHECKED), ("gaps.md", GAPS)):
        if not (notes / name).exists():
            with open(notes / name, "w", encoding="utf-8", newline="\n") as handle:
                handle.write(text)

    print(f"created {target} (stage {args.stage})")
    print(f"notes in {notes}")


main()
