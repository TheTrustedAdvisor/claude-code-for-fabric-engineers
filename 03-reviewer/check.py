"""Check your result of exercise 3.

    python3 check.py --project <project folder> --notes <notes folder>
"""
import argparse
import hashlib
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
EXPECTED_MARK = {"1": "g", "2": "g", "3": "g", "4": "g", "5": "u"}
EXPECTED_FINAL = {"1": "keep", "2": "strike", "3": "keep", "4": "keep", "5": "not a fact"}
SOURCES = ("modeling-guidelines.md", "Sales.SemanticModel/definition/tables/Sales.tmdl")
UNCHANGED = SOURCES + ("review/colleague-review.md", ".claude/agents/reviewer.md")
WRITE_TOOLS = ("Edit", "Write", "Bash", "NotebookEdit", "PowerShell")

results = []


def check(ok, label, reason=""):
    results.append(ok)
    print(f"{'ok  ' if ok else 'FAIL'}  {label}" + ("" if ok or not reason else f": {reason}"))


def read(path):
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return None


def section(text, heading_start):
    lines, inside = [], False
    for line in text.splitlines():
        if line.startswith("## "):
            inside = line[3:].lower().startswith(heading_start)
            continue
        if inside:
            lines.append(line)
    return "\n".join(lines).strip()


def table(text):
    rows = {}
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("|") or re.fullmatch(r"\|[\s:|-]+\|", line):
            continue
        cells = [cell.strip().strip("`*").strip().lower() for cell in line.strip("|").split("|")]
        if cells and cells[0].isdigit():
            rows[cells[0]] = cells[1:]
    return rows


def prose(text):
    return [line for line in text.splitlines() if line.strip() and not line.lstrip().startswith(("|", "In \"", "One sentence", "What did", "Same question", "Finding (", "Quote from", "For the two"))]


def flat(text):
    return re.sub(r"\s+", " ", text.replace("`", "").replace("**", "")).strip()


def digest(path):
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest() if path.is_file() else None


def check_project(project):
    for name in UNCHANGED:
        check(digest(project / name) == digest(HERE / "project" / name), f"unchanged: {name}",
              "this file differs from the exercise; the review changes no file (run setup again for a clean copy)")
    agent = read(project / ".claude" / "agents" / "reviewer.md") or ""
    tools = re.search(r"^tools:\s*(.+)$", agent, re.M)
    listed = [t.strip() for t in tools.group(1).split(",")] if tools else []
    check(bool(listed) and not any(t in WRITE_TOOLS for t in listed), "reviewer can only read",
          "the reviewer's tools line must list only reading tools, such as Read, Grep, Glob")


def check_notes(notes, project):
    text = read(notes / "sign-off.md")
    check(text is not None, "sign-off.md exists", f"no sign-off.md in {notes}")
    if text is None:
        return
    marks = table(section(text, "step 2"))
    for number, want in EXPECTED_MARK.items():
        got = (marks.get(number) or [""])[0]
        why = ("it cites a file and line, so it's grounded, whether or not it holds" if want == "g"
               else "it cites nothing in the files, so it's ungrounded, however sure it sounds")
        check(got == want, f"step 2: statement {number} marked {want.upper()}", f"you wrote '{got}'; {why}")
    holds = {n: (row[1] if len(row) > 1 else "") for n, row in marks.items()}
    checked = [n for n, value in holds.items() if value in ("yes", "no")]
    check(len(checked) >= 2, "step 2: two statements spot-checked", "write yes or no in 'Holds?' for two grounded statements")
    if holds.get("2") in ("yes", "no"):
        check(holds["2"] == "no", "step 2: statement 2 doesn't hold",
              "read M1 to the end: it says what to use when the denominator is a constant")
    for number in ("1", "3", "4"):
        if holds.get(number) in ("yes", "no"):
            check(holds[number] == "yes", f"step 2: statement {number} holds",
                  "look at the cited lines again: the statement matches the TMDL and the rule")
    check(len(prose(section(text, "step 3"))) >= 1, "step 3: first judgment written", "write one sentence before you call any reviewer")
    for step, label in (("step 4", "session A"), ("step 5", "session B")):
        check(len(prose(section(text, step))) >= 1, f"{step}: delegation message of {label} noted",
              "open the reviewer call with Ctrl+O and note what the task prompt contained")
    finding = section(text, "step 6")
    quotes = re.findall(r"[\"“«]([^\"”»\n]{12,})[\"”»]", finding) + [
        line.strip().lstrip(">").strip() for line in finding.splitlines() if line.lstrip().startswith(">")]
    sources = {name: flat(read(project / name) or read(HERE / "project" / name) or "") for name in SOURCES}
    found = [q for q in quotes if flat(q) and any(flat(q) in text for text in sources.values())]
    check(bool(found), "step 6: a word-for-word quote from the source",
          "put the quote in quotation marks or on a line starting with >, copied exactly from modeling-guidelines.md or Sales.tmdl "
          "(backticks and ** don't matter)")
    if found:
        settles = [q for q in found if "constant" in flat(q).lower()]
        check(bool(settles), "step 6: the quote settles statement 2",
              "quote the part of M1 that says what to use when the denominator is a constant")
    final = table(section(text, "step 7"))
    for number, want in EXPECTED_FINAL.items():
        got = (final.get(number) or [""])[0]
        check(got == want, f"step 7: statement {number} → {want}", f"you wrote '{got}'")


def main():
    parser = argparse.ArgumentParser(description="Check your result of exercise 3.")
    parser.add_argument("--project", required=True)
    parser.add_argument("--notes", required=True)
    args = parser.parse_args()
    project = pathlib.Path(args.project).expanduser().resolve()
    notes = pathlib.Path(args.notes).expanduser().resolve()
    check_project(project)
    check_notes(notes, project)
    if all(results):
        print("all checks passed")
        return 0
    print(f"{results.count(False)} of {len(results)} checks failed")
    return 1


sys.exit(main())
