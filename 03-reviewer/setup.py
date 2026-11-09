"""Create a fresh project for exercise 3.

    python3 setup.py <folder> --notes <notes folder>
"""
import argparse
import pathlib
import shutil
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent

SIGN_OFF = """# Sign-off: Jonas's review of the Sales measures

## Step 2: mark and spot-check

In "G or U" write `G` (grounded: the statement cites a place in the files) or `U` (ungrounded: no citation).
For the two statements you spot-check, write `yes` or `no` in "Holds?". Leave the others empty.

| # | G or U | Holds? |
|---|---|---|
| 1 |  |  |
| 2 |  |  |
| 3 |  |  |
| 4 |  |  |
| 5 |  |  |

## Step 3: first judgment

One sentence, before any reviewer, and don't change it later:



## Step 4: delegation message, session A

What did Claude's task prompt for the reviewer contain besides the files and the job?



## Step 5: delegation message, session B

Same question for the fresh session:



## Step 6: one finding checked at the source

Finding (statement number and what the reviewer said):

Quote from the source, copied word for word:



## Step 7: final decision

In "Final" write `keep` (passes on as it is), `strike` (doesn't hold) or `not a fact` (can't be checked here).

| # | Final |
|---|---|
| 1 |  |
| 2 |  |
| 3 |  |
| 4 |  |
| 5 |  |
"""


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


def main():
    parser = argparse.ArgumentParser(description="Create a fresh project for exercise 3.")
    parser.add_argument("folder")
    parser.add_argument("--notes", required=True, help="notes folder, outside the project")
    args = parser.parse_args()

    target = pathlib.Path(args.folder).expanduser().resolve()
    notes = pathlib.Path(args.notes).expanduser().resolve()
    check_target(target)
    if notes == target or target in notes.parents:
        fail("Keep the notes folder outside the project, or the reviewer can read your notes.")

    source = HERE / "project"
    for path in sorted(source.rglob("*")):
        if path.is_file() and "__pycache__" not in path.parts:
            copy_text(path, target / path.relative_to(source))

    if shutil.which("git"):
        subprocess.run(["git", "init", "-q", str(target)], check=False)
        subprocess.run(["git", "-C", str(target), "add", "-A"], check=False)
        subprocess.run(["git", "-C", str(target), "-c", "user.name=exercise", "-c", "user.email=exercise@example.com",
                        "commit", "-q", "-m", "Sales model and Jonas's review"], check=False)
    else:
        print("setup: git not found; the project is not a Git repository.", file=sys.stderr)

    notes.mkdir(parents=True, exist_ok=True)
    if not (notes / "sign-off.md").exists():
        with open(notes / "sign-off.md", "w", encoding="utf-8", newline="\n") as handle:
            handle.write(SIGN_OFF)

    print(f"created {target}")
    print(f"notes in {notes}")


main()
