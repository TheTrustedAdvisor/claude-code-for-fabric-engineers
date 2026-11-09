"""Check your result of exercise 6.

    python3 check.py --project <project folder>
"""
import argparse
import pathlib
import re
import subprocess
import sys

results = []


def check(ok, label, reason=""):
    results.append(ok)
    print(f"{'ok  ' if ok else 'FAIL'}  {label}" + ("" if ok or not reason else f": {reason}"))


def git(project, *args):
    run = subprocess.run(["git", "-C", str(project), *args], capture_output=True, text=True)
    return run.returncode, run.stdout


def section(text, heading_start):
    lines, inside = [], False
    for line in text.splitlines():
        if line.startswith("## "):
            inside = line[3:].lower().startswith(heading_start)
            continue
        if inside:
            lines.append(line)
    return "\n".join(lines).strip()


def check_git(project):
    code, _ = git(project, "rev-parse", "--git-dir")
    check(code == 0, "the project is a Git repository", f"{project} is not a Git repository; run setup again")
    if code != 0:
        return
    _, log = git(project, "log", "--format=%s")
    commits = [line for line in log.splitlines() if line.strip()]
    check(commits == ["baseline"], "history: one commit, baseline",
          f"found {len(commits)} commit(s): {', '.join(commits) or 'none'}; this exercise undoes changes, it doesn't commit them")
    code, _ = git(project, "diff", "--quiet", "HEAD")
    check(code == 0, "tracked files match the baseline",
          "git diff HEAD still shows changes; use git diff to find them and git restore <file> to undo them")
    _, status = git(project, "status", "--porcelain", "--untracked-files=all")
    lines = [line for line in status.splitlines() if line.strip()]
    others = [line for line in lines if line != "?? notes.md"]
    check(not others, "git status shows only your own note",
          "git status also shows: " + "; ".join(others) if others else "")
    check("?? notes.md" in lines, "notes.md is still there, untracked",
          "notes.md is missing or was added to Git; did git clean -f without a file name delete it?")
    check(not (project / "clean_counts.bak.py").exists(), "the backup copy is gone",
          "clean_counts.bak.py still exists; git clean -n shows it, git clean -f clean_counts.bak.py removes it")


def check_notes(project):
    text = (project / "notes.md").read_text(encoding="utf-8") if (project / "notes.md").is_file() else None
    if text is None:
        check(False, "notes.md exists", "write your notes again from the template in the README")
        return
    prediction = section(text, "prediction")
    prediction = "\n".join(line for line in prediction.splitlines() if not line.startswith("After \"Restore code\""))
    check(bool(prediction.strip()), "notes.md: a prediction", "the Prediction section is empty")
    happened = section(text, "what happened")
    named = all(re.search(name, happened, re.I) for name in (r"notebook", r"clean_counts\.py", r"bak|backup|copy"))
    check(named, "notes.md: what happened, for each of the three files",
          "name the notebook, clean_counts.py and the backup copy, and what brought each one back")
    check(bool(re.search(r"\b(own|my|your)\b[^.]{0,40}\b(line|sentence|edit|change|text|note|review)|\b(line|sentence)\b[^.]{0,40}\b(I|you) (added|wrote|typed)|\breview(ed)?\b[^.]{0,30}\b(note|line)\b", happened, re.I)),
          "notes.md: what happened to your own line", "say what happened to the line you added yourself")
    rule = section(text, "my rule")
    check(bool(re.search(r"rewind", rule, re.I) and re.search(r"\bgit\b", rule, re.I)),
          "notes.md: your rule names /rewind and Git", "your rule should say when you use /rewind and when Git")


def main():
    parser = argparse.ArgumentParser(description="Check your result of exercise 6.")
    parser.add_argument("--project", required=True)
    args = parser.parse_args()
    project = pathlib.Path(args.project).expanduser().resolve()
    if not project.is_dir():
        print(f"FAIL  {project} is not a folder")
        sys.exit(1)
    check_git(project)
    check_notes(project)
    if all(results):
        print("all checks passed")
    else:
        print(f"{results.count(False)} of {len(results)} checks failed")
    sys.exit(0 if all(results) else 1)


main()
