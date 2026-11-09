"""Create a fresh project for exercise 2.

    python3 setup.py <folder> --notes <notes folder>
"""
import argparse
import pathlib
import shutil
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent

SETTINGS = """{
  "permissions": {}
}
"""

NOTES = """# Notes, exercise 2

## Step 2: without the guidelines

- Number of findings:
- Messages in /context after the review:

## Step 3: your prediction

Which findings will the team's guidelines keep? Write the file:line of each, before step 4.

-

## Step 4: with the guidelines

- Number of findings:
- Messages in /context after the review:
- Which of your predictions held:

## Step 5: one line changed

- Rule ID you change:
- The finding you expect to appear or drop (file:line):
- What happened:

## Step 6: one task per session

One sentence: why does the review against the guidelines get its own session?

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


def write_text(destination, text):
    destination.parent.mkdir(parents=True, exist_ok=True)
    with open(destination, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text.replace("\r\n", "\n"))


def main():
    parser = argparse.ArgumentParser(description="Create a fresh project for exercise 2.")
    parser.add_argument("folder")
    parser.add_argument("--notes", required=True, help="folder for your notes")
    args = parser.parse_args()

    target = pathlib.Path(args.folder).expanduser().resolve()
    notes = pathlib.Path(args.notes).expanduser().resolve()
    check_target(target)
    if notes == target or target in notes.parents:
        fail("Keep the notes folder outside the project, so Claude doesn't read your predictions.")

    source = HERE / "project"
    for path in sorted(source.rglob("*")):
        if path.is_file() and "__pycache__" not in path.parts:
            write_text(target / path.relative_to(source), path.read_text(encoding="utf-8"))
    write_text(target / ".claude" / "settings.json", SETTINGS)
    (target / "reviews").mkdir()

    if shutil.which("git"):
        subprocess.run(["git", "init", "-q", str(target)], check=False)
        subprocess.run(["git", "-C", str(target), "add", "-A"], check=False)
        subprocess.run(["git", "-C", str(target), "-c", "user.name=exercise", "-c", "user.email=exercise@example.com",
                        "commit", "-q", "-m", "Sales semantic model"], check=False)
    else:
        print("setup: git not found; the project is not a Git repository.", file=sys.stderr)

    notes.mkdir(parents=True, exist_ok=True)
    if not (notes / "notes.md").exists():
        write_text(notes / "notes.md", NOTES)

    print(f"created {target}")
    print(f"notes in {notes}")


main()
