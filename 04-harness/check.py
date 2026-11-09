"""Check your result of exercise 4.

    python3 check.py --project <project folder> --notes <notes folder>
"""
import argparse
import json
import pathlib
import re
import sys

# When notebooks/CLAUDE.md is in the context: (under "Memory files"?, Claude names the time zone rule?)
EXPECTED_LOADING = {
    "before the first prompt": ("no", "-"),
    "after step 3": ("no", "no"),
    "after reading the notebook": ("no", "yes"),
    "after /clear": ("no", "no"),
    "after the import": ("yes", "yes"),
}
# Part -> words of which at least one must appear in "Where I saw it"
EXPECTED_WHERE = {
    "system prompt": ("/context",),
    "tools": ("/context",),
    "claude.md": ("/context", "/memory"),
    "notebooks/claude.md": ("loaded line", "loaded notebooks", "/context", "/memory", "@-imported"),
    "agent definition": (".claude/agents", "/context", "reviewer.md"),
    "permissions": ("/permissions", "settings.json"),
    "approval": ("prompt",),
}
# Part -> words of which at least one must appear in "Comes from"
EXPECTED_SOURCE = {
    "system prompt": ("claude code",),
    "tools": ("claude code", "profile", r"\bmcp\b"),
    "claude.md": ("project",),
    "notebooks/claude.md": ("project",),
    "agent definition": ("project",),
    "permissions": ("project", r"(?<!~/)\.claude/settings\.json"),
    "approval": (r"\bme\b", r"\byou\b", r"\bi\b", r"\bmyself\b"),
}
RULES = ("snake_case", "markdown cell", "never deploy to the production workspace")

results = []


def check(ok, label, reason=""):
    results.append(ok)
    print(f"{'ok  ' if ok else 'FAIL'}  {label}" + ("" if ok or not reason else f": {reason}"))


def read(path):
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return None


def table_rows(text):
    rows = []
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("|") or re.fullmatch(r"\|[\s:|-]+\|", line):
            continue
        rows.append([cell.strip().strip("`*").strip() for cell in line.strip("|").split("|")])
    return rows[1:]


def section(text, heading_start):
    lines, inside = [], False
    for line in text.splitlines():
        if line.startswith("## "):
            inside = line[3:].lower().startswith(heading_start)
            continue
        if inside:
            lines.append(line)
    return "\n".join(lines)


def prose(text):
    """Text of a section without its table."""
    return "\n".join(line for line in text.splitlines() if not line.strip().startswith("|")).strip()


def imports(text):
    """@path imports outside fenced code blocks and code spans."""
    found, fenced = [], False
    for line in text.splitlines():
        if line.strip().startswith("```"):
            fenced = not fenced
            continue
        if fenced:
            continue
        line = re.sub(r"`[^`]*`", "", line)
        found += re.findall(r"(?:^|\s)@(\S+)", line)
    return found


def check_project(project):
    text = read(project / "CLAUDE.md")
    check(text is not None, "CLAUDE.md exists", "no CLAUDE.md in the project")
    if text is None:
        return
    lowered = text.lower()
    missing = [rule for rule in RULES if rule not in lowered]
    check(not missing, "CLAUDE.md: the three team rules are still there", "missing: " + ", ".join(missing))
    found = [path.lstrip("./") for path in imports(text)]
    check("notebooks/CLAUDE.md" in found, "CLAUDE.md imports notebooks/CLAUDE.md",
          "no line @notebooks/CLAUDE.md outside code; on Windows too, write / and not \\")
    nested = read(project / "notebooks" / "CLAUDE.md") or ""
    check("utc" in nested.lower(), "notebooks/CLAUDE.md still holds the time zone rule",
          "notebooks/CLAUDE.md is missing or changed; the import needs the file")
    for name in ("settings.json", "settings.local.json"):
        raw = read(project / ".claude" / name)
        try:
            data = json.loads(raw) if raw else {}
        except ValueError as error:
            check(False, f".claude/{name} is valid JSON", str(error))
            continue
        perms = data.get("permissions", {}) if isinstance(data, dict) else {}
        if name == "settings.json":
            check("Bash(fab rm *)" in perms.get("deny", []), "deny rule Bash(fab rm *) is still in .claude/settings.json",
                  "the deny rule is gone; set up the project again or put it back")
        fab = [rule for rule in perms.get("allow", []) if "fab" in rule]
        check(not fab, f"no allow rule for fab in .claude/{name}",
              f"remove {', '.join(fab)}; in step 7 the answer is No, not \"don't ask again\"")


def check_loading(text):
    rows = {row[0].lower(): row for row in table_rows(section(text, "when did")) if row}
    for when, expected in EXPECTED_LOADING.items():
        row = next((r for key, r in rows.items() if key.startswith(when)), None)
        if row is None:
            check(False, f"harness.md: row \"{when}\"", "the row is missing; keep the rows of the template")
            continue
        got = tuple((cell.lower().split() or ["(empty)"])[0].strip(".,") for cell in row[1:3])
        want = tuple(expected)
        check(got == want, f"harness.md: {when}: {' / '.join(got)}",
              f"compare with what you saw; expected {' / '.join(want)}")
    sentence = prose(section(text, "when did")).replace("What brought the rule into the context, and which line showed it?", "")
    ok = bool(re.search(r"\bloaded\b", sentence, re.I) and re.search(r"\bread", sentence, re.I)
              and re.search(r"notebook", sentence, re.I) and not re.search(r"\bnot loaded\b|at launch", sentence, re.I))
    check(ok, "harness.md: the sentence names what loaded the rule",
          "write one sentence under the table: Claude reading a file in notebooks/ loaded it, and the line you saw (Loaded …)")


def check_parts(text):
    rows = {row[0].lower(): row for row in table_rows(section(text, "the parts")) if row}
    for part, words in EXPECTED_WHERE.items():
        row = rows.get(part)
        if row is None:
            check(False, f"harness.md: part \"{part}\"", "the row is missing; keep the seven rows of the template")
            continue
        source = " " + row[1].lower() + " " if len(row) > 1 else ""
        where = row[2].lower() if len(row) > 2 else ""
        sources = EXPECTED_SOURCE[part]
        hint = ", ".join(re.sub(r"\\b|\(\?<!~/\)|\\", "", w).strip() for w in sources)
        check(any(re.search(word, source) for word in sources), f"harness.md: {part}, comes from",
              "compare with what you saw; expected one of: " + hint)
        check(any(word in where for word in words) and "not loaded" not in where, f"harness.md: {part}, where I saw it",
              f"name the command, file or prompt; expected one of: {', '.join(words)}")


def check_practice(text):
    body = prose(section(text, "what i check"))
    check(bool(re.search(r"/context|/memory", body)) and len(body) > 40,
          "harness.md: what you check before the first prompt, and why",
          "one sentence that names the command and the reason")


def main():
    parser = argparse.ArgumentParser(description="Check your result of exercise 4.")
    parser.add_argument("--project", required=True, help="the project folder from setup")
    parser.add_argument("--notes", required=True, help="the notes folder")
    args = parser.parse_args()
    project = pathlib.Path(args.project).expanduser().resolve()
    notes = pathlib.Path(args.notes).expanduser().resolve()
    if not project.is_dir():
        sys.exit(f"check: no project at {project}")

    check_project(project)
    text = read(notes / "harness.md")
    check(text is not None, "harness.md exists", f"not found in {notes}")
    if text is not None:
        check_loading(text)
        check_parts(text)
        check_practice(text)

    failed = results.count(False)
    print()
    if failed:
        print(f"{failed} check(s) failed")
        sys.exit(1)
    print("all checks passed")


main()
