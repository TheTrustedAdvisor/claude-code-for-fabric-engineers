"""Check your result of exercise 7.

    python3 check.py --project <project folder>
"""
import argparse
import json
import pathlib
import re
import subprocess
import sys

SECTIONS = ("state", "open question", "next step", "files")
LIMIT = 16

results = []


def check(ok, label, reason=""):
    results.append(ok)
    print(f"{'ok  ' if ok else 'FAIL'}  {label}" + ("" if ok or not reason else f": {reason}"))


def read(path):
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return None


def sections(text):
    found, current = {}, None
    for line in text.splitlines():
        if line.startswith("## "):
            current = line[3:].strip().lower()
            found[current] = []
            continue
        if current is not None:
            found[current].append(line)
    return {name: "\n".join(lines).strip() for name, lines in found.items()}


def mentions_limit(text):
    return re.search(rf"(?<!\d)(?<!\d\.){LIMIT}(?!\d)(?!\.\d)", text) is not None


def check_note(project):
    text = read(project / "handoff-note.md")
    check(text is not None, "handoff-note.md exists", "no handoff-note.md in the project")
    if text is None:
        return
    parts = sections(text)
    for name in SECTIONS:
        body = parts.get(name, "")
        check(bool(body) and "…" not in body, f"note: section \"{name.capitalize()}\" is filled in",
              "missing, empty or still holds the … placeholder")
    check(re.search(r"\b20\d\d-\d\d-\d\d\b", text) is not None, "note: has a date (YYYY-MM-DD)",
          "add the date the note was written")
    check("sales-migration" in text, "note: names the session sales-migration",
          "add the session name, so tomorrow you can find the session with /resume")
    check(mentions_limit(text) and "config/source.yaml" in text,
          f"note: holds the limit of {LIMIT} parallel copies with its source config/source.yaml",
          "the finding from step 5 is missing, or its source isn't named")
    lines = [line for line in text.splitlines() if line.strip()]
    check(len(lines) <= 40, "note: short (at most 40 non-empty lines)", f"{len(lines)} lines; a note is a page, not a log")

    step = parts.get("next step", "")
    check(re.search(r"pipeline-content\.json|config/source\.yaml|\bpipeline\b|test run|re-?run", step, re.I) is not None,
          "note: the next step says where to start",
          "name the file to open (pipeline-content.json) or, after the fix, the pipeline run to check")
    check("gateway" not in step.lower(), "note: the next step doesn't send tomorrow's session to the gateway",
          "migration.md already rules the gateway out; say why in the note instead")
    stale = "source.yaml" in step and re.search(r"\b(not (been |yet )?read|neither|unread)\b", step, re.I)
    check(not stale, "note: no contradiction between the finding and the next step",
          "\"Next step\" still says config/source.yaml hasn't been read, while the note already holds its limit")


def numbered_items(text):
    items, current = {}, None
    for line in text.splitlines():
        match = re.match(r"\s*(?:#+\s*)?([1-5])\.\s*(.*)", line)
        if match:
            current = match.group(1)
            items[current] = match.group(2).strip()
        elif current and line.strip():
            items[current] = (items[current] + " " + line.strip()).strip()
    return items


def check_cold_start(project):
    text = read(project / "cold-start.md")
    check(text is not None, "cold-start.md exists", "write your three test results and your rule into cold-start.md, items 1 to 4 (not into the note)")
    if text is None:
        return
    items = numbered_items(text)
    for number in ("1", "2", "3", "4"):
        check(bool(items.get(number)), f"cold-start.md: item {number}. is filled in", f"nothing under {number}.")
    for number in ("1", "2"):
        if items.get(number):
            says_none = re.search(r"\bno number\b|\bdoesn['’]t (say|give)\b|\bdoes not (say|give)\b|\bnot in the note\b|\bnumber\W+none\b|^\W*(none|unknown)\b", items[number], re.I)
            check(not mentions_limit(items[number]) or says_none is not None, f"cold-start.md: test {number} has no number of copies",
                  f"test {number} ran before the finding was in the note; the fresh session can't know {LIMIT}. "
                  "Did you ask the right session, or write the number into the note too early?")
    if items.get("3"):
        check(mentions_limit(items["3"]), f"cold-start.md: test 3 names {LIMIT}",
              "after you added the finding, the fresh session should name it; if it didn't, fix the note and test again")
    if items.get("4"):
        check(len(items["4"].split()) >= 8, "cold-start.md: item 4. states your rule and why",
              "one sentence: what you check before ending a session, and why")


def check_pipeline(project):
    path = project / "workspace" / "pl_sales_nightly.DataPipeline" / "pipeline-content.json"
    try:
        content = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        check(False, "pipeline-content.json is valid JSON", str(error))
        return
    loops = [a for a in content.get("properties", {}).get("activities", []) if a.get("type") == "ForEach"]
    props = loops[0].get("typeProperties", {}) if loops else {}
    count = props.get("batchCount")
    check(isinstance(count, int) and 1 <= count <= LIMIT,
          f"pipeline: the ForEach has a batch count between 1 and {LIMIT}",
          "no batchCount, so Fabric uses its default of 20" if count is None else f"batchCount is {count}")
    check(props.get("isSequential") is False, "pipeline: the ForEach still runs in parallel",
          "isSequential should stay false; the limit is the batch count, not one copy at a time")


def check_git(project):
    if not (project / ".git").exists():
        return
    run = subprocess.run(["git", "-C", str(project), "status", "--porcelain", "--", "adf", "config", "logs", "migration.md"],
                         capture_output=True, text=True)
    changed = [line for line in run.stdout.splitlines() if line.strip()]
    check(run.returncode == 0 and not changed, "adf/, config/, logs/ and migration.md are unchanged",
          ", ".join(line[3:] for line in changed) or run.stderr.strip())


def main():
    parser = argparse.ArgumentParser(description="Check your result of exercise 7.")
    parser.add_argument("--project", required=True, help="the project folder you created with setup.sh")
    args = parser.parse_args()
    project = pathlib.Path(args.project).expanduser().resolve()
    if not project.is_dir():
        print(f"check: {project} is not a folder", file=sys.stderr)
        sys.exit(2)

    check_note(project)
    check_cold_start(project)
    check_pipeline(project)
    check_git(project)

    failed = results.count(False)
    print()
    print("all checks passed" if not failed else f"{failed} of {len(results)} checks failed")
    sys.exit(0 if not failed else 1)


main()
