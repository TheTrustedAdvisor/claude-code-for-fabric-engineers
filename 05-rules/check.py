"""Check your result of exercise 5.

    python3 check.py --project <project folder> --notes <notes folder>
"""
import argparse
import json
import pathlib
import re
import shutil
import subprocess
import sys

STATUS = {"kept", "broken", "not checkable"}
EXPECTED_GAPS = {"deny rule": {"no"}, "hook": {"partly"}, "fabric role": {"yes", ""}}
DENY_RULES = ("Bash(./deploy.sh prod*)", "Bash(python3 deploy.py --env prod*)")

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
    return "\n".join(lines).strip()


def check_claude_md(project):
    text = read(project / "CLAUDE.md")
    check(text is not None, "CLAUDE.md exists", "no CLAUDE.md in the project")
    if text is None:
        return
    body = [line.strip() for line in text.splitlines()
            if line.strip() and not line.strip().startswith(("#", "```"))]
    check("be careful with prod" not in text.lower(), "CLAUDE.md: the vague line is gone",
          '"Be careful with prod" is still there; replace it with a rule you can check')
    check(3 <= len(body) <= 6, "CLAUDE.md: one line on the project, two to five rules",
          f"{len(body)} lines of text; aim for one project line plus two to five rules")
    both = [line for line in body if re.search(r"\bdev", line, re.I) and re.search(r"\bprod", line, re.I)
            and re.search(r"\b(never|not|don't|do not|no)\b", line, re.I)]
    check(bool(both), "CLAUDE.md: the deploy rule names dev and prod",
          "no line says both where deploys go (dev) and where they never go (prod)")


def check_local(project):
    local = read(project / "CLAUDE.local.md")
    check(bool(local and local.strip()), "CLAUDE.local.md holds a preference", "CLAUDE.local.md is missing or empty")
    ignore = read(project / ".gitignore") or ""
    listed = any(line.strip().lstrip("/") == "CLAUDE.local.md" for line in ignore.splitlines())
    check(listed, ".gitignore lists CLAUDE.local.md", "add a line CLAUDE.local.md to .gitignore")
    if listed and shutil.which("git") and (project / ".git").exists():
        run = subprocess.run(["git", "-C", str(project), "check-ignore", "-q", "CLAUDE.local.md"])
        check(run.returncode == 0, "git ignores CLAUDE.local.md", "git check-ignore doesn't ignore it; check the spelling")


def check_settings(project):
    raw = read(project / ".claude" / "settings.json")
    try:
        settings = json.loads(raw) if raw else None
    except ValueError as error:
        check(False, ".claude/settings.json is valid JSON", str(error))
        return
    if settings is not None and not isinstance(settings, dict):
        check(False, ".claude/settings.json is valid JSON", "the top level must be an object")
        return
    check(settings is not None, ".claude/settings.json exists", "the project settings file is missing")
    if settings is None:
        return
    deny = settings.get("permissions", {}).get("deny", [])
    for rule in DENY_RULES:
        check(rule in deny, f"deny rule {rule} in .claude/settings.json",
              "not under permissions.deny; add it with /permissions and save it under Project settings")
    for name in ("settings.json", "settings.local.json"):
        raw = read(project / ".claude" / name)
        try:
            data = json.loads(raw) if raw else {}
            allow = data.get("permissions", {}).get("allow", []) if isinstance(data, dict) else []
        except (ValueError, AttributeError):
            allow = []
        prod = [rule for rule in allow if "prod" in rule]
        check(not prod, f"no allow rule for prod in .claude/{name}", f"remove {', '.join(prod)}")


def check_deployed(project):
    log = read(project / "deployed" / "dev" / "deploy.log") or ""
    check(bool(log.strip()), "deployed/dev/deploy.log has a deploy", "no dev deploy recorded; do step 3")
    check(not (project / "deployed" / "prod").exists(), "deployed/prod/ is gone",
          "deployed/prod/ still exists; look at deploy.log, then delete the folder")


def check_rules_checked(notes):
    text = read(notes / "rules-checked.md")
    check(text is not None, "rules-checked.md exists", f"not found in {notes}")
    if text is None:
        return
    rows = [row for row in table_rows(text) if row and row[0]]
    check(2 <= len(rows) <= 5, "rules-checked.md: one row per rule", f"{len(rows)} rules in the table, expected 2 to 5")
    bad = [row[0] for row in rows if len(row) < 4 or any(cell.lower() not in STATUS for cell in row[1:4])]
    check(rows and not bad, "rules-checked.md: every cell says kept, broken or not checkable",
          "check the row(s): " + "; ".join(bad) if bad else "no rows")
    step4 = section(text, "step 4")
    sessions = re.findall(r"session \d:[ \t]*(.*)", step4, re.I)
    check(len(sessions) >= 2 and all(s.strip() for s in sessions[:2]), "rules-checked.md: both step 4 outcomes noted",
          "write what Claude did in session 1 and session 2")
    step5 = section(text, "step 5")
    check(bool(re.search(r"deny|permission", step5, re.I)), "rules-checked.md: step 5 names who stopped the call",
          "the step 5 note doesn't name the deny rule or the permission settings")


def check_gaps(notes):
    text = read(notes / "gaps.md")
    check(text is not None, "gaps.md exists", f"not found in {notes}")
    if text is None:
        return
    rows = {row[0].lower(): row for row in table_rows(text) if row}
    for layer, expected in EXPECTED_GAPS.items():
        row = rows.get(layer)
        if row is None:
            check(False, f"gaps.md: row {layer}", "the row is missing; keep the three rows of the template")
            continue
        first = re.match(r"[a-z]+", row[1].lower()) if len(row) > 1 else None
        answer = first.group(0) if first else ""
        why = row[2] if len(row) > 2 else ""
        if layer == "fabric role" and not answer:
            check(True, "gaps.md: Fabric role (step 9 skipped)")
            continue
        check(answer in expected, f"gaps.md: {layer} stopped it? {answer or '(empty)'}",
              f"compare with what you saw; the expected answer is {' or '.join(sorted(e for e in expected if e))}")
        check(bool(why), f"gaps.md: {layer}, what got through and why", "write one sentence in the third column")


def main():
    parser = argparse.ArgumentParser(description="Check your result of exercise 5.")
    parser.add_argument("--project", required=True, help="the project from step 1 (stage rule-only)")
    parser.add_argument("--notes", required=True, help="the notes folder")
    args = parser.parse_args()
    project = pathlib.Path(args.project).expanduser().resolve()
    notes = pathlib.Path(args.notes).expanduser().resolve()
    if not project.is_dir():
        sys.exit(f"check: no project at {project}")

    check_claude_md(project)
    check_local(project)
    check_settings(project)
    check_deployed(project)
    check_rules_checked(notes)
    check_gaps(notes)

    failed = results.count(False)
    print()
    if failed:
        print(f"{failed} check(s) failed")
        sys.exit(1)
    print("all checks passed")


main()
